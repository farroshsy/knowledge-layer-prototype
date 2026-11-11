# Bahan diskusi GPT — memaksimalkan resource untuk aplikasi besok pagi

Snapshot 10 November 2026, sekitar 21.17 WIB. Ditulis dari file dan event proses yang benar-benar diperiksa. Status akan berubah setelah snapshot ini. Ini bahan kritik dan brainstorming, bukan spesifikasi CTO yang sudah disetujui.

## 1. Mulai dari apa yang bisa dimaksimalkan

Tujuan kita adalah memaksimalkan peluang aplikasi lokal berfungsi saat CTO menguji dokumen baru pada 11 November pukul 08.00 WIB. Kuota, model, council, hardware dan dokumentasi adalah sarana. Ukuran hasilnya adalah business process yang bisa dijalankan dan diverifikasi.

| Faktor | Fakta sekarang | Cara memanfaatkan | Risiko dan batas |
|---|---|---|---|
| Kuota Grok | Farros melaporkan 9% weekly terpakai, reset sekitar 10 jam 36 menit dari waktu laporan | Gunakan untuk implementasi, review independen, debugging dan pengujian input baru | Persentase itu laporan user, bukan telemetry runner. Jangan membakar token tanpa hipotesis atau pekerjaan yang jelas |
| Model | CLI menyediakan Grok 4.7 dan Grok 4.7 Build Fast | 4.7 untuk desain, implementasi dan integrity review; Build Fast untuk review kontrak/test | Pilihan ini kebijakan awal, bukan hasil benchmark kualitas/biaya model pada task kita |
| Paralelisme | Dua panggilan per council; implementasi dan audit dapat aktif bersama | Proposal independen serta review silang berjalan bersamaan tanpa menulis file aplikasi yang sama | Lebih banyak agent bisa memperbesar latency provider, konteks berulang dan biaya koordinasi. Saat ini maksimum empat panggilan lintas kedua proses, bukan paralelisme tak terbatas |
| Komunikasi agent | Proposal awal dibutakan; hasil dibaca adjudicator. Audit memiliki tahap cross-examination | Agent menyebut klaim lawan, bukti, kontra-contoh, rekomendasi yang berubah dan eksperimen pemutus | Satu keluarga model dapat memiliki kesalahan yang berkorelasi. Kesepakatan bukan bukti |
| Waktu | Sekitar 10 jam 43 menit menuju demo saat snapshot | Prioritaskan vertical slice lengkap lalu uji dokumen baru dan siapkan demo | Jangan habiskan malam merancang supervisor atau menulis laporan. Sisakan waktu integrasi, restart dan latihan |
| Mac | Mac Intel, RAM 16 GB; Orca sebelumnya lag | Panggilan headless, output ringkas, hindari banyak TUI berat | Proses lokal harus tetap hidup. Workflow ini bukan layanan hosted |
| PC | RTX 2060 6 GB VRAM, RAM 64 GB; Tailscale tersambung, identitas SSH cocok | Bisa membantu jika autentikasi dan layanan berhasil disiapkan | SSH belum berhasil login. PC belum dipakai. Jangan menjadikan instalasi local LLM jalur kritis; 6 GB VRAM membatasi model/context |
| Kode yang ada | Prototype Python, SQLite, UI lokal, provider Grok dan fallback rules sudah ada | Perkuat modul yang ada agar menggabungkan independent business records dengan dokumen | Jangan rewrite ke banyak layanan/graph DB tanpa kebutuhan terukur |
| Evaluasi | Baseline aplikasi 10 tests; supervisor 13 tests; live provider smoke tersimpan | Tambahkan pengujian perilaku dua sumber, counterexample, lalu live model spot checks | Test count bukan kualitas semantik. Tests fake provider dan real inference harus dibedakan |
| Observability | Event council, durasi, model, test output, diff/hash tersedia | Jadikan metrics aplikasi terlihat pada execution path, bukan sekadar dokumen | F1, recall, citation support dan p95 belum terukur; jangan isi angka dekoratif |

