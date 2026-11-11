# Ledger — fondasi produk

Tanggal olahan: 10 November 2026. Sumber: dump v0.2 "Knowledge Platform — Research Ledger & Product Foundation" plus inspeksi publik Perkara AI. Status: usulan Farros. Bukan spesifikasi yang disetujui CTO, bukan audit lengkap akun X, bukan bukti produksi.

Submission Rakamin yang sudah dibekukan tidak boleh disentuh. Enam bulan adalah amplop perencanaan, bukan janji. Pilihan berikutnya adalah lanjut, jeda, putar arah, atau berhenti.

## Pakai sekarang

Demo 11 November 2026 pukul 08.00 WIB adalah Proof of Concept lokal, bukan Proof of Value.

1. Dua sumber tetap terpisah: rekaman bisnis yang diisi sendiri, dan dokumen yang diunggah.
2. Pertanyaan boleh memakai basis data, dokumen, atau keduanya. Rencana kueri memilih operasi yang diizinkan. Model tidak menulis SQL yang langsung dijalankan.
3. Nama yang sama bukan identitas yang sama. Rencana bukan kejadian, dan juga bukan bukti bahwa kejadian tidak ada.
4. Kutipan yang menunjuk lokasi belum berarti klaimnya benar. Jawaban tanpa bukti harus menolak.
5. Teks unggahan adalah data, bukan instruksi.
6. Angka dari pos publik (biaya per halaman, latensi, token, "empat agen") adalah laporan penulis. Bukan target produk ini.
7. Inti yang stabil boleh punya adapter yang bisa diganti. Jangan mengunci inti ke satu contoh pengadaan, dan jangan membuat mesin ontologi umum sebelum ada klien.

## Nanti

Kerjakan hanya setelah demo dan ada keputusan lanjut.

| Ide | Syarat sebelum dikerjakan |
| --- | --- |
| PostgreSQL, object storage, pencarian teks penuh | Ada kebutuhan yang SQLite lokal tidak penuhi |
| Graph database | Kumpulan kueri nyata gagal pada model relasional untuk kebenaran, keterawatan, dan latensi sekaligus |
| Council agen saat setiap pertanyaan | Dukungan bukti naik terukur dibanding satu pemeriksa, pada anggaran yang disetujui |
| Vektor dan reranker | Ada label emas dan anggaran konteks, bukan karena pos publik menyebut 1,2 juta token |
| RBAC, tenant, audio, OCR ensemble | Ada persona, data nyata yang diizinkan, dan pemilik keamanan |

Pilihan awal yang direkomendasikan dump: model semantik relasional, dengan batas modul yang kecil (`EvidenceRepository`, `EntityResolver`, `QueryPlanner`, `RetrievalProvider`, `ModelGateway`). Graph adalah proyeksi belakangan, bukan sumber kebenaran kedua.

## Bukti dari pos publik

Label tidak dinaikkan. "Pernyataan langsung" berarti penulis mengatakannya. "Angka penulis" berarti metodenya belum dibuka. "Inferensi" bukan kata penulis.

