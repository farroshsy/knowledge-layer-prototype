# Riset domain publik Rakamin

Masukan untuk peninjau bisnis A/B. Bukan wewenang mengubah `klayer`, skema, atau janji fitur. Bukan konfirmasi roadmap, masalah departemen, atau hasil seleksi. Hipotesis pengguna: tugas repositori lokal ini mungkin mencerminkan kebutuhan internal. Itu tetap hipotesis.

Dibaca 2026-11-10 tanpa login, formulir, atau API privat. `https://www.rakamin.com` dialihkan ke `https://app.rakamin.com/`. Fetch langsung akar aplikasi dan halaman Job Guarantee hanya mengembalikan judul "Rakamin". `open_page` pada dua URL aplikasi: "No content found". `blog.rakamin.com` gagal DNS saat fetch langsung. Teks di bawah berasal dari indeks publik URL resmi yang sama. Pusat bantuan, kebijakan privasi, dan syarat terpisah tidak terbaca.

## 1. Fakta publik yang terbaca

Entitas di footer beberapa halaman aplikasi: PT. Rakamin Kolektif Madani, Menara Caraka, Jl. Mega Kuningan Barat, Setiabudi, Jakarta Selatan. Label "Official Internship Partner": Kementerian Komunikasi dan Informatika RI. Footer fitur: Explore Course, Digital Career Profiler, Project-Based Internship. Kontrak kemitraan dan sertifikat tidak dibuka.

Navigasi terindeks di `https://app.rakamin.com/free-class/fullstack-web-development` dan `https://app.rakamin.com/job-guarantee-bootcamp/data-science`: Short Course; Digital Bootcamp (Data Science, Digital Marketing, Fullstack Web Development, Product Management); Project-Based Internship; For Campus; Prakerja; Lowongan Kerja. Isi For Campus dan Prakerja tidak dibuka. Free class FSWD menulis layanan gratis: sertifikat, kesempatan diskon, mini portfolio, akses konten selamanya, belajar fleksibel, video learning.

`https://app.rakamin.com/virtual-internship-experience/data-governance-specialist-rakamin`: Project-Based Internship Data Governance di Rakamin Academy; article review, company coaching video, latihan, tugas, umpan balik, survei kepuasan minggu 3 dan 4. Cuplikan indeks: "202 orang telah berpartisipasi"; pendaftaran sampai 03 Mei 2026, 12.59. Tools: Excel, Google Workspace. Blurb Inggris: platform ujung-ke-ujung untuk karier teknologi, kelas langsung, asesmen dan konseling karier, coaching, virtual internship, job guarantee. URL VIX lain (`vix-muamalat-bi-analyst`) hanya menampilkan halaman tidak ditemukan.

`https://app.rakamin.com/job-guarantee-bootcamp/data-science` (indeks): Job Connector untuk Job Guarantee Bootcamp setelah lulus dan kategori "High Value Talent"; jika belum masuk kategori, skor masih bisa ditambah, fasilitas disebut berlaku seumur hidup. Jalur Job Guarantee Program merekomendasikan siswa berkualifikasi ke Hiring Partners. Halaman yang sama: pengembalian dana dapat diajukan jika 6 bulan setelah lulus belum bekerja, sesuai syarat. Kelulusan disebut terjamin karena belajar sampai minimal nilai 75 dan kehadiran 80%. Halaman juga menyebut Batch 65 mulai 13 Februari 2026, 12+ mini portfolio, 1 portofolio dari PBI 4 minggu, dan sertifikasi Education Alliance Finland. Badan sertifikat EAF tidak dibaca.

`https://blog.rakamin.com/cara-daftar-pbi/` (FAQ 18 Jan 2024, indeks saja): akun, pilih program, isi data diri, pilih Free atau VIP. Free berstatus "Dalam proses seleksi" dan menunggu pengumuman; ada "Upgrade to VIP Now" ke Checkout. VIP menunggu tanggal mulai lalu langsung mengakses. Program dikerjakan dalam 28 hari. Blog 31 Jan 2024 (`mengulik-program-job-guarantee-intensive-dan-blended-bootcamp-data-science-rakamin`) menulis jaminan kerja maksimal 9 bulan atau 100% uang kembali, plus angka portfolio dan durasi yang berbeda dari halaman aplikasi. Blog 27 Feb 2024 menulis bahwa fitur lowongan kerja tersedia. Alur Digital Career Profiler / Unified Assessment Test tidak dibuka; hanya nama di footer dan blog.

