# Ledger — metrik yang benar-benar terlihat

Tanggal olahan: 10 November 2026. Status: hasil pengukuran lokal. Bukan spesifikasi CTO. Angka pos publik Perkara tidak masuk sebagai baris pengukuran kita. `null` dan `not_measured` bukan nol dan bukan lulus.

Kontrak ada di `docs/metrics-contract.md`. Layar jawaban di http://127.0.0.1:8765 menampilkan rute, metode, dan `trace.duration_s`. Panel http://127.0.0.1:8766 menampilkan waktu agen, bukan mutu jawaban.

## Yang terukur pada buku demo yang sedang jalan

Buku `16cd89dcda064fe2b6390deb7b91e00d`, provider jalur bisnis `rules`. Tiga pertanyaan, satu sampel masing-masing, 10 November 2026 sekitar 16:58 UTC. Bukan persentil.

| Pertanyaan | Rute | Jawaban | Detik |
| --- | --- | --- | --- |
| Apa status Budiono? | db_only | occurred | 0,000395 |
| Apa status Budi? | db_only | unknown | 0,000345 |
| Berapa harga saham kemarin? | unsupported | abstain | 0,000389 |

Rekaman di buku itu: Onboarding karyawan GROK-DEMO berstatus planned, Budi unknown, Budiono occurred. Pertanyaan gabungan pada buku ini tidak diukur ulang pada giliran ini.

## Laporan tersimpan

| Laporan | Waktu UTC | Hasil | Batas |
| --- | --- | --- | --- |
| `.acceptance-runs/rules-http-01/results.json` | 14:25 | 6/6 | Provider rules. Bukan rute gabungan dan bukan mutu model. `quality_f1` null. `production_ready` false. |
| `.acceptance-runs/grok-http-01/results.json` | 14:27 | 5/6 | Unggah 75,0264 detik, lalu dua kueri 21,4496 dan 17,2108 detik. Gagal karena timeout Grok 75 detik dan fallback `local-rules`. `quality_f1` null. |
| `.acceptance-runs/macro-business-v1/results.json` | 15:04 | 6/9 | Tiga domain sintetis. `db_only` dan isolasi lulus. Tiga kueri gabungan gagal. `business_value` not_measured. |
| `.parallel-builds/grok-20261110-2222/macro-rules/results.json` | 15:25 | 9/9 | Provider rules pada `synthetic-macro-v1`. Tiga domain berpola sama. Bukan bukti model dan bukan bukti pasar. |
| `.parallel-builds/repair-20261110-221217/macro-0` dan `macro-1` | 15:13 dan 15:18 | 9/9 masing-masing | Kandidat lain, provider rules. |

## Operasi agen

Panel aktivitas, dikumpulkan 16:58 UTC: 0 panggilan tercatat aktif, overlap tertinggi 6. Delapan run tersimpan. Semua `quality_metrics` bernilai `not_measured`. Label aktif berarti panggilan sudah mulai, bukan token sedang keluar.

## Belum terukur

Presisi, recall, F1, MRR, NDCG, p50, p95, token, dan biaya. Dukungan semantik terpisah dari lokasi kutipan. Waktu kerja pengguna nyata. Klasifikasi multi-label. Tidak ada target angka dari CTO di berkas ini.

Angka yang disebut pos publik — sekitar 10 menit 7 detik, recall tambah 0,083, sekitar 1,2 juta token, 1–2 pertanyaan per menit — tetap laporan penulis. Bukan hasil aplikasi ini.
