module Evidence
  # Pure text rules. No database.
  module Lexicon
    CATEGORIES = %w[sop notulen proposal laporan_progres other].freeze
    KEYWORDS = {
      "notulen" => ["notulen", "peserta", "keputusan", "rapat"],
      "sop" => ["sop", "prosedur", "langkah", "penanggung jawab"],
      "proposal" => ["proposal", "latar belakang", "anggaran"],
      "laporan_progres" => ["laporan progres", "capaian", "hambatan"]
    }.freeze
    FIELD_PATTERNS = {
      "peserta" => /^peserta\s*:\s*(.+)$/i,
      "keputusan" => /^keputusan\s*:\s*(.+)$/i,
      "tindakan" => /^tindakan\s*:\s*(.+)$/i,
      "langkah" => /^langkah(?:\s*\d+)?\s*:\s*(.+)$/i,
      "penanggung_jawab" => /^penanggung jawab\s*:\s*(.+)$/i,
      "tujuan" => /^tujuan\s*:\s*(.+)$/i,
      "anggaran" => /^anggaran\s*:\s*(.+)$/i,
      "capaian" => /^capaian\s*:\s*(.+)$/i,
      "hambatan" => /^hambatan\s*:\s*(.+)$/i
    }.freeze
    CATEGORY_FIELDS = {
      "sop" => %w[langkah penanggung_jawab],
      "notulen" => %w[peserta keputusan tindakan],
      "proposal" => %w[tujuan anggaran],
      "laporan_progres" => %w[capaian hambatan],
      "other" => []
    }.freeze

    def sections(body)
      found = []
      buf = []
      buf_start = 0
      pos = 0
      flush = lambda do
        raw = buf.join
        buf.clear
        return if raw.strip.empty?

        lead = raw[/\A\n*/].to_s.length
        text = raw.strip
        start = buf_start + lead
        start = body.index(text, buf_start) if body[start, text.length] != text
        found << { ordinal: found.length, start: start, finish: start + text.length, text: text }
      end
      body.each_line do |line|
        if line.strip.empty?
          flush.call unless buf.empty?
          pos += line.length
          buf_start = pos
        else
          buf_start = pos if buf.empty?
          buf << line
          pos += line.length
        end
      end
      flush.call unless buf.empty?
      found.each do |section|
        if body[section[:start], section[:text].length] != section[:text]
          raise Error.new("validation", "offset bagian tidak cocok dengan teks sumber")
        end
      end
      found
    end

    def classify(text)
      scores = KEYWORDS.transform_values { |words| words.select { |word| text.downcase.include?(word) } }
      best = scores.values.map(&:length).max
      return ["other", "tidak ada kata kunci kategori"] if best.zero?

      winners = scores.select { |_name, hits| hits.length == best }.keys
      return ["other", "kata kunci dua kategori sama kuat"] if winners.length != 1

      [winners.first, "kecocokan leksikal: #{scores[winners.first].join(', ')}"]
    end

    # Three raters vote without seeing each other.
    # The filename rater is recorded and then ignored when it is the only vote
    # or when it contradicts the text. Disagreement becomes other.
    def consensus(text, filename: nil)
      kata = keyword_vote(text)
      isian = field_vote(text)
      nama = filename_vote(filename)
      category, status = agree(kata, isian)
      detail = "kata=#{kata || "abstain"}; isian=#{isian || "abstain"}; nama=#{nama || "abstain"}"
      detail = "#{detail}, diabaikan" if nama && nama != category
      reason = case status
      when :sepakat then "konsensus #{category}: #{detail}"
      when :sendiri then "satu penilai, tanpa bantahan: #{detail}"
      else "konsensus gagal, jenis other: #{detail}"
      end
      [category, reason]
    end

    # Decides the physical path before any reader runs.
    # Designed files are not OCR. OCR is only the branch for pixels.
    def intake_plan(filename, body, byte_size = nil)
      ext = File.extname(filename.to_s).downcase
      if %w[.txt .md .markdown].include?(ext)
        return intake("plain", "reject", "blocked", "teks dokumen kosong") if body.to_s.strip.empty?
        if body.to_s.length > 200_000
          return intake("plain", "chunk", "blocked", "Berkas teks lebih dari 200000 karakter. Ia harus dipotong per halaman atau per blok sebelum penilai. Pemotongan belum dijalankan, dan isi tidak disimpan.")
        end

        return intake("plain", "direct", "mapped", "Teks polos. Tidak lewat OCR. Langsung dipecah pada baris kosong.")
      end
      if ext == ".pdf"
        return intake("pdf", "text_layer_or_ocr", "blocked", "PDF belum dibuka. Jalur yang benar: baca lapisan teks bila ada, lalu susun urutan baca untuk kolom, kop, dan tabel. OCR hanya untuk halaman yang tidak punya lapisan teks. Keduanya belum dijalankan.")
      end
      if %w[.png .jpg .jpeg .tif .tiff .webp .bmp].include?(ext)
        return intake("image", "ocr", "blocked", "Gambar adalah piksel. Jalurnya OCR per halaman, lalu urutan baca. OCR belum dijalankan.")
      end
      if %w[.docx .pptx .odt].include?(ext)
        return intake("designed", "text_layer", "blocked", "Berkas berdesain ini menyimpan teks di dalam XML, bukan gambar. Jalurnya ambil teks dan urutan bentuk. Bukan OCR. Belum dijalankan.")
      end
      if %w[.m4a .mp3 .wav .aac .mp4 .mov .webm].include?(ext)
        return intake("recording", "transcript", "blocked", "Rekaman butuh transkrip, bukan OCR. Transkrip belum dijalankan.")
      end

      intake("unknown", "reject", "blocked", "Jenis fisik tidak dikenal. Tidak ada OCR yang dijalankan.")
    end

    def sentences(text)
      found = []
      text.to_enum(:scan, /[^.!?\n]+(?:[.!?]|$)/).each do
        raw = Regexp.last_match(0)
        stripped = raw.strip
        next if stripped.length < 8

        lead = raw.length - raw.lstrip.length
        start = Regexp.last_match.begin(0) + lead
        next unless text.byteslice(start, stripped.length) == stripped

        found << [start, stripped]
      end
      attach_codes(text, found)
    end

    def claim_drafts(text)
      sentences(text).map do |sentence|
        {
          quote: sentence,
          polarity: sentence.match?(/\b(tidak|bukan|belum)\b/i) ? "negated" : "affirmed",
          modality: sentence.match?(/\b(direncanakan|rencana|dijadwalkan)\b/i) ? "plan" : "asserted",
          predicate: predicate_for(sentence)
        }
      end
    end

    extend self

    def field_drafts(text, category)
      CATEGORY_FIELDS.fetch(category).filter_map do |name|
        match = text.match(FIELD_PATTERNS.fetch(name))
        next unless match

        { name: name, value: match[1].strip, quote: match[0].strip }
      end
    end

    private

    def intake(kind, route, status, reason)
      { physical_kind: kind, route: route, status: status, reason: reason }
    end

    def keyword_vote(text)
      category, = classify(text)
      category == "other" ? nil : category
    end

    def field_vote(text)
      votes = text.each_line.flat_map do |line|
        FIELD_PATTERNS.filter_map do |name, pattern|
          category_for_field(name) if line.match?(pattern)
        end
      end.uniq
      votes.one? ? votes.first : nil
    end

    def filename_vote(filename)
      base = File.basename(filename.to_s, ".*").downcase.tr("_", " ").tr("-", " ")
      hits = {
        "sop" => base.match?(/\bsop\b/),
        "notulen" => base.include?("notulen"),
        "proposal" => base.include?("proposal"),
        "laporan_progres" => base.include?("laporan progres") || base.include?("laporanprogres")
      }.select { |_category, hit| hit }.keys
      hits.one? ? hits.first : nil
    end

    def category_for_field(name)
      CATEGORY_FIELDS.each do |category, names|
        return category if names.include?(name)
      end
      nil
    end

    def agree(kata, isian)
      if kata && isian
        kata == isian ? [kata, :sepakat] : ["other", :gagal]
      elsif kata || isian
        [kata || isian, :sendiri]
      else
        ["other", :gagal]
      end
    end

    def predicate_for(sentence)
      if sentence.match?(/hadir|ikut meeting|mengikuti/i)
        "attendance"
      elsif sentence.match?(/\bpilot\b/i)
        "pilot"
      else
        ""
      end
    end

    def attach_codes(text, found)
      merged = []
      index = 0
      while index < found.length
        current = found[index][1]
        if index + 1 < found.length && found[index + 1][1].match?(/\AKode\s+\S+\z/)
          joined = "#{current} #{found[index + 1][1]}"
          if text.include?(joined)
            merged << joined
            index += 2
            next
          end
        end
        merged << current
        index += 1
      end
      merged
    end
  end
end
