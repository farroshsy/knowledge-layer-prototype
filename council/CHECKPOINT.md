# Checkpoint koordinasi

Diperbarui 2026-11-11. Satu percakapan koordinator. Tidak ada push atau publikasi.

## Tujuan

Aplikasi lokal bisa dijalankan dan diuji sebelum 2026-11-11 08:00 WIB. Dua sumber tetap terpisah: rekaman bisnis di basis data dan dokumen yang diunggah. Jawaban menyebut rute, bukti, dan batasnya.

## Pemilik integrasi

Produk yang berjalan adalah `ops-notebook/`: Rails 7.0.10, Ruby 3.3.2, PostgreSQL. Server PID 99635 di http://127.0.0.1:3000. Ekstraksi berlabel `rules`, `semantic` selalu false. Bukan model.

Kandidat Python `.parallel-builds/grok-20261110-2222/candidate` hash `1ae2a53a2642d31283b87ef35e332e2fd2753b9a70374d371515cf3775462401` tetap sebagai bukti lama. Jangan dilanjutkan. Sumber `klayer/` asli tidak diubah. Sesi 45866 sempat menulis pohon itu; kepemilikan tunggal produk sekarang ada di `ops-notebook/`.

Sesi kiri `01a1c608-ef85-7832-9553-915c49d0ad6a` (pane `term_d1957653-d06c-48dc-9508-a4a8d663ea37`) berhenti sebagai penulis. Pane itu menganggur di Grok 4.7 medium. Jangan kirim prompt baru ke sana.

## Graf tugas

1. Selesai dan ditutup: council, parallel build, repair, strategy review, research review, serta sesi Grok riset/desain yang sudah `done`. Proses penulisnya memang sudah mati. Terminalnya ditutup supaya tidak dobel.
2. Produk: `ops-notebook` di http://127.0.0.1:3000. Dasbor `127.0.0.1:8766` dan `context_hub` tetap proses pantau lama, bukan aplikasi.
3. Selesai sebagai koordinator: sesi medium kiri. Konteksnya tetap di pane itu, tetapi penulisannya pindah ke sesi xhigh ini.
4. Jangan menambah penulis pada kandidat Python. Jangan memakai 38 tes Python atau macro 9/9 sebagai penerimaan Rails.
5. Agen `brainstorm-ledger` hanya mengolah dump ke `council/ledger/`. Ia bukan penulis kandidat. Pane itu dibuka terpisah.

## Kegagalan yang tetap tercatat

- Council `20261110-212748-e5a9aa`: `no_progress`, 16 panggilan, 1 rilis lama, bukan aplikasi final.
- Parallel build `20261110-214747-9bf46f`: `blocked`. Review integritas menolak candidate-1 lama.
- Repair `repair-20261110-221217`: `blocked` pada attempt 1. Tes 34 saat itu 1 gagal dan 1 error.
- Unggah live `baru-grok-live.txt`: Grok timeout 75 detik, job menerbitkan `local-rules` dan menyimpan `provider_error`.

## Bukti yang dipakai ulang

- Unit test kandidat setelah perbaikan planner: 34 lulus.
- Macro rules 9/9 di `.parallel-builds/grok-20261110-2222/macro-rules/results.json`.
- Basis `data/final-demo.sqlite` tetap memuat notebook `16cd89dcda064fe2b6390deb7b91e00d` dan tiga rekaman setelah restart.
- `Apa status Budiono?` 0,006 detik, `db_only` / `occurred`, hanya Budiono. `Apa status Budi?` 0,001 detik, `unknown`, hanya Budi.
- UI sebelumnya sudah menunjukkan kehadiran Budi sebagai `document_only` / `negated`.
- Dasbor sekarang melaporkan 0 panggilan aktif. PID council 73314 tidak lagi dihitung hidup karena perintahnya bukan `automation.council`.

## Keputusan

Pertanyaan bisnis tidak lagi memanggil planner dokumen. Schema itu ditolak dan menambah puluhan detik. Lookup tertutup memakai aturan. Pertanyaan dokumen tetap boleh memanggil Grok. `Berapa harga saham kemarin?` tetap abstain, kali ini 20 detik karena planner dokumen benar-benar dipanggil.

## Langkah berikutnya

Uji di http://127.0.0.1:3000. Aplikasi ini Rails. Ekstraksi model belum dipasang; halaman menyatakan aturan leksikal. PDF, DOCX, dan OCR belum didukung. Job masih sinkron di dalam transaksi, bukan Sidekiq.

## Perubahan 23:45 WIB

Proses server koordinator PID 57938 berhenti dengan kode 143. Port 8765 langsung diisi PID 79897, induknya sesi Grok 45866, direktori kerja tetap kandidat yang sama, basis data tetap `data/final-demo.sqlite`. Beranda menjawab 200 dan notebook `16cd89dcda064fe2b6390deb7b91e00d` masih ada.