Profil publik `app.rakamin.com/profile/…` menampilkan ajakan "Login as a recruiter explore full digital CV details." CV lengkap di balik login tidak dibaca. Tidak ada nama, GPA, atau kredensial orang nyata di laporan ini. Pola indeks: status kesempatan berbeda-beda; sebagian entri menampilkan GPA 0.00; ada jendela tanggal selesai berdampingan dengan label "Present".

Konflik salinan publik, belum diselesaikan: jendela refund 6 bulan (halaman aplikasi) versus 9 bulan (blog 2024); durasi 28 hari versus PBI 4 minggu versus pengalaman 12 minggu di artikel lain; jumlah portfolio tidak seragam. Ini beda teks publik, bukan kebijakan internal yang terverifikasi.

## 2. Hipotesis pemakaian pengetahuan internal

Bukan temuan tentang sistem Rakamin. Hipotesis yang berguna untuk demo lokal: staf operasi perlu menggabungkan catatan terstruktur (program, cohort, status pendaftaran, nilai, kehadiran, versi kebijakan) dengan berkas lepas (SOP, memo penerimaan, cuplikan FAQ, catatan tugas). Pertanyaan nyata sering membandingkan status basis data dengan kalimat di dokumen. Klasifikasi tunggal tidak cukup karena satu berkas dapat memuat SOP dan catatan survei sekaligus. Kebutuhan CTO yang sudah diberikan tetap dua kelas sumber plus pertanyaan gabungan, data dummy, dokumen tak terlihat pada 2026-11-11 08:00 WIB. Hipotesis ini tidak memilih Postgres, graf, atau embeddings.

## 3. Dua skenario dummy

Semua ID dan nama sintetis. Bukan data Rakamin dan bukan pembangunan LMS atau platform rekrutmen.

### A. Meja operasi program (disarankan)

Menempel pada label publik (cohort, Free/VIP, status seleksi, ambang 75/80, jendela refund) supaya penggabungan dua sumber teruji. Risiko: bentuknya mirip data peserta, jadi wajib sintetis dan tidak boleh diisi dari profil publik.

Tabel minimal: `person(person_id, nama)`; `cohort(cohort_id, label)`; `enrollment(enrollment_id, person_id, cohort_id, tier, status, nilai, hadir_pct)`; `kebijakan(kebijakan_id, topik, bulan)`.

Baris: PSN-A Sari Contoh / ENR-1001 / CHT-MEI / free / `dalam_proses_seleksi` / null / null. PSN-B Bima Contoh / ENR-1002 / CHT-MEI / vip / `mulai` / 80 / 90. PSN-C Sari Lain / ENR-1003, nama depan sama. POL-REFUND bulan = 6.

Dokumen: DOC-SOP-01 (Free menunggu pengumuman; VIP menunggu tanggal mulai). DOC-MEMO-02 (kalimat "ENR-1001 diterima"). DOC-FAQ-03 (kalimat refund 9 bulan). DOC-CATATAN-04 ("Bima Contoh belum mengerjakan tugas minggu 4").

- Hanya DB: tier dan status ENR-1001? `free`, `dalam_proses_seleksi`. Bukti: baris enrollment. Memo tidak mengubah baris.
- Hanya dokumen: apakah DOC-SOP-01 menyuruh peserta VIP menunggu pengumuman seleksi? Tidak. VIP menunggu tanggal mulai. Bukti: kalimat SOP.
- Gabungan: apakah ENR-1002 memenuhi ambang angka publik dan sudah selesai tugas minggu 4? Nilai 80 dan hadir 90 memenuhi ambang 75/80 pada baris DB. DOC-CATATAN-04 menyatakan tugas minggu 4 belum dikerjakan. Kedua bukti tampil berdampingan. "Belum" bukan bukti penyerahan. Pertanyaan refund: POL-REFUND = 6 versus DOC-FAQ-03 = 9 adalah konflik, tanpa pemenang. "Sari" saja tidak memilih PSN-A atau PSN-C. Jumlah peserta nyata batch Mei tidak ada di DB dummy: abstain.

