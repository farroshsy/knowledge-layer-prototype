# Riset sumber primer Perkara AI

Tanggal baca: 2026-11-10. Ini laporan koordinator, bukan proposal implementasi dan bukan audit kode internal. Tiga label dipakai di seluruh dokumen:

- **Sumber**: teks yang benar-benar terbaca dari halaman, bundel publik, atau post.
- **Inferensi**: bacaan yang masuk akal, tetapi tidak dinyatakan oleh sumber.
- **Tidak terjangkau**: tidak dibaca, tidak ditonton, atau tidak dipublikasikan.

Pada saat bagian sumber di bawah ditulis, tidak ada kode produk yang dijalankan. Kalimat itu status riset saat itu, bukan klaim bahwa folder ini tetap kosong. Angka volume, latensi, dan model di bagian sumber adalah klaim penulis atau kutipan wawancara, bukan hasil ukur ulang.

## Yang diminta untuk prototipe ini

Notebook atau basis pengetahuan lokal, banyak dokumen, lapisan informasi yang bermakna, terinspirasi Perkara AI. CTO mengizinkan dokumen dummy. Bukan klon produk hukum. Bukan unggahan data privat atau rekaman. Server dan UI lokal berbeda dari inferensi yang benar-benar offline. Belum ada dokumen CTO lain yang mengubah batas ini.

## Situs perkara.ai

`https://perkara.ai/` adalah aplikasi satu halaman. HTML statis hanya memuat judul dan deskripsi. Salinan produk ada di bundel publik `/assets/index-DlM17x7b.js` (diunduh 2026-11-10, sekitar 119 KB). Ini materi pemasaran, bukan spesifikasi pipeline. Situs sendiri menulis bahwa contoh di halaman memakai data rekaan.

Deskripsi meta: Perkara AI membaca seluruh berkas dan rekaman sidang, memverifikasi analisis dengan banyak agen AI, dan menunjukkan sumber asli untuk setiap jawaban.

### Lima lapisan dan sebelas jenis artefak bukan daftar yang sama

Animasi "lima lapisan" memakai label kasar:

| Bahasa situs | Label |
| --- | --- |
| Indonesia | BERKAS, TEKS, PENGETAHUAN, FAKTA, SINTESA |
| Inggris | FILES, TEXT, KNOWLEDGE, FACTS, SYNTHESIS |

Di objek yang sama, jejak "telusuri lapisan" memakai sebelas nama berurutan:

| Indonesia | Inggris |
| --- | --- |
| Berkas | Files |
| Segmen | Segments |
| Pindaian | Scans |
| Teks | Text |
| Klasifikasi | Classification |
| Dokumen | Documents |
| Struktur | Structure |
| Pernyataan | Statements |
| Fakta | Facts |
| Premis | Premises |
| Sintesa | Synthesis |

Kalimat fitur: setiap halaman dibaca dua kali, lalu diurai lima lapis, dari teks dan struktur dokumen sampai fakta, termasuk siapa melakukan apa, di mana, kapan, dan bagaimana. Kalimat lain: dari satu fakta, telusuri lapisan demi lapisan sampai ke halaman dan kalimat asal. Klaim tanpa sumber dihapus, dan setiap kalimat menunjuk ke halaman atau menit rekaman.

**Sumber berhenti di situ.** Bundel tidak mendefinisikan skema simpul, sisi graf, atau pemetaan resmi sebelas nama ke dalam lima label. "Dibaca dua kali" tidak menjelaskan dua kali oleh apa.

**Inferensi, bukan fakta produk:** sebelas nama tampak seperti anak tangga artefak dari berkas mentah menuju sintesis, sedangkan lima label adalah cerita yang lebih kasar untuk animasi. Menyisipkan Segmen dan Pindaian ke dalam BERKAS, atau Premis ke dalam FAKTA, adalah tebakan. Prototipe tidak boleh memperlakukan tebakan itu sebagai perilaku Perkara AI.

