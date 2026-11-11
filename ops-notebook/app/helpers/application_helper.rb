module ApplicationHelper
  DECISION_LABELS = {
    "accepted" => "diterima",
    "rejected" => "ditolak",
    "needs_evidence" => "bukti kurang",
    "status_changed" => "status diubah"
  }.freeze

  def decision_label(decision)
    DECISION_LABELS.fetch(decision.to_s, decision.to_s)
  end

  FILE_KINDS = {
    ".txt" => "teks",
    ".md" => "markdown",
    ".markdown" => "markdown",
    ".pdf" => "pdf",
    ".docx" => "docx"
  }.freeze

  def quote_held?(claim)
    claim.section&.body_text.to_s.include?(claim.quote.to_s)
  end

  def file_kind(filename)
    FILE_KINDS.fetch(File.extname(filename.to_s).downcase, "ekstensi tidak dikenal")
  end

  def review_badge(claim)
    review = claim.latest_review
    return "belum ditinjau" unless review

    decision_label(review.decision)
  end

  # What actually runs today, what blocks the stage, and the next improvement.
  # A model is listed only as a later step. None is called.
  PIPELINE = [
    {
      key: "show",
      title: "Dump",
      uses: "Rails dan PostgreSQL",
      how: "Berkas masuk sebagai arsip. Rekaman pekerjaan dan orang disimpan terpisah, tidak diambil dari kalimat berkas.",
      stuck: "Simpan selesai di dalam permintaan yang sama. Tidak ada antrian, jadi dump besar menahan halaman.",
      improve: "Antrian setelah data tersimpan, supaya unggahan tidak menahan halaman."
    },
    {
      key: "pemetaan",
      title: "Pemetaan",
      uses: "Lapisan teks PDF dan XML DOCX",
      how: "Teks polos kecil dilanjutkan. PDF yang punya lapisan teks dan DOCX yang punya XML diubah menjadi teks bagian. Gambar, rekaman, PPTX, dan PDF tanpa teks ditahan.",
      stuck: "OCR, transkrip, PPTX, dan urutan kolom belum ada. Halaman yang hanya berupa gambar tidak dibaca.",
      improve: "OCR hanya untuk halaman tanpa lapisan teks. Susun urutan kolom dan tabel."
    },
    {
      key: "proses",
      title: "Proses",
      uses: "Tiga penilai aturan",
      how: "Kata di dalam teks dan baris isian menimbang sendiri-sendiri. Nama berkas dicatat, lalu diabaikan bila berselisih. Tidak sepakat menjadi other.",
      stuck: "Penilai berjalan di dalam permintaan yang sama. Prosa yang tidak berbentuk Nama: nilai tidak menjadi isian.",
      improve: "Bila isi abstain, nama berkas boleh menjadi penanda lemah yang tetap terlihat dan bisa dikoreksi."
    },
    {
      key: "analisis",
      title: "Analisis",
      uses: "Baris PostgreSQL, skema tertutup",
      how: "Jenis membuka daftar kolom. Hanya baris yang tertulis yang disimpan, menempel pada kutipan.",
      stuck: "Label di luar skema, misalnya Risiko atau PIC, tidak menjadi peserta, langkah, atau anggaran.",
      improve: "Kolom baru ditambah dengan sengaja. Usulan model, kalau ada nanti, tetap berstatus calon sampai orang menerima."
    },
    {
      key: "keputusan",
      title: "Keputusan",
      uses: "Aturan bentrok dan modalitas",
      how: "Rencana tidak dihitung sebagai kejadian. Klaim yang ditolak tidak dipakai. Bentrok tetap terlihat.",
      stuck: "Bentrok yang dikenali masih sempit: tanggal pilot yang berbeda, dan kehadiran yang saling menolak.",
      improve: "Orang tetap yang memutuskan. Model tidak boleh menutup bentrok."
    },
    {
      key: "verifikasi",
      title: "Verifikasi",
      uses: "Cek kutipan ke teks sumber",
      how: "Kutipan harus masih ada di teks. Pemeriksaan tidak membaca jenis berkas. Kemiripan topik bukan dukungan.",
      stuck: "Belum ada peninjau kedua. Setiap keputusan masih manual, dan belum ada akun.",
      improve: "Jawaban model, kalau dipasang, tetap harus lolos cek kutipan ini. Gagal berarti ditolak."
    },
    {
      key: "tanya",
      title: "Tanya",
      uses: "Irisan kata, semantic false",
      how: "Pertanyaan mencari judul bagian, isian, dan klaim, lalu mengulang baris yang ketemu. Tidak ada baris berarti menolak. Model tidak menulis SQL.",
      stuck: "Beda susunan kata bisa tidak ketemu, karena ini irisan kata, bukan makna. Chat tidak menyusun kalimat.",
      improve: "Model seperti Gemini boleh mengembalikan maksud tertutup, misalnya jenis dan nama kolom. Rails yang menyusun kueri."
    }
  ].freeze

  def pipeline_key
    action_name == "query" ? "tanya" : action_name
  end
end
