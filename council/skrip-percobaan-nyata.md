# Skrip percobaan nyata

Buka http://127.0.0.1:3000/?notebook_id=20. Ruang ini bernama "Uji ujung ke ujung 11 Nov". Percobaan dimulai dari ruang kosong. Model tidak terpasang. Layar Tanya menulis metode `rules` dan `semantic false`.

## Yang diucapkan

Saya mulai dari ruang kosong, bukan dari contoh yang sudah terisi.

Pertama saya menaruh berkas. `lapisan-uji.pdf` saya dump bersama teks dan DOCX. Di Pemetaan, sistem tidak langsung membaca isinya sebagai makna. Ia melihat bentuk fisiknya dulu. PDF itu berstatus dipetakan, jalur `text_layer_or_ocr`. Kalimat di kartu berbunyi: lapisan teks diambil per halaman, urutan mengikuti aliran berkas, kolom dan tabel belum disusun ulang. `pindai-rapat.png` berhenti di langkah yang sama, status ditahan, karena berkas itu piksel dan OCR belum dijalankan. `anggaran-uji.docx` berstatus dipetakan karena teksnya diambil dari XML paragraf.

Cara sistem melihat struktur begini. Teks yang sudah keluar dari PDF dipotong pada baris kosong. Setiap potongan menyimpan posisi awal dan akhir di teks sumber. Kalau potongan itu tidak sama persis dengan sumber, unggah gagal. Dari situ muncul bagian, lalu baris isian hanya jika tertulis seperti `Peserta:` atau `Anggaran:`. Kalimat yang memuat tidak, bukan, atau belum ditandai negated. Kalimat yang memuat rencana atau dijadwalkan ditandai sebagai rencana, bukan kejadian.

Pada percobaan ini, konteks tidak dipahami oleh model AI. Di halaman Proses tertulis: jenis isi dipilih tiga penilai yang tidak saling melihat, yaitu kata, isian, dan nama berkas. Nama berkas hanya dicatat. Kalau kata dan isian berbeda, jenisnya other. Kalimat di halaman itu: ini masih aturan, bukan model. Di Analisis, proses tersimpan berlabel `local-rules`. Gemini atau model lain belum dipasang, dan berkas tidak dikirim ke model pihak ketiga.

Klasifikasi yang terlihat adalah jenis file dari ekstensi, lalu jenis isi per bagian. Satu berkas boleh punya lebih dari satu bagian. Notulen menyimpan peserta dan keputusan. Proposal menyimpan anggaran. Kolom yang tidak tertulis tidak dibuat.

Lalu verifikasi. Kutipan diletakkan di samping teks sumber. Orang menerima, menolak, atau meminta bukti lagi. Keputusan itu tidak ditimpa saat berkas diproses ulang.

Saat ditanya, yang menjawab masih aturan yang sama. Hasil pada ruang ini:

- Apa status Budiono? Jawaban occurred, rute db_only.
- Apa status Budi? Jawaban unknown. Nama itu tidak meminjam status Budiono.
- Apakah Budi hadir? Jawaban negated, dari kalimat yang memuat tidak hadir.
- Apakah pilot sudah berjalan? Jawaban plan_not_occurrence.
- Berapa harga saham kemarin? Jawaban abstain.
- Pertanyaan yang menempel identitas Onboarding dan kata dokumen menjawab planned, rute combined.
- Berapa anggaran uji DOCX? Baris anggaran ketemu, tetapi keputusan dan kalimat kehadiran dari berkas lain ikut tertarik.
- Apakah Sari hadir? Jawaban conflict, karena jalur kehadiran masih mencampur klaim semua orang.

Bagian "model sudah bisa menjawab dengan mudah" belum terjadi. Tempat model dipasang nanti ada dua. Model mengusulkan jenis bagian saat dua penilai seri, atau mengarahkan pertanyaan ke satu operasi yang sudah ada. Jawaban akhir tetap baris yang tersimpan. Usulan yang kutipannya tidak ada di teks dibuang. Kalau model tidak selesai, aturan tetap menjawab dan kegagalan itu tetap tertulis.

## Kenapa belum memakai jalur RAG besar

Ada jalur lain untuk ribuan jurnal berukuran terabyte: MCP, prompt pengguna, similarity search, reranking, pembobotan ulang, sentuhan LLM pada keluaran, dan klien Vercel AI SDK. Kekurangannya yang disebut pemilik jalur itu: memori tidak bisa besar dan token menjadi mahal.

Jalur itu belum dipakai di prototipe ini. Korpus uji adalah beberapa berkas, bukan terabyte. Pertanyaan operasional punya identitas, status, dan kutipan. Similarity search membuang sebagian besar korpus sebelum reranking. Dokumen yang benar, kalau jatuh di situ, tidak kembali. Ibrahim Arief, pada balasan yang ditempel, menanyakan apakah recall jalur semacam itu pernah dievaluasi, dan memperkirakan 95 sampai 98 persen korpus tidak lanjut dari langkah similarity. Angka itu perkiraan beliau pada jalur orang lain, bukan hasil ukur aplikasi ini. Post beliau sendiri, 9 November 2026, memakai tahap recall pada simpul graf lalu rerank besar. Bedanya, saringan pertama beliau adalah simpul yang sudah bertipe, bukan kemiripan atas jurnal mentah, dan biaya rerank-nya ia sebut sendiri: sekitar 1,2 juta token per pertanyaan.

Pada ruang uji, pertanyaan anggaran DOCX sudah menarik kalimat kehadiran dari berkas lain hanya karena irisannya kata. Itu versi kecil dari risiko yang sama. Reranking dan sentuhan LLM di akhir tidak memperbaiki dokumen yang sudah terbuang di langkah ketiga. MCP dan AI SDK mengangkut permintaan. Keduanya tidak memilih bukti.

Jalur itu masuk akal setelah korpusnya besar, ada label untuk menghitung recall, dan ada batas token. Sebelum angka itu ada, jawaban tetap baris yang tersimpan atau abstain.