Prinsip resource allocation yang diusulkan: setiap panggilan harus menghasilkan salah satu dari perubahan kode yang teruji, bug yang dapat direproduksi, keputusan yang memiliki trade-off, atau hasil evaluasi yang mengubah tindakan berikutnya. Hindari beberapa agent hanya memparafrasekan pendapat yang sama.

## 2. Tugas dari CTO dan business process

CTO meminta simulasi lokal knowledge repository. Saat ini dokumen dummy diperbolehkan. Besok CTO akan membawa dokumen baru. Ada dua sumber yang harus berbeda secara nyata:

1. Structured business records di database, misalnya person, project dan assignment yang berdiri sendiri.
2. Unstructured documents yang diunggah, diproses dan diklasifikasikan; satu dokumen bisa memiliki beberapa kategori atau bagian.

Pertanyaan harus dapat memakai data database saja, dokumen saja, atau menggabungkan keduanya. Tidak cukup menyimpan hasil ekstraksi dokumen ke tabel lalu menyebutnya dua sumber independen.

Business process demo yang dituju:

**Pilih knowledge workspace → masukkan dokumen → lihat status pemrosesan dan klasifikasi → periksa informasi hasil ekstraksi beserta sumber → ajukan pertanyaan → sistem mengambil evidence dari sumber yang relevan → tampilkan jawaban/konflik/ambiguity/insufficient evidence → pengguna dapat membuka sumbernya.**

PerkaraAI merupakan inspirasi semantic model dan ontology, bukan kewajiban meniru graph database, domain hukum, jumlah layer atau council tertentu. Domain internal Rakamin belum dikonfirmasi. Contoh project/person/assignment adalah domain dummy, bukan representasi kebijakan Rakamin.

## 3. Hasil aplikasi yang benar-benar ada

Prototype berada di `CaseStudy/knowledge-layer-prototype` dan terpisah dari repository submission AI Interview yang dibekukan.

- Backend Python modular, penyimpanan SQLite dan UI HTML lokal tersedia.
- Ada dokumen, sections, classifications, claims, fields, relations dan status ingest.
- Provider Grok CLI tersedia untuk inference online; aplikasi lokal tidak berarti model offline.
- Fallback rule-based diberi label berbeda dari Grok.
- Catatan provider smoke menyatakan method grok, tanpa provider error, kategori notulen, empat quote dan nonce quote exact. Ini spot check tersimpan, bukan benchmark kualitas menyeluruh.
- Baseline tests aplikasi lulus 10 tests. Ada ResourceWarning socket HTTP belum ditutup, sehingga jangan disebut bebas warning.

Batas penting yang masih ada pada baseline:

- Belum ada independent operational business tables yang diperlukan untuk hybrid query sungguhan.
- Query masih sempit pada dokumen/claims. Belum terbukti mampu menjawab pertanyaan bisnis umum atau dokumen arbitrer.
- Native PDF/DOCX upload belum terbukti; jalur yang diketahui menerima filename/text JSON atau teks. Format dokumen CTO belum diketahui dan menjadi risiko demo penting.
- Status job tidak otomatis berarti pemrosesan sudah asynchronous.
- Exact substring citation membuktikan lokasi teks, bukan bahwa makna kesimpulan didukung.
- Multi-label classification, semantic correctness, application latency distributions dan kualitas retrieval belum memiliki hasil evaluasi lengkap.

## 4. Hasil terbaru council implementasi

Run dimulai 21.12 WIB. Pada snapshot, kedua proposal independen sudah selesai dan adjudicator sedang berjalan. Jumlah panggilan dimulai 3, kandidat diterima 0. Belum ada implementasi baru dari run ini yang dinyatakan lolos.

Kedua proposal secara terpisah menemukan gap terpenting yang sama:

- Tambahkan record people/project/assignment yang tersimpan terpisah dari isi dokumen.
- Gunakan stable IDs; nama yang sama tidak otomatis menjadi join.
- Buat closed query plan yang dikompilasi backend menjadi parameterized SQL; model tidak mengeksekusi SQL bebas.
- Bedakan route DB-only, document-only, combined dan unsupported berdasarkan eksekusi nyata.
- Sertakan lineage record ID/version dan/atau source span dokumen.
- Rekam trace ID, durasi monotonic, method/provider dan counter route.

Ini masih proposal, bukan fitur selesai.

### Kritik terhadap proposal tersebut yang perlu dibahas

Keduanya mengusulkan acceptance untuk kalimat plan atau dokumen negasi dengan hasil non-occurrence. Ini harus diperjelas: **rencana bukan bukti bahwa event terjadi, tetapi rencana saja juga tidak membuktikan event tidak terjadi**. Jika database menyebut not_started, sistem bisa mengatakan “menurut record versi X statusnya not_started”; jangan mengubahnya menjadi kepastian universal tanpa mempertimbangkan waktu, otoritas dan konflik sumber.

Selain itu, contoh project code dan intent harus menguji mekanisme umum, bukan menjadi hardcoded answers. Nama, nonce dan isi dokumen baru perlu diganti ketika menguji. Kesepakatan dua proposal bisa menunjukkan gap nyata, tetapi juga bisa mengulang asumsi yang sama.

## 5. Workflow otomatis yang sudah dijalankan

Graph implementasi:

**Baseline → 2 proposal independen paralel → adjudicator memilih bounded slice → builder → 2 reviewer paralel memeriksa exact diff → compile/tests dan pinned legacy tests → simpan kandidat versi terpisah → putaran berikutnya membawa findings.**

Batas default 8 putaran, 64 panggilan, 4 jam, 480 detik per provider call. Deadline absolut 06.30 WIB adalah batas tambahan; run yang dimulai 21.12 akan lebih dahulu mencapai batas empat jam sekitar 01.12 jika tidak selesai/berhenti sebelumnya. STOP file, budget, perubahan source dari luar dan dua putaran tanpa progress dapat menghentikannya.

Grok tidak memiliki tools pada panggilan supervisor. Model mengirim JSON manifest, runner memvalidasi path dan menjalankan commands pengujian yang tetap. Kandidat tidak otomatis menimpa source asli. Pointer latest-approved menunjuk kandidat yang lolos gates. Ini bukan OS sandbox: Python tests kandidat tetap dieksekusi lokal, sehingga jangan menyebutnya isolasi keamanan penuh.

Supervisor lulus 13 tests dan probe Grok sungguhan mengembalikan ok true. Itu memvalidasi bagian controller, bukan seluruh acceptance aplikasi.

Council audit terpisah juga aktif:

**Design challenger + evaluation challenger secara paralel → saling membaca hasil dan membuat rebuttal → adjudicator menyusun acceptance backlog.**

Audit dibatasi lima panggilan/sekitar satu jam, read-only terhadap aplikasi. Pada snapshot kedua analisis awal masih berjalan. Hasilnya belum otomatis dibaca oleh run implementasi yang sudah memuat goal di awal; coordinator perlu meninjau dan memasukkannya pada tahap integrasi/iterasi berikutnya. Jangan mengklaim semua jalur sudah terhubung otomatis.

## 6. Hasil yang perlu terlihat besok

- Aplikasi lokal benar-benar menyala dengan instruksi start yang dapat diulang.
- Data bisnis independen dapat diperiksa.
- Dokumen baru dapat dimasukkan melalui format yang benar-benar didukung.
- Processing/classification terlihat dan kegagalan dapat dipahami.
- Tiga query demo memakai database, dokumen dan kombinasi keduanya.
- Evidence menunjuk record/version dan dokumen/span yang relevan.
- Negation, plan, ambiguity dan conflicting sources tidak dipaksakan menjadi kepastian.
- Unsupported question menghasilkan insufficient evidence yang jelas.
- Restart mempertahankan data dan hasil aktif.
- Trace durasi, route, error/fallback dan method dapat dibuka.

