# Pondasi dulu, pipeline kemudian

Catatan untuk menjelaskan ke CTO. Tanggal 11 November 2026. Ini bukan spesifikasi yang sudah dikunci, dan bukan klaim bahwa recall, F1, atau nilai bisnis sudah diukur.

Layar yang mengikuti catatan ini ada di aplikasi `ops-notebook`. Halaman **Proses** menampilkan alur pemakaian, empat rute, dan adegan **Use case berat: 150 PDF**. Halaman **Riset dan perbandingan** (`/riset`) menampilkan perbandingan sumber. Adegan 150 PDF adalah ilustrasi urutan kerja, bukan kapasitas yang sudah diukur.

## Yang diminta

Dari catatan pertemuan, kebutuhan yang mengikat ada empat.

1. Repositori pengetahuan lokal.
2. Dua kelas sumber yang kepemilikannya terpisah. Rekaman bisnis diisi sendiri di basis data. Dokumen tidak terstruktur masuk sebagai dump yang lain. Menyimpan hasil ekstraksi dokumen ke tabel belum memenuhi dua sumber itu.
3. Satu pertanyaan boleh memakai rekaman saja, dokumen saja, atau keduanya. Jawaban menunjuk asal. Bukti tidak cukup, nama ambigu, dan dua sumber yang tidak sepakat harus terlihat.
4. Klasifikasi membantu pengorganisasian. Klasifikasi bukan produknya. Satu berkas boleh punya lebih dari satu jenis. Dokumen yang belum pernah dilihat harus bisa masuk.

Referensi yang menyertai permintaan itu adalah petunjuk, bukan perintah salin.

- Perumpamaan pemakaiannya mirip buku catatan sumber: unggah, lalu jawaban yang menunjuk kalimat. Gemini Notebook menolak bila informasi tidak ada di sumber.
- Lapisan pada materi publik Perkara AI adalah kosakata. Lima label animasi, sebelas strata di video fitur, dan jenis berkas hukum adalah tiga daftar. Pemetaannya tidak dipublikasikan. Videonya animasi pada data rekaan, 90 detik. Lencana terverifikasi di animasi itu bukan bit kebenaran.
- Pos 2 November 2026: jangan biarkan model menulis SQL ke data mentah. `LIKE '%meeting%'` ikut menangkap "tidak bisa ikut meeting". Jembatan yang disebut adalah semantic model. Pilihan mereka graf berlapis. ETL berbasis kejadian, atau materialized view PostgreSQL, disebut sebagai cara, bukan skema. Ontologi ekspor-impor, rumah sakit, dan persidangan harus berbeda. Angka ~1 juta entitas adalah klaim perkara mereka.
- Video fitur menunjukkan urutan yang sama dalam bentuk produk hukum: uraikan halaman, padukan kutipan tanpa menghapus jejak, pilih sejumlah potongan, uji klaim, baru buka halaman sumber. Angka "20 potongan" di layar adalah label animasi, bukan recall yang dievaluasi.
- Lowongan internal menyebut Rails, Express, dan React. Itu bukti tim bisa menerima tumpukan yang sebanding. Bukan perintah untuk menulis ulang malam itu.
- Makalah manajemen pengetahuan 2025–2026 yang terbuka membahas budaya dan pemakaian, bukan skema. GraphRAG, LightRAG, late chunking, dan EAGR dibaca pada abstrak. Tidak ada yang dipasang, dan angka penulis tidak dihitung ulang di sini.

## Bentuk solusi yang utuh

Dua laporan proses bisnis, 10 November, sampai pada irisan yang sama. Bentuk akhirnya seperti ini.

Satu notebook. Dua pintu tulis. Penulis katalog mengisi rekaman bisnis. Operator mengunggah dokumen. Ekstraksi tidak boleh mengubah status rekaman. Jawaban dihitung saat ditanya, dan tidak ditulis kembali sebagai rekaman.

Pertanyaan menjadi maksud tertutup, bukan SQL bebas. Maksud itu memilih rute.

- Rekaman saja, bila yang diminta adalah status yang tercatat.
- Dokumen saja, bila yang diminta adalah apa yang tertulis, termasuk rencana dan negasi.
- Gabungan, hanya lewat identitas stabil yang sama. Kemiripan nama bukan sambungan.
- Abstain, bila rute tidak punya baris, atau pertanyaan di luar operasi yang diizinkan.

