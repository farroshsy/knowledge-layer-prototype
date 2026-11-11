# Riset KMS 2025–2026 yang lolos pemeriksaan

Status: sebagian. Tanggal olahan 10 November 2026. Sumbernya laporan `deep-research` sesi ini. Angka di bawah adalah angka penulis makalah, bukan hasil yang dihitung ulang di mesin ini. Satu pertanyaan peneliti gagal: dukungan pustaka untuk polaritas, modalitas, rencana-lawan-kejadian, dan skor kesegaran tidak masuk laporan.

## Yang menempel pada demo ini

Prototipe lokal satu pengguna bukan objek makalah manajemen pengetahuan multinasional. Makalah yang terbuka membahas budaya, pemakaian karyawan, atau perpindahan pengetahuan lintas batas. Mereka tidak menetapkan skema, indeks, atau aturan menolak jawaban [S4][S5][S1].

Yang berpindah ke demo:

- Jawaban boleh memakai baris terstruktur dan teks sekaligus. TableRAG menyimpan tabel di basis relasional dan teks di indeks padat, lalu bergantian mengambil teks dan menjalankan SQL [S13].
- Kunci stabil dipakai untuk membaca kembali baris. Pada korpus EDGAR, graph hanya proyeksi dari PostgreSQL yang sama. Jawaban naratif tetap dibaca dari baris lewat accession number [S14].
- Text-to-SQL bisa menggabungkan orang yang hanya sama nama belakang, lalu menyatakan penggabungan itu dengan yakin. Enam dari 180 percobaan adalah kebohongan yang yakin, semuanya text-to-SQL pada pertanyaan multi-hop. Lengan graph pada set itu tidak punya kasus itu [S15].
- Model sering tetap menjawab ketika bukti hilang, menyesatkan, atau bertentangan. Pada tujuh model, jawaban berlebih saat bukti bertentangan berada di 65% sampai 91% [S11]. Pada model kecil yang dibekukan, 41,6% pertanyaan menyesatkan tetap dijawab, dan 63% jawaban itu mengulang entitas salah yang disisipkan [S7].
- Sitasi bisa dipasang setelah jawaban. Sekitar satu dari tujuh sitasi RAG pada pertanyaan Wikipedia tidak setia pada sumbernya. Hadiah untuk jawaban yang benar tidak menurunkan pola itu [S9].

## Klaim yang ditempel, dan statusnya

| Klaim | Status |
| --- | --- |
| Artikel Itelkom adalah desain sistem | Bukan. Muslikhudin dan Yaqin, tinjauan PRISMA faktor keberhasilan, JAIIT 8(1), Mei 2026, DOI 10.52435/jaiit.v8i1.768 [S1] |
| Springer 10.1007/s40171-025-00448-w adalah arsitektur | Bukan. Survei 221 responden tentang budaya dan pemakaian KMS di perusahaan multinasional, 24 Juni 2025 [S4] |
| ScienceDirect S1367327025000900 adalah arsitektur | Bukan. Tinjauan sensemaking dan sensegiving, Journal of Knowledge Management 29(11), 23 September 2025 [S5] |
| Enterprise Knowledge 2026 mengukur multi-agen | Bukan. Esai konsultan Zach Wahl, 29 Januari 2026, diakhiri ajakan kontak [S6] |
| Pencarian perusahaan hanya berhasil 10% pada percobaan pertama | Ada di halaman pemasaran Speakwise, dikreditkan ke laporan Slite yang tidak dibuka. Tidak ada di pos Coworker. Bukan pengukuran primer [S2][S3] |
| ResearchGate 237149844 adalah riset 2025–2026 | Tidak terbukti dari halaman penerbit. Ekstrak pencarian menunjuk bab 2011. Byline bab tidak dikonfirmasi |
| ResearchGate 395376485 dan halaman Vable tentang sidik jari digital | Halaman tidak cukup terbuka untuk menetapkan penulis, tahun, atau mekanisme |

## Agen banyak, yang terukur

Debat beberapa agen pada ICML 2024 menaikkan akurasi biografi dari 66,0% ke 73,8% dibanding satu agen. Itu di luar 2025–2026 [S18]. Pada tugas keuangan, koordinasi terpusat disebut memberi kenaikan relatif sekitar 80,8% dengan 285% giliran penalaran tambahan terhadap satu agen. Pada tugas berurutan, setiap varian multi-agen lebih buruk daripada satu agen [S19][S21]. Jika satu agen sudah cukup kuat, menambah agen sering tidak menambah kebenaran [S20].

## Yang tidak mengubah demo besok

Budaya, anak perusahaan, transkripsi rapat, kembaran digital, dan kontrol akses berbasis peran tidak ada sebagai syarat untuk satu pengguna pada basis datanya sendiri. RBAC text-to-SQL adalah hasil untuk banyak peran [S16][S17].

## Sumber

- [S1] https://journal.ittelkom-sby.ac.id/jaiit/article/download/768/307/3682
- [S2] https://speakwiseapp.com/blog/knowledge-management-statistics
- [S3] https://coworker.ai/blog/knowledge-management-trends
- [S4] https://doi.org/10.1007/s40171-025-00448-w
- [S5] https://www.emerald.com/jkm/article/29/11/291/1311733/Multinational-enterprises-knowledge-management
- [S6] https://enterprise-knowledge.com/top-knowledge-management-trends-2026/
- [S7] https://arxiv.org/abs/2608.22228
- [S9] https://arxiv.org/abs/2609.23053
- [S11] https://doi.org/10.32604/cmc.2026.086343
- [S13] https://aclanthology.org/2025.emnlp-main.710/
- [S14] https://ar5iv.labs.arxiv.org/html/2610.37728
- [S16] https://arxiv.org/html/2607.22115v1
- [S17] https://arxiv.org/abs/2607.12341
- [S18] https://arxiv.org/pdf/2305.14325.pdf
- [S19] https://www.nature.com/articles/s42256-026-01268-y
