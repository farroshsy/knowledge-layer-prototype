# Ledger — diskusi akhir share Codex

Tanggal olahan: 10 November 2026. Sumber: thread publik [Set up Codex for Rakamin repo (2)](https://chatgpt.com/s/cx_6af3487461c881919e5ba07e51affabf), giliran 117–126, plus angka yang Codex simpan di berkas riset pada giliran itu. Status: usulan dan laporan sesi. Bukan spesifikasi CTO, bukan status kandidat yang sedang dijalankan, bukan bukti produksi.

Fondasi yang sudah diolah tetap di [2026-11-10-product-foundation.md](2026-11-10-product-foundation.md). Catatan ini hanya menambah yang berubah di chat terakhir.

## Pakai sekarang

1. Besok pagi tetap Proof of Concept lokal yang bisa dijalankan. Enam bulan adalah kemungkinan jika pekerjaan dilanjutkan, bukan janji. Proof of Value, pilot, dan kesiapan produksi menunggu pengguna nyata.
2. Satu percakapan cukup: Farros berbicara ke koordinator. Pekerja lain melapor ke koordinator, bukan ke Farros. Agen bisa diganti. Yang harus bertahan adalah berkas: tujuan, kandidat, tugas, kegagalan, bukti, keputusan, langkah berikut.
3. Koordinator dan peninjau integritas memakai usaha penalaran yang kuat. Potongan implementasi yang sempit boleh model cepat. Pemeriksaan ulang adalah tes, bukan agen tambahan. Codex memilih medium agar latensi turun, lalu tidak mengubah sesi yang sedang jalan. Sesi koordinator ini sudah pada usaha tertinggi. Jangan kirim prompt baru ke pane kiri.
4. Banyak agen hanya aman bila berkasnya terpisah dan ada satu pemilik integrasi. Codex memecah empat irisan lalu integrasi kandidat lama gagal. Itu alasan menjaga satu penulis, bukan alasan menambah penulis pada berkas yang sama.
5. Angka 6/9 dan “kueri gabungan gagal di tiga domain” milik kandidat `.parallel-builds/20261110-214747-9bf46f/candidate-1` dengan provider rules. Jangan dikutip sebagai hasil demo yang sedang berjalan.
6. Label “aktif” di panel `127.0.0.1:8766` berarti panggilan sudah mulai. Panel tidak melihat apakah token sedang keluar.
7. Jangan menyalakan always-allow. Codex tidak berhasil mengaktifkannya untuk semua sesi, dan mode itu bukan syarat demo.

## Nanti

Kerjakan hanya setelah demo, dan hanya jika syaratnya ada.

| Ide | Syarat sebelum dikerjakan |
| --- | --- |
| Ganti bahasa ke Rust, Rails, atau TypeScript | Ada hambatan yang terukur, pemilik kode di tim Rakamin sudah jelas, dan batas HTTP tetap bisa diwariskan |
| Graph, vektor, plugin pasar | Kueri nyata gagal pada model sekarang, ada label emas, dan izin pemasangan sudah ada |
| LLM lokal di FarrosPC | Identitas mesin terverifikasi tanpa kata sandi, dan uji kecil lulus sebelum masuk jalur demo |
| Arus pendapatan (langganan, API, private deploy, paket domain, jasa) | Ada pembeli, pekerjaan yang berulang, dan bukti mau bayar atau penghematan waktu yang diukur |
| PDF kompendium sebagai acuan | Isinya dicek ulang. Berkas ada, jumlah halaman belum dihitung ulang di sini |

Urutan keputusan fitur yang dicatat Codex: pekerjaan pengguna, bukti masalah, hasil terukur, biaya, lalu nilai. Keamanan dan integritas tetap gerbang, walaupun tidak langsung menjadi pendapatan.

## Bukti

Label tidak dinaikkan. Laporan Codex adalah apa yang dikatakan sesi itu pada saat itu.

| ID | Sumber | Klaim yang layak diingat | Label |
| --- | --- | --- | --- |
| C01 | Giliran 117, tempelan GPT | Enam kemampuan minimum: dokumen baru, rekaman bisnis independen, pertanyaan gabungan, bukti yang bisa dibuka, menolak bila tidak bisa dijawab atau bentrok, hasil tersimpan dan bisa diulang | Usulan GPT, bukan perintah CTO |
| C02 | Giliran 117 | Lima artefak waris: proses bisnis, model domain, catatan keputusan, panduan uji, batas yang diketahui | Usulan |
| C03 | Giliran 117, jawaban Codex | Pusat konteks ada di `.context-hub/`. Daftar periksa tidak membuktikan kontrol sudah jalan. Codex menyebut pemeriksaan live 5/6 dan timeout unggah Grok | Laporan sesi. Angka belum diuji ulang di catatan ini |
| C04 | Giliran 119 | Empat irisan paralel, masing-masing berkas sendiri, lalu tes integrasi dan dua peninjau | Laporan cara kerja. Bukan izin menambah penulis |
| C05 | Giliran 120 dan `research/stack-and-retrieval-source-notes.md` | Rails/PostgreSQL pada repo studi kasus lain bukan syarat tugas ini. Prototipe baru adalah Python dan SQLite. Rust tidak memperbaiki negasi atau identitas | Catatan riset. Bukan keputusan stack |
| C06 | Giliran 121 dan `research/macro-validation-and-value.md` | Pada kandidat lama, 6 dari 9 cek rules lulus. Tiga pertanyaan gabungan tetap `db_only` tanpa klaim dokumen. Tiga domain memakai pola yang sama, jadi bukan bukti pasar | Laporan pada kandidat lain |
| C07 | Giliran 122 | Pisahkan definisi domain dari data contoh. Pemrosesan selesai bukan retrieval yang tepat. Metrik per tahap. Pandangan semantik sebelum mesin graph. Codex menamai empat gagal: label hanya-dokumen, bukti melebar, nama sebagai substring, kueri gabungan | Prinsip. Dua tautan X disebut belum terbuka, jadi atribusi akun tetap laporan GPT |
| C08 | Giliran 124–125 | Satu otak percakapan. Memori di berkas. Usaha tinggi untuk keputusan yang berakibat. Codex tidak mengubah effort sesi yang hidup | Keputusan operasi yang sudah dipakai sesi ini |
| C09 | Berkas `output/pdf/Knowledge-Platform-Complete-Discussion-and-Engineering-Compendium.pdf` | Codex menyebut PDF 136 halaman masih diperiksa render-nya. Berkasnya ada, sekitar 456 KB | Keberadaan berkas. Jumlah halaman tidak dihitung ulang |

## Kesimpulan yang tidak sah

- Tempelaan GPT tentang lapisan Perkara adalah arsitektur internal Perkara.
- Empat irisan atau empat peninjau membuat jawaban benar.
- Kandidat lama yang 6/9 adalah aplikasi yang dibuka besok.
- Panel aktivitas yang bergerak berarti token masih keluar atau pekerjaan selesai.
- Hipotesis langganan, API, atau private deploy adalah pendapatan.
- PDF kompendium adalah status terbaru atau spesifikasi.
- Always-allow membuat council lebih aman atau lebih cepat.

## Pertanyaan yang masih mengubah desain

- Siapa pemilik kode ini di Rakamin, sehingga pilihan bahasa punya arti.
- Kueri gabungan mana yang harus lulus besok, dengan dokumen yang belum pernah dilihat.
- Apakah CTO akan membawa berkas baru, atau demo cukup pada data dummy yang sudah ada.

Jangan mengisi domain pelanggan, harga, atau target akurasi dari chat ini.

## Jangan dikutip sebagai

Jangan mengutip catatan ini sebagai perintah CTO, hasil tes kandidat aktif, atau bukti bahwa Perkara memakai graph, Rust, atau council empat agen.
