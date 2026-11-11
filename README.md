# Notebook operasional

Produk yang dijalankan ada di `ops-notebook`: Rails 7.0.10, Ruby 3.3.2, PostgreSQL. Ekstraksi berlabel `rules` dan `semantic` false.

```bash
cd ops-notebook
export RBENV_VERSION=3.3.2
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
bin/rails db:prepare
bin/ops
```

Buka http://127.0.0.1:3000 dan pilih **Buka contoh produk**.

`klayer/`, `automation/`, dan `data/*.sqlite` adalah sisa jalur Python. Jangan dijadikan aplikasi. Catatan riset di `research/` dan `council/` tetap arsip, bukan cara menjalankan produk.
