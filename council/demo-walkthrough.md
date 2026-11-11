# Naskah demo, sekitar 3 menit

Untuk pembicara manusia. Satu tab aplikasi. Empat pertanyaan, masing-masing sekali.

Jangan restart. Jangan hentikan PID 57938. Jangan mengikat server baru. Jangan klik `Buat notebook`, `Simpan rekaman`, `Unggah dan proses`, `Muat ulang hasil`, atau `Simpan kategori`. Jangan mengetik pertanyaan lain. Pemilih berkas hanya TXT/MD. Jangan menyebut PDF, DOCX, atau kesiapan produksi.

## GET saat naskah ditulis

GET loopback tidak selesai. Membaca `http://127.0.0.1:8765/api/notebooks` sebagai berkas gagal: path itu tidak ada. Sesi penulis tidak punya klien HTTP. Itu bukan bukti server mati, dan bukan cuplikan layar.

Buka URL sendiri. Jika peramban gagal memuat, ucapkan kegagalan yang terlihat, lalu berhenti. Jangan mengarang dropdown, tabel, panel Hasil, atau jawaban. Angka dasbor juga tidak diambil ulang.

## 0:00–0:25 Alamat dan perintah start

Buka `http://127.0.0.1:8765`.

Ucapkan:

"Aplikasi yang sudah hidup ada di http://127.0.0.1:8765, PID 57938, basis `data/final-demo.sqlite`. Perintah di README kandidat, dari direktori `.parallel-builds/grok-20261110-2222/candidate`, adalah `python3 -m klayer serve --db data/notebook.sqlite --seed fixtures/demo --provider auto`. Di `klayer/__main__.py` port bawaan 8765, provider bawaan `auto`, dan `--seed` kosong kecuali diisi. Demo ini tidak memakai seed itu. Seed README membuat notebook lain. Kita tidak menyalakannya."

Judul yang ada di UI: `Notebook operasional`. Banner: aplikasi lokal; inferensi Grok CLI, bila dipakai, tetap online; `local-rules` bukan ekstraksi semantik.

## 0:25–0:45 Notebook, tanpa unggah

Di `Notebook aktif`, pilih entri yang membuat baris `ID notebook:` persis `16cd89dcda064fe2b6390deb7b91e00d`. Nama saat notebook dibuat tercatat `Demo Grok 10 Nov`. Jika label dropdown berbeda, ikuti ID. Isi daftar tidak diverifikasi GET.

Ucapkan, tanpa mengisi panel Hasil:

"Unggah live `baru-grok-live.txt` sebelumnya timeout Grok pada 75 detik. Job menerbitkan `local-rules` dan menyimpan `provider_error`. Itu fallback leksikal, bukan ekstraksi semantik. Kita tidak mengunggah lagi."

"Setelah restart, `data/final-demo.sqlite` tetap memuat notebook ini dan tiga rekaman. Kita tidak restart di panggung. Jika tabel tidak menampilkan tiga rekaman, katakan apa yang terlihat."

## 0:45–1:10 Status Budiono

Kotak label `Pertanyaan`. Ketik persis `Apa status Budiono?`. Klik `Tanya` sekali. Tunggu `Selesai.`

Ucapkan:

"Checkpoint: rute `db_only`, status `occurred`, hanya Budiono, sekitar 0,006 detik. Lookup bisnis memakai aturan, bukan perencana dokumen."

Bila panel sama, tunjuk `Rute: db_only — rekaman basis data`, `Status jawaban: occurred`, dan kartu Rekaman yang hanya Budiono. Jika Budi ikut, ucapkan layar tidak sesuai pengukuran. Jangan klik `Tanya` lagi.

## 1:10–1:30 Status Budi

Ganti menjadi persis `Apa status Budi?`. Klik `Tanya` sekali.

Ucapkan:

"Checkpoint: `unknown`, hanya Budi, sekitar 0,001 detik. Budi tidak meminjam status `occurred` milik Budiono."

Tunjuk Rekaman bernama Budi, bukan Budiono, dan `Status jawaban: unknown`. Jika yang tampil `occurred` atau nama Budiono, ucapkan isolasi nama gagal di layar ini.

## 1:30–2:15 Kehadiran di dokumen

Ganti menjadi persis `Apakah Budi hadir?`. Klik `Tanya` sekali. Kata `hadir` membuat ini pertanyaan dokumen. Provider yang hidup adalah `auto`, jadi klik ini boleh memanggil perencana Grok yang online. Tunggu `Selesai.` Jangan klik dua kali.

Ucapkan:

"Yang terukur: rute `document_only`, jawaban `negated`. Kutipannya: Menurut Saksi A, Budi tidak hadir di rapat 14 Maret. Kalimat itu dinegasi. Bukan bukti Budi hadir, dan bukan status rekaman basis data."

Bila panel sama, tunjuk `Rute: document_only — klaim dokumen yang dipilih, bukan rekaman basis data`, `Status jawaban: negated`, dan kutipan itu pada Klaim atau JSON. Jika rute atau kutipan berbeda, bacakan yang tampil. Jangan ganti pertanyaan.

## 2:15–2:45 Harga saham

Ketik persis `Berapa harga saham kemarin?`. Klik `Tanya` sekali. Checkpoint: abstain, sekitar 20 detik, karena perencana dokumen benar-benar dipanggil. Tunggu. Jangan klik lagi.

Ucapkan:

"Tidak ada harga. Rute yang tercatat `unsupported`, jawaban `abstain`. Jika panel menulis angka saham, jangan dibaca sebagai fakta."

Label UI untuk rute itu: `unsupported — pertanyaan tidak didukung, sistem abstain`.

## 2:45–3:00 Batas

Ucapkan:

"Macro 9/9 di `.parallel-builds/grok-20261110-2222/macro-rules/results.json` adalah provider `rules`: tiga skenario, masing-masing `db_only`, `combined`, dan `isolation`, semuanya lulus. Itu bukan mutu model. Laporan yang sama menulis `business_value` `not_measured`. Restart yang sudah diukur tetap menyimpan notebook `16cd89dcda064fe2b6390deb7b91e00d`. Dasbor `http://127.0.0.1:8766` hanya status baca. Saat checkpoint, 0 panggilan aktif. GET dasbor tidak diulang, jadi jangan mengarang angkanya. Bukan PDF, bukan DOCX, bukan siap produksi."

Berhenti.
