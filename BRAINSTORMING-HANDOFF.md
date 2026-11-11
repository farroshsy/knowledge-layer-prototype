# Catatan lengkap untuk brainstorming dengan GPT

Tanggal catatan: 10 November 2026, WIB. Ini snapshot pekerjaan yang masih berlangsung, bukan laporan final atau bukti seluruh fungsi sudah lolos.

## 1. Cara memakai catatan ini

Saya, Farros Hilmi Syafei, sedang mengerjakan tugas lanjutan setelah Google Meet dengan CTO Rakamin. Saya ingin berdiskusi tentang business process, arsitektur, retrieval, dan evaluasi. Jangan langsung menyetujui rancangan yang sudah ada atau memperlakukan referensi sebagai spesifikasi wajib.

**Permintaan saya kepada GPT**

> Baca catatan ini sebagai konteks. Mulai dengan menyampaikan pemahamanmu tentang problem dan outcome yang harus dibuktikan. Kemudian kritik business process dan pilihan arsitektur berdasarkan kebutuhan tersebut. Bedakan kebutuhan yang jelas, asumsi, keputusan desain, dan klaim yang belum terverifikasi. Berikan alternatif beserta pros, cons, failure modes, dan cara mengujinya. Prioritaskan keputusan yang memengaruhi demo besok pukul 08.00 WIB. Jangan membuat daftar fitur enterprise tanpa batas atau menganggap persetujuan banyak agent sebagai bukti kebenaran. Gunakan Bahasa Indonesia yang mudah saya pahami dengan technical terms dalam English bila lebih tepat. Jangan mengarang apa yang dikatakan CTO atau hasil test yang belum dijalankan.

## 2. Latar dan batas pekerjaan

- Tugas baru ini terpisah dari studi kasus AI Interview Platform yang sebelumnya sudah saya submit. Repository submission lama harus tetap tidak disentuh.
- Target tugas baru adalah demo yang berjalan di lokal sebelum **11 November 2026 pukul 08.00 WIB**.
- CTO mengizinkan memakai **dummy data dan dummy documents** dahulu. Belum ada dokumen contoh resmi yang diberikan.
- Besok CTO akan memasukkan beberapa dokumen baru dan mencoba query. Jadi sistem tidak boleh hanya bekerja pada contoh yang sudah ditanam ketika coding.
- Backend, business process, dan fondasi arsitektur menjadi fokus. UI sederhana boleh, tetapi alur produk harus sungguh bekerja.
- Saya menggunakan Grok melalui Orca untuk riset, implementasi, dan independent review; Codex berperan sebagai pengarah dan pemeriksa agar penggunaan sesi tidak habis untuk semua implementasi.
- Belum ada otorisasi untuk push, deployment publik, mengirim pesan kepada orang lain, atau mengunggah dokumen privat ke provider.

## 3. Penjelasan CTO yang memperjelas scope

Berikut ringkasan penjelasan CTO yang saya sampaikan kembali setelah meeting, bukan rekaman verbatim yang sudah ditranskripsikan secara independen.

CTO meminta sistem untuk mengumpulkan dokumen dan melakukan retrieval context dari kumpulan dokumen tersebut. Simulasi harus mempunyai **dua kelas sumber data**.

1. **Structured business data** dalam database, menggunakan PostgreSQL atau pilihan lain yang fondasinya dapat dipertanggungjawabkan.
2. **Unstructured documents**, yaitu kumpulan dokumen yang dimasukkan ke repository pengetahuan.

Pertanyaan pengguna dapat membutuhkan kombinasi kedua sumber itu. UI boleh berupa chatbot atau tampilan sederhana. Dokumen perlu dapat diklasifikasikan, dan satu dokumen mungkin masuk beberapa kategori. Teknik layer pada Perkara AI bisa menjadi inspirasi, termasuk turunan informasi dari dokumen, tetapi definisi dan rancangan kita boleh berbeda.

Perumpamaan pengalamannya mirip NotebookLM. Namun, untuk sistem internal perusahaan, memasukkan dokumen lalu memasang embedding saja belum tentu menghasilkan retrieval yang sesuai. Produk ini berpotensi dikembangkan dan dipakai sungguhan, sehingga pros, cons, dan trade-off perlu dipikirkan.

