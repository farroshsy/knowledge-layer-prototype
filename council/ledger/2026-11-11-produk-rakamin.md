# Ledger — cara terima modul Rakamin

Tanggal olahan: 11 November 2026. Sumber: teks lowongan yang ditempel Farros, "Product Manager B2B / Product Consultant", Jakarta Selatan, hybrid. Status: deskripsi perekrutan. Bukan perintah CTO, bukan bukti bahwa prototipe ini adalah engagement klien.

Lowongan engineer di `2026-11-11-stack-rakamin.md` membangun modul. Lowongan ini menulis proses, aturan, dan kriteria yang modul itu dibangun untuk memenuhinya.

## Pakai sekarang

Uji pukul 08.00 membuktikan masalahnya selesai, bukan hanya bahwa tombolnya hidup. Masalah yang dikatakan CTO: berkas baru masuk ke sistem lokal, data terstruktur tetap terpisah, pertanyaan bisa menggabungkan keduanya, dan jawaban tidak melampaui bukti.

Kriteria di bawah memakai bentuk Given/When/Then. Yang bertanda "terukur" punya hasil tersimpan. Yang lain adalah aturan yang sudah dikodekan, belum diulang pada buku demo malam ini.

1. Given buku `16cd89dcda064fe2b6390deb7b91e00d` memuat Budiono dengan status occurred. When pertanyaan `Apa status Budiono?`. Then rute `db_only`, jawaban occurred, hanya rekaman itu, metode `rules`. Terukur 10 Nov, 0,000395 detik.
2. Given Budi berstatus unknown dan Budiono berstatus occurred. When pertanyaan `Apa status Budi?`. Then hanya Budi, jawaban unknown. Terukur 10 Nov, 0,000345 detik.
3. Given tidak ada data harga saham. When pertanyaan `Berapa harga saham kemarin?`. Then rute `unsupported`, jawaban abstain, metode `rules`. Terukur 10 Nov, 0,000389 detik.
4. Given kalimat rencana kehadiran, tanpa kalimat kejadian. When pertanyaan menanyakan kehadiran orang itu. Then hasilnya rencana, bukan kejadian, dan bukan bukti bahwa kejadian tidak ada.
5. Given kutipan yang memotong kata tidak, bukan, atau belum dari kalimat sumbernya. When kutipan itu hendak disimpan sebagai dukungan. Then kutipan ditolak.
6. Given dokumen baru berformat teks atau Markdown yang belum pernah dilihat. When berkas diunggah lalu ditanya hal yang ada di dalamnya. Then jawaban menunjuk kutipan dari berkas itu. Jika Grok habis 75 detik, metode yang tercatat adalah `local-rules` beserta `provider_error`. Satu unggah live pernah jatuh ke jalur itu. Pengulangan pada server yang hidup belum dicatat di sini.
7. Given rekaman bisnis dan dokumen baru memuat ID rekaman yang sama. When pertanyaan meminta status rekaman itu beserta bukti dokumennya. Then rute `combined` hanya jika kutipan memuat ID itu. Macro rules 9/9 pada 10 Nov 15:25 UTC memakai data sintetis, bukan berkas CTO.
8. Given berkas berisi dua jenis bagian. When bagian-bagian itu diklasifikasi. Then tiap bagian punya kategorinya sendiri. Belum diuji pada berkas yang akan dibawa CTO.
9. Given berkas PDF, DOCX, atau hasil pindai. When berkas itu diunggah. Then jalur demo ini tidak membacanya. Kegagalan itu dikatakan, tidak diganti dengan jawaban.

Lulus bila skenario 1–3 terlihat di layar dan skenario 6 berlaku untuk berkas teks yang dibawa. Gagal bila jawaban tanpa bukti, nama yang mirip digabung, atau `local-rules` disebut ekstraksi semantik.

## Nanti

| Artefak lowongan | Syarat sebelum dikerjakan |
| --- | --- |
| Peta proses klien sungguhan | Ada proses operasi klien, bukan skenario dummy |
| UAT bersama pengguna klien | Ada pengguna dan soal yang ditulis sebelum uji |
| SOP dan pelatihan | Modul sudah diterima pada UAT |
| Dua engagement sekaligus, laporan mingguan, log perubahan | Ada Senior Product Consultant dan klien |
| Domain SDM atau BUMN | Klien itu yang menentukannya. Lowongan hanya menyebutnya sebagai kelebihan tambahan |

## Bukti

| ID | Sumber | Klaim yang layak diingat | Label |
| --- | --- | --- | --- |
| P01 | Lowongan, bagian pekerjaan | Kriteria terima bernomor, berbentuk Given/When/Then, cukup untuk engineer membangun tanpa bertanya ulang | Teks lowongan |
| P02 | Lowongan, bagian pekerjaan | UAT menguji apakah masalah klien selesai. Tombol yang berfungsi belum cukup | Teks lowongan |
| P03 | Lowongan, kualifikasi | Data klien diperiksa: kosong, duplikat, rusak, dan arti tiap kolom di dalam proses | Teks lowongan |
| P04 | Lowongan, kualifikasi | Bahasa Indonesia dan Inggris. Keluaran AI diperiksa sebelum sampai ke klien atau engineer | Teks lowongan |
| P05 | Lowongan, kelebihan tambahan | Paparan domain SDM disebut tambahan, bukan lingkup wajib | Teks lowongan |

## Kesimpulan yang tidak sah

- Lowongan ini mengubah prototipe menjadi produk B2B untuk BUMN atau bank.
- Dua engagement, SOP, dan laporan klien harus ada sebelum pukul 08.00.
- Naskah `council/demo-walkthrough.md` adalah status server sekarang. Naskah itu masih menyebut PID 57938.
- Domain SDM pada kelebihan tambahan mewajibkan data karyawan Rakamin.

## Jangan dikutip sebagai

Jangan mengutip catatan ini sebagai spesifikasi klien yang sudah ditandatangani, atau sebagai bukti UAT bersama CTO sudah dijalankan.
