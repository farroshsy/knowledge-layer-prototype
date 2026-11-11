# Keputusan council

Tanggal: 2026-11-10. Ini keputusan koordinator riset setelah dua laporan independen, peta perilaku, dan sanggahan peninjau. Bukan `docs/delivery-decision.md`. Bukan sertifikat bahwa uji aplikasi saat ini lulus.

## Laporan yang dipakai

- Perancang, `research/mvp-proposal.md`: SQLite lokal, unggah, span, jawaban dari klaim terkonfirmasi. Adapter Grok CLI disebut belum diuji pada saat laporan itu ditulis.
- Peninjau, `research/risk-and-acceptance.md`: kutipan bukan kebenaran, kategori bukan fakta, enam kasus plus injeksi. Rekomendasi produknya adalah browser fixture.
- Peta perilaku dan verifikasi Microsoft, Docling, serta Gemini Notebook di `research/public-behavior-map.md` dan `research/cross-domain-references.md`.

Uji CLI pada 2026-11-10, dari folder prototipe, satu panggilan `grok -p` dengan `--json-schema`, `--max-turns 1`, `--permission-mode dontAsk`, tanpa `--always-approve`. Keluarannya memuat `structuredOutput.category` = `notulen` untuk kalimat peserta rapat. Model yang dilaporkan CLI adalah `grok-4.7-build`. Ini inferensi online lewat langganan CLI, bukan model offline. Tidak ada kunci API yang dibaca atau disimpan.

Uji kedua memakai cwd kosong dan `--system-prompt-override`. Artefak yang tersisa, `provider-smoke.json`: `method` grok, kategori `notulen`, `nonce_quote_exact` true, `grok_quote_count` 4, `warnings` kosong, `provider_error` null, `offline_model` false. Berkas itu tidak menyimpan string nonce. Log sesi koordinator: nonce `KLAYER-SMOKE-4420` lulus; percobaan `KLAYER-SMOKE-4419` gagal karena kalimat nonce tidak disalin persis. Prompt yang meminta satu klaim per kalimat, disalin persis, adalah syarat kutipan itu lolos. Satu lulus bukan akurasi semantik. Perencana kueri JSON belum di-smoke dari ujung ke ujung.

## Diterima

- Backend satu proses, SQLite, publikasi transaksional, hash, lokator, dan status job.
- Kategori (`sop`, `notulen`, `proposal`, `laporan_progres`, `other`) terpisah dari lapisan representasi. Dokumen campuran punya beberapa segmen. `other` tidak mendapat field kategori.
- Koreksi kategori membuat turunan schema lama menjadi basi. Span sumber tetap.
- Polaritas, modalitas, dan atribusi disimpan. Negasi dan rencana tidak dinaikkan menjadi kejadian.
- Konflik ditampilkan berpasangan. Bukti tidak cukup menghasilkan abstain.
- Kutipan wajib substring sumber aktif. Sitasi yang gagal dibuang, tidak digeser.
- Teks dokumen adalah data. Tidak ada SQL atau perintah dari isi dokumen.
- Fixture dan expected output hanya untuk uji. Jawaban kaleng berdasarkan nama berkas ditolak.

## Ditolak sebagai produk yang dikirim

Peninjau menganggap demo cukup berupa browser fixture. Itu tetap berguna sebagai uji, dan tidak cukup sebagai satu-satunya fungsi. `DELIVERY.md` menolak jalur itu. Produk harus mengklasifikasi dan mengekstrak unggahan sintetis baru. Kecocokan leksikal boleh ada hanya dengan label `local-rules`, dan tidak disebut ekstraksi semantik.

Azure, Docling, Postgres, antrean terdistribusi, council runtime, dan rekaman tidak masuk slice ini.

## Yang belum ditutup saat riset berhenti

`research/architecture-challenge.md` sudah ada. Isinya menerima pembedaan oracle fixture dan jalur produk, plus satu kontra-contoh nama berkas yang lulus uji beku tetapi gagal pada unggahan baru. `worker_done` untuk `ctx_c8a0ca81a559` belum terkirim: pekerja tertahan pada prompt persetujuan perintah Orca. Jangan pilih always-approve.

Sanggahan yang ada, `research/public-behavior-counterexamples.md`, menambah tiga kontrak yang keenam kasus belum mengunci. Peta perilaku sudah disesuaikan. Tiga butir itu belum berupa uji bernomor.

- Simpul turunan tidak boleh membalik polaritas atau modalitas klaim hidup. Relasinya `meniadakan`.
- Rencana tidak `mendukung` kejadian di dokumen lain, walau tanggalnya sama.
- Kalimat "hanya mendengar" melemahkan kesaksian langsung. Itu bukan saksi kedua, dan jawaban "hadir, dua sumber" gagal.

Rekomendasi peninjau agar produk hanya browser fixture tetap ditolak sebagai fungsi tunggal. Fixture tetap berguna sebagai uji.

## Batas terhadap kode yang sudah ada

Setelah draf awal keputusan ini, sesi yang sama menulis prototipe lokal di folder ini. Keputusan riset tidak mengaudit ulang kode itu dan tidak menyatakan uji saat ini lulus. Sesi sebelumnya melaporkan `python3 -m unittest tests.test_flow` sepuluh tes OK. Penutupan riset tidak menjalankan ulang uji itu.

Saat riset ditutup, proses `python3 -m klayer serve --db data/demo.sqlite --provider auto --port 8765` masih tercatat berjalan di `127.0.0.1:8765`. Penutupan ini tidak menghentikannya. Unggahan baru ke proses itu dapat memanggil Grok CLI online. Isi basis data yang di-seed sebelumnya memakai aturan lokal, bukan klaim bahwa model mengklasifikasinya.

Koordinator pengiriman di terminal `term_8a2c0e4c-6764-4ba0-95e1-a9a8eaae1bb7` tertahan pada prompt persetujuan. Jangan anggap terminal itu sedang memiliki implementasi yang hidup. Berkas ini tidak menggantikan `docs/delivery-decision.md`.

## Koreksi kebutuhan hibrida

Kebutuhan CTO adalah dua sumber yang terpisah: rekaman bisnis terstruktur yang berdiri sendiri di basis data, dan dokumen tidak terstruktur yang diunggah terpisah. Pertanyaan boleh memakai basis data saja, dokumen saja, atau keduanya. Klasifikasi hanya satu langkah. Satu dokumen boleh punya lebih dari satu kategori. Dokumen yang belum pernah dilihat akan diuji besok. Saran teknis CTO, termasuk PostgreSQL, bukan perintah untuk disalin.

Skema `klayer/store.py` hanya menyimpan notebook, dokumen, job, seksi, klasifikasi, klaim, field, dan relasi. Field dan klaim diturunkan dari teks unggahan. Tidak ada rekaman bisnis terstruktur yang independen. Notebook ini tidak memenuhi kebutuhan itu. Perluasan arsitektur ditahan sampai `council/business-process-a.md` dan `council/business-process-b.md` ditinjau. Ringkasnya ada di `council/coordinator-handoff.md`.