**Pembedaan penting**

Database yang hanya menyimpan hasil ekstraksi dokumen belum otomatis memenuhi maksud dua sumber. Kita perlu mendemonstrasikan data bisnis terstruktur yang berdiri sendiri, lalu menghubungkannya dengan isi dokumen yang relevan.

## 4. Outcome yang ingin dibuktikan

Pengguna dapat memasukkan dokumen baru, mengajukan pertanyaan bisnis, dan memperoleh jawaban yang menggunakan sumber yang tepat, termasuk kombinasi database dan dokumen ketika memang diperlukan.

Jawaban harus membantu pengguna memeriksa asal informasi. Jika bukti tidak cukup, ada nama yang ambigu, atau dua sumber bertentangan, sistem perlu menyampaikan kondisi itu secara jelas.

Ini lebih luas daripada document classification. Klasifikasi adalah salah satu tahap untuk membantu ekstraksi, pengorganisasian, dan retrieval.

## 5. Kebutuhan, asumsi, dan hal yang belum dipastikan

| Status | Butir |
|---|---|
| Jelas dari percakapan | Aplikasi lokal, dua kelas sumber, dummy diperbolehkan, dokumen baru akan diuji, query bisa menggabungkan sumber, satu dokumen bisa punya beberapa klasifikasi. |
| Preferensi saya | Backend kuat, business process jelas, AI benar-benar digunakan, beberapa agent independen saling mereview, keputusan dan trade-off dapat dijelaskan. |
| Belum pasti | Domain dokumen besok, format file, banyak dan panjang dokumen, bahasa, jenis query, tingkat akurasi/latensi yang dianggap cukup oleh CTO. |
| Asumsi kerja | Mulai dari satu domain dummy operasional perusahaan, bukan seluruh jenis dokumen perusahaan sekaligus. |
| Bukan kewajiban yang sudah terkonfirmasi | PostgreSQL, graph database, vector database, sebelas layer, event bus, microservices, learned router, atau council di setiap runtime query. |

Pilihan teknis CTO adalah panduan. Kita tetap harus mempertimbangkan pendekatan yang lebih cocok dan menjelaskan alasannya.

## 6. Business process yang perlu disepakati

Ini usulan awal untuk dikritik, bukan requirement final yang sudah diputuskan.

### Alur memasukkan pengetahuan

1. Pengguna memilih notebook atau ruang pengetahuan.
2. Structured dummy data disiapkan secara terpisah, misalnya data proyek dan penanggung jawab.
3. Pengguna menambahkan dokumen melalui upload atau paste sesuai format yang benar-benar didukung.
4. Sistem menyimpan sumber asli, identitas/hash, dan informasi versi.
5. Sistem membaca struktur dan lokasi teks, kemudian menyarankan klasifikasi serta mengekstrak informasi yang sesuai.
6. Hasil AI diperiksa terhadap schema dan sumber sebelum diterbitkan.
7. Pengguna dapat melihat hasil, menelusuri sumber, dan memperbaiki klasifikasi atau hubungan entitas yang ambigu.
8. Jika proses gagal, status dan penyebab terlihat; retry tidak membuat data aktif berganda.

### Alur pertanyaan

1. Pengguna mengajukan pertanyaan.
2. Sistem mengidentifikasi informasi dan entitas yang dibutuhkan.
3. Sistem menentukan kebutuhan retrieval dari database, dokumen, atau keduanya.
4. Structured query yang tervalidasi mengambil record yang relevan. Document retrieval mengambil span/klaim yang relevan.
5. Data digabungkan melalui identitas dan relasi yang memiliki dasar, bukan sekadar nama yang tampak mirip.
6. Sistem menyusun jawaban dengan sumber record dan kutipan dokumen yang dapat diperiksa.
7. Bukti kurang, konflik, atau ambigu menghasilkan jawaban terbatas atau pertanyaan klarifikasi.

### Alur perubahan