Hash kandidat berubah dari `763f4da9fdf0b619f3d8ad2ddef83a83309b7f09e28c775b3066bd4a2cdbcbc0` menjadi `1ae2a53a2642d31283b87ef35e332e2fd2753b9a70374d371515cf3775462401`. Berkas yang berubah beberapa menit terakhir: `klayer/business_query.py`, `klayer/domain.py`, `klayer/pipeline.py`, `klayer/static/index.html`, `tests/test_business_query.py`, `tests/test_flow.py`. Tes belum diulang pada hash baru ini. Sesi 45866 kini juga menulis kandidat, jadi kepemilikan tunggal belum terjaga.

## Keputusan dari catatan arsitektur, 23:59 WIB

Catatan itu memisahkan kapabilitas dari pilihan stack. Untuk demo lokal, kapabilitas yang dipertahankan adalah bukti, rute, koreksi, dan kegagalan yang terlihat. Rails, Sidekiq, Gemini, dan jumlah tes pada submission lain tidak dipindahkan ke prototipe ini. Submission itu tetap beku.

Keputusan 23:59 untuk tidak port ke Rails digantikan oleh pesan pengguna: "maksud saya jangan gunakan python". Neo4j, pgvector, microservice, dan multi-agent tetap tidak dikerjakan.

Hash Python `1ae2a53a…` lulus 38 tes pada 23:59 WIB. Itu bukti historis, bukan penerimaan aplikasi Rails.

## Rails, 00:17 WIB

`bin/rails db:create db:migrate` membuat `ops_notebook_development` dan `ops_notebook_test`, lalu migrasi `20261111000100` pada development. `bin/rails test`: 5 run, 44 assertion, 0 gagal. Minitest dikunci `~> 5.25` karena Minitest 6 tidak cocok dengan Rails 7.0.

HTTP pada server hidup, bukan hanya tes:

- Budiono `db_only` / `occurred`, hanya Budiono. Budi `unknown`, hanya Budi.
- "Apakah pilot sudah berjalan?" `document_only` / `plan_not_occurrence`, kutipan memuat `HTTP-RAILS-1` dan `15 November`, tanpa kalimat ketidakhadiran.
- "Apakah Budi hadir?" `document_only` / `negated`.
- Id yang tidak ada di kutipan: `db_only` / `insufficient_evidence`.
- Id yang ada di kutipan: `combined`, jawaban `planned`.
- Notebook lain tidak melihat Budiono: `unsupported` / `abstain`.
- Koreksi kategori `other` dengan alasan "koreksi pengguna" tetap ada setelah proses ulang. Bagian lain tetap punya alasan leksikal.

Pagar koreksi ada di `Evidence.reprocess`: bagian dengan klasifikasi aktif `method=user` dilewati. Belum ada antrean terpisah. Permintaan yang memakai kata "sudah" pada rekaman `planned` tetap bisa menjadi `plan_not_occurrence`.

## Produk, 00:30 WIB

Halaman http://127.0.0.1:3000 sekarang produk kerja, bukan daftar dokumen. Ada pekerjaan, orang, bukti, tinjauan klaim, dan jejak keputusan. Tombol "Buka contoh produk" membuat notebook contoh. `ops-notebook/bin/ops` menjalankan server.

Perubahan status butuh catatan dan tidak mengikuti kalimat rencana. Klaim `rejected` atau `needs_evidence` tidak dipakai untuk menjawab. Proses ulang menyalin keputusan ke kutipan yang sama. HTTP pada server hidup: contoh terbuka, Onboarding `combined` / `planned`, status pilot yang diubah manusia menjadi `occurred`, pertanyaan dokumen pilot tetap `plan_not_occurrence`, klaim kehadiran yang ditolak tetap abstain setelah proses ulang.

Tes: 7 run, 68 assertion, 0 gagal. PDF, OCR, dan pemanggilan model belum ada. Job tetap sinkron.

## Banyak agent, 00:45 WIB

Pengguna minta pekerjaan dipecah ke banyak agent. Irisan ada di `council/AGENT-SLICES.md`. Integrator tetap satu.

Agent terpisah menulis tampilan isian dan tiga pertanyaan siap pakai, tes model, tes tepi, serta tes unggah kosong. Investigator memetakan rute. Tes tepi menunjukkan dua rekaman "Onboarding" sempat dianggap satu. `names_in_question` sekarang mengelompokkan nama yang sama, sementara nama yang lebih panjang tetap menelan nama yang lebih pendek.

`bin/rails test`: 17 run, 107 assertion, 0 gagal. HTTP pada server hidup: isian `Peserta: Sari, Budi` tampil, tombol "Apakah pilot sudah berjalan?" menjawab `plan_not_occurrence`.

## Arsitektur, setelah tinjauan

`Evidence` sekarang pintu masuk. Empat modul di bawahnya: `Lexicon` untuk teks, `Ingest` untuk unggah dan proses ulang, `Query` untuk rute jawaban, `Review` untuk keputusan manusia. Halaman dibaca lewat `Notebook::Board`. Tampilan terpecah per bagian: dokumen, klaim, pertanyaan, jejak.

