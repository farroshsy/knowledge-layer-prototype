# Referensi lintas kasus: klasifikasi vs knowledge layers

Arahan terbaru pengguna: bandingkan referensi serupa di domain lain; ia menduga fokus CTO adalah document classification. Ini hipotesis yang perlu diselaraskan dengan permintaan layer/struktur/premis sebelumnya, bukan alasan otomatis menghapus source lineage.

## 1. Microsoft Content Understanding: berkas keuangan dan aplikasi pinjaman

Sumber primer: https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/concepts/classifier

Dokumentasi membedakan classify, segment, dan analyze. Satu file dapat berisi beberapa dokumen; klasifikasi dapat menentukan extractor yang sesuai. Contoh aplikasi pinjaman berisi formulir, slip gaji dan rekening koran. Konsep yang dapat diadaptasi: definisi kategori yang eksplisit, segmen beserta page range, kemudian ekstraksi dengan schema sesuai kategori. Unknown/other dan hasil yang perlu diperiksa harus punya perilaku terdefinisi. Tidak perlu memakai layanan Azure berbayar untuk mengambil pola desainnya. Perhatikan dokumentasi membedakan GA vs preview; jangan campur batas unit segmentasi antarversi.

## 2. Docling: struktur dan model dokumen

Sumber primer: https://docling-project.github.io/docling/concepts/docling_document/

Referensi ini berguna untuk model parsing dokumen, bukan classifier bisnis siap pakai. Periksa hierarchy, urutan bacaan, tabel dan provenance sebelum mengklaim implementasinya cocok. Parsing struktur tidak sama dengan menetapkan kategori dokumen atau membuktikan klaim. Ide untuk backend kita: satu representasi dokumen terstruktur yang tetap menyimpan lokasi asal. Jangan menambah dependensi dan download model besar sebelum mengecek kebutuhan serta biaya setup Mac Intel.

## 3. NotebookLM: penelitian dari kumpulan sumber

Sumber primer: https://support.google.com/notebooklm/answer/16164461?hl=en (saat akses diarahkan ke https://support.google.com/gemininotebook/answer/16164461?hl=en)

Dokumentasi menjelaskan pengunggahan sumber dan percakapan berbasis sumber dengan inline citations. Ini referensi pengalaman penggunaan knowledge notebook, bukan bukti arsitektur ontology/graph internal. Ambil kebutuhan source selection dan inspect citation, bukan fitur audio/mind map tambahan.

## Rekomendasi awal untuk diperdebatkan council

Gunakan satu domain dummy operasional perusahaan: SOP, notulen rapat, proposal/brief, laporan progres. Definisikan tiap kategori dengan deskripsi dan contoh/kontra-contoh; satu kategori other/unknown. Klasifikasi menentukan schema, misalnya notulen mempunyai peserta, keputusan dan action item; SOP mempunyai langkah dan tanggung jawab. Pisahkan category (jenis dokumen) dari layer (level representasi informasi).

Vertical slice yang diprioritaskan: ingest -> parsing/lokasi sumber -> klasifikasi dan koreksi -> ekstraksi sesuai kategori -> inspect hasil dan provenance. Tambahkan query grounded minimal hanya jika diperlukan untuk membuktikan penggunaan lapisan hasil; jangan bangun chatbot kaya fitur sebelum klasifikasi/lineage bekerja. Tetap pakai contoh negatif, campuran jenis dalam satu file dan kategori yang tidak dikenal. Domain dan kategori ini rekomendasi untuk dummy, bukan data atau aturan resmi Rakamin.

## Pertanyaan untuk reviewer

Apakah kategori hanya label kosmetik atau benar mengubah schema ekstraksi? Apa yang terjadi pada unknown/mixed? Bagaimana menelusuri alasan klasifikasi dan asal field? Apakah koreksi kategori membuat hasil lama usang? Jika jawaban butuh relasi lintas dokumen, apa kontrak minimalnya tanpa membangun seluruh graph engine? Jangan menyamakan threshold confidence model dengan angka akurasi terukur.

## Verifikasi sumber, 2026-11-10

Tiga halaman di bawah dibaca langsung. Tidak ada layanan yang dipanggil.

### Microsoft

[Classifier overview](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/concepts/classifier), tanggal dokumen 9 Juli 2026. Perilaku GA yang tertulis:

- Classify only memberi satu kategori untuk seluruh berkas.
- Classify and analyze mengarahkan berkas ke analyzer ekstraksi lewat `analyzerId`.
- Classify and segment memecah satu berkas yang berisi beberapa dokumen dan mengembalikan rentang halaman. Contoh paket pinjaman: formulir, slip gaji, rekening koran.
- Classify, segment, and analyze mengarahkan tiap segmen ke analyzer masing-masing.
- `analyzerId` boleh dikosongkan: ada kategori, tidak ada ekstraksi field.
- Sejak GA, kategori `other` wajib. Tanpa kategori itu, semua isi dipaksa masuk ke kategori yang didefinisikan.
- Unit minimum GA adalah satu halaman. Klasifikasi di dalam satu halaman tidak didukung pada GA.
- Preview `2026-06-01-preview` menambah `allowInPageSegments` dan skor `confidence` 0–1. Dokumen itu menyebut preview bukan GA. Skor itu bukan akurasi yang diukur.

Ini pola desain, bukan komponen yang akan dipasang. Demo tidak memakai Azure.

### Docling

[DoclingDocument](https://docling-project.github.io/docling/concepts/docling_document/). Representasi parsing: `texts`, `tables`, `pictures`, `key_value_items`, pohon `body` dan `furniture`, plus provenance dan bounding box bila ada. Ini bukan classifier bisnis. Struktur dan lokasi tidak sama dengan kategori, dan tidak membuktikan klaim. Dependensi Docling dan model unduhan tidak masuk demo.

### Gemini Notebook

[Learn about Gemini Notebook](https://support.google.com/gemininotebook/answer/16164461?hl=en). URL NotebookLM pada arahan diarahkan ke halaman ini. Yang tertulis: unggah sumber, lalu percakapan berbasis sumber dengan sitasi inline. Salah satu alasan tidak menjawab adalah informasi tidak ada di sumber. Audio overview dan mind map ada di produk itu dan tidak diambil. Halaman ini bukan spesifikasi ontology atau graph internal.

## Kontrak yang mengikat council

Satu domain dummy operasional perusahaan: `sop`, `notulen`, `proposal`, `laporan_progres`, dan `other`. Bukan data Rakamin.

Kategori adalah label jenis segmen. Lapisan adalah tingkat representasi: berkas, span, pernyataan, relasi, premis, sintesis. Kategori tidak menaikkan status fakta.

Klasifikasi boleh memilih schema field tambahan, dan hanya itu. Notulen boleh punya peserta, keputusan, dan action item. SOP boleh punya langkah dan penanggung jawab. Semua kategori tetap memakai span, kutipan, polaritas, modalitas, dan atribusi. `other` dan segmen campuran yang belum terklasifikasi tidak mendapat field kategori. Teks dan lokasinya tetap disimpan.

Satu berkas boleh berisi beberapa segmen. Satu label untuk seluruh berkas gagal pada berkas campuran.

Koreksi kategori membuat turunan yang terikat pada penetapan lama menjadi basi. Span sumber tetap. Field schema lama tidak boleh tetap aktif.

Relasi lintas dokumen untuk slice ini hanya pasangan konflik atau dukungan yang sudah ada di uji peninjau. Bukan mesin graph baru, bukan Azure, bukan Docling, bukan fitur NotebookLM.
