# Diagram notebook operasional

Bagan ini menggambarkan sistem yang berjalan di `ops-notebook`. Kotak kuning adalah batas yang belum dipasang. OCR, model, dan antrian tidak ada di jalur yang sedang berjalan.

## Dari dump sampai tanya

```mermaid
flowchart LR
  dump["1 Dump<br/>arsip masuk"]
  peta["2 Pemetaan<br/>bentuk berkas"]
  proses["3 Proses<br/>jenis isi"]
  analisis["4 Analisis<br/>baris tersimpan"]
  putusan["5 Keputusan<br/>boleh dipakai"]
  verif["6 Verifikasi<br/>kutipan lawan sumber"]
  tanya["7 Tanya<br/>ulang baris atau tolak"]
  dump --> peta --> proses --> analisis --> putusan --> verif --> tanya
```

| Tahap | Dipakai | Masih macet |
|---|---|---|
| Dump | Rails dan PostgreSQL | Tidak ada antrian |
| Pemetaan | Lapisan teks PDF dan XML DOCX | OCR, PPTX, transkrip, urutan kolom |
| Proses | Tiga penilai aturan | Prosa tanpa `Nama: nilai` tidak menjadi isian |
| Analisis | Baris PostgreSQL, skema tertutup | Label di luar skema tidak dibuat |
| Keputusan | Aturan bentrok | Bentrok yang dikenali masih sempit |
| Verifikasi | Cek kutipan | Belum ada peninjau kedua |
| Tanya | Irisan kata, `semantic false` | Beda susunan kalimat bisa tidak ketemu |

## Dua sumber

```mermaid
flowchart TD
  orang["Rekaman diisi orang<br/>pekerjaan dan orang, id stabil"]
  berkas["Berkas diunggah<br/>bagian, jenis, isian, klaim"]
  orang --> pisah["Tidak dicampur"]
  berkas --> pisah
  pisah --> gabung{"Kutipan memuat id publik, utuh"}
  gabung -->|ya| jawaban["Boleh digabung saat ditanya"]
  gabung -->|tidak| sendiri["Masing-masing tetap sendiri"]
  orang --> rencana["Rencana bukan kejadian"]
```

## Bentuk berkas

```mermaid
flowchart TD
  unggah["Berkas diunggah"]
  unggah --> bentuk{"Bentuk"}
  bentuk -->|"txt, md, kecil"| langsung["Langsung dipecah"]
  bentuk -->|"pdf punya lapisan teks"| pdf["Teks per halaman"]
  bentuk -->|"docx punya XML"| docx["Paragraf XML"]
  bentuk -->|"pdf gambar, png, pptx, audio, teks terlalu besar"| tahan["Ditahan<br/>isi tidak disimpan"]
  langsung --> penilai["Penilai aturan"]
  pdf --> penilai
  docx --> penilai
  tahan --> catatan["Alasan tertulis di Pemetaan"]
```

PDF dan DOCX tidak dijadikan gambar. Halaman tanpa lapisan teks tidak di-OCR. Urutan kolom dan tabel belum disusun ulang.

## Tiga penilai

```mermaid
flowchart TD
  bagian["Teks satu bagian"]
  bagian --> kata["Penilai kata"]
  bagian --> isian["Penilai baris isian"]
  bagian --> nama["Nama berkas"]
  kata --> putusan{"Kata dan isian"}
  isian --> putusan
  nama -.->|"dicatat, tidak memutuskan"| putusan
  putusan -->|sepakat| jenis["Jenis itu"]
  putusan -->|"satu suara, yang lain abstain"| jenis
  putusan -->|"selisih atau sama-sama abstain"| other["other"]
```

## Skema isian

```mermaid
flowchart LR
  sop["SOP"] --> langkah["langkah"]
  sop --> pj["penanggung jawab"]
  notulen["Notulen"] --> peserta["peserta"]
  notulen --> keputusan["keputusan"]
  notulen --> tindakan["tindakan"]
  proposal["Proposal"] --> tujuan["tujuan"]
  proposal --> anggaran["anggaran"]
  laporan["Laporan progres"] --> capaian["capaian"]
  laporan --> hambatan["hambatan"]
  lain["other"] --> kosong["tidak ada kolom"]
```

Kolom itu batas yang boleh diambil, bukan daftar yang wajib ada. Isian hanya terbaca dari baris sendiri, misalnya `Peserta: Sari`.

## Bila dokumen tidak mencakup kolom itu

```mermaid
flowchart TD
  dokumen["Dokumen yang diberikan"]
  dokumen --> kenal{"Jenisnya dikenal"}
  kenal -->|"ya, satu kolom tidak tertulis"| tetap["Jenis tetap<br/>kolom kosong tidak dibuat<br/>pertanyaan kolom itu ditolak"]
  kenal -->|"tidak mirip empat jenis"| other["other<br/>kalimat bisa tersimpan sebagai kutipan"]
  dokumen --> baru{"Label belum dikenal"}
  baru -->|"Risiko atau PIC"| tidak["Tidak disalin menjadi peserta, langkah, atau anggaran"]
```

## Tanya

```mermaid
flowchart TD
  tanya["Pertanyaan"]
  tanya --> rekaman{"Ada rekaman yang cocok"}
  rekaman -->|ya| db["Jawab dari rekaman<br/>rencana tetap rencana"]
  rekaman -->|tidak| baris{"Ada baris di bawah judul yang cocok"}
  baris -->|ya| ulang["Ulang baris itu"]
  baris -->|tidak| tolak["Tolak"]
  bentrok["Bentrok tetap terlihat"] --> tanya
```

## Yang berjalan dan yang belum

```mermaid
flowchart LR
  subgraph hari_ini["Berjalan hari ini"]
    rails["Rails"]
    pg["PostgreSQL"]
    aturan["Aturan lokal"]
  end
  subgraph nanti["Belum dipasang"]
    antri["Antrian"]
    ocr["OCR halaman gambar"]
    kolom["Urutan kolom dan tabel"]
    model["Model, maksud tertutup saja"]
  end
  rails --> aturan
  pg --> aturan
  model -.->|"Rails yang menyusun kueri<br/>kutipan gagal berarti ditolak"| aturan
```