- Dokumen baru tidak otomatis membatalkan dokumen lama; perlu aturan versi dan status yang jelas.
- Koreksi kategori dapat memengaruhi schema ekstraksi dan membuat hasil lama tidak lagi sesuai.
- Perubahan record bisnis dapat membuat jawaban tersimpan perlu dievaluasi ulang.
- Penghapusan/perubahan sumber tidak boleh meninggalkan sitasi aktif yang tampak sah padahal sumbernya sudah tidak sesuai.

## 7. Contoh bisnis untuk menguji pemahaman

Contoh berikut **usulan dummy**, belum dinyatakan sebagai data yang sudah diimplementasikan.

Structured records:

| Project ID | Proyek | PIC ID | Anggaran disetujui |
|---|---|---|---:|
| PRJ-017 | Pilot Orion | EMP-004 | Rp120 juta |

Record karyawan menyatakan EMP-004 adalah Rani, anggota tim Delivery.

Dokumen A memuat bahwa Pilot Orion direncanakan mulai 15 November dan masih menunggu pelatihan operator. Dokumen B memuat usulan penundaan menjadi 1 Desember. Kedua dokumen menyebut PRJ-017 atau rujukan yang dapat dikonfirmasi.

Pertanyaan yang perlu didemonstrasikan:

- **DB-only** — “Siapa PIC Pilot Orion dan berapa anggarannya?” Sumber utamanya record proyek dan karyawan.
- **Document-only** — “Apa alasan penundaan yang disebut dalam memo?” Jawaban menunjuk kutipan memo.
- **Combined** — “Proyek yang ditangani Rani mana yang dokumennya menyebut penundaan, dan berapa anggarannya?” Jawaban membutuhkan record PIC/proyek/anggaran serta isi dokumen.
- **Konflik** — “Kapan pilot mulai?” Sistem membedakan tanggal rencana awal dari usulan baru; tidak menganggap usulan otomatis disetujui.
- **Unanswerable** — “Berapa penghematan setelah pilot berjalan?” Tidak ada bukti penghematan atau bahwa pilot sudah berjalan.
- **Ambigu** — Dua orang bernama Rani tidak boleh digabung otomatis tanpa identitas tambahan.

Contoh ini membantu menguji integrasi sumber, bukan mengunci seluruh produk ke satu nama proyek atau template dokumen.

## 8. Istilah yang jangan dicampur

| Istilah | Makna yang diusulkan |
|---|---|
| Document category | Jenis dokumen, misalnya SOP, notulen, proposal, laporan. Bisa lebih dari satu atau per segmen. |
| Document structure | Heading, paragraf, tabel, atau bagian lain beserta lokasi sumbernya. |
| Statement/claim | Isi pernyataan yang diatribusikan ke sumber; belum otomatis menjadi kenyataan yang terbukti. |
| Polarity | Pernyataan afirmatif atau negatif. |
| Modality | Rencana, permintaan, dugaan, atau kejadian yang dinyatakan terjadi. |
| Semantic relation | Hubungan yang bermakna, misalnya bertanggung jawab atas, menghadiri, atau direncanakan mulai. |
| Premise | Pernyataan/asumsi yang dipakai untuk penalaran, dengan asal dan statusnya. |
| Synthesis | Kesimpulan atau rangkuman turunan yang menyimpan hubungan ke dukungannya. |
| Provenance/lineage | Jejak dari hasil kembali ke record atau lokasi sumber yang mendasarinya. |

Sitasi yang valid secara lokasi tidak otomatis membuktikan kebenaran atau dukungan semantik. Kata “terverifikasi” harus mempunyai definisi yang spesifik jika dipakai.

## 9. Pelajaran dari PerkaraAI

Sumber utama yang dibahas adalah post Ibrahim Arief:

https://x.com/ibamarief/status/2117104412824944848

Salinan yang berhasil diakses ketika X langsung bermasalah:

https://nitter.cf/ibamarief/status/2117104412824944848

Situs produk:

https://perkara.ai/#fitur

