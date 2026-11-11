# Ledger — produk senior dan kunci lingkup

Tanggal olahan: 11 November 2026. Sumber: teks lowongan yang ditempel Farros, "Senior Product Manager B2B / Product Consultant", Jakarta Selatan, hybrid, senior. Status: deskripsi perekrutan. Bukan kontrak klien, bukan metrik bisnis yang sudah disepakati.

Peran ini memegang maksud produk pada satu engagement, menyetujui spesifikasi di gerbang bangun, dan memutus trade-off di dalam lingkup yang sudah dikunci. Konsultan produk menulis kriteria. Technical Lead memberi putusan kelayakan sebelum ada janji ke klien. Project Leader menyerahkan lingkup terkunci beserta hasil yang diinginkan klien.

## Pakai sekarang

Lingkup uji pukul 08.00 belum dikunci oleh CTO. Belum ada prototipe yang beliau ketuk lalu setujui sebagai kontrak. Daftar ini adalah usulan yang dibawa ke demo, supaya ketukan itu yang mengunci, dan supaya hal yang dilepas terlihat.

Masuk lingkup rilis ini:

1. Satu buku catatan lokal.
2. Rekaman bisnis terstruktur, terpisah dari dokumen yang diunggah.
3. Berkas teks atau Markdown. Satu berkas boleh punya beberapa bagian, tiap bagian satu kategori.
4. Pertanyaan ke rekaman, ke dokumen, atau ke keduanya bila ID rekaman yang sama ada di kutipan.
5. Jawaban menyebut rute, metode, kutipan, dan `duration_s`.
6. Tanpa bukti, sistem menolak. Rencana bukan kejadian. Kutipan yang membuang "tidak" ditolak. Nama yang mirip tidak digabung.
7. Jika Grok habis waktu, metode yang tertulis adalah `local-rules` beserta kesalahan provider.

Di luar lingkup rilis ini:

1. PDF, DOCX, pindai, OCR, dan audio.
2. Postgres, Neo4j, mesin graph, dan embedding.
3. Rails, Express, React, Vite, Playwright, dan gerbang CI.
4. LMS, ATS, dan program pelatihan.
5. Banyak pengguna, hak akses, dan klaim produksi atau Proof of Value.
6. Metrik bisnis klien dengan garis dasar. Angka itu belum ada, jadi tidak dilaporkan.
7. Council saat menjawab, dan janji enam bulan.

Trade-off yang sudah diambil: jalur bacaan teks tetap jalan dengan cadangan leksikal yang diberi label, daripada menahan demo sampai model selesai atau menyebut cadangan itu sebagai pemahaman semantik.

Model memilih di dalam operasi yang sudah ditutup. Orang yang memutuskan lingkup, lanjut atau berhenti, dan apakah angka bisnis sudah cukup. Janji ke CTO menunggu kelayakan yang sudah diukur: 38 tes lulus pada hash `1ae2a53a…`, tiga kueri rekaman terukur, unggah Grok pernah timeout 75 detik.

## Nanti

| Isi lowongan | Syarat sebelum dikerjakan |
| --- | --- |
| Irama mingguan dan laporan yang mengusulkan langkah berikut | Ada klien yang bertindak atas laporan itu |
| Dua engagement, dua konsultan produk, dan satu desainer | Engagement itu memang ditugaskan |
| Adopsi terukur, fase kedua, atau perluasan | Ada pengguna dan garis dasar yang disepakati |
| Permintaan perubahan tingkat menengah | Ada lingkup yang sudah dikunci lewat prototipe yang diketuk |

Empat kalimat di akhir tempelan — klien BUMN atau bank, kedalaman domain SDM, metode yang diwariskan ke lima klien, dan produk B2B yang sudah terkirim — tidak punya judul sendiri di teks yang ditempel. Jangan dinaikkan menjadi syarat prototipe ini.

## Bukti

| ID | Sumber | Klaim yang layak diingat | Label |
| --- | --- | --- | --- |
| M01 | Lowongan, pekerjaan | Lingkup dikunci pada prototipe yang bisa diketuk dan disetujui klien, dengan daftar di luar lingkup | Teks lowongan. Ketukan CTO belum terjadi |
| M02 | Lowongan, kepemilikan | Hasil produk diukur pada metrik bisnis klien yang punya garis dasar | Teks lowongan. Garis dasar prototipe ini belum ada |
| M03 | Lowongan, pekerjaan | Putusan kelayakan dari Technical Lead datang sebelum janji ke klien | Teks lowongan |
| M04 | Lowongan, kualifikasi | AI dipakai untuk analisis dan prototipe. Ada wilayah yang diputus model, dan wilayah yang harus diputus orang | Teks lowongan |
| M05 | Lowongan, kualifikasi | Data perusahaan yang berantakan: sistem yang tidak sepakat, kolom kosong, pengenal yang tidak sama antar sumber | Teks lowongan. Ini selaras dengan ID stabil di demo |

## Kesimpulan yang tidak sah

- Daftar lingkup di atas sudah ditandatangani CTO.
- Tidak adanya metrik bisnis berarti demo gagal. Metrik itu belum disepakati, jadi tidak diisi.
- Peran ini menggantikan kriteria Given/When/Then atau tes 38 jalur.
- Empat kalimat tanpa judul di akhir tempelan adalah wajib untuk pagi ini.

## Jangan dikutip sebagai

Jangan mengutip catatan ini sebagai kontrak lingkup yang sudah disetujui klien, atau sebagai laporan adopsi dan hasil bisnis.
