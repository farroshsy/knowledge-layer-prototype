module Evidence
  # Turns uploaded text into sections, claims, and fields.
  module Ingest
    extend self

    def receive(notebook, filename, body = "", byte_size: nil)
      if filename.blank? || filename.include?("/") || filename.include?("\\") || filename.start_with?(".")
        raise Error.new("validation", "nama berkas harus label, bukan jalur")
      end

      return read_text_layer(notebook, filename, body, byte_size) if text_layer?(filename)

      plan = Lexicon.intake_plan(filename, body, byte_size)
      if plan[:status] == "mapped"
        document = upload(notebook, filename, body)
        return notebook.intakes.create!(plan.merge(document: document, filename: filename, byte_size: body.to_s.bytesize))
      end
      raise Error.new("validation", plan[:reason]) if plan[:physical_kind] == "plain" && plan[:route] == "reject"

      notebook.intakes.create!(plan.merge(filename: filename, byte_size: byte_size || body.to_s.bytesize))
    end

    def upload(notebook, filename, body, character_limit: 200_000)
      validate!(filename, body, character_limit: character_limit)
      parsed = Lexicon.sections(body)
      raise Error.new("validation", "dokumen tidak punya bagian teks") if parsed.empty?

      digest = Digest::SHA256.hexdigest(body)
      existing = notebook.documents.find_by(content_hash: digest)
      if existing
        existing.reused_upload = true
        return existing
      end

      document = nil
      ActiveRecord::Base.transaction do
        document = notebook.documents.create!(filename: filename, body: body, content_hash: digest)
        job = document.jobs.create!(status: "running", provider_method: "rules", provider_label: "local-rules")
        publish(document, parsed, generation: 1, locked: [])
        job.update!(status: "completed")
      end
      document
    end

    def correct(section, category)
      unless Lexicon::CATEGORIES.include?(category) && category != "mixed"
        raise Error.new("validation", "kategori tidak dikenal")
      end

      ActiveRecord::Base.transaction do
        replace(section, category: category, method: "user", reason: "koreksi pengguna", generation: next_generation(section.document))
      end
      section.document.reload
    end

    def reprocess(document)
      ActiveRecord::Base.transaction do
        job = document.jobs.create!(
          status: "running",
          attempt: document.jobs.maximum(:attempt).to_i + 1,
          provider_method: "rules",
          provider_label: "local-rules"
        )
        generation = next_generation(document)
        locked = document.sections.select(&:user_locked?).map(&:id)
        document.sections.order(:ordinal).each do |section|
          next if locked.include?(section.id)

          category, reason = Lexicon.consensus(section.body_text, filename: document.filename)
          replace(section, category: category, method: "consensus", reason: reason, generation: generation)
        end
        job.update!(status: "completed")
      end
      document.reload
    end

    def load_demo_fixtures(notebook)
      dir = Rails.root.join("..", "fixtures", "demo")
      raise Error.new("validation", "folder contoh tidak ada") unless dir.directory?

      dir.children.select { |path| %w[.md .txt].include?(path.extname) }.sort.each do |path|
        upload(notebook, path.basename.to_s, path.read)
      end
      notebook
    end

    private

    def text_layer?(filename)
      %w[.pdf .docx].include?(File.extname(filename.to_s).downcase)
    end

    def read_text_layer(notebook, filename, body, byte_size)
      binary = body.to_s.dup.force_encoding(Encoding::ASCII_8BIT)
      if binary.empty?
        plan = Lexicon.intake_plan(filename, "", byte_size)
        return notebook.intakes.create!(plan.merge(filename: filename, byte_size: byte_size || 0))
      end

      result = Readers.extract(filename, binary)
      kind = File.extname(filename).downcase == ".pdf" ? "pdf" : "designed"
      route = File.extname(filename).downcase == ".pdf" ? "text_layer_or_ocr" : "text_layer"
      if result[:status] == "mapped"
        document = upload(notebook, filename, result[:text], character_limit: Readers::MAX_TEXT)
        return notebook.intakes.create!(
          physical_kind: kind,
          route: route,
          status: "mapped",
          reason: result[:reason],
          document: document,
          filename: filename,
          byte_size: binary.bytesize
        )
      end

      notebook.intakes.create!(
        physical_kind: kind,
        route: route,
        status: "blocked",
        reason: result[:reason],
        filename: filename,
        byte_size: binary.bytesize
      )
    end

    def validate!(filename, body, character_limit: 200_000)
      raise Error.new("validation", "teks dokumen kosong") if body.blank?
      raise Error.new("validation", "dokumen lebih dari #{character_limit} karakter") if body.length > character_limit
      if filename.blank? || filename.include?("/") || filename.include?("\\") || filename.start_with?(".")
        raise Error.new("validation", "nama berkas harus label, bukan jalur")
      end
    end

    def next_generation(document)
      [document.classifications.maximum(:generation), document.claims.maximum(:generation)].compact.max.to_i + 1
    end

    def publish(document, parsed, generation:, locked:)
      parsed.each do |row|
        section = document.sections.create!(
          ordinal: row[:ordinal],
          body_text: row[:text],
          start_offset: row[:start],
          end_offset: row[:finish]
        )
        next if locked.include?(section.id)

        category, reason = Lexicon.consensus(row[:text], filename: document.filename)
        replace(section, category: category, method: "consensus", reason: reason, generation: generation)
      end
    end

    def replace(section, category:, method:, reason:, generation:)
      carried = {}
      section.claims.where(state: "active").find_each do |claim|
        review = claim.review_decisions.order(:id).last
        carried[claim.quote] = review if review
      end
      section.classifications.where(state: "active").update_all(state: "stale", updated_at: Time.current)
      section.claims.where(state: "active").update_all(state: "stale", updated_at: Time.current)
      section.extracted_fields.where(state: "active").update_all(state: "stale", updated_at: Time.current)
      section.classifications.create!(category: category, method: method, reason: reason, state: "active", generation: generation)
      Lexicon.claim_drafts(section.body_text).each do |draft|
        start = section.body_text.index(draft[:quote])
        raise Error.new("validation", "kutipan tidak ada di teks sumber") if start.nil?

        claim = section.claims.create!(
          document: section.document,
          notebook: section.document.notebook,
          quote: draft[:quote],
          start_offset: section.start_offset + start,
          end_offset: section.start_offset + start + draft[:quote].length,
          polarity: draft[:polarity],
          modality: draft[:modality],
          predicate: draft[:predicate],
          method: method,
          state: "active",
          generation: generation
        )
        copy_review(claim, carried[draft[:quote]])
      end
      Lexicon.field_drafts(section.body_text, category).each do |draft|
        section.extracted_fields.create!(
          document: section.document,
          name: draft[:name],
          value: draft[:value],
          quote: draft[:quote],
          method: method,
          state: "active",
          generation: generation
        )
      end
    end

    def copy_review(claim, review)
      return unless review

      claim.review_decisions.create!(
        notebook: claim.notebook,
        decision: review.decision,
        note: review.note,
        authority: review.authority,
        previous_status: review.previous_status,
        next_status: review.next_status
      )
    end
  end
end
