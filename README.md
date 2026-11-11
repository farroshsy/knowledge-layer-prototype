# Notebook operasional

Prototipe lokal untuk gudang pengetahuan dokumen internal atau dokumen klien. Berkas yang belum terstruktur menjadi baris yang bisa ditanya. Jawaban hanya mengulang baris yang sudah tersimpan. Kalau barisnya tidak ada, atau para penilai tidak sepakat, sistem menolak menjawab.

Ini bukan produk sidang, dan belum produksi. Model bahasa belum dipasang. Jawaban bertanda `rules` dan `semantic false`. Aplikasi yang dijalankan hanya `ops-notebook`: Rails 7.0.10, Ruby 3.3.2, PostgreSQL. Docker Compose belum ada.

Engineer lain mulai dari urutan di bawah ini. Jangan mulai dari `klayer/`, `research/`, atau `council/`.

## Bacaan sebelum mencoba

Kerjakan dari atas ke bawah. Satu baris selesai sebelum pindah ke baris berikutnya.

| Urutan | Yang dibaca atau dikerjakan | Selesai bila |
|---|---|---|
| 1 | README ini, sampai akhir bagian "Coba sendiri" | Server hidup di http://127.0.0.1:3000 dan tombol **Buka contoh produk** sudah dibuka |
| 2 | [PENGGUNAAN.md](PENGGUNAAN.md), setelah server hidup | Tujuh halaman sudah dibuka sekali: Dump, Pemetaan, Proses, Analisis, Keputusan, Verifikasi, Tanya |
| 3 | Empat berkas di `fixtures/demo/`, dalam urutan bagian "Unggah empat berkas ini" | Setiap berkas sudah diunggah ke notebook kosong dan hasilnya cocok dengan tabel |
| 4 | Bagian "Penjelasan perilaku" di README ini | Jenis, kolom, nama berkas, dan batas macet sudah dipahami sebelum kode diubah |
| 5 | Kode, hanya setelah empat langkah di atas | Pintu masuk yang dibaca: `ops-notebook/app/services/evidence.rb`, lalu `evidence/lexicon.rb`, `evidence/ingest.rb`, `evidence/query.rb` |

`CTO.md` dan `EMAIL-CTO.md` adalah naskah pertemuan. Baca hanya bila perlu menjelaskan produk kepada orang lain. Keduanya tidak diperlukan untuk menjalankan atau mengubah kode.

Bukan bacaan pertama:

| Berkas atau folder | Alasan |
|---|---|
| `klayer/`, `automation/`, `tests/test_flow.py`, `data/*.sqlite` | Jalur Python yang sudah ditinggalkan. Port 8765 bukan produk ini. |
| `research/`, `council/`, `DELIVERY.md`, `BRAINSTORMING-HANDOFF.md`, `BRAINSTORMING-UPDATE-2026-11-10.md` | Arsip pembahasan. Sebagian masih menyebut Python, port 8765, atau keputusan yang sudah diganti Rails. |
| `fixtures/heldout/` | Berkas uji lama. Tidak dimuat oleh tombol contoh dan tidak dijalankan oleh `bin/rails test`. |
| `tmp/`, `output/` | Hasil sampingan, termasuk gambar halaman. Bukan cara mencoba produk. |
| `ops-notebook/config/master.key` | Tidak ada di git. Development tidak membutuhkan kunci itu untuk berjalan. Jangan dibuat atau disalin ke repo. |

## Yang harus terpasang

Cek ini sebelum `bundle install`.

```bash
RBENV_VERSION=3.3.2 ruby -v
```

Hasilnya harus `ruby 3.3.2`. Ruby bawaan sistem tidak dipakai. Jangan mengganti Ruby global.

```bash
psql -d postgres -c 'SELECT version();'
```

PostgreSQL harus menerima koneksi pengguna sistem lewat soket lokal. `bin/rails db:prepare` membuat basis data `ops_notebook_development`. Uji membuat `ops_notebook_test`. Jangan memakai konfigurasi production di `ops-notebook/config/database.yml`.

Di macOS, gem `pg` perlu alat kompilasi. `bin/ops` mengisi `SDKROOT` sendiri. Untuk `bundle install`, isi variabel yang sama seperti perintah di bawah.

## Jalankan

Dari akar repositori:

```bash
cd ops-notebook
export RBENV_VERSION=3.3.2
export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
bundle install
bin/rails db:prepare
bin/ops
```

Berhasil bila peramban di http://127.0.0.1:3000 menampilkan judul **Notebook operasional**. Server hanya mendengarkan `127.0.0.1`, port 3000. Port lain: `PORT=3001 bin/ops`. Berhenti dengan Ctrl+C.

Kalau port 3000 sudah terpakai, hentikan proses lama itu atau pakai port lain. Jangan menjalankan `klayer`.

