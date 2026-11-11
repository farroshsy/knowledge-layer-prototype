# Ledger — jaring mutu Rakamin

Tanggal olahan: 11 November 2026, 00:07 WIB. Sumber: teks lowongan yang ditempel Farros, "Fullstack Engineer - SDET Depth (Quality Engineer)", Jakarta Selatan, hybrid. Status: deskripsi perekrutan. Bukan perintah memasang Playwright atau Next.js sebelum pukul 08.00.

Peran ini membangun jaring yang menahan rilis saat spesifikasi hilang, syarat jatuh, atau regresi lolos diam-diam. Ia juga membangun modulnya sendiri. Pemeriksaan manual di akhir antrean bukan pekerjaan yang dilamarkan.

## Pakai sekarang

1. Sembilan skenario di `2026-11-11-produk-rakamin.md` adalah kriteria terima yang sudah tertulis. Cerita tanpa kriteria itu belum siap dibangun.
2. Pada hash kandidat `1ae2a53a2642d31283b87ef35e332e2fd2753b9a70374d371515cf3775462401`, 19 berkas, `python3 -m unittest tests.test_business_query tests.test_query_regressions tests.test_flow tests.test_business_http` menghasilkan 38 tes lulus dalam 3,488 detik. Ada ResourceWarning soket. Tidak ada kegagalan.
3. Yang dibuktikan suite itu: rute, jejak `duration_s`, rencana bukan kehadiran, kutipan yang membuang "tidak" ditolak, dan pertanyaan tanpa operasi bisnis menolak lewat aturan. Itu regresi pada jalur yang sudah ditulis.
4. Yang belum dibuktikan: presisi, recall, F1, berkas yang besok dibawa CTO, PDF, unggah Grok yang tidak timeout, dan bahwa jawaban yang tampak benar menyimpan nilai yang benar. Tes yang lulus karena meniru teks keluaran, tanpa oracle, tidak menahan rilis.
5. Keparahan untuk pagi ini: salah gabung nama, rencana dihitung hadir, kutipan membuang negasi, atau `local-rules` disebut ekstraksi semantik adalah cacat integritas data. Cacat itu menahan klaim, walaupun layarnya rapi. Salah ejaan label adalah kosmetik.
6. Tidak ada gerbang GitHub Actions pada folder ini. Jaring yang ada adalah tes lokal dan skenario bernomor. Keduanya harus disebut apa adanya saat demo.

## Nanti

| Isi lowongan | Syarat sebelum dikerjakan |
| --- | --- |
| Playwright, Jest atau Vitest, Next.js | Modul sudah berada di aplikasi React skuad, dan ada jalur yang harus ditahan di CI |
| GitHub Actions yang menolak perubahan tanpa tes | Repositori modul itu punya pipeline |
| Definition of Ready sebagai alat, bukan halaman wiki | Ada alur tiket yang bisa ditolak otomatis |
| Set evaluasi dan ground truth untuk perubahan prompt | Ada label independen dan pertanyaan yang tidak ikut ditulis oleh pembuat tes |

## Bukti

| ID | Sumber | Klaim yang layak diingat | Label |
| --- | --- | --- | --- |
| Q01 | Lowongan, pekerjaan | Definition of Ready menahan cerita yang belum punya kriteria terima. CI menahan perubahan yang merusak jalur tercakup. Definition of Done ditahan saat rilis | Teks lowongan |
| Q02 | Lowongan, kualifikasi | Bug yang tampil benar di layar tetapi menyimpan nilai yang salah digolongkan serius | Teks lowongan |
| Q03 | Lowongan, pekerjaan | Tes yang dihasilkan AI tetap dipilih. Tes yang lulus tanpa membuktikan apa pun tidak menjadi gerbang | Teks lowongan |
| Q04 | Lowongan, kelebihan | Set evaluasi, ground truth, dan regresi saat prompt berubah adalah paparan tambahan untuk fitur AI | Teks lowongan |
| Q05 | Uji lokal 11 Nov 2026 00:07 WIB | 38 tes lulus, 3,488 detik, hash `1ae2a53a…` | Pengukuran pada pohon kandidat. Bukan mutu model dan bukan UAT CTO |

## Kesimpulan yang tidak sah

- 38 tes lulus berarti berkas CTO akan terbaca.
- ResourceWarning adalah kegagalan rilis.
- Tidak adanya Playwright berarti mutu demo kosong.
- Peran ini hanya menguji di akhir dan tidak membangun modul.

## Jangan dikutip sebagai

Jangan mengutip 38 tes lulus sebagai bukti produksi, bukti F1, atau bukti unggah Grok pada server yang sedang hidup.