| ID | Sumber | Klaim yang layak diingat | Label |
| --- | --- | --- | --- |
| E01 | 6 Mar | Sekitar 4.700 halaman dan 8.900 kesaksian lewat praolah, ekstraksi, graph, dan agen tinjau-diri | Pernyataan langsung plus skala yang dilaporkan |
| E02 | 26 Mar | Audio dipecah: ucapan-ke-teks, ganti pembicara, identitas pembicara, lalu ke graph | Pernyataan langsung. Audio bukan syarat demo |
| E03 | 31 Jul | Ada percobaan konkurensi dan persentil waktu serta biaya untuk 10.000 halaman | Pernyataan langsung. Tiru cara mengukur, bukan mesinnya |
| E04 | 1 Agu | Beberapa OCR dibanding, lalu adjudicator. Klaim galat 3–5 kali lebih rendah disebut nonscientific | Angka penulis. Uji pada kebenaran sendiri |
| E05 | 6 Agu | Imaging, OCR, adjudicator, ditambah log kemajuan dan kesehatan | Pernyataan langsung. Butuh status pekerjaan dan ulang yang idempoten |
| E06 | 6 Agu | Perkiraan sekitar Rp72/halaman lawan Rp7.000/halaman | Angka penulis. Bukan target biaya |
| E07 | 8 Agu | Model mengembalikan wilayah dan offset. Backend mengambil teks dari sumber | Petunjuk terkuat. Lokasi tetap harus dicek dukungannya |
| E08 | 2 Nov | Agen tidak menebak SQL mentah. Ada model semantik. Alternatif sederhana: materialized view PostgreSQL | Pernyataan langsung. Kebenaran semantik di atas pilihan graph |
| E09 | 5 Nov | Council disebut menjadi empat. UI memperlihatkan orkestrasi dan sumber | Pernyataan langsung. Jumlah agen belum ada uji manfaat |
| E10 | 6 Nov | Jawaban kompleks disebut 10 menit 7 detik. Ada pikiran memisahkan lookup cepat dari analisis dalam | Angka penulis. Dua jalur, bukan satu jalur lambat |
| E11 | 7 Nov | Model dipilih lewat kebenaran, jumlah tugas, konteks, dan interval ketidakpastian | Prinsip evaluasi. Angkanya tidak otomatis berlaku di sini |
| E12 | 9 Nov | Menolak konteks 6 kali lipat untuk recall tambah 0,083 | Pernyataan langsung. Ukur mutu, latensi, dan biaya bersama |
| E13 | 9–10 Nov | Sekitar 1,2 juta token simpul masuk reranker. Throughput disebut 1–2 pertanyaan per menit. Decision model disebut 60% lebih murah | Angka penulis, belum diuji ulang |

Cakupan pos itu pilihan, bukan arsip lengkap. Akun disebut sekitar 10.800 pos. Gambar, video, pos terhapus, dan yang perlu login belum diperiksa.

## Kesimpulan yang tidak sah

- Sebelas lapisan pada gambar produk berarti sebelas tabel atau sebelas layanan.
- Empat agen membuat jawaban bebas halusinasi.
- Kutipan di halaman yang benar berarti klaimnya benar.
- Basis graph menyelesaikan negasi.
- Tangkapan layar benchmark penulis adalah ambang terima CTO.
- Landing page Perkara membuktikan akurasi OCR, transkripsi, atau sitasi.

## Inspeksi publik Perkara

Ini bacaan halaman publik, bukan arsitektur internal. Ketentuan layanan disebut melarang rekayasa balik. Jangan mendekompilasi bundle atau menguji endpoint privat.

Yang terlihat dari materi publik: produk bukti untuk kerja hukum, berkas masuk, jawaban yang menunjuk sumber, dan ilustrasi dengan data rekaan. Sebelas nama lapisan (berkas sampai sintesis) adalah pembagian konsep. Model relasional dengan tautan sumber dapat mewujudkannya. Beberapa calon jawaban sebelum jawaban akhir bisa berupa generasi lalu pemeriksaan, bukan agen yang bebas saling bicara.

Dua kalimat publik tentang lokasi data perlu dibaca hati-hati: penyimpanan di Indonesia dan pemrosesan oleh pihak ketiga di luar Indonesia bukan kalimat yang sama. Keduanya belum diverifikasi ulang di sini.

## Pertanyaan yang masih mengubah desain

- Siapa pengguna pertama, dan sakitnya apa.
- Apakah data perusahaan asli akan diproses, dan provider mana yang diizinkan.
- Siapa yang berhak memutuskan lanjut, jeda, atau berhenti.

Persona, format berkas, tenant, RBAC, SLO, dan target akurasi masih kosong. Jangan diisi diam-diam.

## Jangan dikutip sebagai

Jangan kutip catatan ini sebagai bukti bahwa semua pos sudah dibaca, bahwa fitur Perkara sudah terverifikasi, atau bahwa CTO sudah menyetujui rekomendasi ini.
