# Skrip penjelasan untuk CTO

Buka http://127.0.0.1:3000 di mesin ini. Ruang yang dipakai: "Operasional contoh". Jangan membuka port 8765. Di layar Tanya, metode yang tampil adalah `rules` dan `semantic` false. Itu sengaja. Kalimat di bawah ini untuk diucapkan.

## Pembuka

Yang saya tunjukkan pagi ini adalah bukti bahwa alur utamanya berjalan di mesin lokal. Data operasional disimpan sendiri. Dokumen yang diunggah disimpan sendiri. Pertanyaan hanya boleh menjawab dari baris yang memang ada. Kalau barisnya tidak ada, sistem menolak. Ini belum mengukur penghematan waktu, akurasi model, atau kesiapan produksi.

## Layar, dari kiri ke kanan

Ada tujuh langkah.

1. Dump. Taruh berkas dan rekaman.
2. Pemetaan. Sistem memutuskan jalur fisik berkas: teks langsung, lapisan teks PDF, atau ditolak.
3. Proses. Teks dipecah menjadi bagian, dengan posisi yang menunjuk kembali ke sumber.
4. Analisis. Tiap bagian dapat jenisnya, lalu isian dan klaim.
5. Keputusan. Hanya baris yang masih boleh dipakai yang ikut menjawab.
6. Verifikasi. Kutipan diletakkan di samping kalimat sumber. Orang bisa menerima atau menolak klaim.
7. Tanya. Pertanyaan mengambil baris itu, bukan menyusun ringkasan baru.

## Dua sumber

Rekaman bisnis tidak lahir dari dokumen. Di ruang contoh ada lima rekaman.

- Budi, status unknown.
- Budiono, status occurred. Status ini ditutup dari catatan operasional, bukan dari kalimat di notulen.
- Sari, status unknown.
- Onboarding karyawan, status planned.
- pilot, status planned.

Setiap rekaman punya identitas publik 32 karakter. Nama hanya label. Budi dan Budiono tidak digabung, karena pencocokan nama memakai batas kata dan nama yang lebih panjang dicek lebih dulu.

Dokumen di ruang yang sama: `rapat-contoh.txt`, `catatan-bebas.md`, `email-dana.md`, `notulen-maret.md`, dan `sop-dapur.md`.

## Teknologi

Aplikasi ini Ruby on Rails 7. Data ada di PostgreSQL, basis `ops_notebook_development`. Layarnya HTML yang dirender server. Tidak ada antrean terpisah pada jalur contoh. Pemrosesan unggah selesai di dalam satu transaksi.

Pembaca berkas: teks dan Markdown langsung. PDF yang sudah punya lapisan teks dibaca dengan pustaka `pdf-reader`, paling banyak 300 halaman. DOCX dibaca dari XML di dalam zip. Gambar, rekaman suara, dan PDF hasil pindai tidak diubah menjadi teks. Sistem menyimpan alasan penolakan, dan OCR tidak dipanggil.

Model bahasa tidak dipasang pada jalur tanya. Yang menjawab adalah aturan di `Evidence::Lexicon` dan `Evidence::Query`.

## Algoritma, dari berkas sampai jawaban

Langkah satu, pintu masuk. Ekstensi menentukan jalur sebelum isi ditafsirkan. Teks kosong, teks di atas 200 ribu karakter, jenis yang tidak dikenal, gambar, dan rekaman ditolak dengan alasan. Isi yang ditolak tidak disimpan sebagai dokumen.

Langkah dua, pecah bagian. Teks dipotong pada baris kosong. Setiap bagian menyimpan awal dan akhir. Jika potongan itu tidak sama dengan teks sumber pada posisi itu, unggah gagal. Offset yang salah tidak dilanjutkan.

Langkah tiga, jenis bagian. Tiga penilai tidak saling melihat. Penilai kata menghitung kata kunci: notulen, sop, proposal, atau laporan progres. Penilai isian melihat baris seperti `Peserta:` atau `Anggaran:`. Penilai nama berkas hanya memberi suara, lalu diabaikan bila ia satu-satunya suara atau bertentangan dengan teks. Dua penilai yang tidak sepakat menghasilkan jenis `other`. Satu berkas boleh berisi beberapa bagian dengan jenis berbeda.

Langkah empat, isian. Jenis menentukan kolom yang dicari. Notulen mencari peserta, keputusan, dan tindakan. SOP mencari langkah dan penanggung jawab. Proposal mencari tujuan dan anggaran. Laporan progres mencari capaian dan hambatan. Nilai yang tersimpan adalah kutipan barisnya, bukan parafrase.

Langkah lima, klaim. Kalimat dipotong pada titik, tanda seru, tanda tanya, atau baris baru. Kalimat yang memuat tidak, bukan, atau belum berpolaritas negated. Kalimat yang memuat direncanakan, rencana, atau dijadwalkan bermodalitas plan. Predikat yang dikenali sekarang adalah kehadiran dan pilot.

Langkah enam, orang. Di verifikasi, satu klaim bisa diterima atau ditolak. Bagian yang dikoreksi orang dikunci, dan proses ulang tidak menimpa kunci itu.

Langkah tujuh, tanya. Urutannya tertutup.