### B. Operasi internal generik

Lebih jauh dari produk publik, privasinya lebih longgar. Tabel: `vendor` VND-01 CV Sumber Fiktif; `po` PO-77 status `dipesan` 15000000; `invoice` INV-9 status `belum_bayar`, `paid_at` null. Dokumen: DOC-KONTRAK (bayar setelah BAST); DOC-SUREL ("jangan bayar INV-9 sebelum revisi"); DOC-NOTULEN ("rencana bayar Jumat"). BAST tidak ada.

- Hanya DB: apakah INV-9 lunas? Tidak. Status `belum_bayar`.
- Hanya dokumen: apakah surel mengizinkan bayar sekarang? Tidak. Kalimatnya melarang sebelum revisi.
- Gabungan: apakah notulen membuat INV-9 layak dilunasi? Tidak. DB belum bayar, surel melarang, notulen hanya rencana, BAST absen sehingga syarat kontrak tidak terbukti. Nama vendor yang mirip tidak boleh menyambung PO lain.

Saran: pakai A untuk walkthrough karena satu pertanyaan butuh ID stabil, ambang di DB, dan negasi di dokumen, serta konflik 6 lawan 9 bulan sudah ada di sumber publik. B tetap disimpan sebagai paket cadangan bila berkas besok bersifat pembelian. Kelemahan A: pengulas bisa mengira ini spesifikasi rekrutmen. Batas eksplisit: demo menjawab pertanyaan atas catatan dan berkas, tidak mendaftarkan peserta, tidak menyeleksi, dan tidak membuka lowongan.

## 4. Privasi, ambiguitas, tiga kendala uji

Jangan menyerap profil, CV, GPA, kredensial, atau email orang nyata. Nama sama bukan kunci gabung. GPA 0.00 dan "Present" pada indeks profil adalah peringatan kualitas tampilan, bukan data demo. Satu berkas boleh punya beberapa segmen. Konflik disimpan bersama. Rencana dan negasi tidak menjadi kejadian.

1. Tenggat 2026-11-11 08:00 WIB dan dokumen tak terlihat: oracle deterministik hanya untuk fixture. Jawaban produksi tidak dikunci ke kalimat skenario ini.
2. Salinan publik sudah bentrok. Uji harus menampilkan konflik dan abstain, bukan menormalkan satu "aturan Rakamin".
3. Set awal yang masuk akal: teks, tabel sederhana, dan metadata ID. Video coaching, scan, dan spreadsheet mentah di luar set itu ditolak dengan alasan yang terlihat. Sertifikat dan video instruksi pada halaman publik tidak dibuka di riset ini.

## 5. Jangan disimpulkan dari UI, dan pertanyaan CTO

Shell kosong bukan bukti produk kosong atau sedang down. Label menu bukan spesifikasi proses. Login rekruter bukan model ATS. Angka peserta dan tanggal batch adalah cuplikan indeks. Klaim Kominfo, EAF, dan Hiring Partners tetap klaim halaman. Riset ini tidak menetapkan arsitektur penyimpanan.

Pertanyaan yang tidak memblokir semalam: berkas uji besok lebih dekat ke operasi program (pendaftaran, SOP, memo) atau ke operasi umum (PO, kontrak, surel), dan ID stabil mana yang sah sebagai kunci gabungan? Kedua paket dummy boleh diunggulkan; jawaban CTO hanya memilih naskah demo.

## Bukti yang benar-benar terbaca

Fetch langsung aplikasi hampir tidak berisi teks. Isi yang dikutip berasal dari indeks `app.rakamin.com` (VIX Data Governance, Job Guarantee Data Science, Free Class FSWD, footer badan hukum) dan indeks `blog.rakamin.com` (FAQ PBI 18 Jan 2024, artikel JGP 31 Jan 2024, artikel lowongan 27 Feb 2024). Blog tidak terfetch langsung karena DNS. Tidak ada sesi login. Tidak ada data orang nyata yang disalin ke skenario.
