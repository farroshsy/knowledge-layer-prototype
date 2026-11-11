# Notebook operasional

Prototipe lokal untuk gudang pengetahuan dokumen internal atau dokumen klien. Berkas yang belum terstruktur menjadi baris yang bisa ditanya. Jawaban hanya mengulang baris yang sudah tersimpan. Kalau barisnya tidak ada, atau para penilai tidak sepakat, sistem menolak menjawab.

Ini bukan produk sidang, dan belum produksi. Model bahasa belum dipasang. Jawaban bertanda `rules` dan `semantic false`.

Produk yang dijalankan ada di `ops-notebook`: Rails 7.0.10, Ruby 3.3.2, PostgreSQL. Docker Compose belum disediakan.

## Dua sumber yang tidak dicampur

Rekaman bisnis diisi orang: pekerjaan dan orang. Masing-masing punya id stabil. Rencana tidak dihitung sebagai kejadian. Dua nama yang sama tetap dua rekaman.

Berkas diunggah terpisah. Sistem memecahnya, menebak jenisnya, lalu menyimpan isian dan klaim. Kalimat di dalam berkas tidak mengubah status rekaman. Gabungan rekaman dan berkas hanya terjadi bila kutipan memuat id publik rekaman itu, utuh, sebagai token sendiri.

Orang yang menerima atau menolak klaim. Klaim yang ditolak tidak dipakai untuk menjawab.

## Cara menjalankan

PostgreSQL harus bisa diakses pengguna sistem. Ruby yang dipakai 3.3.2. Dari akar repositori:

```bash
cd ops-notebook
export RBENV_VERSION=3.3.2
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
bundle install
bin/rails db:prepare
bin/ops
```

Buka http://127.0.0.1:3000 dan pilih **Buka contoh produk**. Server hanya mendengarkan `127.0.0.1`, port 3000. `bin/ops` sudah mengisi kedua variabel lingkungan itu. Uji otomatis, dari folder yang sama: `bin/rails test`.

Langkah memakai tiap halaman ada di [PENGGUNAAN.md](PENGGUNAAN.md). Naskah singkat untuk penjelasan lisan ada di [CTO.md](CTO.md).

## Alur dari dump sampai tanya

Tujuh halaman adalah tujuh tahap. Di aplikasi, pita alur ada di setiap halaman. Peta lengkap, termasuk yang dipakai, yang macet, dan perbaikan berikutnya, ada di halaman **Proses**.

| Tahap | Yang dikerjakan | Yang dipakai |
|---|---|---|
| Dump | Berkas masuk sebagai arsip. Rekaman pekerjaan dan orang diisi terpisah. | Rails dan PostgreSQL |
| Pemetaan | Teks polos kecil dilanjutkan. Bentuk lain ditahan beserta alasannya. | Aturan ekstensi berkas |
| Proses | Jenis isi ditimbang. Nama berkas hanya penanda. | Tiga penilai aturan |
| Analisis | Bagian menyimpan jenis dan baris isian yang tertulis. | Baris PostgreSQL, skema tertutup |
| Keputusan | Rencana bukan kejadian. Bentrok tetap terlihat. Klaim yang ditolak tidak dipakai. | Aturan bentrok dan modalitas |
| Verifikasi | Kutipan dicek masih ada di teks sumber. Orang yang memutuskan. | Cek kutipan |
| Tanya | Pertanyaan mengulang baris yang ketemu, atau menolak. | Irisan kata pada judul, isian, dan klaim |

Tiga penilai di tahap Proses tidak saling melihat.

- Kata di dalam teks. Tidak ada kata, atau dua jenis sama kuat, berarti abstain.
- Baris isian seperti `Peserta:` atau `Langkah:`. Lebih dari satu jenis, atau tidak ada baris, berarti abstain.
- Nama berkas. Ia dicatat. Ia diabaikan bila menjadi satu-satunya suara, atau bila bertentangan dengan isi.

Kalau kata dan isian sepakat, jenis itu yang dipakai. Kalau hanya satu yang bersuara dan yang lain abstain, suara itu yang dipakai. Kalau keduanya berselisih atau sama-sama abstain, jenisnya `other`.