Inti pelajaran yang relevan adalah semantic model sebagai jembatan antara model AI dan raw data, ontologi sesuai domain, serta penelusuran hasil ke sumber. Contoh penulis memperlihatkan bahwa keyword matching dapat salah menyimpulkan seseorang menghadiri rapat dari kalimat yang justru mengatakan ia tidak bisa ikut.

Post dan situs bukan source code internal. Kita tidak tahu seluruh schema, prompt, pipeline, atau mekanisme validasi mereka. Rancangan kita harus berdiri atas kebutuhan sendiri, bukan klaim menyalin arsitektur yang belum dilihat.

Sebelas jenis artefak yang disebut situs dan lima kelompok layer pada animasi tidak otomatis harus menjadi jumlah tabel atau modul kita.

## 10. Referensi lain dan alasan relevansinya

- **Microsoft Content Understanding** — klasifikasi, segmentasi berkas campuran, dan routing ke ekstraksi yang sesuai jenis dokumen. Pola prosesnya relevan; memakai Azure bukan kewajiban.
  https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/concepts/classifier
- **Docling** — representasi struktur dokumen dan provenance. Ini berbeda dari classifier bisnis atau semantic knowledge repository.
  https://docling-project.github.io/docling/concepts/docling_document/
- **NotebookLM** — pengalaman pengguna bertanya terhadap kumpulan sumber dan memeriksa sitasi. Dokumentasinya bukan bukti arsitektur graph internal.
  https://support.google.com/notebooklm/answer/16164461?hl=en

Tidak ada keputusan untuk memasang seluruh tools atau layanan tersebut. Perlu mempertimbangkan waktu setup, biaya, hardware Mac Intel, dan kebutuhan demo.

## 11. Pilihan arsitektur yang perlu dibandingkan

| Pilihan | Kelebihan | Biaya/risiko | Pertanyaan keputusan |
|---|---|---|---|
| Relational semantic model | Cocok untuk business records dan relasi eksplisit; transaksi dan query terkontrol. | Relasi kompleks membutuhkan schema dan query yang dirancang. | Apakah contoh bisnis cukup dengan tabel, node/edge, dan query tervalidasi? |
| Graph database | Traversal hubungan kompleks lebih alami. | Setup dan operasi tambahan; belum menyelesaikan kesalahan ekstraksi. | Apakah benar ada kebutuhan traversal yang tidak praktis secara relasional? |
| Embedding-heavy retrieval | Membantu menemukan teks yang semantically related dan berbeda istilah. | Similarity bukan pembuktian relasi, negasi, atau kelengkapan jawaban. | Dipakai sebagai pencarian kandidat atau justru satu-satunya dasar jawaban? |
| Hybrid retrieval | Structured filters/relations dipadukan dengan pencarian teks dan/atau vector. | Lebih banyak tahap dan potensi kehilangan evidence. | Tahap mana terbukti menambah kualitas pada contoh kita? |

**SQLite vs PostgreSQL** adalah keputusan terpisah. SQLite mengurangi setup untuk demo single-process lokal; PostgreSQL lebih cocok jika kebutuhan concurrent/multiuser/integrasi mengharuskannya. Keduanya tidak otomatis membuat semantic retrieval benar. Pilihan harus disertai alasan dan batas klaim.

**Modular monolith** menjadi arah awal yang layak diuji. Modul dipisahkan berdasarkan tanggung jawab, dengan Interface yang kecil dan error/invariant jelas. Tidak perlu microservices hanya agar terlihat siap berkembang.

## 12. AI dan SQL

Usulan kontrak yang perlu diuji:

```text
Pertanyaan
  -> pemahaman intent dan entitas oleh AI
  -> query plan terstruktur dengan schema terbatas
  -> validasi scope, predikat, filter dan limit oleh backend
  -> compiler ke SQL berparameter / document retrieval
  -> gabungan evidence
  -> jawaban dengan sumber
```

Jangan menjadikan keluaran bebas model sebagai SQL yang langsung dieksekusi. Model juga tidak boleh menjalankan perintah dari isi dokumen. Kata-kata yang serupa tidak cukup untuk memastikan entitas atau relasinya sama.

Desain masih harus memutuskan query yang didukung, cara menangani pertanyaan di luar scope, dan bagaimana merencanakan retrieval gabungan tanpa mengunci jawaban pada daftar kalimat contoh.

