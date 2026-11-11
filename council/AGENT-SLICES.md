# Peta irisan agen

Integrator tunggal menggabungkan. Agent lain hanya menulis irisan di bawah.

Produk adalah `ops-notebook` (Rails 7, Ruby 3.3.2, PostgreSQL). Jangan lanjutkan kandidat Python. Jangan sentuh sibling `ai-interview-platform`. Jangan push.

## Irisan paralel

Berkas terpisah, boleh dikerjakan bersamaan. Satu agent per irisan. Jangan dua agent mengedit berkas yang sama.

1. `app/views/workbench` dan `app/assets/stylesheets/application.css`
2. `app/services/evidence.rb` bersama `app/services/evidence/` — leksikon, ingest, pertanyaan, keputusan
3. `app/services/sample_workspace.rb`
4. `app/controllers/workbench_controller.rb` dan `config/routes.rb` — satu penulis untuk keduanya
5. `test/integration`
6. `test/models`
7. `db/migrate` — satu migrasi baru per agent, nama berbeda

## Batas

- Jangan mengubah ambang jawaban supaya tes menjadi hijau.
- `semantic` tetap `false` untuk aturan leksikal.
- Jangan menambah fitur di luar irisan.
- Jangan mengubah `council/CHECKPOINT.md`.

## Selesai

`bin/rails test` lulus dari direktori `ops-notebook` dengan `RBENV_VERSION=3.3.2` dan `SDKROOT` macOS.