Contoh yang bisa dicoba setelah **Buka contoh produk**:

- "Apa status pilot?" membaca rekaman bisnis.
- "Apakah pilot sudah berjalan?" tetap rencana, bukan kejadian.
- "Apakah Budi hadir?" menampilkan bentrok bila kutipan kehadiran saling menolak.
- "Siapa peserta notulen?" mengulang baris `Peserta:` di bawah judul bagian.
- "Berapa anggaran proposal?" ditolak bila baris anggaran tidak ada.

## Skema isian

Kolom di bawah ini adalah kolom yang prototipe ini tahu cara menyimpan. Kolom itu batas yang boleh diambil, bukan daftar yang wajib ada di setiap berkas. Isian hanya terbaca dari baris sendiri, misalnya `Peserta: Sari`.

| Jenis | Kolom |
|---|---|
| SOP | langkah, penanggung jawab |
| Notulen | peserta, keputusan, tindakan |
| Proposal | tujuan, anggaran |
| Laporan progres | capaian, hambatan |
| Lainnya (`other`) | tidak ada |

Jika dokumen yang diberikan tidak mencakup struktur itu, ada tiga jalan.

1. Jenisnya dikenal, tetapi satu kolom tidak tertulis. Berkas tetap masuk. Kolom kosong tidak dibuat. Pertanyaan tentang kolom itu ditolak.
2. Isinya tidak mirip empat jenis di atas. Jenisnya `other`. Tidak ada kolom peserta, langkah, atau anggaran. Kalimat tetap bisa tersimpan sebagai klaim, yaitu kutipan apa adanya.
3. Labelnya belum dikenal, misalnya `Risiko:` atau `PIC:`. Label itu tidak disalin menjadi peserta, langkah, atau anggaran. Kolom baru hanya ada bila ditambahkan ke skema.

## Yang membuatnya bekerja, dan yang masih macet

Yang berjalan hari ini:

- Rails menerima unggahan, menyimpan, dan menjawab di dalam satu aplikasi.
- PostgreSQL menyimpan rekaman, berkas, bagian, jenis, isian, dan klaim.
- Aturan lokal menimbang jenis, menandai bentrok, mengecek kutipan, dan mencari baris.

Yang masih macet:

- Tidak ada antrian. Pemrosesan selesai di dalam permintaan yang sama.
- Pemetaan adalah macet terbesar. PDF, gambar, dokumen kantor, rekaman, dan teks di atas 200.000 karakter ditahan. Lapisan teks, OCR, pembacaan XML, transkrip, dan pemotongan belum dijalankan. Isi berkas yang ditahan tidak disimpan.
- Prosa yang tidak berbentuk `Nama: nilai` tidak menjadi isian.
- Bentrok yang dikenali masih sempit: tanggal pilot yang berbeda, dan kehadiran yang saling menolak.
- Tanya memakai irisan kata, bukan makna. Beda susunan kalimat bisa tidak ketemu. Chat tidak menyusun kalimat.
- Belum ada akun.

Perbaikan yang sudah direncanakan, dan belum berjalan:

1. Antrian setelah data tersimpan.
2. PDF yang punya lapisan teks dibaca beserta urutan bacanya. OCR hanya untuk halaman yang berupa gambar.
3. Berkas besar dipotong per halaman sebelum penilai.
4. Bila isi abstain dan nama berkas konsisten, nama boleh menjadi penanda lemah, tetap terlihat, tetap bisa dikoreksi.
5. Model seperti Gemini, kalau dipasang, hanya mengembalikan maksud tertutup, misalnya jenis dan nama kolom. Rails yang menyusun kueri. Model tidak menulis SQL.
6. Jawaban model tetap harus lolos cek kutipan. Kalau gagal, sistem menolak.

## Yang bukan produk ini

`klayer/`, `automation/`, dan `data/*.sqlite` adalah sisa jalur Python. Jangan dijalankan. Catatan di `research/` dan `council/` adalah arsip, bukan cara memakai produk. Kunci kredensial tidak ikut di repositori.

Uji `bin/rails test` yang terakhir dijalankan pada cabang ini: 27 run, 189 assertion, 0 gagal.
