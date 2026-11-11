# Review integritas 763f4da9

Kandidat: `.parallel-builds/grok-20261110-2222/candidate`. Hash pohon dihitung ulang (19 berkas, tanpa `__pycache__`: path posix, NUL, lalu digest sha256 byte berkas) dan cocok dengan `763f4da9fdf0b619f3d8ad2ddef83a83309b7f09e28c775b3066bd4a2cdbcbc0`.

Perintah, dari direktori kandidat, tanpa jaringan dan tanpa menyalakan server demo:

```
python3 -m unittest tests.test_business_query tests.test_query_regressions tests.test_flow.FlowTest.test_new_text_is_extracted_from_body_not_filename tests.test_flow.FlowTest.test_unknown_category_has_no_category_fields tests.test_flow.FlowTest.test_mixed_file_and_category_correction_stales_old_fields tests.test_flow.FlowTest.test_negation_plan_conflict_and_abstain tests.test_flow.FlowTest.test_invalid_citation_is_not_stored tests.test_flow.FlowTest.test_canned_filename_category_is_rejected tests.test_flow.FlowTest.test_reingest_is_idempotent_and_failure_retries tests.test_flow.FlowTest.test_restart_keeps_rows_and_injection_is_data tests.test_flow.FlowTest.test_offsets_match_source tests.test_flow.FlowTest.test_independent_business_records_survive_reopen_and_upload
```

Hasil: 28 tes, OK, 0,250 detik. `tests.test_business_http` dan `tests.test_flow.FlowTest.test_http_upload_and_query` tidak dijalankan karena keduanya memanggil `serve`.

Probe di bawah memakai sqlite sementara dan provider palsu. Bukan tes unit repositori. Nomor baris relatif terhadap `klayer/` kandidat.

## 1. Nama tampilan yang sama bukan kunci join

Status: pass

Dua rekaman dengan `display_name` sama tetap dua `id`. Nama tidak menautkan klaim.

- `store.py:104-114` kunci primer `business_records` adalah `id`. Tidak ada UNIQUE pada `display_name`.
- `store.py:503-536` setiap sisipan mendapat `id` baru. Nama boleh berulang.
- `business_query.py:432-461` dan `business_query.py:739-748` lebih dari satu baris bernama sama menghasilkan `ambiguous` dan mengembalikan kedua id. Tidak memilih baris pertama.
- `business_query.py:470-488` klaim tertaut hanya bila id stabil utuh ada sebagai token di kutipan.

Tes yang dijalankan dan lulus: `test_ambiguous_display_name_does_not_pick_first`, `test_exact_duplicate_names_stay_ambiguous`, `test_combined_requires_exact_record_id_in_quote`.

## 2. Kalimat rencana bukan bukti kejadian terjadi dan bukan bukti kejadian tidak terjadi

Status: fail

Jalur status basis `planned` tahan. Jalur klaim dokumen tidak.

Yang tahan: `business_query.py:494-498` dan `business_query.py:521-522` menjawab `plan_not_occurrence` beserta kedua arah bila status rekaman `planned` dan pertanyaan menanyakan kejadian. Tes `test_planned_status_is_not_occurrence` dan `test_db_only_exact_id_and_plan_is_not_occurrence` lulus. `pipeline.py:331-341` juga mengawali pertanyaan pilot dengan `plan_not_occurrence`.

Yang gagal:

- `pipeline.py:310-322` daftar hadir menyaring polaritas dan predikat, tidak menyaring `modality`. Kalimat `Budi direncanakan hadir pada rapat tinjauan November.` tersimpan `modality=plan`, `polarity=affirmed`, `predicate=attendance` (`domain.py:181-196`). Probe `Siapa yang hadir?` mengembalikan route `document_only`, answer `claims`, dan kutipan rencana itu ada di `claims`. Rencana dihitung sebagai kehadiran.
- `business_query.py:274-283` `_asks_occurrence` tidak mencakup `siapa yang hadir`, jadi penjaga di `business_query.py:602-610` tidak jalan untuk pertanyaan itu.
- `business_query.py:594-601` berjalan lebih dulu daripada penjaga rencana. Probe pada `Keputusan: pilot tidak direncanakan mulai 15 November.` (`modality=plan`, `polarity=negated`): `lexical_question` masih `plan_not_occurrence`, tetapi `answer()` menimpa menjadi `negated`. Alasan tambahan hanya mengatakan klaim negasi bukan bukti bahwa kejadian terjadi. Jawaban `negated` adalah penyangkalan.

