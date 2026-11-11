# Handoff

Tanggal: 11 November 2026. Cabang yang dipakai: `prototype`. Perilaku produk sebelum dokumen dan layar handoff ini: commit `970baea`. Ini satu-satunya berkas yang dibaca lebih dulu oleh agen, model, atau engineer yang melanjutkan pekerjaan. Tujuannya supaya riset tidak diulang, pondasi tidak ditulis ulang, dan perbaikan berikutnya tetap menempel pada alur bisnis yang sudah digambar.

Ini bukan sertifikat produksi. Recall, presisi, F1, ROI, dan nilai bisnis aplikasi ini belum diukur. `null` dan `not_measured` bukan nol dan bukan lulus. Angka penulis tetap angka penulis.

Layar yang sama ada di aplikasi, tautan **Handoff** atau http://127.0.0.1:3000/handoff. Isi layar itu dibaca dari berkas ini, jadi tidak ada salinan kedua.

## Daftar isi

1. [Produk yang diserahkan](#produk-yang-diserahkan)
2. [Janji yang tidak boleh dikerjakan ulang](#janji-yang-tidak-boleh-dikerjakan-ulang)
3. [Keputusan yang sudah ditutup](#keputusan-yang-sudah-ditutup)
4. [Yang sengaja tidak dikerjakan](#yang-sengaja-tidak-dikerjakan)
5. [Pondasi, lalu perbaikan](#pondasi-lalu-perbaikan)
6. [Biaya dan manfaat yang harus ditimbang](#biaya-dan-manfaat-yang-harus-ditimbang)
7. [Proses bisnis yang bisa menyusul](#proses-bisnis-yang-bisa-menyusul)
8. [Verifikasi yang membuktikan selaras dengan alur](#verifikasi-yang-membuktikan-selaras-dengan-alur)
9. [Delivery sebagai produk](#delivery-sebagai-produk)
10. [Koordinasi bila ini produk tim](#koordinasi-bila-ini-produk-tim)
11. [Docker dan lingkungan bersama](#docker-dan-lingkungan-bersama)
12. [Urutan baca](#urutan-baca)
13. [Jangan dipercaya mentah](#jangan-dipercaya-mentah)

## Produk yang diserahkan

Yang dijalankan hanya `ops-notebook/`: Rails 7.0.10, Ruby 3.3.2, PostgreSQL. Server lokal http://127.0.0.1:3000. Jawaban bertanda `rules` dan `semantic false`. Model tidak dipasang pada jalur tanya.

Cara menjalankan dan urutan percobaan ada di [README.md](README.md), lalu [PENGGUNAAN.md](PENGGUNAAN.md). Bagan ada di [DIAGRAM.md](DIAGRAM.md). Naskah bicara ada di [CTO.md](CTO.md).

Layar yang menjelaskan keputusan:

- **Proses** memuat peta alur, lima langkah pemakaian, empat rute tanya, dan adegan **Use case berat: 150 PDF**.
- **Riset dan perbandingan** (`/riset`) merangkum folder `research/`.

Uji `bin/rails test` dari folder `ops-notebook` pada pohon yang memuat layar handoff ini: 30 run, 288 assertion, 0 gagal. Pada commit `970baea`, sebelum layar ini, hasilnya 29 run dan 269 assertion. Uji itu menahan regresi yang sudah ditulis. Uji itu tidak membuktikan berkas CTO yang belum dilihat, dan tidak mengukur recall.

Yang bukan produk:

| Jalur | Status |
| --- | --- |
| `klayer/`, port 8765, `data/*.sqlite` | Jalur Python yang ditinggalkan. Jangan dilanjutkan dan jangan dijadikan penerimaan Rails. |
| `research/`, `council/` | Arsip keputusan dan bukti. Sebagian kalimatnya sudah kedaluwarsa. Bagian "Jangan dipercaya mentah" di bawah menyebut yang mana. |
| Adegan 150 PDF | Ilustrasi urutan kerja. Bukan kapasitas yang sudah diukur. |
| Halaman riset | Kutipan sumber. Bukan hasil ukur mesin ini. |
| Repositori studi kasus AI Interview | Submission lama. Jangan disentuh. |

## Janji yang tidak boleh dikerjakan ulang

Perilaku ini sudah menjadi kode dan uji. Perbaikan pipeline boleh mengganti mesin di belakang satu tahap. Janji di kolom kiri tetap, kecuali ada uji baru yang sengaja mengubah expected-nya dan menyebut alasannya.

| Janji | Di kode | Uji yang menahannya |
| --- | --- | --- |
| Rekaman bisnis dan dokumen adalah dua sumber. Kalimat berkas tidak mengubah status rekaman. | `BusinessRecord` terpisah dari unggahan | Alur contoh di README |
| Budi bukan Budiono. Nama yang lebih panjang didahulukan. | `evidence/query.rb` | `evidence_flow_test.rb`, Budiono tidak cocok dengan Budi |
| Rencana bukan kejadian, dan bukan bukti bahwa sesuatu tidak terjadi. | leksikon modalitas | pertanyaan pilot |
| Tidak ada baris berarti abstain. | rute `unsupported` | pertanyaan di luar operasi |
| Gabungan hanya lewat id publik yang sama di pertanyaan dan di kutipan. | rute `combined` | uji gabungan |
| Kutipan yang membuang "tidak" dari satu kalimat ditolak pada pola yang diuji. | leksikon | uji negasi yang ada |
| Nama berkas bukan suara tunggal jenis. `other` tetap ada. | tiga penilai | unggah `catatan-bebas.md` dan berkas nama yang menipu |
| Teks di dalam berkas adalah data, bukan perintah. | ingest | jangan menambah jalur yang menjalankan kalimat berkas |
| PDF berlapis teks dan DOCX ber-XML dibaca. Pindai, gambar, PPTX, dan audio ditahan. OCR tidak dipanggil. | `evidence/readers.rb` | uji pemetaan |
| Model tidak menulis SQL. | tidak ada penyusun SQL dari model | jangan memasang text-to-SQL ke tabel mentah |

Tiga kontrak tertulis belum punya uji bernomor di Rails. Jangan dinyatakan lulus:

- Turunan tidak boleh membalik polaritas klaim yang masih hidup.
- Rencana di dokumen lain tidak menjadi bukti kejadian.
- "Hanya mendengar" bukan saksi kedua.

Dua kelemahan yang sudah terlihat dan belum ditutup: irisan kata bisa menarik kalimat yang hanya kebetulan berbagi token, dan pertanyaan kehadiran belum selalu menyaring nama orang.

## Keputusan yang sudah ditutup

Jangan membuka kembali pertanyaan ini kecuali ada bukti baru pada korpus kita. Sumber lengkapnya disebut di kolom terakhir.

| Keputusan | Status untuk agen berikutnya | Sumber |
| --- | --- | --- |
| Dua sumber terpisah, bukan satu tabel hasil ekstraksi. | Mengikat. | Catatan CTO, `council/business-process-a.md`, `council/business-process-b.md` |
| Klasifikasi membantu, bukan produknya. Satu berkas boleh beberapa jenis. | Mengikat. | Catatan yang sama |
| Jawaban dari baris yang sudah terbit. Bukti kosong, nama ambigu, dan bentrok harus terlihat. | Mengikat. | `research/risk-and-acceptance.md` |
| Kutipan wajib ada di teks aktif. Sitasi yang gagal dibuang, tidak digeser ke kalimat terdekat. | Mengikat. | `research/architecture-challenge.md` |
| Kecocokan kata boleh ada hanya dengan label `local-rules`. Jangan disebut ekstraksi semantik. | Mengikat. Layar sekarang menulis `rules` dan `semantic false`. | `research/council-decision.md` |
| Jangan biarkan model menulis SQL ke data mentah. `LIKE '%meeting%'` ikut menangkap negasi. | Mengikat sebagai batas. Bukan perintah memasang graf. | Pos Ibrahim Arief 2 November 2026, dibaca di `research/perkara-research.md` |
| Lima label animasi, sebelas strata video, dan jenis berkas hukum adalah tiga daftar. Jangan dijadikan satu skema. | Mengikat. | `research/perkara-research.md`. Video lokal tidak ada di git. |
| PostgreSQL disebut sebagai saran, bukan perintah salin. | Diganti oleh produk yang jalan: Rails dan PostgreSQL dipakai untuk perilaku yang sama. Keputusan riset 10 November yang menerima SQLite tidak mengaudit layar Rails. | `research/council-decision.md`, lalu kode `ops-notebook` |
| FastAPI, Neo4j, Celery, Kafka, LangGraph bukan fakta produk orang lain. | Jangan dipasang hanya karena tebakan. | `council/ledger/2026-11-11-tebakan-stack-perkara.md` |
| GraphRAG, LightRAG, late chunking, EAGR. | Abstrak dibaca. Tidak dipasang. Angka makalah bukan hasil kita. | `research/stack-and-retrieval-source-notes.md`, halaman `/riset` |
| Makalah manajemen pengetahuan 2025–2026 yang terbuka. | Bukan desain sistem. Bukan LMS dan bukan kurikulum pelatihan. | `research/kms-2025-2026-verified.md` |
| Azure Content Understanding, Docling, Gemini Notebook. | Dipakai sebagai batas perilaku: `other` wajib ada, struktur bukan kategori, tolak bila sumber tidak memuat jawaban. Dependensinya tidak dipasang. | `research/cross-domain-references.md` |
| Macro 6/9 lalu 9/9. | Milik kandidat Python dan `synthetic-macro-v1`, provider rules. Bukan mutu model. Bukan audit Rails. `business_value` belum diukur. | `research/macro-validation-and-value.md`, `council/ledger/2026-11-10-metrics-terlihat.md` |
| Unggah Grok 5/6 dengan timeout 75 detik, lalu dua kueri sekitar 21 dan 17 detik. | Sampel kecil pada jalur Python. Bukan SLO. | Catatan ledger metrik |
| Perkiraan 95–98% korpus tidak lolos saringan kemiripan. | Perkiraan Ibrahim tentang jalur orang lain. Bukan recall aplikasi ini. | Halaman `/riset` |
| Lowongan Rakamin menyebut Rails, Express, dan React. | Tim dapat menerima tumpukan yang sebanding. Bukan perintah menulis ulang. Layar perusahaan adalah React di Vite. Layar prototipe ini masih HTML server. | `council/ledger/2026-11-11-stack-rakamin.md`, `2026-11-11-ui-rakamin.md` |
| Banyak agen menaikkan biaya dan bisa memperburuk tugas berurutan. | Jangan menambah agen sebagai bukti kebenaran. | `research/kms-2025-2026-verified.md` |
| Kontrak metrik. | `not_measured` bukan nol. Adanya sitasi bukan dukungan semantik. | `docs/metrics-contract.md` |

## Yang sengaja tidak dikerjakan

Jangan menambah ini sebagai "kelengkapan" tanpa uji pada korpus kita:

- Ontologi perkara, bedah saksi, sidik suara, graf sejuta simpul.
- LMS, pelatihan, asesmen, SAP, akun produksi, Proof of Value.
- Embedding atau RAG sebagai jawaban. Vektor boleh nanti sebagai indeks calon, bukan sebagai pemutus bentrok.
- Council beberapa model pada setiap pertanyaan.
- OCR yang mengubah pindaian menjadi klaim tanpa alasan bila teks tetap kosong.
- Text-to-SQL bebas, MCP yang meneruskan SQL ke tabel mentah, atau materialized view yang isinya masih kalimat mentah. MCP mengangkut permintaan. Ia tidak memahami negasi.

## Pondasi, lalu perbaikan

Alur pemakaian yang sudah bisa dilihat tetap lima langkah: notebook, rekaman terpisah, unggah, jenis, tanya. Rute tanya tetap empat: rekaman saja, dokumen saja, gabungan, abstain.

Perbaikan dilakukan satu tahap. Sebelum dan sesudah memakai pertanyaan yang sama. Catatan lengkapnya `council/pondasi-lalu-pipeline.md`. Urutan yang paling layak, karena di situlah use case berat hidup dan fondasi paling lemah:

1. Antrian dump, supaya 150 PDF tidak menahan satu permintaan HTTP. Isi halaman dan lokasi disimpan dulu. Pindai yang gagal dibaca tetap ditahan.
2. Klasifikasi dan klaim saat dump, bukan saat ditanya. Rumah pertama tetap baris PostgreSQL. Vektor hanya ditambah bila pencarian calon pada korpus kita mengalahkan irisan kata, dan recall saringan pertama diukur.
3. Relasi lintas berkas: bentrok dan dukungan, dengan jejak kedua berkas. Rencana tidak menjadi dukungan kejadian.
4. Tanya hanya membaca struktur yang sudah tersimpan.
5. Verifikasi lebih dari sekali: kutipan ada di halaman, kalimat utuh bukan sekata, klaim tanpa sumber dibuang, bentrok dan dukungan tetap terlihat, halaman asli bisa dibuka.
6. Baru kemudian prosa model, setelah bukti dipilih. Prosa tidak menjadi bukti baru.

## Biaya dan manfaat yang harus ditimbang

Jangan mengisi sel yang kosong. Manfaat hanya sah bila diukur pada set kasus yang sama, sebelum dan sesudah, dengan metode di `docs/metrics-contract.md`.

| Pilihan | Biaya yang sudah diketahui bentuknya | Manfaat | Status manfaat |
| --- | --- | --- | --- |
| Tetap irisan kata | Salah ambil kalimat yang berbagi token. Konteks terpotong. | Murah, bisa diuji, tidak memanggil model. | Perilaku ini ada. Recall-nya `not_measured`. |
| RAG kemiripan sebagai saringan pertama | Bagian korpus tidak pernah sampai ke jawaban. Perkiraan 95–98% adalah perkiraan orang lain tentang jalur ini. | Hanya bila Recall@K pada bukti berlabel naik tanpa memotong negasi. | `not_measured` di mesin ini. |
| LightRAG atau GraphRAG | Indeks, penyimpanan, dan kerja kueri tambahan. Angka makalah tidak boleh disalin. | Hanya bila pertanyaan relasi pada korpus kita mengalahkan irisan kata. | `not_measured`. |
| Late chunking | Butuh embedding dulu. | Belum ada alasan memasang embedding. | `not_measured`. |
| Model mengusulkan jenis atau polaritas | Waktu, biaya penyedia, dan kegagalan. Timeout 75 detik pada jalur lama menerbitkan fallback. | Boleh bila label metode yang benar-benar jalan tersimpan, dan fallback tetap `local-rules`. | Belum dipasang di Rails. |
| Council beberapa model | Token dan latensi naik. Pada tugas berurutan, makalah yang dibaca melaporkan hasil lebih buruk daripada satu model. | Hanya bila kasus bentrok dan abstain pada set kita membaik. | `not_measured`. |
| OCR | Teks salah bisa menjadi klaim. | Hanya untuk berkas yang hari ini ditahan karena tidak punya teks. | `not_measured`. |
| Docker untuk tim | Waktu menyusun image dan menjaga kunci di luar image. | Lingkungan Ruby dan PostgreSQL yang sama bagi lebih dari satu orang. | Compose belum ada. Manfaat lingkungan belum diukur. |
| Akun dan peran | Pekerjaan otorisasi, dan data nyata belum boleh masuk sebelum itu ada. | Beberapa orang bisa memakai notebook yang sama tanpa saling menimpa. | `not_measured`. |

Biaya uang penyedia tidak tersedia. Sisa kuota langganan tidak terbaca sebagai angka yang boleh ditulis. Jangan mengarang ROI.

## Proses bisnis yang bisa menyusul

Yang berjalan sekarang: satu operator, satu notebook, domain fiktif. Ia membuat ruang, mengisi rekaman, mengunggah, melihat jenis, lalu bertanya.

Yang selaras dengan alur dan boleh menjadi pekerjaan tim berikutnya:

| Proses | Siapa | Kapan mesinnya siap |
| --- | --- | --- |
| Mengisi katalog rekaman | Penulis katalog | Sudah bisa, lewat formulir. Jangan diganti oleh ekstraksi. |
| Dump berkas baru | Operator | Sudah bisa untuk teks, PDF berlapis, dan DOCX. Antrian belum ada. |
| Meninjau jenis dan klaim | Peninjau | Koreksi jenis dan keputusan klaim sudah ada. Belum ada akun, jadi ini masih orang yang sama di mesin yang sama. |
| Bentrok dua berkas dan dukungan lintas berkas | Peninjau melihat, mesin mengusulkan | Baru ilustrasi di adegan 150 PDF. Relasi dukungan belum disimpan. |
| Tanya operasional | Pemakai notebook | Empat rute sudah ada. Irisan kata masih longgar. |
| Dump 150 PDF puluhan halaman | Operator, lalu peninjau sampel | Belum. Ini use case berat yang dituju, bukan yang sudah lulus. |

Yang tidak menjadi proses produk ini: perkara hukum, LMS, asesmen karyawan, dan integrasi SAP.

## Verifikasi yang membuktikan selaras dengan alur

Satu perubahan selaras dengan alur hanya bila empat hal ini ada dalam laporan yang sama.

1. Tahap pipeline yang diganti, satu saja.
2. Janji di tabel atas yang tetap.
3. Perintah uji dan hasilnya, termasuk yang gagal. Jangan menyembunyikan gagal di dalam rata-rata.
4. Set kasus yang sama sebelum dan sesudah. Jangan mengubah pertanyaan hanya agar papan menjadi hijau.

Set minimum yang sudah bisa dijalankan hari ini:

```bash
cd ops-notebook
export RBENV_VERSION=3.3.2
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
bin/rails test
```

Lalu, dengan server hidup, ulangi bagian "Coba sendiri" di README: contoh produk, empat berkas `fixtures/demo/`, dan pertanyaan yang harus abstain atau bentrok.

Untuk use case 150 PDF, laporan belum boleh menulis lulus sebelum ada set berkas berlabel dan hasilnya menyimpan:

- jumlah berkas masuk, ditahan, dan alasannya
- klaim dengan berkas dan halaman
- pasangan bentrok yang diharapkan, dan pasangan yang tidak boleh terjadi
- pasangan dukungan yang diharapkan, tanpa mengubah status rekaman
- jawaban tanya yang menyebut rute, kutipan, dan halaman
- tiga cek verifikasi: substring, kalimat utuh, dan klaim tanpa sumber
- waktu monotonic per tahap, dengan jumlah sampel

Kontrak angka ada di `docs/metrics-contract.md`. Adanya sitasi bukan dukungan. ALCE dan ARES disebut di halaman riset sebagai batas. Keduanya tidak dijalankan di mesin ini.

## Delivery sebagai produk

Yang boleh ditunjukkan kepada orang lain:

1. Buka http://127.0.0.1:3000 dan klik **Buka contoh produk**.
2. Lewati Dump, Pemetaan, Proses, Analisis, Keputusan, Verifikasi, Tanya.
3. Di Proses, tunjukkan peta dan adegan 150 PDF, lalu katakan bahwa adegan itu ilustrasi.
4. Di Tanya, tunjukkan rekaman saja, rencana yang tidak menjadi kejadian, bentrok, dan abstain.
5. Buka **Riset dan perbandingan** bila ditanya mengapa belum memakai RAG besar.
6. Buka **Handoff** bila ditanya keputusan, biaya, tim, atau Docker. Layar itu membaca berkas ini.

Selesai untuk satu irisan berarti perilaku di README bisa diulang orang lain dari commit yang sama, dan `bin/rails test` lulus. Selesai tidak berarti produksi, tidak berarti Proof of Value, dan tidak berarti 150 PDF sudah aman.

Cabang yang dibagikan: `prototype`. `main` adalah naskah lama. Jangan mengirim orang ke akar repositori tanpa menyebut cabang.

## Koordinasi bila ini produk tim

Hari ini belum ada akun. Satu basis data development boleh ditimpa siapa saja yang menjalankan server di mesin yang sama. Karena itu data klien nyata tidak masuk.

Peran yang sudah cocok dengan alur, walaupun belum ada hak akses:

| Peran | Boleh | Tidak boleh |
| --- | --- | --- |
| Penulis katalog | Membuat rekaman dan mengubah status rekaman | Mengambil status dari kalimat berkas |
| Operator | Mengunggah berkas | Menggabungkan dua notebook diam-diam |
| Peninjau | Menerima, menolak, atau meminta bukti lagi pada klaim | Menutup bentrok tanpa jejak |
| Pemilik pipeline | Mengganti satu tahap di belakang alur | Mengganti janji tanpa uji yang disebut di atas |
| Pemilik integrasi | Menggabungkan ke `prototype` | Menerima 9/9 rules Python sebagai lulus Rails |

Cabang integrasi satu: `prototype`. Perubahan lewat pull request yang menyebut tahap, janji yang tetap, perintah uji, dan set kasus. Dua orang tidak menulis `ops-notebook/app/services/evidence/` pada saat yang sama.

Agen yang membantu mengikuti batas yang sama. Riset baru hanya bila keputusan di tabel atas benar-benar tidak memuat pertanyaannya. Jangan membuka pane lama dan jangan mengirim prompt ke sesi yang sudah berhenti. Jangan menyalakan always-approve.

## Docker dan lingkungan bersama

Docker Compose belum ada. README menyatakan itu. Jangan menganggap image sudah siap.

Bila lebih dari satu orang menjalankan produk yang sama, Compose berikutnya perlu memenuhi kontrak ini sebelum dipakai bersama.

- Dua layanan: aplikasi Rails dan PostgreSQL. Tidak perlu Neo4j, Redis, atau worker sampai ada tahap pipeline yang uji-nya membutuhkan itu.
- Ruby di image 3.3.2, sama dengan `Gemfile`.
- Perintah siaga aplikasi: migrasi, lalu Puma pada port yang diumumkan. Pemeriksaan hidup: `GET /` mengembalikan 200 dan judul Notebook operasional.
- Basis data development dan test terpisah. Uji `bin/rails test` dijalankan di CI pada set yang sama, bukan hanya di laptop satu orang.
- `config/master.key` tidak masuk image dan tidak masuk git. Development hari ini tidak membutuhkan kunci itu.
- Berkas unggahan dan data Postgres ada di volume. Menghapus container tidak menghapus volume itu tanpa perintah yang disengaja.
- Variabel penyedia model, bila suatu hari dipakai, masuk dari lingkungan saat dijalankan. Jangan dibakar ke image. Jalur tanpa kunci tetap harus menjawab dengan `local-rules` dan label yang jujur.
- Compose tidak mengubah janji perilaku. Uji yang sama harus lulus di dalam container dan di luar container.

Di macOS, tanpa Docker, `gem pg` butuh `SDKROOT` alat kompilasi macOS. `bin/ops` mengisi itu untuk server lokal. Image Linux tidak memakai variabel itu.

## Urutan baca

1. Berkas ini.
2. [README.md](README.md) sampai "Coba sendiri", lalu jalankan aplikasi.
3. [PENGGUNAAN.md](PENGGUNAAN.md) dan [DIAGRAM.md](DIAGRAM.md).
4. [council/pondasi-lalu-pipeline.md](council/pondasi-lalu-pipeline.md) bila akan mengubah pipeline.
5. [docs/metrics-contract.md](docs/metrics-contract.md) bila akan menulis angka.
6. Kode: `ops-notebook/app/services/evidence.rb`, lalu `lexicon.rb`, `ingest.rb`, `readers.rb`, `query.rb`.
7. `research/` hanya untuk membuka sumber yang disebut tabel keputusan. Jangan merangkum ulang dari nol.

## Jangan dipercaya mentah

Kalimat lama ini kalah oleh kode yang jalan:

- `council/CHECKPOINT.md` masih menulis bahwa PDF, DOCX, dan OCR belum didukung, dan menyebut PID server. Lapisan teks PDF dan XML DOCX sudah dibaca sejak commit `65c75cb`. OCR memang belum ada. PID di berkas itu bukan status hidup.
- `research/council-decision.md` menerima SQLite untuk irisan riset 10 November. Produk yang diserahkan memakai Rails dan PostgreSQL.
- Ledger 11 November yang menulis "demo pagi tetap Python dan SQLite" adalah catatan saat itu, bukan status `prototype` sekarang.
- `council/demo-walkthrough.md` menyebut proses yang sudah mati.
- Angka 38 tes Python dan macro 9/9 bukan penerimaan Rails.
