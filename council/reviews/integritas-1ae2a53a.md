# Review integritas 1ae2a53a

Kandidat: `.parallel-builds/grok-20261110-2222/candidate`. Hash pohon dihitung ulang, 19 berkas, tanpa `__pycache__`: path relatif posix terurut, byte path, NUL, lalu digest sha256 mentah isi berkas. Hasil `1ae2a53a2642d31283b87ef35e332e2fd2753b9a70374d371515cf3775462401`. Cocok dengan hash yang diklaim. Review tidak berhenti di hash.

Perintah, dari direktori kandidat, tanpa menyalakan server demo:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_business_query tests.test_query_regressions tests.test_flow tests.test_business_http
```

Hasil yang saya jalankan: 38 tes, OK, 3,460 detik. Ada ResourceWarning soket tidak ditutup pada pembersihan `tests.test_business_http`, plus HTTPError 404 dan 400. Bukan pengulangan angka 3,488 detik pada 11 Nov 2026 00:07 WIB; itu catatan koordinator, bukan keluaran sesi ini.

Probe di bawah memakai sqlite sementara dan provider palsu. Bukan tes unit repositori. Tes 38 tidak memuat probe yang gagal.

## Yang lulus

### Rencana bertanda `modality=plan` tidak lagi menjadi daftar hadir

Probe `Budi direncanakan hadir pada rapat tinjauan November.` lalu `Siapa yang hadir?` dan `Apakah Budi hadir?`: route `document_only`, answer `plan_not_occurrence`, kutipan rencana tetap ada, alasan dua arah. Bukan `claims`.

Campuran `Budi direncanakan hadir pada rapat November. Siti hadir pada rapat tinjauan.` pada `Siapa yang hadir?`: satu kutipan, hanya `Siti hadir pada rapat tinjauan.` Rencana tidak masuk.

`Keputusan: pilot tidak direncanakan mulai 15 November.` pada `Apakah pilot sudah berjalan?`: answer `plan_not_occurrence`, bukan `negated`.

- `klayer/pipeline.py:326-334` klaim hadir yang semuanya `modality=plan` menjadi `plan_not_occurrence`, bukan `claims`.
- `klayer/pipeline.py:345-351` pertanyaan pilot yang bertanya kejadian memakai filter `modality=plan` dan label yang sama.
- `klayer/business_query.py:274-284` `_asks_occurrence` mencakup `siapa`/`who` plus `hadir`/`ikut`.
- `klayer/business_query.py:591-597` jika semua klaim dokumen adalah rencana, jawaban `plan_not_occurrence` dipasang sebelum cabang negasi. Rencana yang memuat `tidak` tidak ditimpa menjadi `negated` pada `Apakah Budi hadir?` (probe: `plan_not_occurrence`).

Tes dalam 38 yang mengunci pola ini dan lulus: `test_planned_attendance_is_not_presence`, `test_negated_plan_is_not_a_denial_of_occurrence`.

### Kutipan yang memotong `tidak`, `bukan`, atau `belum` di dalam satu kalimat terdeteksi tidak disimpan

Probe provider yang menambahkan kutipan `ikut meeting` pada `Budi tidak bisa ikut meeting dengan Pejabat Z.`: kutipan pendek tidak ada di klaim aktif. Yang tersimpan kalimat utuh berpolaritas `negated`. Hal yang sama untuk `bukan` dan `belum`: `quote_drops_negation` benar, `Siapa yang hadir?` abstain.

- `klayer/domain.py:256-266` menolak kutipan yang merupakan substring sejati dari kalimat `_sentences` yang memuat token itu, bila token tidak ada di kutipan.
- `klayer/pipeline.py:76-78` memakai penolakan itu sebelum klaim ditulis.
- `klayer/providers.py:104-106` masih hanya menolak kutipan yang tidak ada sebagai substring. Penjaga yang menyimpan ada di pipeline, bukan di pesan "exact source span".

Tes `test_quote_that_drops_tidak_is_not_stored` lulus. Tes itu hanya kalimat satu baris dan kutipan `ikut meeting`.

### Pertanyaan generik tanpa kata dokumen dan tanpa rekaman abstain, tanpa planner dokumen

Probe `Berapa harga saham kemarin?` lewat `answer()`, provider punya `plan` yang mengembalikan `list_claims` tanpa filter: route `unsupported`, answer `abstain`, `plan` nol kali, `plan_business` nol kali. Planner yang mengembalikan `intent=abstain` pada kalimat yang sama juga abstain.

- `klayer/business_query.py:735-744` operasi bisnis `abstain` yang bukan pertanyaan dokumen lama dan bukan dokumen polos berhenti di `unsupported`. Tidak memanggil `ask`.
- `klayer/pipeline.py:385-398` bila `ask` benar-benar dipanggil dan planner abstain, lalu pola leksikal tidak punya klaim, jawabannya abstain.

Tes `test_unrelated_question_abstains_without_document_planner` dan `test_legacy_docs_question_delegates_and_generic_abstains` lulus. Keduanya tidak mengirim `list_claims` tanpa filter.

## Yang masih gagal

### 1. Bukan semua kalimat rencana keluar dari kehadiran

`Budi akan hadir pada rapat tinjauan November.` tersimpan `modality=asserted`, `polarity=affirmed`, `predicate=attendance`. `Siapa yang hadir?`: route `document_only`, answer `claims`, satu-satunya kutipan kalimat `akan`. Ini dihitung hadir.

- `klayer/domain.py:183-186` rencana hanya `direncanakan`, `rencana`, atau `dijadwalkan`. `akan` tidak masuk.
- `klayer/pipeline.py:313-324` lalu memakai polaritas `affirmed` dan predikat `attendance`, tanpa melihat `akan`.

`Siapa yang hadir?` pada satu-satunya klaim `Budi tidak direncanakan hadir pada rapat November.` (`negated`, `plan`, `attendance`): route `unsupported`, answer `abstain`, nol klaim, alasan `no active claim matches the filters`. Bukan `claims` dan bukan `negated`, tetapi juga bukan `plan_not_occurrence`. Rencana yang memuat `tidak` disaring habis sebelum cabang rencana.

- `klayer/pipeline.py:316-322` pertanyaan `siapa` memaksa `polarity=affirmed` sebelum pemisahan modality di `klayer/pipeline.py:326-334`.
- `klayer/business_query.py:592-593` abstain tanpa klaim menjadi `unsupported`.

`Siapa yang tidak hadir?` dan `Siapa yang belum hadir?` pada korpus `Budi hadir pada rapat tinjauan November.` plus `Siti tidak bisa ikut meeting dengan Pejabat Z.`: answer `claims`, satu kutipan `Budi hadir pada rapat tinjauan November.` Penyangkalan Siti tidak keluar. Kata `tidak`/`belum` di pertanyaan tidak dibaca; cabang `siapa` tetap meminta kehadiran affirmed.

`klayer/domain.py:303-315` `conflicting_pairs` memasangkan predikat `attendance` yang polaritasnya berlawanan tanpa membuang `modality=plan`. Dipanggil dari `klayer/pipeline.py:180`. Ini tidak saya jalankan sebagai probe banding. Dari kode, rencana tetap bisa menjadi salah satu sisi konflik kehadiran.

### 2. Kutipan yang membuang `tidak` masih bisa tersimpan dan menjadi jawaban hadir

Tiga probe. `quote_drops_negation` hanya benar bila kutipan duduk di dalam satu hasil `_sentences` dan kutipan itu sendiri tidak memuat `tidak`/`bukan`/`belum`.

Baris baru, provider `rules`, tanpa kutipan tambahan. Teks `Budi tidak` lalu baris `bisa ikut meeting dengan Pejabat Z.` Klaim tersimpan hanya `bisa ikut meeting dengan Pejabat Z.`, polaritas `affirmed`, predikat `attendance`. `Siapa yang hadir?`: answer `claims`, kutipan itu satu-satunya. `quote_drops_negation` pada kutipan itu false.

- `klayer/domain.py:147` pemecah kalimat `[^.!?\n]+(?:[.!?]|$)` tidak mengeluarkan baris `Budi tidak` karena baris itu tidak berakhir tanda titik dan bukan akhir string. Token `tidak` hilang, bukan jadi klaim negasi.
- `klayer/domain.py:182-194` sisa baris yang memuat `ikut meeting` menjadi kehadiran affirmed.
- `klayer/domain.py:261-266` tidak menolak, karena kutipan bukan substring kalimat yang masih memuat token negasi.

Lintas titik, provider menambah kutipan `hadir. Rapat selesai dengan baik.` pada `Budi tidak hadir. Rapat selesai dengan baik.` `quote_drops_negation` false. Kutipan tersimpan `affirmed` / `attendance` di samping `Budi tidak hadir.` yang `negated`. `Siapa yang hadir?` hanya mengembalikan kutipan yang memotong `tidak`, answer `claims`.

Kutipan `hadir. Keputusan: tidak ada anggaran rapat.` pada `Budi tidak hadir. Keputusan: tidak ada anggaran rapat.` memotong `tidak` yang mengikat `hadir`, tetapi masih memuat `tidak` yang lain. `klayer/domain.py:261` langsung mengembalikan false. Kutipan tersimpan affirmed. `Siapa yang hadir?`: answer `claims`, kutipan itu.

Polaritas tidak dicek ulang terhadap kutipan. Provider yang mengirim kalimat utuh `Budi tidak bisa ikut meeting dengan Pejabat Z.` dengan `polarity=affirmed` menyimpannya affirmed. `Siapa yang hadir?`: answer `claims`, kutipan yang masih berisi `tidak`. Ini bukan pemotongan kata; ini lubang di gerbang yang sama.

- `klayer/pipeline.py:79-87` menulis `polarity` dari draf apa adanya setelah cek rentang dan `quote_drops_negation`.

### 3. Pertanyaan tanpa bukti masih bisa mengembalikan semua klaim

`ask` tetap menjalankan `list_claims` tanpa satu pun filter. String kosong menjadi `None`. `search_claims` tidak menambah klausa yang kosong, jadi semua klaim aktif kembali, answer `claims`.

Probe `ask` pada `Berapa harga saham kemarin?`, planner `list_claims` dengan polaritas, modality, predikat, dan `quote_contains` kosong: `plan` satu kali, answer `claims`, tiga klaim, termasuk `Keputusan: pilot direncanakan mulai 15 November.`

Probe `answer` pada `Berapa harga saham di dokumen kemarin?` dengan planner yang sama: `plan` satu kali, `plan_business` nol, route `document_only`, answer `claims`, dua klaim kehadiran (`Budi hadir...` dan `Siti tidak bisa ikut meeting...`). Bukan abstain. Kata `dokumen` cukup untuk masuk jalur dokumen.

Probe `answer` pada `Siapa yang hadir?` dengan planner yang sama: answer `claims` memuat kehadiran affirmed dan penyangkalan Siti. Filter leksikal `siapa` tidak terpakai, karena planner mengembalikan baris.

- `klayer/pipeline.py:399-411` tidak menolak `list_claims` yang semua filternya kosong, lalu memanggil `structured_query`.
- `klayer/pipeline.py:279-292` dan `klayer/store.py:431-446` filter kosong tidak mempersempit.
- `klayer/business_query.py:307-315` dan `klayer/business_query.py:666-677` kata dokumen membuat `docs_only`.
- `klayer/business_query.py:661-662` `siapa`/`hadir` langsung ke `_delegate_docs`, yang memanggil `ask`.
- `klayer/business_query.py:591-601` hanya membuang `modality=plan` bila ada klaim lain. Sisa daftar tetap answer `claims`.
- `klayer/providers.py:282-300` skema dan prompt mengizinkan filter kosong. Kode tidak memaksa abstain bila model mengirim `list_claims` kosong.

`klayer/business_query.py:644` menyertakan objek `docs` mentah dari `ask`. Pada probe saham lewat `ask`, objek itu answer `claims` beserta rencana. Saya tidak mencetak isi `docs` pada probe `answer`; yang terukur di jawaban atas adalah `answer` dan `claims` tingkat atas.

## Yang tidak boleh diklaim

Yang tidak boleh diklaim: hash `1ae2a53a…` sudah menutup tiga cacat itu, karena rencana ber-`akan`, kutipan yang memotong `tidak` lewat batas kalimat atau baris, dan `list_claims` tanpa filter masih menghasilkan jawaban `claims` bukan abstain.
