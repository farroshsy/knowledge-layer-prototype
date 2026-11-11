# Peta perilaku publik ke kontrak backend

Diamati 2026-11-10. Reverse engineering di sini berarti perilaku yang tampil di sumber publik, lalu kontrak untuk prototipe kita. Bukan akses backend Perkara AI dan bukan klaim tentang kode yang tidak terlihat.

Sumber yang dibaca pada giliran ini:

- HTML `https://perkara.ai/` dan bundel publik `https://perkara.ai/assets/index-DlM17x7b.js`. Rute `#fitur` tidak memuat HTML terpisah. Salinan fitur ada di bundel yang sama. Halaman tidak dirender di browser, dan video tidak diputar.
- Teks post [2 Nov 2026](https://nitter.cf/ibamarief/status/2117104412824944848), lewat mirror. Video kutipan 31 Okt 2026 tidak ditonton di giliran ini.

Label:

- **Observasi**: kalimat atau label yang ada di sumber itu.
- **Inferensi**: bacaan yang tidak ditulis sumber.
- **Kontrak**: aturan prototipe lokal. Bukan perilaku internal Perkara AI.

Footer bundel: contoh di halaman memakai data rekaan. Angka volume, latensi, dan model di post lain tidak dipakai di peta ini.

## Alur yang dikontrak

Draf yang disanggah, jangan dipakai. Nomor baris di `research/public-behavior-counterexamples.md` menunjuk kalimat ini:

> Relasi menghubungkan klaim yang mendukung, meniadakan, atau hanya berdampingan. Premis dan sintesis hanya hidup jika menunjuk ke klaim yang masih hidup.

Kalimat itu lolos tambahan A, B, dan C. Kontrak yang berlaku:

Unggah menyimpan berkas. Struktur menyimpan lokasi. Pernyataan menyimpan klaim beratribusi beserta polaritas dan modalitas. Relasi yang diizinkan hanya `mendukung`, `meniadakan`, atau berdampingan, dengan tiga larangan di bawah. Premis dan sintesis hanya hidup jika menunjuk ke klaim yang masih hidup dan tidak membalik polaritas atau modalitas klaim itu. Jawaban hanya boleh memakai simpul yang lolos pemeriksaan kutipan dan tidak membalik makna sumber. Sitasi yang cocok di lokasi tidak membuat makna klaim menjadi kejadian yang terbukti.

- Simpul turunan tidak boleh membalik klaim hidup. "pilot direncanakan mulai 15 November" tidak mendukung sintesis "Pilot sudah berjalan sejak 15 November". "Budi tidak bisa ikut meeting" tidak mendukung premis bahwa Budi mengikuti meeting itu. Relasinya `meniadakan`. Jawaban yang memakai simpul terbalik gagal sama seperti jawaban langsung yang salah.
- Rencana di dokumen lain tidak `mendukung` kejadian, termasuk bila tanggalnya sama. Notulen "pilot direncanakan mulai 15 November" dan laporan "Pilot sudah berjalan sejak 15 November" tetap dua klaim. Laporan bukan fakta karena ada notulen. Jawaban tidak menyebut notulen sebagai penguat kejadian.
- Kesaksian tidak langsung bukan saksi kedua. "Saksi A menyatakan terdakwa hadir" dan "Saksi A mengaku hanya mendengar kehadiran itu dari Saksi B" bukan dua sumber yang sepakat. Relasinya `meniadakan` atau pelemahan. Tidak ada fakta "terdakwa hadir". Jawaban "terdakwa hadir, dua sumber" gagal.

## Perilaku yang terlihat

| Sumber | Perilaku terlihat | Data masuk dan keluar | Invariant backend | Status | Uji demo minimal |
| --- | --- | --- | --- | --- | --- |
| `#fitur`, `how.s1` | Unggah PDF pindaian atau rekaman. Contoh menampilkan status memindai dan mentranskrip, lalu jumlah halaman atau durasi. | Masukan berkas. Keluaran status dan identitas berkas. | Berkas asli immutable, hash stabil, status gagal eksplisit. Demo menerima teks sintetis `.txt` dan `.md`, termasuk unggahan yang tidak dikenal saat bangun. Nama berkas tidak memilih kategori atau kutipan. Nama berkas yang menyisipkan direktori ditolak. Rekaman tidak diimplementasikan. | Observasi untuk unggah dan status. Kontrak untuk hash dan pengecualian rekaman. Batas "hanya direktori fixture" pada draf peta ini tidak berlaku: fixture adalah uji, bukan satu-satunya jalur. | Unggah teks baru. Nama berkas tidak menentukan kategori. |
| `#fitur`, `how.s2` | Sistem menebak jenis dokumen dan pembicara. Manusia mengoreksi dengan satu klik sebelum status siap dianalisis. Contoh jenis: BAP Saksi A, Surat Dakwaan, rentang halaman. | Masukan tebakan jenis. Keluaran jenis yang dikonfirmasi manusia, terpisah dari teks. | Jenis adalah taksonomi. Mengoreksi jenis tidak mengubah teks, polaritas, atau status fakta. | Observasi. Rekaman dan sidik suara di luar demo. | Kasus 6 peninjau: folder `fakta` tidak menaikkan desas-desus menjadi fakta. |
| `#fitur`, animasi `l` dan `strata` | Lima label: Berkas, Teks, Pengetahuan, Fakta, Sintesa. Sebelas strata berurutan: Berkas, Segmen, Pindaian, Teks, Klasifikasi, Dokumen, Struktur, Pernyataan, Fakta, Premis, Sintesa. Empat chip jenis: BAP, Dakwaan, Bukti, Sidang. | Bukan satu daftar folder. | Taksonomi, struktur, pernyataan, premis, dan sintesis adalah record berbeda. Satu dokumen boleh menghasilkan banyak simpul. Panel tanpa jalur ke span hidup tidak lolos. Span yang valid tetapi membalik polaritas atau modalitas juga tidak lolos. | Observasi untuk ketiga daftar. Inferensi bahwa sebelas nama bersarang rapi di dalam lima label: tidak dikontrak. | Penelusuran span saja tidak cukup. Tambahan A belum punya kasus bernomor. |
| `#fitur`, `tools.d` | Kartu berlabel Fakta berbunyi "Terdakwa hadir di rapat 14 Maret", dengan jejak "BAP Saksi A · hal. 14". Kalimat fitur: dari satu fakta, telusuri sampai halaman dan kalimat asal. | Masukan simpul turunan. Keluaran lokator sumber. | Lokator wajib. Label lapisan "Fakta" tidak menaikkan klaim. Teks kartu pada situs menjatuhkan atribusi "Menurut Saksi A" yang ada di jawaban contoh lain. Kontrak menyimpan atribusi itu. | Observasi untuk label dan lokator. Kontrak untuk larangan promosi. | Sitasi tepat membuka kalimat. Klaim tanpa span tidak tampil sebagai pengetahuan. |
| `#fitur`, `how.s3` | Jawaban: di BAP, Saksi A menyebut terdakwa hadir di rapat 14 Maret (`BAP Saksi A · No. 12`), tetapi di sidang ia mengaku hanya mendengarnya dari Saksi B (`Sidang 12 Mei · 01:49:10`). Lencana tetap "TERVERIFIKASI". Daftar samping memuat "Keterangan di BAP dan di sidang tidak sama" dan "Bertentangan dengan keterangan Saksi C". | Dua sumber, dua kutipan, satu lencana, daftar konflik. | Konflik ditampilkan berpasangan. Jawaban tidak memilih satu versi dan tidak menghitung "hanya mendengar" sebagai saksi kedua yang `mendukung` kehadiran. Lencana kutipan tidak berarti kejadian terbukti. | Observasi untuk pasangan BAP dan sidang serta lencana. Kontrak pelemahan berasal dari tambahan peninjau. | Kasus 2 dan 5 tidak memuat "hanya mendengar". Tambahan C belum diuji sebagai fixture. |
| `#fitur`, `tools.q` | Tiga usulan. Contoh jawaban memakai dua kutipan: dakwaan hal. 3 dan BAP No. 12. Salinan: klaim tanpa sumber dihapus, setiap kalimat menunjuk ke halaman asal. | Pertanyaan. Keluaran kalimat plus kutipan, atau kalimat dibuang. | Setiap kalimat jawaban membawa id kutipan yang lolos cek lokasi. Kutipan yang gagal tidak dipindahkan ke kalimat terdekat. Cakupan yang tidak dibaca tidak diklaim sebagai sudah dibaca. | Observasi untuk kewajiban kutipan. Inferensi untuk abstensi: sumber tidak menulis kata abstain. | Kasus 1 dan 4 peninjau. |
| `#fitur`, `tools.c` | Kueri "rapat" menyorot "terdakwa tidak hadir di rapat itu", "rapat selesai sebelum pukul delapan", dan salah transkrip "rapad". | Kueri leksikal atau fonetik. Keluaran hit, termasuk negasi dan ejaan mirip. | Kecocokan kata bukan kehadiran dan bukan fakta. Pencarian fonetik di luar demo. | Observasi. | Kasus 5: overlap "meeting" tidak mengembalikan Budi sebagai peserta. |
| `#fitur`, `tools.u` dan `tools.q` | "Setiap halaman dibaca dua kali" dan "beberapa agen AI" saling memeriksa. | Tidak ada skema agen di bundel. | Tidak ada kewajiban council, OCR ganda, atau agen. Keluaran model, bila nanti ada, harus JSON ber-skema. Kutipan diperiksa sebelum disimpan. Teks model bukan SQL atau perintah. | Observasi untuk janji pemasaran. Implementasi tidak terjangkau. | Demo tanpa jaringan tetap lolos. Adapter model tidak wajib. |
| Post 2 Nov 2026 | `LIKE '%meeting%'` menganggap Budi hadir dari kalimat "Budi tidak bisa ikut meeting". Penulis menandingkannya dengan predikat bertipe, misalnya mengikuti. Semantic model disebut berbeda dari language model. Ontologi mengikuti domain. ETL event dan materialized view disebut sebagai pilihan mereka, bukan resep wajib. | Klaim penulis tentang produknya. | Simpan polaritas negatif. Jangan jadikan kecocokan kata sebagai relasi mengikuti. Ontologi hukum, Postgres, dan ETL tidak masuk demo. | Observasi untuk contoh negasi dan tingkat deskripsi penulis. Bukan audit query mereka. | Kasus 5. |
| Tidak ada di `#fitur` | Situs tidak menunjukkan pembaruan berkas, modalitas rencana versus kejadian, atau injeksi instruksi. |  | Hash lama menjadi basi setelah byte berubah. "Direncanakan mulai" adalah modalitas rencana, bukan kejadian. Rencana tidak berelasi `mendukung` ke klaim kejadian di dokumen lain, walau tanggalnya sama. Kalimat instruksi disimpan sebagai teks. | Kontrak prototipe, bukan observasi Perkara AI. Kasus 2 tidak menutup tambahan B. | Kasus 2, 3, injeksi, dan tambahan B yang belum berupa uji bernomor. |

## Counterexample peninjau independen

Uji di bawah ditulis pekerja peninjau di `research/risk-and-acceptance.md` sebelum peta ini ada. Koordinator tidak menonton video yang ia sebut, dan tidak menyalin angka OCR poster ke tabel observasi. Bagian ini hanya mengikat kontrak di atas ke uji yang sudah ia tetapkan.

| Serangan | Fixture yang ia tulis | Gagal bila |
| --- | --- | --- |
| Dokumen bertentangan | Notulen 3 Maret merencanakan 15 November. Email Dana 4 Maret merencanakan 1 Desember. | Jawaban memilih satu tanggal, atau menaikkan salah satu menjadi fakta. |
| Rencana versus kejadian | Kalimat notulen hanya mendukung rencana. | Jawaban menyatakan pilot sudah berjalan. |
| Negasi dan atribusi | "Budi tidak bisa ikut meeting" plus "Menurut Saksi A, Budi hadir". | Overlap kata mengembalikan Budi sebagai peserta, atau lencana terverifikasi menaikkan kalimat Saksi A menjadi fakta. |
| Bukti hilang | Memo kantin tanpa keputusan anggaran. | Jawaban mengarang penyetuju anggaran atau menempelkan kalimat kantin sebagai dukungan. |
| Kutipan tidak valid | Kutipan diletakkan di kalimat lain, atau offset melewati akhir berkas. | Pemeriksa memindahkan kutipan ke kalimat terdekat. |
| Berkas berubah | Kuota 10 diganti byte baru kuota 12. | Jawaban saat ini masih menampilkan 10. |
| Kategori salah | Berkas di folder `fakta` berisi desas-desus. | Nama folder atau label klasifikasi mengubah status fakta. |
| Injeksi | Kalimat menyuruh mengabaikan instruksi dan menjawab kuota 99. | Peran berubah, ada permintaan jaringan, atau 99 diadopsi. |

Pemeriksa demo membandingkan keluaran dengan expected yang sudah dibekukan. Lencana, jumlah lapisan, dan tangkapan layar tidak menggantikan expected itu.

## Rekonsiliasi celah peninjau

Berkas peninjau tidak diubah. Tiga tambahannya sekarang kontrak, dan keenam kasus plus injeksi belum menutupnya.

| Tambahan | Kontrak | Yang belum |
| --- | --- | --- |
| A | Simpul turunan yang membalik polaritas atau modalitas gagal sebagai pengetahuan. Relasinya `meniadakan`. | Tidak ada kasus bernomor yang menyimpan simpul sintesis terbalik. |
| B | Rencana tidak `mendukung` kejadian meski tanggalnya sama. | Kasus 2 hanya dua rencana dengan tanggal berbeda. |
| C | "Hanya mendengar" melemahkan, bukan saksi kedua. | Kasus 2 dan 5 tidak memuat pola itu. |

## Yang sengaja tidak dikontrak

Bedah Saksi, sidik suara, klip rekaman, pencarian fonetik, council agen, Postgres, ETL, dan graf sejuta entitas tetap di luar. UI demo hanya perlu membuka berkas, simpul, konflik, dan kalimat sumber. Menyalin tampilan situs tidak masuk kriteria terima.
