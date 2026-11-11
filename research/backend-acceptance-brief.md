# Arahan pengguna: backend sebagai fokus utama

Pengguna menegaskan backend dan fondasi arsitektur sebagai prioritas. Ini bukan otorisasi untuk membangun semua fitur enterprise. Target tetap demo lokal besok 08.00 WIB, dummy docs, research sebelum implementasi. Reviewer independen harus menantang proposal, bukan sekadar menyetujui. Telusuri author-thread-leads.md termasuk permalink post target yang kini berhasil dibaca via mirror.

## Kontrak yang perlu diputuskan council

1. Domain dan ontology: bedakan kategori dokumen, struktur, pernyataan beratribusi, klaim, premis dan sintesis. Definisikan relasi, negasi, modalitas (rencana vs kejadian), dukungan dan konflik. Jangan naikkan klaim menjadi fakta tanpa dasar.
2. Data: dokumen asli immutable atau versioned, hash/identitas stabil, lokasi sumber (halaman/section/offset), derived nodes dan lineage yang valid. Pembaruan atau penghapusan sumber tidak meninggalkan jawaban aktif dengan provenance usang.
3. Ingestion: validasi jenis/ukuran, parsing dan error eksplisit, state yang bermakna, retry aman/idempotent, transaksi untuk publikasi hasil yang utuh. Jangan perlu Redis/microservice bila job persisten SQLite dan single worker cukup untuk demo; keputusan harus diuji.
4. AI boundary: provider adapter terpisah dari domain, structured output schema, kutipan/ID sumber divalidasi sebelum disimpan, timeout/error, keluaran AI tidak boleh menjadi SQL/command bebas. Document prompt injection diperlakukan sebagai konten, bukan instruksi aplikasi.
5. Query: retrieval dari representasi terstruktur dan sumber relevan, jawaban mencantumkan sumber, evidence yang tidak cukup menghasilkan abstention. Konflik ditampilkan, tidak diputuskan diam-diam. Token/context dibatasi dengan penjelasan coverage; jangan klaim membaca semua dokumen bila tidak.
6. API: kontrak upload/process/status/layers/source/query yang konsisten, input validation dan error codes, tidak membaca arbitrary filesystem path dari request. Bind lokal loopback, tanpa klaim aman untuk multiuser/production.
7. Evaluasi: happy path, reingest dokumen sama, proses gagal, kutipan invalid, pernyataan negatif, sumber bertentangan, pertanyaan tanpa jawaban, serta data persisten setelah restart. Expected outputs dummy ditetapkan sebelum test model; pisahkan tes pipeline dari semantic accuracy.
8. Operasional minimal: satu perintah start, konfigurasi tanpa secrets di repo, logs yang cukup tanpa dokumen sensitif, catatan keterbatasan. Provider live harus dibuktikan jika diiklankan; mode fixture/precomputed wajib berlabel.

## Deliverable council

Desainer mengusulkan schema, API, pipeline, invariants dan acceptance tests. Reviewer memberi counterexample yang bisa diuji. Satu putaran revisi dengan alasan diterima/ditolak per poin, bukan voting. Pilih satu vertical slice yang sungguh bekerja end-to-end sebelum memperluas format atau fitur. UI cukup untuk membuktikan alur backend dan source inspection.

## Catatan kontrol agent

Layar coordinator terlihat always-approve aktif tak terduga saat interaksi izin. Hindari mode izin menyeluruh; jangan approve hooks/secret access/global changes. Dua worker independen terlihat ada di folder prototype, tetapi hasil riset dan review belum terverifikasi saat catatan ini dibuat. Root chat tidak memiliki ORCA_TERMINAL_HANDLE untuk menjadi coordinator terstruktur; coordinator Grok di terminal Orca menjalankan council dengan identitasnya sendiri.
