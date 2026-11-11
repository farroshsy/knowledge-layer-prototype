# Cara memakai notebook operasional

Produk ada di folder `ops-notebook`. Ini Rails 7.0.10, Ruby 3.3.2, dan PostgreSQL. Server hanya mendengarkan `127.0.0.1:3000`.

Docker Compose belum disediakan. Jalur yang dicek adalah perintah di bawah ini, pada mesin yang sudah punya Ruby 3.3.2 dan PostgreSQL. Jangan menjalankan `klayer/` atau port 8765. Itu sisa jalur lama.

## Yang perlu terpasang

- Ruby 3.3.2. Di mesin ini dipakai lewat rbenv. Versi Ruby bawaan sistem tidak punya Rails.
- PostgreSQL yang bisa diakses pengguna sistem lewat soket lokal. Nama basis data dibuat otomatis: `ops_notebook_development`.
- Alat kompilasi macOS, karena gem `pg` perlu dikompilasi.

## Menjalankan

Dari akar repositori:

```bash
cd ops-notebook
export RBENV_VERSION=3.3.2
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
bundle install
bin/rails db:prepare
bin/ops
```

Lalu buka http://127.0.0.1:3000.

`bin/ops` sudah mengisi `RBENV_VERSION` dan `SDKROOT`, lalu menjalankan Puma di port 3000. Untuk port lain:

```bash
PORT=3001 bin/ops
```

Menghentikan server: tekan Ctrl+C di terminal yang menjalankan `bin/ops`.

Uji otomatis, dari folder `ops-notebook`, dengan dua variabel lingkungan yang sama:

```bash
bin/rails test
```

## Memakai produk

1. Di beranda, klik **Buka contoh produk**. Tombol ini membuat satu notebook bernama "Operasional contoh", beberapa rekaman pekerjaan dan orang, serta berkas teks contoh. Data itu dummy.
2. Lewati tujuh halaman dari kiri ke kanan: **Dump**, **Pemetaan**, **Proses**, **Analisis**, **Keputusan**, **Verifikasi**, **Tanya**.
3. Di **Tanya**, tiga pertanyaan siap pakai:
   - "Apa status pilot?" membaca rekaman bisnis. Status rencana tidak dihitung sebagai kejadian.
   - "Apakah pilot sudah berjalan?" tetap rencana, bukan kejadian.
   - "Apakah Budi hadir?" menampilkan bentrok, karena ada kutipan yang saling menolak.
4. Ketik juga "Siapa peserta notulen?". Jawaban mengulang baris `Peserta:` di bawah judul bagian, bukan kalimat yang disusun model.
5. "Berapa anggaran proposal?" ditolak bila baris anggaran tidak ada.

Notebook kosong, tanpa contoh: isi nama ruang, lalu klik **Buat notebook**.

## Menambah berkas sendiri

Di halaman **Dump**, seret berkas atau tempel teks lalu klik **Unggah berkas**.

- `.txt`, `.md`, dan `.markdown` yang kecil langsung dipecah menjadi bagian, jenis, isian, dan klaim.
- Nama berkas harus label, misalnya `notulen-maret.md`. Jangan jalur seperti `folder/berkas.md`.
- Teks yang sama tidak disimpan dua kali.
- PDF, gambar, DOCX, PPTX, audio, video, dan teks di atas 200.000 karakter muncul di **Pemetaan** dengan status ditahan. Isinya tidak dibaca. OCR, lapisan teks, dan transkrip belum dijalankan.
- Koreksi jenis ada di **Analisis**. Pilih jenis bagian, atau klik **Proses ulang**. Koreksi orang tidak ditimpa proses ulang.
- Menerima atau menolak klaim ada di **Verifikasi**. Klaim yang ditolak tidak dipakai untuk menjawab.

Rekaman pekerjaan dan orang diisi terpisah dari berkas. Kalimat di dalam berkas tidak mengubah status mereka. Gabungan rekaman dan berkas hanya terjadi bila kutipan memuat id publik rekaman itu, utuh, sebagai token sendiri.

## Skema isian

Halaman **Proses** menampilkan bagan ini. Empat jenis punya kolom tetap:

- SOP: langkah, penanggung jawab.
- Notulen: peserta, keputusan, tindakan.
- Proposal: tujuan, anggaran.
- Laporan progres: capaian, hambatan.

Kolom itu batas yang boleh diambil, bukan daftar yang wajib ada. Isian hanya terbaca dari baris sendiri, misalnya `Peserta: Sari`.

Jika berkas tidak mencakup struktur itu:

1. Jenisnya dikenal, tetapi satu kolom tidak tertulis. Berkas tetap masuk. Kolom kosong tidak dibuat. Pertanyaan tentang kolom itu ditolak.
2. Isinya tidak mirip empat jenis di atas. Jenisnya `other`. Tidak ada kolom peserta, langkah, atau anggaran. Kalimat tetap bisa tersimpan sebagai klaim.
3. Labelnya belum dikenal, misalnya `Risiko:` atau `PIC:`. Label itu tidak disalin ke kolom yang sudah ada.

## Yang tidak boleh diharapkan

Belum ada akun, antrian latar, atau model. Jawaban bertanda `rules` dan `semantic false`. Ini prototipe lokal, bukan produksi.