Jumlah layar atau fitur dekoratif bukan ukuran utama. Harus ada satu perjalanan pengguna utuh yang dapat diulang dengan input baru.

## 7. Eksperimen yang lebih bernilai daripada menambah diskusi

1. Buat business record yang informasinya tidak ada di dokumen, lalu tanyakan lewat UI. Ini membedakan DB-only sungguhan dari fixture RAG.
2. Upload dokumen baru dengan nonce acak dan fakta yang tidak ada di seed. Ganti nama/filename agar tidak mengandalkan keyword filename.
3. Buat dua orang bernama sama dan stable ID berbeda. Sistem harus meminta klarifikasi atau memilih lewat ID eksplisit, bukan salah join.
4. Pisahkan “direncanakan”, “tidak hadir”, “mengaku hadir”, dan “tercatat hadir”. Tetapkan expected behavior sebelum run.
5. Ubah source/version atau buat sumber yang berbeda pendapat. Tanyakan kembali dan periksa lineage aktif.
6. Uji provider timeout/unavailable. Jangan diam-diam menampilkan output rules sebagai semantic AI.
7. Rekam raw wall-clock duration dan provider/method untuk setiap case. Ukur kualitas hanya dengan label yang telah ditentukan, denominator jelas, dan hasil yang benar-benar dijalankan.

Tidak ada target F1/latency resmi dari CTO yang sudah dikonfirmasi. External benchmark PerkaraAI tidak boleh dipakai sebagai hasil kita.

## 8. Pertanyaan untuk GPT

Tolong kritisi rencana ini untuk deadline besok pukul 08.00 WIB, bukan merancang enterprise platform tanpa batas.

1. Bagaimana mengalokasikan kuota Grok dan paralelisme agar menghasilkan aplikasi, bukan berulang kali menganalisis baseline yang sama?
2. Mana vertical slice terkecil yang memenuhi dua sumber independen dan input dokumen baru? Apa yang harus benar-benar tampak di UI?
3. Apakah slice people/project/assignment + query compiler + metrics terlalu besar untuk satu builder call? Bagaimana membaginya tanpa merusak alur pengguna?
4. Apa aturan untuk menjawab saat record database berbeda dengan isi dokumen, terutama temporal context dan otoritas sumber? Hindari anggapan database selalu benar.
5. Bagaimana menghindari closed intents menjadi demo sempit yang gagal saat pertanyaan CTO berbeda? Apa trade-off terhadap query bebas yang tidak aman?
6. Apa format dokumen yang paling perlu diprioritaskan dan bagaimana membuktikannya tanpa install besar yang menghabiskan waktu?
7. Apa lima counterexample terpenting untuk acceptance? Berikan expected behavior, bukan hanya nama test.
8. Apa stop condition pengembangan agar tersedia waktu integrasi, uji real-provider dan persiapan demo?

Jangan menganggap rekomendasimu otomatis menjadi requirement baru. Bedakan fakta dari source, asumsi, usulan dan keputusan yang perlu dikonfirmasi Farros/CTO. Jangan menambahkan metrik atau klaim hasil yang belum dijalankan.

## 9. Bukti lokal untuk Codex

- Implementasi supervisor: `automation/council.py`
- Test controller: `automation/test_council.py`
- Audit read-only: `automation/challenge_council.py`
- Business contract: `DELIVERY.md`, `council/shared-business-task.md`
- Metric definitions: `docs/metrics-contract.md`
- Current implementation evidence: `.council-runs/20261110-211254-a352d8/`
- Current audit evidence: `.council-audits/20261110-211630-5125ef/`
- App provider spot check: `provider-smoke.json`

Folder evidence bersifat lokal. GPT yang hanya menerima file ini tidak otomatis bisa membuka path-path tersebut. Isi file ini tidak menyertakan credentials, database pribadi atau dokumen perusahaan.