### Kategori dokumen bukan tingkat abstraksi

Animasi juga punya kelompok jenis berkas, terpisah dari kedua daftar di atas:

- Indonesia: BAP, DAKWAAN, BUKTI, SIDANG
- Inggris: STATEMENTS, INDICTMENT, EXHIBITS, HEARINGS

Salinan lain: AI menebak jenis setiap dokumen, lalu pengguna mengoreksinya. Jenis berkas adalah taksonomi. Lapisan dan strata adalah tingkat pengolahan atau abstraksi. Satu dokumen dapat memuat banyak pernyataan, fakta, dan premis. Contoh jawaban di situs, "Menurut Saksi A, terdakwa hadir", tetap kutipan beratribusi dengan sitasi "BAP Saksi A · No. 12", bukan kenyataan yang otomatis terbukti. Label "TERVERIFIKASI" di animasi adalah status produk pada data rekaan.

Ketentuan layanan di bundel yang sama: keluaran AI adalah petunjuk awal, bukan pernyataan fakta, bukan nasihat hukum, dan satu-satunya acuan sah adalah dokumen sumber. Pengguna wajib memeriksa sendiri. Ini memperkuat perbedaan antara klaim yang dikutip dan fakta yang sudah terbukti.

Fitur hukum yang terlihat di salinan, dan **di luar** prototipe ini: Bedah Saksi, dakwaan, pleidoi, rekaman sidang, sidik suara, pencarian fonetik, serta enkripsi berkas perkara. Tidak ada ontologi yang tertulis di bundel beranda.

## Post semantic model

Post yang diminta terbaca lewat API X, bukan lewat halaman `x.com` (pengambilan HTML sebelumnya 403). Video di dalam thread tidak ditonton.