Di dalam dokumen, tiga hal tetap terpisah. Lapisan data menyimpan berkas, hash, dan lokasi teks. Jenis dokumen memilih kolom. Lapisan semantik menyimpan kutipan, polaritas, modalitas, dan bentrok, masing-masing menunjuk kembali ke kalimat sumber.

Yang belum masuk irisan pertama, dan tetap kandidat kemudian: graf sejuta simpul, embedding sebagai jawaban, council beberapa model pada setiap pertanyaan, sidik suara, dan ontologi perkara.

## Yang saya pasang terlebih dahulu

Saya memasang pondasi cara kerja dan batasnya, supaya use case bisa dijalankan sebelum pipeline diganti.

Aplikasi yang dibuka adalah `ops-notebook`: Rails 7.0.10, Ruby 3.3.2, PostgreSQL. Layarnya di mesin ini, `http://127.0.0.1:3000`. Jalur tanya menulis `rules` dan `semantic false`. Model tidak dipasang pada jawaban. Keputusan riset 10 November sempat menerima satu proses dan SQLite. Layar ini memakai Rails dan PostgreSQL untuk perilaku yang sama. Keputusan itu tidak mengaudit ulang layar Rails.

Batas yang sudah menjadi perilaku:

- Rekaman dan dokumen dua sumber. Kalimat di berkas tidak mengubah status rekaman.
- Id publik yang stabil adalah sambungan. Budi dan Budiono tidak digabung.
- Rencana bukan kejadian, dan bukan bukti bahwa sesuatu tidak terjadi.
- Negasi pada satu kalimat tetap menempel. Kutipan yang membuang "tidak" dari kalimat itu ditolak pada pola yang diuji.
- Dua kutipan yang tidak sepakat tetap bentrok.
- Tidak ada baris berarti abstain.
- Nama berkas bukan kebenaran. Kalimat instruksi di dalam dokumen adalah data.
- Jenis yang ada: `sop`, `notulen`, `proposal`, `laporan_progres`, `other`. Tiga penilai: kata, baris isian, nama berkas. Nama berkas diabaikan bila menjadi satu-satunya suara atau bertentangan dengan isi.
- Teks, Markdown, PDF yang punya lapisan teks, dan DOCX yang punya paragraf XML dibaca. Gambar, PPTX, audio, dan PDF pindai ditahan dengan alasan. OCR tidak dipanggil.
- Gabungan hanya bila pertanyaan memuat id publik rekaman itu dan kutipan memuat id yang sama.

Yang masih terbuka, dan saya tidak menutupinya dengan label lulus: irisan kata bisa menarik kalimat yang hanya kebetulan berbagi token. Pertanyaan kehadiran belum selalu menyaring nama orang. Tiga kontrak tambahan belum punya uji bernomor: turunan yang membalik polaritas, rencana yang dipakai sebagai bukti kejadian di dokumen lain, dan "hanya mendengar" yang bukan saksi kedua. Recall, presisi, dan F1 aplikasi ini belum diukur.

## Alur penggunaan yang dilihat dulu

Satu operator, satu notebook, domain operasional fiktif.

1. Buat notebook.
2. Isi rekaman terpisah dari berkas. Contoh yang sudah dipakai: Budi status tidak diketahui, Budiono sudah terjadi, pilot masih rencana.
3. Unggah berkas baru. Berkas kosong, gambar, dan pindai tidak ikut masuk sebagai teks. PDF berlapis teks dan DOCX masuk sebagai bagian.
4. Lihat jenis dan isian. Notulen menyimpan peserta dan keputusan. SOP menyimpan langkah. Isi yang tidak mirip keempat jenis itu menjadi `other`.
5. Tanya, dan baca rute serta kutipan.
   - "Apa status Budiono?" memakai rekaman saja, jawaban sudah terjadi.
   - "Apa status Budi?" memakai rekaman saja, jawaban tidak diketahui. Namanya tidak mengambil baris Budiono.
   - "Apakah pilot sudah berjalan?" pada kalimat rencana menjawab rencana, bukan kejadian.
   - Pertanyaan di luar operasi, misalnya harga saham, abstain.
   - Gabungan hanya saat pertanyaan membawa id publik rekaman dan kutipan memuat id itu.