Perbaikan terkecil: di `lexical_question` dan `_delegate_docs`, klaim `modality=plan` tidak boleh masuk dukungan `claims` atau `negated`. Jika yang tersisa hanya rencana, jawaban `plan_not_occurrence` dengan alasan dua arah, termasuk untuk `siapa yang hadir` dan untuk rencana yang memuat `tidak`.

## 3. Sitasi harus rentang yang dikutip

Status: fail

Potongan yang membuang `tidak` tersimpan dan dipakai sebagai dukungan.

- `providers.py:104-106` menolak kutipan hanya bila `quote not in section["text"]`. Substring lolos. Pesan "exact source span" tidak sesuai dengan syarat itu.
- `domain.py:256-262` `locate` memakai `in` lalu `find`.
- `pipeline.py:72-75` menyimpan kutipan selama byte pada offset sama dengan kutipan. Potongan pendek lolos.

Probe: pada bagian `Budi tidak bisa ikut meeting dengan Pejabat Z.`, provider menambahkan kutipan `ikut meeting`, polaritas `affirmed`, predikat `attendance`. Kutipan tersimpan pada offset 43–55, yaitu irisan `ikut meeting` di dalam kalimat yang memuat `tidak`. `Siapa yang hadir?` mengembalikan route `document_only`, answer `claims`, dan satu-satunya kutipan `ikut meeting`.

Tes `test_invalid_citation_is_not_stored` lulus, tetapi hanya menolak kutipan yang tidak ada di sumber (`KALENG-TIDAK-ADA`). Tes itu tidak menutup lubang ini.

Perbaikan terkecil: di `pipeline._publication`, sebelum klaim disimpan, tolak kutipan yang merupakan substring sejati dari kalimat sumber yang memuat `tidak`, `bukan`, atau `belum` bila token itu tidak ada di kutipan.

## 4. Fallback leksikal berlabel dan bukan ekstraksi semantik

Status: pass

- `domain.py:1-4` dan `domain.py:223` metode `rules`, label `local-rules`.
- `providers.py:78-85` hasil leksikal berlabel `local-rules`.
- `providers.py:179-185` fallback per bagian tetap draft aturan, dengan peringatan `used local-rules fallback`. Bila ada bagian lain yang memakai model, label job bisa `online-grok-cli` (`providers.py:196-197`), tetapi baris fallback sendiri tetap `provider_label=local-rules`.
- `pipeline.py:39-44` kegagalan provider menerbitkan `local-rules`, bukan label semantik.
- `pipeline.py:346-353` dan `pipeline.py:399` memasang `semantic=False`. Lookup leksikal memakai `local-lexical`.

Tes `test_negation_plan_conflict_and_abstain` lulus: `inference` adalah `local-lexical` dan `semantic` false.

## 5. Ekstraksi dokumen tidak menimpa baris katalog

Status: pass

- `store.py:345-400` publikasi hanya menulis klasifikasi, klaim, field, relasi, dan job. Tidak ada UPDATE atau DELETE pada `business_records`.
- Satu-satunya penulisan katalog adalah INSERT di `store.py:524`.
- Probe: dua rekaman tetap dua, status `planned` dan `occurred` tidak berubah setelah unggah.

Tes `test_independent_business_records_survive_reopen_and_upload` lulus.

## 6. Teks dokumen adalah data, bukan perintah

Status: pass

