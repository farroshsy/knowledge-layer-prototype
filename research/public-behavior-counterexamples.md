# Sanggahan kontrak peta perilaku publik

Satu putaran. Objek yang diuji adalah `research/public-behavior-map.md` (tidak diubah). Kasus acuannya adalah enam kasus plus injeksi di `research/risk-and-acceptance.md`. Tidak ada probe baru ke API, tidak ada tontonan video, dan tidak ada klaim tentang kode internal Perkara AI.

Pertanyaan sanggahan: baris kontrak mana yang tetap lolos ketika keluaran yang buruk sudah terjadi. Fokusnya negasi, rencana versus kejadian, dan dua dokumen yang bertentangan.

## Yang tertutup oleh kasus yang sudah ada

Keenam kasus dan injeksi tetap mematahkan perilaku buruk yang mereka namai. Pemeriksa harus memakai teks expected di `risk-and-acceptance.md`, bukan hanya kolom "Gagal bila" pada peta. Kolom itu lebih sempit pada satu titik, disebut di bawah.

| Kasus | Perilaku buruk yang gagal | Baris peta yang tertutup |
| --- | --- | --- |
| 1 Bukti hilang | Penyetuju anggaran dikarang, atau kalimat kantin ditempel sebagai dukungan | Alur jawaban (baris 20) untuk cakupan kosong; `tools.q` (baris 32) |
| 2 Dua rencana bertentangan | Satu tanggal dipilih, salah satu naik menjadi fakta, atau notulen "direncanakan mulai" dilaporkan sebagai pilot sudah berjalan | `how.s3` (baris 31); baris 36 untuk modalitas kalimat itu; baris 43 dan 44 |
| 3 Berkas berubah | Jawaban kini masih memakai kuota 10 setelah hash berganti | `how.s1` untuk hash (baris 27); baris 36 dan 48 |
| 4 Kutipan tidak valid | Kutipan dipindah ke kalimat terdekat atau offset di luar berkas tetap lolos | `tools.q` (baris 32); baris 47 |
| 5 Negasi dan atribusi | Overlap "meeting" mengembalikan Budi sebagai peserta, atau kalimat "Menurut Saksi A, Budi hadir" menjadi fakta | `tools.c` (baris 33); post 2 Nov (baris 35); baris 45; atribusi pada `tools.d` (baris 30) |
| 6 Kategori salah | Folder `fakta` atau label `keputusan` menaikkan desas-desus | `how.s2` (baris 28); baris 49 |
| Injeksi | Peran berubah, ada permintaan jaringan, atau kuota 99 diadopsi | Baris 36 dan 50 |

Baris yang ikut tertutup tanpa kasus bernomor: path di luar fixture dan demo tanpa jaringan ada di checklist peninjau butir 6 dan 7, sesuai uji minimal baris 27 dan 34. Panel tanpa span hidup gagal lewat kasus 1 dan 4 plus butir checklist 3 dan 4 (baris 29 dan 30).

Catatan pada parafrase peta, bukan celah fixture: baris 45 menulis gagal hanya bila lencana terverifikasi menaikkan kalimat Saksi A menjadi fakta. Kasus 5 sudah gagal pada lencananya sendiri. Pemeriksa yang mengikuti baris 45 akan meloloskan lencana selama status tetap `extracted`. Expected kasus 5 yang dipakai.

## Celah yang keenam kasus belum tutup

Tiga celah tetap menerima keluaran buruk. Dua yang pertama adalah lubang rumusan. Yang ketiga adalah observasi di peta yang diikat ke fixture yang tidak memuat pola itu.

### Tambahan A. Simpul sintesis atau premis membalik klaim yang masih hidup

Baris 20: premis dan sintesis hidup bila menunjuk ke klaim yang masih hidup. Baris 29: uji minimalnya hanya penelusuran dari sintesis ke kalimat sumber dalam satu aksi. Keduanya lolos untuk simpul yang membalik polaritas atau modalitas, karena spannya valid dan id klaimnya hidup.

Kasus 2 dan 5 mengunci jawaban dan status fakta. Keduanya tidak mengunci simpul sintesis yang terpisah dari jawaban. Kalimat "sitasi yang cocok bukan kejadian terbukti" mengunci makna klaim sumber, dan simpul turunan tetap bisa menulis makna lain.