## 13. AI development council vs AI di dalam produk

Ini dua hal berbeda.

- **Development council** — beberapa sesi agent independen untuk merancang, mengimplementasikan, mengkritisi, dan memeriksa hasil.
- **Runtime product AI** — klasifikasi, ekstraksi, query planning dan/atau sintesis ketika pengguna memakai produk.

Banyak agent development tidak berarti produk wajib memanggil banyak model untuk setiap pertanyaan. Runtime council dapat menambah latensi, biaya dan kompleksitas. Jika ada, harus dibuktikan manfaatnya dan menunjukkan proses yang benar-benar terjadi.

Saya meminta task tertentu dikerjakan oleh beberapa agent dengan brief identik, hasil awal independen, lalu cross-review. Ketidaksepakatan tidak harus dipaksakan. Kesimpulan dipilih dari evidence, bukan voting. Agent dengan model sama dapat mempunyai kesalahan yang berkorelasi.

Skill lokal yang relevan adalah `codebase-design` untuk deep modules/Interface/Seam/testability dan `domain-modeling` untuk istilah domain. Memakai nama skill tidak membuktikan desain menjadi baik; hasilnya perlu terlihat pada kontrak dan kode.

## 14. Constraints dan evaluasi

Angka benchmark dalam screenshot yang saya kirim berasal dari pihak lain. Itu contoh cara eksperimen, bukan hasil produk saya dan bukan threshold wajib dari CTO.

Evaluasi harus memisahkan:

1. **Classification** — kategori benar, unknown, multi-category/mixed, dan dampak koreksi.
2. **Extraction** — field/relasi, negasi, modalitas dan atribusi sesuai isi.
3. **Retrieval** — evidence penting ditemukan, termasuk data terstruktur yang diperlukan.
4. **Answer quality** — jawaban didukung evidence, tidak menambah klaim tanpa dasar.
5. **Pipeline integrity** — provenance, versi, retry, transaksi, scope dan persistence.
6. **Performance** — server wall-clock latency, waktu provider, ukuran context dan concurrency.

Rencana awal adalah dev set dummy dan held-out dummy yang dibuat independen. Uji pipeline deterministik dipisahkan dari live semantic evaluation. Nol error pada kumpulan kecil bukan jaminan nol halusinasi secara umum.

Macro-F1 dan per-category precision/recall masuk akal untuk klasifikasi dengan label jelas. PR-AUC baru relevan jika ada score/ranking dan protokol yang sesuai. Jangan memakai metric hanya karena tampil ilmiah.

Kenaikan retrieval recall akibat lebih banyak context perlu diuji terhadap kualitas jawaban akhir dan latensi. Jangan menganggap lebih banyak chunk pasti lebih baik. Jika jumlah task dan panjang context sama-sama berubah, efek keduanya tidak dapat dipisahkan dari satu eksperimen itu.

## 15. Status implementasi pada snapshot ini

Folder kerja baru:

`/Users/farros/Downloads/Rakamin-MagangHub/CaseStudy/knowledge-layer-prototype`

**Artefak yang benar-benar sudah ada dan sempat dibaca oleh Codex**

- Laporan riset, proposal, review risiko, dan keputusan awal council.
- Kode Python `klayer/` dengan SQLite store, domain, provider adapter, pipeline, HTTP API dan UI sederhana.
- Dummy Markdown dan `tests/test_flow.py`.
- Provider adapter memuat jalur Grok CLI dan fallback leksikal yang dibedakan dengan label.

Laporan Grok menyebut satu structured-output smoke call ke Grok berhasil. Codex belum menjalankan ulang call itu. Itu bukti terbatas yang dilaporkan agent, bukan jaminan kualitas semua unggahan.

**Kesenjangan penting terhadap penjelasan CTO terbaru**