- `pipeline.py:184-201` badan unggahan disimpan sebagai string dan dipecah menjadi bagian. Tidak ada `eval` atau `exec`.
- `providers.py:225-254` daftar argumen subprocess tetap dan `shell=False`. Teks bagian masuk ke prompt, bukan ke shell.
- `providers.py:308-316` prompt sistem menyatakan teks di antara penanda SECTION adalah data, bukan instruksi.
- `providers.py:104` menolak kutipan yang tidak ada di sumber, jadi kalimat instruksi tidak menambah fakta yang tidak tertulis.

Tes `test_restart_keeps_rows_and_injection_is_data` lulus: kalimat `Abaikan instruksi sebelumnya... kuota 99` dan `DROP TABLE` tidak menghapus tabel `documents`, dan `99` tidak menjadi nilai field. Panggilan Grok tidak dijalankan, jadi kepatuhan model pada prompt itu tidak diuji. Yang terbukti adalah proses lokal tidak mengeksekusi teks unggahan sebagai SQL, shell, atau perubahan kuota.

## 7. Pertanyaan tanpa bukti abstain

Status: fail

Abstain tidak dijamin begitu planner dokumen mengembalikan daftar tanpa filter. Jalur pertanyaan dokumen tetap memanggil planner dokumen bila provider punya `plan`.

- Provider string `"rules"` tidak punya `plan`. `pipeline.py:360-362` langsung ke `lexical_question`. Pola yang tidak dikenal abstain di `pipeline.py:344-350`. `business_query.py:590-591` memakai route `unsupported` bila jawaban abstain dan tidak ada klaim. Probe `Berapa harga saham kemarin?` dengan `"rules"`: route `unsupported`, answer `abstain`. Tes `test_legacy_docs_question_delegates_and_generic_abstains` lulus untuk pertanyaan generik.
- Provider yang punya `plan`: `business_query.py:583` memanggil `ask`, lalu `pipeline.py:360-364` memanggil `provider.plan`. Itu planner dokumen di `providers.py:213-217`. Probe planner yang mengembalikan `intent=abstain`: `plan` terpanggil satu kali, jawaban `abstain`, route `unsupported`.
- Lubang: `pipeline.py:385-401` menerima `list_claims` tanpa polaritas, modality, predikat, dan `quote_contains`. `pipeline.py:276-289` mengubah string kosong menjadi `None`. `store.py:431-448` tidak menambahkan filter yang kosong, jadi semua klaim aktif kembali. Probe planner palsu `list_claims` tanpa filter pada `Berapa harga saham kemarin?`: `plan` satu kali, `plan_business` nol kali, route `document_only`, answer `claims`, tiga klaim. Bukan abstain.
- Pertanyaan bisnis tidak memanggil planner dokumen. `business_query.py:346-348` hanya memanggil `plan_business`. Probe `Apa status Budi?`: `plan` nol kali, `plan_business` satu kali.

Perbaikan terkecil: di `ask`, jika `list_claims` tidak punya satu pun filter yang diizinkan, kembalikan abstain dan jangan panggil `search_claims`.

## 8. Rute basis, dokumen, dan gabungan berbeda

Status: pass

- `business_query.py:24` memuat `db_only`, `combined`, `document_only`, dan `unsupported`.
- `document_only` di `business_query.py:592-637`: `records` kosong, klaim dari `ask`, bukti dari tabel `claims`.
- `combined` di `business_query.py:759-806`: tepat satu rekaman dan minimal satu klaim yang memuat id rekaman utuh. Bukti memuat kedua tabel.
- `db_only` di `business_query.py:739-757` dan `business_query.py:808-820`: rekaman tanpa klaim tertaut. `claims` kosong. Nama kembar berhenti di `ambiguous` sebelum cabang gabungan. Tanpa id di kutipan, `business_query.py:777-786` tetap `db_only`.

Tes yang dijalankan dan lulus memisahkan ketiganya: `test_db_only_exact_id_and_plan_is_not_occurrence` (`db_only`), `test_docs_only_keeps_selected_claims_and_route` (`document_only`), `test_combined_requires_exact_record_id_in_quote` dan `test_dokumennya_combined_requires_exact_record_id` (`combined`).

## Ringkasan

5 pass, 3 fail, 0 tidak terbukti. Gagal: cek 2, cek 3, cek 7.