Uji, dari folder `ops-notebook`, dengan dua variabel lingkungan yang sama:

```bash
bin/rails test
```

Jalankan uji ini setelah percobaan di bawah, atau sebelum mengubah kode. Hasil terakhir pada cabang ini: 27 run, 189 assertion, 0 gagal.

## Coba sendiri

### 1. Contoh produk

1. Klik **Buka contoh produk**. Ruang yang muncul bernama "Operasional contoh". Isinya dummy: orang, pekerjaan, satu berkas `rapat-contoh.txt`, dan empat berkas dari `fixtures/demo/`.
2. Buka **Proses**. Di halaman itu ada **Peta alur** dan **Skema isian**. Peta itu yang menjelaskan apa yang dipakai, apa yang macet, dan apa yang belum dipasang.
3. Buka **Tanya** dan tekan tiga pertanyaan yang sudah tersedia:
   - "Apa status pilot?" membaca rekaman bisnis. Statusnya rencana.
   - "Apakah pilot sudah berjalan?" tetap rencana, bukan kejadian.
   - "Apakah Budi hadir?" menampilkan bentrok, karena ada kutipan yang saling menolak.
4. Ketik "Siapa peserta notulen?". Jawaban mengulang baris `Peserta:` di bawah judul bagian. Contoh ini memuat lebih dari satu notulen, jadi bisa ada lebih dari satu baris.
5. Ketik "Berapa anggaran proposal?". Tidak ada baris `Anggaran:`, jadi jawabannya ditolak.

Rekaman pekerjaan dan orang ada di bagian yang bisa dibuka pada halaman **Dump**. Kalimat di berkas tidak mengubah status mereka.

### 2. Unggah empat berkas ini

Buat notebook kosong: isi nama ruang, klik **Buat notebook**. Lalu unggah berkas berikut satu per satu, dari halaman **Dump**. Urutannya memang ini, karena tiap berkas menambah satu perilaku.

| Urutan | Berkas | Yang harus terlihat |
|---|---|---|
| 1 | `fixtures/demo/sop-dapur.md` | Jenis SOP. Baris `Langkah` dan `Penanggung jawab`. Ini jalur yang bersih. |
| 2 | `fixtures/demo/notulen-maret.md` | Jenis notulen. Baris `Peserta`, `Keputusan`, dan `Tindakan`. |
| 3 | `fixtures/demo/email-dana.md` | Ada baris `Keputusan:` tentang pilot pada tanggal lain. Di **Keputusan**, tanggal pilot yang berbeda tetap terlihat sebagai bentrok. |
| 4 | `fixtures/demo/catatan-bebas.md` | Jenis `other`. Tidak ada kolom peserta, langkah, atau anggaran. Kalimatnya tetap tersimpan sebagai kutipan. |

Nama berkas yang diunggah harus label, misalnya `sop-dapur.md`. Jangan menempel jalur folder ke kolom nama.

Setelah empat berkas itu, coba dua batas ini pada notebook yang sama.

Teks campur, tempel sebagai `sop-palsu.txt`:

```text
Notulen rapat peserta keputusan.
Langkah: Cuci bahan.
```

Kata menunjuk ke notulen, baris `Langkah:` menunjuk ke SOP. Keduanya berselisih, jadi jenisnya `other` dan alasannya memuat `konsensus gagal`. Lihat di **Analisis**.

Satu berkas `.pdf` apa saja. Ia tidak dibaca. Di **Pemetaan** statusnya ditahan, dengan alasan lapisan teks dan OCR belum dijalankan.

### 3. Baru baca penjelasan di bawah

Bagian "Penjelasan perilaku" menjelaskan kenapa hasil di atas seperti itu. Baca bagian itu sebelum mengubah `lexicon.rb` atau skema kolom.

## Penjelasan perilaku

### Dua sumber

Rekaman bisnis diisi orang: pekerjaan dan orang. Masing-masing punya id stabil. Rencana tidak dihitung sebagai kejadian. Dua nama yang sama tetap dua rekaman.

Berkas diunggah terpisah. Sistem memecahnya, menebak jenisnya, lalu menyimpan isian dan klaim. Kalimat di berkas tidak mengubah status rekaman. Gabungan rekaman dan berkas hanya terjadi bila kutipan memuat id publik rekaman itu, utuh, sebagai token sendiri. Orang yang menerima atau menolak klaim. Klaim yang ditolak tidak dipakai untuk menjawab.

### Tujuh tahap

Pita alur ada di setiap halaman. Peta lengkap ada di **Proses**.