- Schema yang dibaca berisi notebook/dokumen/job/section/klasifikasi/claim/field/relation. Belum terlihat independent structured business records seperti proyek, karyawan atau transaksi. Menyimpan ekstraksi dalam SQLite belum cukup untuk menyatakan hybrid-source requirement terpenuhi.
- HTTP endpoint yang terlihat menerima JSON `filename` dan `text`. Upload PDF/DOCX sesungguhnya belum dapat diklaim dari implementasi tersebut.
- README memberi contoh menjalankan server di `127.0.0.1:8765`, tetapi keberadaan perintah itu bukan bukti server saat ini aktif atau demo sudah lolos.
- Adanya state job tidak otomatis berarti pekerjaan asynchronous. Perlu menguji respons API dan perilaku proses yang nyata.
- Hasil test final, mutu live model, cold start, retrieval gabungan, dan acceptance pada dokumen unseen belum terverifikasi dalam catatan ini.

**Status agent**

Dua agent riset terpisah sudah menghasilkan proposal dan review. Coordinator Grok awal kemudian membuat kode awal. Coordinator delivery lain sempat tertahan pada menu permission, sehingga jangan menganggap semua worker implementasi sudah aktif.

Dua sesi Grok tambahan A dan B sudah benar-benar membaca brief identik untuk business process dan hybrid retrieval secara independen. Pada snapshot ini, file laporan akhir keduanya belum tersedia. Cross-review belum boleh diklaim selesai.

## 16. Risiko yang perlu diselesaikan sebelum demo

- Aplikasi tampak pintar pada fixture tetapi gagal pada dokumen baru.
- Klasifikasi menjadi label kosmetik yang tidak membantu retrieval/ekstraksi.
- Sistem hanya mencari dokumen dan melupakan independent business records.
- Join salah karena nama sama, alias, atau hubungan yang cuma diduga.
- Evidence valid secara substring tetapi tidak mendukung makna jawaban.
- Negasi/rencana dipromosikan menjadi kejadian positif.
- Fallback leksikal menyamarkan kegagalan model.
- Format dokumen yang dibawa CTO tidak didukung.
- Semua query dikirim ke model dengan context berlebihan, tanpa latency/coverage yang terlihat.
- Perubahan sumber meninggalkan derived results atau jawaban lama yang tampak current.
- Terlalu banyak agent menulis file yang sama, atau terlalu banyak perencanaan menghabiskan waktu membangun.

## 17. Pertanyaan brainstorming yang paling membantu sekarang

1. Apakah interpretasi dua sumber sudah tepat? Apa contoh combined query yang paling kuat untuk membuktikannya?
2. Domain dummy mana yang paling representatif tanpa membuat ontology terlalu luas?
3. Apa business process minimal dari menyiapkan data sampai memakai jawabannya?
4. Apa yang sebaiknya menjadi category, field, claim, relation, premise dan synthesis? Adakah layer yang tidak memberi manfaat?
5. Bagaimana menghubungkan dokumen ke business entity secara aman dan menangani ambiguitas?
6. Kapan relational model cukup, kapan graph/vector memberi manfaat yang terukur?
7. Apa kemampuan inti yang perlu dipertahankan pada deadline, dan apa yang layak ditunda?
8. Bagaimana menguji unseen documents dan query baru tanpa hardcode demo?
9. Bagaimana membedakan sumber bertentangan, versi baru, rencana dan keputusan final?
10. Apa batas kemampuan yang perlu disampaikan secara tepat tanpa mengaburkan fungsi yang benar-benar bekerja?

## 18. Bentuk jawaban GPT yang saya harapkan

Tolong jangan hanya menilai dengan angka atau menambah daftar tools. Jawab berurutan:

1. Pemahaman problem dan koreksi bila interpretasi saya keliru.
2. Business process yang disarankan, dengan satu contoh berjalan.
3. Dua opsi arsitektur yang realistis beserta trade-off.
4. Pilihan yang direkomendasikan berdasarkan constraint lokal/deadline.
5. Lima failure modes terpenting dan test yang membedakannya dari demo semu.
6. Koreksi prioritas implementasi terhadap status saat ini.

Jika masih ada pertanyaan, prioritaskan yang benar-benar mengubah desain. Saran harus membantu melahirkan produk lokal yang dapat diuji besok, bukan memulai ulang riset tanpa batas.