Utas utama: [Ibrahim Arief, 2 Nov 2026](https://x.com/ibamarief/status/2117104412824944848), mengutip [31 Okt 2026](https://x.com/ibamarief/status/2116500288467321058).

Yang dikatakan penulis, sebagai klaim publik:

- Memberi agen akses mentah ke basis data lalu membiarkannya menyusun SQL sendiri rentan salah, karena satu pertanyaan terbuka dapat menjadi ribuan kueri.
- Semantic model dipakai sebagai jembatan antara model AI dan data perkara. Penulis bilang ada banyak jenis semantic model dan pembaca harus memilih yang cocok. Ia tidak mempublikasikan skema internal.
- Untuk perkara mereka, pilihannya adalah graf pengetahuan berlapis. Sebagian lapisan memakai ontologi yang dirancang untuk semantik investigasi hukum. Graf itu disebut "otak pengetahuan". Satu perkara disebut dapat memuat sekitar satu juta entitas dan hubungan. Angka ini klaim kasus mereka, bukan kuota prototipe.
- Contoh kegagalan kata kunci: mencari karyawan yang "ikut meeting" dengan Pejabat Z lewat `LIKE '%meeting%'` ikut menangkap kalimat "Budi tidak bisa ikut meeting". Penyebab yang disebut: kueri tidak memahami negasi.
- Kontras yang ia tunjukkan adalah kueri graf semantik dengan predikat bertipe, misalnya orang bertipe karyawan, bekerja di perusahaan, mengikuti event bertipe meeting, pada tanggal, bersama orang bertipe pejabat. Predikat seperti "mengikuti" dipilih model untuk menjawab pertanyaan. Hasilnya dipakai untuk analisa perkara, bedah saksi, dan RAG chat.
- Implementasi yang disebut hanya pada tingkat pilihan: ETL berbasis event untuk menyusun ulang data mentah, dan dalam beberapa kasus materialized view PostgreSQL. Ia menyuruh pembaca menanyakan pendekatan teknis ke coding agent masing-masing. Ontologi ekspor-impor, rumah sakit, dan persidangan disebut harus berbeda.
- Balasan penulis pada utas yang sama: semantic model adalah konsep sebelum LLM untuk mereduksi data tidak terstruktur menjadi pengetahuan terstruktur. Agen hidup di dalam aplikasi, bukan di harness. Mereka belum melihat nilai dari clustering simpul graf. Dukungan ontologi lain, misalnya perdata dan arbitrase, disebut sebagai rencana.

**Tidak terjangkau dari post ini:** definisi lapisan graf, daftar predikat, skema event ETL, dialek kueri, dan apakah sebelas strata di situs adalah lapisan graf yang sama. Jangan menyamakan keduanya.

## Jejak publik lain yang relevan

Semua butir di bawah adalah klaim penulis atau ringkasan media, bukan inspeksi sistem.

- [6 Mar 2026](https://x.com/ibamarief/status/2029735414303707470): prapemrosesan dan beberapa jenis ekstraksi teks pada PDF; kawanan agen; graf padat; lapisan inteligensi yang lebih tinggi memberi pemahaman semantik untuk chat; sub-agen yang menantang hasil. Klaim volume: 4700+ halaman dan 8900+ keterangan. Nama lapisan tidak disebut.
- [6 Agu 2026, balasan](https://x.com/ibamarief/status/2085231493731987626): verifikasi manual disebut hanya pada instruction tuning transkripsi. Koreksi fakta atau data disebut terjadi di lapisan berikutnya, yaitu semantic atau analysis layers. Nama itu tidak dijabarkan.
- [25 Jul 2026](https://x.com/ibamarief/status/2080990005003186184): deduplikasi lewat LLM karena jarak suntingan saja menyamakan "Direktorat SMP" dan "Direktorat SMK".
- Wawancara Tirto, 30 Okt 2026, [artikel 2 Nov 2026](https://tirto.id/perkara-ai-inovasi-ibam-arief-melawan-kriminalisasi-hukum-hEti): kutipan tentang struktur pengetahuan khusus perkara, agen dari beberapa sudut, auditor yang memeriksa sumber, lalu "AI hakim", disebut tiga lapis pengecekan. Jawaban dapat menyatakan informasi tidak ada. Setiap butir bedah saksi punya tautan ke dokumen asal. Rekaman sidang dan sidik suara juga diceritakan. Klaim terpisah: lebih dari 800.000 data dan hubungan. Artikel adalah sumber sekunder.
- [5 Nov 2026](https://x.com/ibamarief/status/2118379528137613823): council of agents naik dari 3 menjadi 4, adjudicator akhir disebut Gemini 4 Argon, tangkapan layar dari perkara simulasi. Angka tiga lapis di wawancara Tirto jadi titik waktu, bukan arsitektur tetap.
- [5 Nov 2026](https://x.com/ibamarief/status/2118380643294023764): panel inspeksi sitasi diperjelas supaya sumber asli bisa diperiksa.
- [6 Nov 2026](https://x.com/ibamarief/status/2118534284340568303) dan [lanjutannya](https://x.com/ibamarief/status/2118721930106908863): satu jawaban disebut 10 menit 7 detik. Penulis lalu menambah decision model: pertanyaan sederhana jadi lookup graf dalam hitungan detik, pertanyaan lain memakai council penuh. [7 Nov](https://x.com/ibamarief/status/2119080222385643638): sebagian besar latensi ada di verifikasi, dan pengguna dapat melihat linimasa tiap agen.
- [9 Nov 2026](https://x.com/ibamarief/status/2119826812704539022) dan [rerank](https://x.com/ibamarief/status/2119829600578707671): pengambilan simpul graf dioptimalkan untuk recall. Rerank disebut mengirim sekitar 1,2 juta token simpul per pertanyaan ke VoyageAI, terbatas kira-kira 1–2 pertanyaan per menit. Ini operasi cloud berbayar, bukan resep lokal.

Akun [@PerkaraAI](https://x.com/PerkaraAI) yang terbaca (24 Okt, 29 Okt, 9 Nov 2026) berisi ajakan produk dan demo sidang. Tidak ada penjelasan model semantik.

## Batas untuk keputusan MVP

Yang boleh ditiru sebagai perilaku yang terlihat, bukan sebagai implementasi tersembunyi:

1. Simpan berkas asli dan lokasi teks. Satu berkas menghasilkan banyak simpul.
2. Pisahkan taksonomi jenis dokumen dari tingkat abstraksi.
3. Pernyataan adalah klaim beratribusi dan tetap membawa sitasi. Span yang valid tidak menaikkan klaim menjadi fakta. Premis dan sintesis adalah turunan: mereka tidak boleh membalik polaritas atau modalitas klaim yang ditunjuk. Relasi mendukung tidak boleh mengikat rencana ke kejadian, dan kesaksian tidak langsung bukan saksi kedua.
4. Negasi, tanggal yang bentrok, dan perubahan dokumen harus tetap terlihat. Jangan menimpa dengan satu jawaban.
5. Jawaban tanpa bukti harus menolak atau abstain. Konsensus model bukan bukti.
6. Penelusuran sumber adalah inti demo. Lapisan dekoratif tanpa sisi ke bukti tidak memenuhi inspirasi situs.

Yang ditunda karena tidak tersedia, tidak muat semalam, atau di luar izin:

- Ontologi investigasi hukum, Bedah Saksi, rekaman, sidik suara, dan council model cloud.
- ETL event, materialized view, reranker, dan graf sejuta entitas.
- Klaim bahwa regex atau pencocokan kata adalah evaluasi semantik. Post 2 Nov justru menunjukkan kegagalan pendekatan itu.
- Inferensi offline. Aplikasi lokal bukan model offline. Kelayakan satu panggilan Grok CLI tercatat kemudian di `provider-smoke.json` dan `research/council-decision.md`. Satu smoke bukan akurasi semantik. Jalur leksikal wajib berlabel dan bukan ekstraksi semantik. Tanpa model, demo tetap harus bisa menjawab lewat aturan yang jujur.

## Asumsi yang tidak mengubah ruang lingkup

Dokumen dummy berbahasa Indonesia, tiga berkas kecil yang saling bertentangan, cukup untuk penerimaan. Lapisan prototipe boleh didefinisikan sendiri, asalkan setiap simpul turunan menyimpan asal dan pembeda antara kutipan, klaim, dan sintesis. Nama boleh mengikuti strata publik sebagai inspirasi, dengan catatan bahwa pemetaannya bukan spesifikasi Perkara AI.

## Rekonsiliasi penutupan riset

Ditulis 2026-11-10 setelah sanggahan `research/public-behavior-counterexamples.md`. Bagian sumber di atas tidak diubah menjadi audit implementasi.

- Tiga celah A, B, dan C pada peta perilaku dikontrak di `research/public-behavior-map.md`. Keenam kasus di `research/risk-and-acceptance.md` tidak menutup celah itu.
- `research/architecture-challenge.md` tidak ada di disk saat riset ditutup. Tidak ada pesan Orca baru yang dikirim untuk memintanya.
- Artefak `provider-smoke.json` yang ada sekarang: `method` grok, kategori `notulen`, `nonce_quote_exact` true, `grok_quote_count` 4, `warnings` kosong, `offline_model` false, `provider_error` null. Berkas itu tidak menyimpan string nonce. Log sesi koordinator menyebut nonce lulus `KLAYER-SMOKE-4420`, setelah percobaan `KLAYER-SMOKE-4419` gagal pada kutipan persis. Ini bukan tolok ukur kualitas.
- Keputusan yang memakai bukti itu ada di `research/council-decision.md`. Ringkas untuk koordinator pengiriman ada di `research/research-handoff.md`.