| Tahap | Yang dikerjakan | Yang dipakai |
|---|---|---|
| Dump | Berkas masuk sebagai arsip. Rekaman diisi terpisah. | Rails dan PostgreSQL |
| Pemetaan | Teks polos kecil dilanjutkan. Bentuk lain ditahan beserta alasannya. | Aturan ekstensi berkas |
| Proses | Jenis isi ditimbang. Nama berkas hanya penanda. | Tiga penilai aturan |
| Analisis | Bagian menyimpan jenis dan baris yang tertulis. | Baris PostgreSQL, skema tertutup |
| Keputusan | Rencana bukan kejadian. Bentrok tetap terlihat. Klaim yang ditolak tidak dipakai. | Aturan bentrok dan modalitas |
| Verifikasi | Kutipan dicek masih ada di teks sumber. Orang yang memutuskan. | Cek kutipan |
| Tanya | Pertanyaan mengulang baris yang ketemu, atau menolak. | Irisan kata pada judul, isian, dan klaim |

Tiga penilai tidak saling melihat.

- Kata di dalam teks. Tidak ada kata, atau dua jenis sama kuat, berarti abstain.
- Baris isian seperti `Peserta:` atau `Langkah:`. Lebih dari satu jenis, atau tidak ada baris, berarti abstain.
- Nama berkas. Ia dicatat. Ia diabaikan bila menjadi satu-satunya suara, atau bila bertentangan dengan isi.

Kalau kata dan isian sepakat, jenis itu yang dipakai. Kalau hanya satu yang bersuara, suara itu yang dipakai. Kalau keduanya berselisih atau sama-sama abstain, jenisnya `other`. Berkas `sop-dapur.md` yang isinya notulen tetap notulen. Alasannya mencatat `nama=sop, diabaikan`.

### Skema isian

Kolom ini batas yang boleh diambil, bukan daftar yang wajib ada di setiap berkas. Isian hanya terbaca dari baris sendiri, misalnya `Peserta: Sari`.

| Jenis | Kolom |
|---|---|
| SOP | langkah, penanggung jawab |
| Notulen | peserta, keputusan, tindakan |
| Proposal | tujuan, anggaran |
| Laporan progres | capaian, hambatan |
| Lainnya (`other`) | tidak ada |

Jika dokumen yang diberikan tidak mencakup struktur itu:

1. Jenisnya dikenal, tetapi satu kolom tidak tertulis. Berkas tetap masuk. Kolom kosong tidak dibuat. Pertanyaan tentang kolom itu ditolak.
2. Isinya tidak mirip empat jenis di atas. Jenisnya `other`. Kalimat tetap bisa tersimpan sebagai kutipan.
3. Labelnya belum dikenal, misalnya `Risiko:` atau `PIC:`. Label itu tidak disalin menjadi peserta, langkah, atau anggaran.

### Yang bekerja, dan yang masih macet

Yang berjalan: Rails di dalam satu aplikasi, PostgreSQL untuk rekaman dan baris turunan, aturan lokal untuk jenis, bentrok, kutipan, dan pencarian.

Yang masih macet:

- Tidak ada antrian. Pemrosesan selesai di dalam permintaan yang sama.
- Pemetaan adalah macet terbesar. PDF, gambar, dokumen kantor, rekaman, dan teks di atas 200.000 karakter ditahan. Lapisan teks, OCR, XML, transkrip, dan pemotongan belum dijalankan.
- Prosa yang tidak berbentuk `Nama: nilai` tidak menjadi isian.
- Bentrok yang dikenali masih sempit: tanggal pilot yang berbeda, dan kehadiran yang saling menolak.
- Tanya memakai irisan kata, bukan makna. Chat tidak menyusun kalimat.
- Belum ada akun.

Perbaikan yang tertulis di peta, dan belum berjalan: antrian setelah data tersimpan, lapisan teks PDF dengan OCR hanya untuk halaman gambar, pemotongan berkas besar, penanda nama berkas yang lemah bila isi abstain, lalu model. Model seperti Gemini, kalau dipasang, hanya mengembalikan maksud tertutup. Rails yang menyusun kueri. Model tidak menulis SQL. Jawaban yang tidak menempel pada kutipan ditolak.

## Kode yang disentuh bila perilaku diubah

| Perilaku | Berkas |
|---|---|
| Unggah, hash isi, bagian, jenis, isian | `ops-notebook/app/services/evidence/ingest.rb` |
| Penilai, kolom, jalur PDF dan OCR | `ops-notebook/app/services/evidence/lexicon.rb` |
| Pertanyaan, bentrok, gabungan id | `ops-notebook/app/services/evidence/query.rb` |
| Halaman | `ops-notebook/app/views/workbench/` |
| Uji alur yang harus tetap hijau | `ops-notebook/test/integration/evidence_flow_test.rb` |

Setelah mengubah perilaku, jalankan `bin/rails test` dari `ops-notebook`.