Dua nama yang sama pada pertanyaan kehadiran menjawab `ambiguous`. Lebih dari satu rekaman terpilih juga `ambiguous`. Offset bagian memakai indeks karakter, jadi teks multibyte tidak ditolak. Kata "sudah" saja tidak mengubah rencana menjadi pertanyaan kejadian.

`bin/rails test`: 20 run, 112 assertion, 0 gagal. Halaman contoh di server hidup tetap menampilkan keenam bagian dan status Budiono `occurred`.

## Berkas lama dan fitur yang dipindah

README akar tidak lagi menyuruh menjalankan Python. README `ops-notebook` menjelaskan `bin/ops`. Mailer Rails yang tidak dipakai, `__pycache__`, dan berkas sampingan sqlite dibuang. Sumber `klayer/`, `automation/`, `research/`, dan `council/` tetap arsip.

Fitur Python yang masuk Rails: hash isi dokumen supaya teks yang sama tidak digandakan, pemuatan `fixtures/demo` pada contoh produk, bentrok antara dua tanggal rencana pilot, dan bentrok kehadiran yang saling menolak untuk nama yang sama. Kutipan yang tidak ada di teks sumber ditolak.

`bin/rails test`: 22 run, 120 assertion, 0 gagal. Server sempat 500 karena migrasi `content_hash` belum dijalankan. Setelah migrasi, contoh produk menampilkan keempat berkas demo dan judul Bentrok.

Gem native membutuhkan `SDKROOT` macOS. Ruby yang dipakai `RBENV_VERSION=3.3.2`. Ruby default 3.4.2 tidak punya Rails. `config/master.key` tidak dibagikan.

## Tiga langkah, dokumen perusahaan atau klien

Halaman mengikuti urutan unggah, konfirmasi jenis, lalu tanya. Ini untuk berkas internal atau berkas klien, bukan sidang. PDF, audio, dan video ditolak di layar karena belum dipindai. Jenis bagian adalah tebakan leksikal dan bisa diganti satu klik. Bedah berkas menampilkan klaim per berkas beserta kutipannya.

`bin/rails test`: 22 run, 120 assertion, 0 gagal. HTTP pada server hidup: contoh produk langkah 1–3, pertanyaan pilot `plan_not_occurrence` dengan sumber berkas, unggah `catatan-klien.txt` masuk ke langkah 2, lalu koreksi kategori `other` tetap di langkah 2.

## Lapisan dokumen, fokus gudang berkas

Layar utama sekarang dump berkas, lalu tujuh lapisan yang terlihat: berkas, teks, bagian, jenis isi, struktur, klaim, tanya. Jenis file dari ekstensi. Jenis isi dari aturan kata, bisa dikoreksi. Baris isian dan klaim yang tersimpan itulah yang dibaca pertanyaan. Banyak TXT/Markdown bisa dijatuhkan sekaligus. PDF, audio, dan video tetap ditolak. Animasi hanya menyalakan lapisan yang sudah punya baris, bukan proses model.

`bin/rails test`: 23 run, 134 assertion, 0 gagal. HTTP pada server hidup: contoh menampilkan jenis file, baris struktur, dan jawaban pilot beserta berkas sumber. Dump `memo-klien.txt` masuk ke lapisan proposal.

## Halaman terpisah untuk tiap tahap

Dump, proses, analisis, keputusan bukti, verifikasi, dan tanya sekarang halaman sendiri. Proses menampilkan rencana lalu empat kotak: inventarisasi, analisis, keputusan, verifikasi, lalu penggabungan dan jawaban. Isi kotak itu aturan lokal, bukan council model. Belum ada akun, undangan, enkripsi, atau unggah PDF.

`bin/rails test`: 24 run, 153 assertion, 0 gagal. HTTP pada server hidup: dump tidak memuat grafik proses, tiap halaman tahap menjawab 200, pertanyaan pilot tetap `plan_not_occurrence`.

## Konsensus tiga penilai

Jenis isi tidak lagi diambil dari penghitung kata yang menang sendiri. Tiga penilai berjalan terpisah: kata, isian, dan nama berkas. Nama berkas dicatat lalu diabaikan bila ia satu-satunya suara atau bertentangan dengan teks. Kata dan isian yang berbeda menghasilkan `other`. Acuan yang dipakai: pemeriksaan kutipan Consensus (kecocokan topik bukan dukungan), Chain-of-Verification (penilai tidak melihat draf penilai lain), dan jangan mengesahkan suara yang bertentangan. Bukan model MiniCheck dan bukan council LLM.

`bin/rails test`: 25 run, 160 assertion, 0 gagal.

## Tanya dari baris berjudul

Dokumen tidak dijadikan satu gumpalan untuk chat. Bagian judul menjadi jalur, isian dan klaim menggantung di bawahnya, lalu pertanyaan hanya mengambil baris yang tokennya cocok. Tidak ada baris berarti abstain. Acuan: chunk hierarkis dan heading-aware retrieval, bukan embedding dan bukan model.

`bin/rails test`: 27 run, 179 assertion, 0 gagal. "Siapa peserta notulen?" mengembalikan isian di bawah judul Notulen rapat.
