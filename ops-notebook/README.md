# Notebook operasional

Rails 7.0.10 dan PostgreSQL. Ruby yang dipakai adalah 3.3.2.

```bash
export RBENV_VERSION=3.3.2
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
bin/rails db:prepare
bin/rails test
bin/ops
```

Server lokal: http://127.0.0.1:3000

Tombol **Buka contoh produk** membuat notebook, rekaman, dokumen contoh, dan berkas di `fixtures/demo`. Teks yang sama tidak disimpan dua kali. Dua rencana pilot pada tanggal berbeda, atau kehadiran yang saling menolak untuk nama yang sama, tampil sebagai bentrok.