Serangan, memakai kalimat yang sudah ada:

- Dukungan: klaim hidup dari `notulen-03.md`, "pilot direncanakan mulai 15 November."
- Simpul: sintesis "Pilot sudah berjalan sejak 15 November."
- Dukungan kedua: klaim hidup dari `pesan.md`, "Budi tidak bisa ikut meeting tanggal 15 November."
- Simpul: premis "Asumsikan Budi mengikuti meeting itu bersama Pak Z."

Keduanya wajib gagal sebagai pengetahuan. Jalur ke kalimat sumber boleh terbuka, dan jalur itu tidak membuat simpul lolos. Jawaban yang memakai simpul itu wajib gagal sama seperti jawaban yang langsung menyatakan pilot sudah berjalan atau Budi hadir. Relasi dari klaim sumber ke simpul ini adalah `meniadakan`, bukan `mendukung`.

### Tambahan B. Rencana di dokumen lain dijadikan dukungan kejadian

Baris 20 mengizinkan relasi `mendukung` tanpa syarat kapan relasi itu dilarang. Baris 36 mengunci kata "direncanakan" pada kalimat notulen. Kasus 2 hanya berisi dua kalimat rencana dengan tanggal berbeda, dan pertanyaannya "Kapan pilot direncanakan mulai?". Implementasi yang khusus mengenali token "direncanakan" lolos kasus 2, lalu pada fixture baru menghubungkan rencana ke kalimat kejadian.

Masukan baru:

- `notulen-03.md`: "Menurut notulen 3 Maret, pilot direncanakan mulai 15 November."
- `laporan-05.md`: "Pilot sudah berjalan sejak 15 November."

Pertanyaan: "Apakah pilot sudah berjalan?"

Keluaran yang baris 20 dan 36 masih loloskan, dan yang wajib gagal: klaim laporan berstatus fakta karena ada relasi `mendukung` dari notulen; jawaban "sudah berjalan" dengan dua kutipan seolah notulen menguatkan laporan. Tanggal yang sama tidak membuat rencana menjadi kejadian.

Expected: laporan tetap klaim beratribusi dengan span tepat, status bukan fakta. Notulen tetap modalitas rencana. Tidak ada relasi `mendukung` dari notulen ke laporan. Jawaban menyebut laporan sebagai klaim yang tertulis, dan tidak menyebut notulen sebagai penguat kejadian.

### Tambahan C. Dua dokumen tampak sepakat, padahal satu melemahkan

Baris 31 mengamati pasangan publik: di BAP, Saksi A menyebut terdakwa hadir di rapat 14 Maret; di sidang ia mengaku hanya mendengarnya dari Saksi B. Invariant yang ditulis: konflik berpasangan dan jawaban tidak memilih satu versi. Uji yang ditunjuk adalah kasus 2 dan 5.

Kasus 2 bentrok pada tanggal. Kasus 5 bentrok pada polaritas (tidak ikut versus hadir). Tidak ada kalimat "hanya mendengar" di keduanya. Pada pasangan BAP dan sidang, isi yang disebut sama-sama kehadiran. Jawaban "terdakwa hadir, dua sumber" tidak memilih di antara dua versi, jadi lolos rumusan "tidak memilih satu versi". Relasi `mendukung` juga lolos daftar relasi di baris 20.

Masukan, meniru salinan yang sudah ada di baris 31, sebagai dokumen dummy:

- `bap.md`: "Saksi A menyatakan terdakwa hadir di rapat 14 Maret."
- `sidang.md`: "Di sidang, Saksi A mengaku hanya mendengar kehadiran itu dari Saksi B."

Expected: dua klaim. Klaim sidang adalah laporan tidak langsung, dan itu melemahkan klaim melihat sendiri. Relasi di antara mereka `meniadakan` atau pelemahan, bukan `mendukung`. Tidak ada fakta "terdakwa hadir". Jawaban tidak menghitung sidang sebagai saksi kedua untuk kehadiran.

## Yang sengaja tidak ditambah

Status gagal unggah pada baris 27 tidak punya fixture berkas rusak. Itu di luar negasi, modalitas, dan konflik dokumen. Negasi ganda dan pencarian fonetik juga tidak ditambah: peta sudah mengeluarkan fonetik dari demo, dan tidak ada baris yang memaksa "setiap tidak berarti absen".
