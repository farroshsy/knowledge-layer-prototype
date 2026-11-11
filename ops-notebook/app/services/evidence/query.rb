module Evidence
  # Closed routes: db_only, document_only, combined, unsupported.
  module Query
    extend self

    def ask(notebook, question)
      text = question.to_s.strip
      raise Error.new("validation", "pertanyaan kosong") if text.empty?
      raise Error.new("not_found", "notebook tidak ditemukan") if notebook.nil?

      records = notebook.business_records.order(:id).to_a
      claims = usable_claims(notebook)
      ids = records.select { |record| exact_id?(text, record.public_id) }
      names = names_in_question(text, records)
      if ids.empty? && names.length > 1 && names.map { |row| row.display_name.downcase }.uniq.one?
        return result("db_only", "ambiguous", "lebih dari satu rekaman cocok dan tidak dipilih salah satu", records: names)
      end
      return document_answer(text, claims) if legacy_document_question?(text)

      if wants_documents?(text) && ids.one?
        linked = claims.select { |claim| exact_id?(claim.quote, ids.first.public_id) }
        if linked.any?
          return result("combined", status_answer(ids.first, text), "kutipan memuat id rekaman yang sama persis", records: ids, claims: linked)
        end

        return result("db_only", "insufficient_evidence", "rekaman ada, tetapi tidak ada kutipan yang memuat id itu", records: ids)
      end

      chosen = ids.presence || names
      if chosen.empty?
        return retrieve_structured(notebook, text)
      end
      if chosen.length > 1
        return result("db_only", "ambiguous", "lebih dari satu rekaman cocok dan tidak dipilih salah satu", records: chosen)
      end

      result("db_only", status_answer(chosen.first, text), status_reason(chosen.first), records: [chosen.first])
    end

    DATE_RE = /\b\d{1,2}\s+(?:Januari|Februari|Maret|April|Mei|Juni|Juli|Agustus|September|Oktober|November|Desember)\b/
    NAME_RE = /\b[A-Z][a-z]{2,}\b/

    def conflicts(claims)
      pairs = []
      seen = {}
      dated = claims.filter_map do |claim|
        next unless claim.predicate == "pilot" && claim.modality == "plan"

        date = claim.quote[DATE_RE]
        [claim, date] if date
      end
      dated.each_with_index do |(left, left_date), index|
        dated[(index + 1)..].each do |right, right_date|
          next if left_date == right_date

          remember(pairs, seen, left, right)
        end
      end
      attendance = claims.select { |claim| claim.predicate == "attendance" }
      attendance.each_with_index do |left, index|
        left_names = left.quote.scan(NAME_RE)
        attendance[(index + 1)..].each do |right|
          next if left.polarity == right.polarity
          next if (left_names & right.quote.scan(NAME_RE)).empty?

          remember(pairs, seen, left, right)
        end
      end
      pairs
    end

    private

    def document_answer(question, claims)
      if question.match?(/\b(siapa|who)\b/i) && question.match?(/\bhadir\b/i)
        chosen = claims.select { |claim| claim.predicate == "attendance" && claim.polarity == "affirmed" }
        return chosen.empty? ? result("unsupported", "abstain", "tidak ada klaim kehadiran affirmed") : result("document_only", "claims", "klaim kehadiran affirmed", claims: chosen)
      end
      if question.match?(/\bhadir|ikut\b/i)
        chosen = claims.select { |claim| claim.predicate == "attendance" }
        polarities = chosen.map(&:polarity).uniq
        answer = if polarities == ["negated"]
                   "negated"
                 elsif polarities.include?("negated") && polarities.include?("affirmed")
                   "conflict"
                 elsif chosen.any?
                   "claims"
                 else
                   "abstain"
                 end
        route = answer == "abstain" ? "unsupported" : "document_only"
        reason = {
          "negated" => "klaim kehadiran yang tersimpan bersifat negated",
          "conflict" => "klaim affirmed dan negated sama-sama tersimpan",
          "abstain" => "tidak ada klaim kehadiran yang masih boleh dipakai"
        }.fetch(answer, "klaim kehadiran yang tersimpan")
        return result(route, answer, reason, claims: chosen)
      end
      if question.match?(/\bpilot\b/i) && question.match?(/\b(berjalan|sudah|terjadi)\b/i)
        chosen = claims.select { |claim| claim.predicate == "pilot" && claim.modality == "plan" }
        return chosen.empty? ? result("unsupported", "abstain", "tidak ada klaim rencana pilot") : result("document_only", "plan_not_occurrence", "rencana tidak membuktikan kejadian sudah terjadi", claims: chosen)
      end
      result("unsupported", "abstain", "tidak ada pola dokumen")
    end

    def legacy_document_question?(question)
      return false if question.match?(/\b(record|records|status|orang|person|pekerjaan|nama)\b/i)
      return false if question.match?(/[0-9a-f]{32}/i)
      return false if question.match?(/\b(dokumen(?:nya)?|documents?|docs|klaim(?:nya)?|claims?|notulen(?:nya)?)\b/i)

      question.match?(/\b(hadir|ikut)\b/i) || (question.match?(/\bpilot\b/i) && question.match?(/\b(berjalan|sudah|terjadi)\b/i))
    end

    def wants_documents?(question)
      question.match?(/\b(dokumen(?:nya)?|documents?|docs|klaim(?:nya)?|claims?|notulen(?:nya)?|quotes?|sumber teks|catatan(?:\s+teks)?)\b/i)
    end

    def names_in_question(question, records)
      consumed = []
      hits = []
      records.sort_by { |row| -row.display_name.length }.group_by { |row| row.display_name.downcase }.each_value do |group|
        spans = name_spans(question, group.first.display_name)
        fresh = spans.reject { |span| consumed.any? { |taken| span[0] < taken[1] && taken[0] < span[1] } }
        next if fresh.empty?

        hits.concat(group)
        consumed.concat(fresh)
      end
      hits
    end

    def name_spans(question, name)
      folded = question.downcase
      needle = name.downcase
      return [] if needle.length < 2

      spans = []
      start = 0
      while (idx = folded.index(needle, start))
        finish = idx + needle.length
        before = idx.zero? ? "" : folded[idx - 1]
        after = finish >= folded.length ? "" : folded[finish]
        spans << [idx, finish] if boundary?(before) && boundary?(after)
        start = idx + 1
      end
      spans
    end

    def boundary?(char)
      char.empty? || !char.match?(/[0-9a-z_]/)
    end

    def exact_id?(text, public_id)
      text.to_s.match?(/#{Regexp.escape(public_id)}(?![0-9a-f])/i)
    end

    def status_answer(record, question)
      return "plan_not_occurrence" if record.status == "planned" && question.match?(/\b(terjadi|berjalan|occurred|already)\b/i)

      record.status
    end

    def status_reason(record)
      if record.status == "planned"
        "#{record.display_name} berstatus planned di basis data. Rencana tidak membuktikan kejadian sudah terjadi dan tidak membuktikan kejadian tidak terjadi."
      else
        "#{record.display_name} berstatus #{record.status} di basis data. Status itu atribusi rekaman, bukan fakta universal."
      end
    end

    def usable_claims(notebook)
      notebook.claims.active.includes(:review_decisions).order(:id).reject(&:blocked?)
    end

    def remember(pairs, seen, left, right)
      key = [left.id, right.id].sort
      return if seen[key]

      seen[key] = true
      pairs << [left, right, "conflict"]
    end

    Hit = Struct.new(:kind, :filename, :heading, :name, :value, :quote, keyword_init: true)
    STOP = %w[apa siapa yang di ke dari pada dan atau untuk apakah bagaimana kapan mana ini itu ada dengan adalah secara tentang sebuah suatu].freeze

    def retrieve_structured(notebook, question)
      tokens = tokens_of(question)
      return result("unsupported", "abstain", "tidak ada operasi bisnis dan tidak ada pola dokumen") if tokens.empty?

      wanted = category_wanted(question)
      hits = []
      notebook.documents.includes(sections: [:classifications, :extracted_fields, { claims: :review_decisions }]).order(:id).each do |document|
        stack = []
        document.sections.sort_by(&:ordinal).each do |section|
          level, title = heading_level(section.body_text)
          if level
            stack = stack.take(level - 1)
            stack << title
            next
          end

          category = section.active_classification&.category
          heading = stack.join(" / ")
          next if wanted && category != wanted && !heading.downcase.include?(wanted.tr("_", " "))

          section.extracted_fields.select { |field| field.state == "active" }.each do |field|
            score = overlap(tokens, tokens_of(field.name.tr("_", " "))) * 4
            score += overlap(tokens, tokens_of(field.value)) * 2
            score += overlap(tokens, tokens_of(heading))
            next if score < 2

            hits << [score, Hit.new(kind: "isian", filename: document.filename, heading: heading, name: field.name, value: field.value, quote: field.quote)]
          end
          section.claims.select { |claim| claim.state == "active" && !claim.blocked? }.each do |claim|
            score = overlap(tokens, tokens_of(claim.quote))
            score += 3 if overlap(tokens, tokens_of(heading)).positive?
            next if score < 2

            hits << [score, Hit.new(kind: "klaim", filename: document.filename, heading: heading, name: claim.predicate, value: claim.quote, quote: claim.quote), claim]
          end
        end
      end
      top = hits.sort_by { |score, _hit, _claim| -score }.first(5)
      return result("unsupported", "abstain", wanted ? "tidak ada baris #{wanted} yang cocok" : "tidak ada baris terstruktur yang cocok") if top.empty?

      answer = top.map { |_score, hit, _claim| hit.kind == "isian" ? "#{hit.name}: #{hit.value}" : hit.value }.uniq.join("; ")
      claims = top.filter_map { |_score, _hit, claim| claim }
      result(
        "document_only",
        answer,
        "diambil dari isian atau klaim pada judul bagian yang cocok. Bukan ringkasan model.",
        claims: claims,
        rows: top.map { |_score, hit, _claim| hit }
      )
    end

    def tokens_of(text)
      text.to_s.downcase.scan(/[a-z0-9]{3,}/).reject { |token| STOP.include?(token) }.uniq
    end

    def overlap(left, right)
      (left & right).length
    end

    def category_wanted(question)
      folded = question.to_s.downcase
      return "laporan_progres" if folded.match?(/\blaporan\b|\blaporan progres\b|\blaporan\b/) || folded.include?("laporan progres")
      return "notulen" if folded.match?(/\bnotulen\b/)
      return "sop" if folded.match?(/\bsop\b|\bprosedur\b/)
      return "proposal" if folded.match?(/\bproposal\b/)

      nil
    end

    def heading_level(text)
      line = text.to_s.strip
      return nil if line.empty? || line.include?("\n")

      if (marks = line.match(/\A(\#{1,3})\s+(.+)\z/))
        return [marks[1].length, marks[2].strip]
      end
      return nil if line.length > 80 || line.match?(/[.!?]/) || line.match?(/:\s*\S/)

      [1, line]
    end

    def result(route, answer, reason, records: [], claims: [], rows: [])
      Result.new(route: route, answer: answer, reason: reason, method: "rules", semantic: false, records: records, claims: claims, rows: rows)
    end
  end
end