- Jika pertanyaan menyebut identitas publik dan juga meminta dokumen, jawaban gabungan hanya keluar bila kutipan memuat identitas yang sama persis. Kalau identitas ada tetapi kutipan tidak memuatnya, jawaban tetap dari rekaman dan alasan menyatakan bukti dokumen tidak cukup.
- Jika pertanyaan tentang hadir atau tentang pilot yang sudah berjalan, dan tidak menyebut kata dokumen, jalur yang dipakai adalah dokumen.
- Jika nama atau identitas menunjuk tepat satu rekaman, jawaban adalah status rekaman itu. Status planned yang ditanya "sudah terjadi" menjadi `plan_not_occurrence`. Rencana tidak membuktikan kejadian, dan tidak membuktikan kejadian tidak ada.
- Jika lebih dari satu rekaman cocok, jawaban ambiguous.
- Jika tidak ada rekaman yang cocok, sistem mencari isian dan klaim di bawah judul bagian. Token pertanyaan harus bertumpang dengan baris, dengan ambang skor. Lima baris teratas yang lolos yang dikembalikan. Skor tidak cukup menghasilkan abstain.
- Jawaban mengulang baris yang tersimpan. Sistem tidak menulis kalimat baru.

## Yang diklik saat ini

Ruang contoh sudah terisi. Empat pertanyaan ini saya jalankan pada ruang itu tadi, dan hasilnya begini.

1. Tanya: Apa status Budiono? Rute `db_only`. Jawaban `occurred`. Hanya Budiono. Ucapkan: status ini atribusi rekaman operasional, bukan kesimpulan dari semua dokumen.
2. Tanya: Apa status Budi? Rute `db_only`. Jawaban `unknown`. Hanya Budi. Ucapkan: nama yang mirip tidak meminjam status Budiono.
3. Tanya: Apakah pilot sudah berjalan? Rute `document_only`. Jawaban `plan_not_occurrence`. Ucapkan: dokumen mengatakan rencana. Rencana tidak saya naikkan menjadi kejadian.
4. Tanya: Apakah Budi hadir? Rute `document_only`. Jawaban `conflict`. Tiga kutipan yang tersimpan: `rapat-contoh.txt` mengatakan Budi tidak hadir di rapat 14 Maret, `email-dana.md` mengatakan Budi tidak bisa ikut meeting, `notulen-maret.md` mengatakan Budi hadir di rapat 14 Maret. Ucapkan: sistem tidak memilih pemenang. Dua sumber tidak sepakat, jadi jawabannya konflik.
5. Tanya: Berapa harga saham kemarin? Rute `unsupported`. Jawaban `abstain`. Ucapkan: tidak ada barisnya, jadi tidak ada tebakan.

Kalau CTO membawa berkas baru, unggah lewat Dump. Berkas teks atau Markdown langsung masuk. PDF yang punya teks ikut terbaca. PDF pindai berhenti di Pemetaan dengan alasan, tanpa jawaban palsu. Setelah unggah, buka Verifikasi, lalu Tanya satu hal yang kalimatnya memang ada di berkas itu.

## Yang saya perbaiki dengan kode, bukan dengan model

Tiga hal ini lebih cepat dan lebih aman dikunci di aturan.

- Kata "akan hadir" belum dihitung sebagai rencana. Daftar modalitas masih `direncanakan`, `rencana`, dan `dijadwalkan`.
- Identitas gabungan masih harus tertulis di pertanyaan. Orang tidak akan menempel identitas 32 karakter. Penggabungan yang wajar adalah: rekaman sudah terpilih lewat nama, dan kutipan memuat identitas rekaman itu.
- Pertanyaan "Apakah Budi hadir?" memakai semua klaim kehadiran di ruang itu, lalu melihat polaritasnya. Penyaringan nama di dalam jalur dokumen masih perlu dikunci supaya klaim orang lain tidak ikut masuk.

## Yang boleh dipercepat dengan model, dengan batas

Model, Gemini atau yang setara, tidak menulis jawaban akhir. Jawaban akhir tetap baris yang tersimpan, atau abstain. Model hanya mengusulkan, di dalam skema, dan backend yang menolak usulan yang keluar dari batas.

1. Pengarah pertanyaan. Masukan adalah pertanyaan plus daftar operasi yang sah: status rekaman, kehadiran, rencana lawan kejadian, isian pada jenis tertentu, atau abstain. Keluaran adalah satu nama operasi dan identitas rekaman bila ada. Filter kosong ditolak, lalu sistem abstain. Model tidak menerima izin menulis SQL.
2. Usulan jenis bagian, hanya bila dua penilai aturan seri. Keluaran wajib salah satu dari `sop`, `notulen`, `proposal`, `laporan_progres`, atau `other`, plus kutipan yang benar-benar ada di bagian itu. Kutipan yang tidak ditemukan dibuang, dan jenis tetap `other`.
3. Usulan rentang untuk PDF yang halamannya berupa gambar. Model mengembalikan teks draf dan nomor halaman. Draf itu tidak menjadi klaim sebelum orang menerimanya di Verifikasi. Halaman yang gagal dibaca tetap tercatat gagal.
4. Pemilihan ulang dari calon yang sudah diambil aturan. Model hanya boleh mengembalikan identitas baris yang ada di daftar calon. Baris baru dari model dibuang.

Batas waktu model dicatat. Kalau waktu habis, jalur aturan tetap menjawab dan layar menampilkan kegagalan provider. Satu kali timeout tidak diganti dengan jawaban yang tampak mulus.

Yang tidak diberikan ke model: menggabungkan dua orang karena namanya mirip, mengubah rencana menjadi kejadian, dan menyusun paragraf yang tidak punya kutipan.