Alur ini yang dipakai untuk melihat use case. Pipeline di belakangnya boleh diganti tanpa mengubah janji langkah 1 sampai 5.

## Peta perbaikan pipeline

Setiap baris adalah satu sambungan. Kandidat kanan hanya masuk bila uji pada korpus kita menunjukkan kenaikan, dan batas kiri tetap.

| Bagian | Pondasi sekarang | Kandidat kemudian | Batas yang tidak ikut terganti |
| --- | --- | --- | --- |
| Pintu rekaman | Formulir menulis baris PostgreSQL | ETL kejadian, atau materialized view, seperti opsi yang disebut di pos 2 November | Ekstraksi dokumen tidak menulis status rekaman |
| Baca berkas | Teks, Markdown, lapisan teks PDF, XML DOCX. Pindai ditahan | Pembaca struktur seperti Docling. OCR hanya untuk berkas yang hari ini ditahan, dengan alasan bila teks tetap kosong | Struktur dan lokasi bukan jenis, dan bukan bukti klaim |
| Jenis dokumen | Tiga penilai leksikal, label `local-rules` | Model mengusulkan jenis. Gagal atau waktu habis tetap jatuh ke aturan, dengan label metode yang benar-benar jalan | `other` tetap ada. Nama berkas tetap bukan suara tunggal |
| Isi dan kutipan | Baris `Nama: nilai` dan kalimat yang lolos cek substring | Ekstraksi semantik per bagian | Kutipan wajib ada di teks versi aktif. Teks dokumen tetap data |
| Identitas | Batas kata, nama yang lebih panjang didahulukan | Tautan yang dikonfirmasi orang. Alias hanya lewat tautan itu | Nama yang mirip tidak menjadi foreign key |
| Rencana, negasi, bentrok | Leksikon dan pasangan kutipan | Model polaritas dan modalitas, diuji pada kasus yang sama | Rencana bukan kejadian. Bentrok tidak memilih pemenang diam-diam |
| Rute pertanyaan | Operasi tertutup: rekaman, dokumen, gabungan, tidak didukung | Perencana maksud. Hasilnya dikompilasi ke kueri berparameter | Model tidak menulis SQL ke data mentah |
| Cari dokumen | Irisan kata pada baris yang sudah disimpan | Di sinilah RAG bisa masuk: potongan, lalu saringan kedua. Late chunking hanya bila sudah ada embedding. LightRAG atau GraphRAG hanya bila pertanyaan relasi pada korpus kita mengalahkan irisan kata. EAGR tetap pracetak yang belum diulang | Saringan pertama yang membuang sebagian besar korpus harus punya ukur recall sebelum dipakai. Perkiraan 95–98% adalah perkiraan tentang jalur orang lain, bukan angka kita |
| Gabungan dua sumber | Id publik harus tertulis di pertanyaan dan di kutipan | Sambungan lewat tautan terkonfirmasi, lalu baru narasi | Kecocokan nama tidak cukup |
| Pemeriksaan jawaban | Satu jalur aturan. Sitasi adalah lokasi, bukan dukungan semantik yang diukur | Pemeriksa kedua, atau pemisahan relevansi konteks, kesetiaan, dan relevansi jawaban seperti ARES. ALCE mengingatkan bahwa adanya sitasi belum berarti sitasi setia | Beberapa agen tidak otomatis lebih benar. Biaya dan latensi dicatat. Angka penulis bukan hasil kita |
| Kalimat jawaban | Mengulang baris yang lolos, atau abstain | Model merangkai prosa setelah bukti dipilih | Prosa tidak menjadi bukti baru |

Urutan yang saya pegang: alur penggunaan di atas tetap. Yang diganti adalah satu kolom "kandidat kemudian", satu per satu, dengan uji sebelum dan sesudah pada pertanyaan yang sama. Gabungan dua sumber dan irisan kata adalah dua tempat yang paling dulu layak diganti, karena di situlah use case CTO hidup, dan di situlah fondasi sekarang paling lemah.
