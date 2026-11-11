require "stringio"
require "pdf/reader"
require "zip"

module Evidence
  # Reads a text layer that is already inside the file.
  # A scanned page is not converted. OCR is not called.
  module Readers
    extend self

    MAX_TEXT = 1_500_000
    MAX_PDF_PAGES = 300
    MAX_DOCX_BYTES = 30_000_000
    MAX_XML_BYTES = 20_000_000

    def extract(filename, binary)
      case File.extname(filename.to_s).downcase
      when ".pdf" then pdf(binary)
      when ".docx" then docx(binary)
      else
        blocked("Jenis fisik tidak dikenal. Tidak ada konversi yang dijalankan.")
      end
    end

    private

    def pdf(binary)
      reader = PDF::Reader.new(StringIO.new(binary))
      return blocked("PDF lebih dari #{MAX_PDF_PAGES} halaman. Isi tidak disimpan.") if reader.page_count > MAX_PDF_PAGES

      found = []
      empty = []
      reader.pages.each_with_index do |page, index|
        text = page.text.to_s.gsub("\r\n", "\n").gsub("\r", "\n").strip
        text.empty? ? empty << (index + 1) : found << [index + 1, text]
      end
      return blocked("PDF tidak punya lapisan teks. OCR untuk halaman gambar belum dijalankan, dan isi tidak disimpan.") if found.empty?

      text = found.map { |number, body| "Halaman #{number}\n\n#{body}" }.join("\n\n")
      return blocked("Teks hasil baca lebih dari #{MAX_TEXT} karakter. Isi tidak disimpan.") if text.length > MAX_TEXT

      reason = "Lapisan teks PDF diambil per halaman. Urutan dalam halaman mengikuti aliran teks berkas, belum disusun ulang untuk kolom atau tabel."
      reason += " Halaman tanpa lapisan teks: #{empty.join(', ')}. OCR belum dijalankan untuk halaman itu." if empty.any?
      mapped(text, reason)
    rescue PDF::Reader::MalformedPDFError, PDF::Reader::UnsupportedFeatureError
      blocked("PDF tidak bisa dibuka. Isi tidak disimpan. OCR tidak dijalankan.")
    end

    def docx(binary)
      return blocked("DOCX lebih dari 30 MB. Isi tidak disimpan.") if binary.bytesize > MAX_DOCX_BYTES

      xml = nil
      Zip::File.open_buffer(binary) do |zip|
        entry = zip.find_entry("word/document.xml")
        return blocked("DOCX tidak punya word/document.xml. Isi tidak disimpan.") unless entry
        return blocked("XML DOCX terlalu besar. Isi tidak disimpan.") if entry.size > MAX_XML_BYTES

        xml = entry.get_input_stream.read
      end
      xml = xml.to_s.dup.force_encoding("UTF-8").scrub
      return blocked("XML DOCX memuat entity. Isi tidak disimpan.") if xml.match?(/<!DOCTYPE|<!ENTITY/i)

      text = paragraphs(xml).join("\n").strip
      return blocked("XML DOCX terbaca, tetapi tidak ada teks. Isi tidak disimpan. Bukan OCR.") if text.empty?
      return blocked("Teks hasil baca lebih dari #{MAX_TEXT} karakter. Isi tidak disimpan.") if text.length > MAX_TEXT

      mapped(text, "Teks DOCX diambil dari XML paragraf, sesuai urutan berkas. Bukan OCR. Urutan kolom dan tabel belum disusun ulang.")
    rescue Zip::Error
      blocked("DOCX tidak bisa dibuka. Isi tidak disimpan.")
    end

    def paragraphs(xml)
      prepared = xml.gsub(/<w:tab\/>/, "\t").gsub(/<w:br\/>/, "\n")
      prepared.split(/<w:p[\s>]/).drop(1).map do |para|
        body = para.split("</w:p>", 2).first.to_s
        body.scan(/<w:t(?:\s[^>]*)?>(.*?)<\/w:t>/m).flatten.map { |piece| unescape(piece) }.join
      end
    end

    def unescape(text)
      text.gsub("&amp;", "&").gsub("&lt;", "<").gsub("&gt;", ">").gsub("&quot;", '"').gsub("&apos;", "'")
    end

    def mapped(text, reason)
      { status: "mapped", text: text, reason: reason }
    end

    def blocked(reason)
      { status: "blocked", text: nil, reason: reason }
    end
  end
end
