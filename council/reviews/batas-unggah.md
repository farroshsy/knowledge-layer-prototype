# Batas unggah

Kandidat: `.parallel-builds/grok-20261110-2222/candidate`.
Sumber di bawah relatif terhadap folder kandidat itu.
Tidak ada berkas lain yang diubah. Timeout tidak dinaikkan.

## Terlihat di kode

### Jenis berkas yang diterima endpoint unggah

Endpoint unggah adalah `POST /api/notebooks/<id>/documents` di `klayer/server.py:182-194`.
Badan permintaan hanya JSON lewat `_read_json` (`klayer/server.py:82-102`).
Tidak ada `multipart`, tidak ada unggah biner, dan tidak ada pemeriksaan MIME berkas.

Field yang dibaca:

- `text` — string isi dokumen (`klayer/server.py:189`). Kosong ditolak: `klayer/pipeline.py:190-191`.
- `filename` — label teks, bawaan `catatan.txt` bila kosong (`klayer/server.py:188`). Di simpanan, label kosong menjadi `untitled.txt` (`klayer/store.py:219`).
- Label tidak boleh berisi garis miring, garis miring terbalik, atau diawali titik (`klayer/pipeline.py:194-195`). Tidak ada daftar putih ekstensi di server.
- Panjang teks maksimal 200000 karakter (`klayer/pipeline.py:12`, `klayer/pipeline.py:192-193`).
- Badan HTTP maksimal 250000 byte (`klayer/server.py:22`, `klayer/server.py:93-94`).

Isi selalu dipotong sebagai teks biasa di `parse_sections` (`klayer/domain.py:79-120`): pecah pada baris kosong, offset menunjuk ke badan asli. Tidak ada dekode format lain.

Gerbang peramban lebih sempit daripada server:

- Pemilih berkas membatasi `.txt`, `.md`, `text/plain`, dan `text/markdown` (`klayer/static/index.html:186`).
- Skrip menolak nama yang tidak berakhiran `.txt` atau `.md` (`klayer/static/index.html:780-784`), lalu membaca berkas sebagai teks ke kotak (`klayer/static/index.html:787-789`).
- Tombol unggah mengirim JSON `filename` dan `text`, bukan berkas mentah (`klayer/static/index.html:802-808`).

Benih CLI hanya membaca `*.md` (`klayer/__main__.py:19-20`).

Yang masuk endpoint adalah teks UTF-8 di JSON plus label nama. UI hanya membuka TXT/MD. Server tidak menolak label berekstensi lain bila `text` tetap string.

### Di mana timeout Grok 75 detik

- Bawaan adapter: `GrokCliProvider.__init__` dengan `timeout: int = 75` di `klayer/providers.py:204-205`.
- Ekstraksi dokumen memakai `self.timeout`: `klayer/providers.py:207-208`.
- Perencana dokumen `plan` memakai `self.timeout`: `klayer/providers.py:213-214`.
- `subprocess.run` menerima `timeout=timeout` di `klayer/providers.py:248-253`.
- `TimeoutExpired` menjadi `ProviderError` dengan teks `grok timed out after {timeout}s` di `klayer/providers.py:259-260`.
- `build_provider("grok")` dan `build_provider("auto")` membuat `GrokCliProvider()` tanpa argumen, jadi 75 detik (`klayer/providers.py:333-339`).
- Perintah `serve` tidak punya flag timeout (`klayer/__main__.py:75-80`). Provider server datang dari `build_provider` (`klayer/__main__.py:28`).
- Hanya `smoke` yang memajukan angka itu: `--timeout` bawaan 75 (`klayer/__main__.py:84`) lalu `GrokCliProvider(timeout=args.timeout)` (`klayer/__main__.py:47`).

Kunci `_GROK_LOCK` mengurung `subprocess.run` (`klayer/providers.py:246-258`). Panggilan Grok lain menunggu sampai proses itu selesai atau timeout.

### Apa yang terjadi saat timeout

Timeout pada ingest (unggah lewat `process_job`), bila provider adalah `GrokCliProvider`:

1. `_call_grok` melempar `ProviderError` berisi `grok timed out after 75s` (`klayer/providers.py:259-260`). `extract` tidak menangkapnya (`klayer/providers.py:207-211`).
2. `_run_provider` menangkap `ProviderError` (`klayer/pipeline.py:37-45`).
3. Fallback adalah `lexical_outcome`: metode `rules`, label `local-rules` (`klayer/providers.py:78-85`).
4. Lalu `provider_error` diisi pesan kekecualian, peringatan `online provider failed; published local-rules output`, metode tetap `rules`, label tetap `local-rules` (`klayer/pipeline.py:41-45`).
5. Draf leksikal memakai `provider_label` `local-rules` (`klayer/domain.py:223`, `klayer/domain.py:238`, `klayer/domain.py:248`).
6. Publikasi menyalin `provider_error` (`klayer/pipeline.py:122-124`). Job ditandai `completed`, bukan `failed`, beserta `provider_label` dan `provider_error` (`klayer/store.py:329-335`).

Ini khusus `ProviderError`. Kekecualian lain di `process_job` membuat job `failed` (`klayer/pipeline.py:182-183`). Di uji, `RuntimeError("parser exploded")` menggagalkan job (`tests/test_flow.py:194-210`), bukan fallback `local-rules`.

Jalur lain tidak memakai label `local-rules` yang sama:

- Pertanyaan dokumen lewat `ask`: `ProviderError` dari `provider.plan` jatuh ke `lexical_question` dan field `provider_error` (`klayer/pipeline.py:374-382`). Inferensi menjadi `local-lexical` (`klayer/pipeline.py:366-367`), bukan label job `local-rules`.
- Perencana bisnis hanya `plan_business`. `ProviderError` dikembalikan sebagai string (`klayer/business_query.py:341-353`). Bila metode akhir `rules`, alasan ditambah `planner fallback:` plus pesan itu (`klayer/business_query.py:799-800` dan `klayer/business_query.py:818-819`). Pola yang sama ada di `tests/test_query_regressions.py:221-233`.
- `smoke` memanggil `extract` langsung (`klayer/__main__.py:47`). `_smoke` tidak punya `try` (`klayer/__main__.py:38-68`). Timeout di smoke tidak masuk `_run_provider`, jadi tidak menulis fallback `local-rules`. `ProviderError` keluar dari proses. Cabang `provider_error` di `klayer/__main__.py:67-68` hanya jalan bila `extract` mengembalikan objek.

Fallback per bagian di `merge_model_with_rules` (`klayer/providers.py:179-185`) lain: itu bila model sudah menjawab tetapi draf tidak sah. `provider_error` di sana tetap kosong (`klayer/providers.py:195`). Timeout tidak sampai ke merge karena `_call_grok` sudah melempar.

### Apakah PDF, DOCX, atau gambar punya parser

Tidak. Di kode kandidat tidak ada parser PDF, DOCX, PNG, JPEG, atau pustaka format itu. Satu-satunya parser isi adalah `parse_sections` untuk string (`klayer/domain.py:79-120`), dipanggil dari unggah (`klayer/pipeline.py:196-198`). Nama berkas tidak memilih parser.

### Apakah pertanyaan bisnis tanpa isyarat dokumen masih memanggil provider dokumen

Tidak, untuk pertanyaan yang sudah masuk jalur bisnis dan tanpa isyarat dokumen.

Isyarat dokumen adalah `_mentions_documents` (`klayer/business_query.py:252-260`): dokumen, docs, klaim, notulen, quote, sumber teks, catatan.

Provider dokumen adalah `provider.plan` di dalam `ask` (`klayer/pipeline.py:371-378`). `GrokCliProvider.plan` memanggil `_call_grok` dengan skema dokumen (`klayer/providers.py:213-214`, skema di `klayer/providers.py:282-293`).

Jalur bisnis hanya boleh memanggil `plan_business` (`klayer/business_query.py:341-349`). Komentar di situ menolak pemakaian perencana dokumen karena skemanya beda. `GrokCliProvider` tidak punya `plan_business`; yang ada `extract` dan `plan` (`klayer/providers.py:207-217`). Bila `plan_business` tidak ada, fungsi kembali tanpa memanggil model (`klayer/business_query.py:347-349`). Lalu `_rules_plan` (`klayer/business_query.py:716-718`).

Syarat masuk jalur itu di `answer` (`klayer/business_query.py:679-711`): kata rekaman, status, orang, person, pekerjaan, atau nama (`klayer/business_query.py:264-270`), id, nama tersimpan, atau nama kandidat, dan provider bukan `None` atau `rules`. Tanpa kata dokumen, aturan tidak memilih `link_claims` (`klayer/business_query.py:398-401` dan `klayer/business_query.py:767`). Hasilnya `db_only`, bukan `ask()`.

Uji di berkas, belum dijalankan pada tugas ini, mengunci hal yang sama:

- Objek yang hanya punya `plan` berbentuk SQL, untuk pertanyaan status rekaman, tetap menghasilkan metode `rules` (`tests/test_query_regressions.py:235-246`). `provider.plan` tidak dipakai.
- Pertanyaan status nama memanggil `plan_business`, bukan `plan` (`tests/test_business_query.py:214-230`).
- Pertanyaan di luar rekaman dan di luar pola dokumen membuat `plan` tetap nol panggilan (`tests/test_business_query.py:179-199`).

Pengecualian yang tetap memanggil provider dokumen, meski tanpa kata dokumen:

- `_is_legacy_docs_question` benar untuk `hadir` atau `ikut`, atau untuk `pilot` bersama `berjalan`, `sudah`, atau `terjadi`, selama tidak ada kata rekaman dan tidak ada id (`klayer/business_query.py:287-303`).
- Itu langsung `_delegate_docs` (`klayer/business_query.py:661-662`), dan `_delegate_docs` memanggil `ask` (`klayer/business_query.py:576-584`).
- Contoh di uji: `siapa yang hadir?` dengan `DocsPlanner.plan` berakhir `delegated` sama dengan `docs_ask` (`tests/test_business_query.py:164-168` dan `tests/test_business_query.py:243-252`). `Apakah pilot sudah berjalan?` juga jalur dokumen (`klayer/business_query.py:291`, uji `tests/test_business_query.py:209-212`).

Ringkas: pertanyaan bisnis (status, rekaman, nama, atau id) tanpa isyarat dokumen tidak memanggil `provider.plan`. Pertanyaan pola dokumen lama tanpa kata dokumen tetap memanggilnya.

## Tidak diuji live pada tugas ini

- Server tidak dijalankan. Tidak ada unggah TXT, MD, PDF, DOCX, atau gambar ke endpoint.
- Timeout 75 detik tidak dipicu pada CLI Grok. Tidak dicek apakah proses berhenti pada detik ke-75, atau apakah job selesai `completed` dengan `provider_error` berisi `grok timed out after 75s`.
- `smoke --timeout 75` tidak dijalankan. Perilaku lempar `ProviderError` di smoke hanya dibaca dari tidak adanya `try`.
- `tests/test_flow.py`, `tests/test_business_query.py`, dan `tests/test_query_regressions.py` tidak dijalankan. Kutipan uji di atas adalah isi berkas, bukan hasil eksekusi tugas ini.
- Tidak dicek di peramban apakah UI menolak PDF. Yang terlihat hanya atribut `accept` dan cek akhiran nama.
