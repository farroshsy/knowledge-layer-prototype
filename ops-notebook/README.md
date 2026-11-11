# Notebook operasional

Aplikasi Rails ini yang dijalankan. Penjelasan produk, alur tujuh tahap, skema isian, dan batasnya ada di [README akar](../README.md). Cara memakai tiap halaman ada di [PENGGUNAAN.md](../PENGGUNAAN.md).

Rails 7.0.10, Ruby 3.3.2, PostgreSQL. Jawaban bertanda `rules` dan `semantic false`. Model belum dipasang.

```bash
export RBENV_VERSION=3.3.2
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
bundle install
bin/rails db:prepare
bin/rails test
bin/ops
```

Server lokal: http://127.0.0.1:3000

Tombol **Buka contoh produk** membuat notebook, rekaman, dan berkas contoh. Teks yang sama tidak disimpan dua kali. Rencana tidak dihitung sebagai kejadian. Kutipan kehadiran yang saling menolak tampil sebagai bentrok.
