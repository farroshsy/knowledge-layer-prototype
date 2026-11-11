# Catatan timeout Grok

Ditulis 10 November 2026 oleh koordinator, setelah agen diagnosis gagal karena kapasitas model (HTTP 500). Tidak ada kode yang diubah. Tidak ada panggilan Grok baru.

## Nilai dan tempatnya

Timeout unggah dan planner adalah 75 detik. Nilai itu argumen bawaan `GrokCliProvider.__init__` di `.parallel-builds/grok-20261110-2222/candidate/klayer/providers.py:204`. `subprocess.run` memakai angka yang sama di `providers.py:253`. Saat waktu habis, `providers.py:259` mengangkat `ProviderError` dengan teks `grok timed out after 75s`.

## Sesudah timeout

`pipeline._run_provider` menangkap `ProviderError` di `pipeline.py:39`. Job tidak kosong. Ia menerbitkan hasil `lexical_outcome`, menyimpan `provider_error`, menambah peringatan `online provider failed; published local-rules output`, lalu menandai `method=rules` dan `label=local-rules` (`pipeline.py:40-44`). Ini cocok dengan unggah `baru-grok-live.txt` di checkpoint.

Label `local-rules` tetap label fallback leksikal. Ia bukan ekstraksi semantik.

## Apakah menaikkan timeout mengubah kontrak

Tidak mengubah label bukti, baris katalog, atau aturan bahwa rencana bukan kejadian. Yang berubah hanya berapa lama permintaan HTTP menunggu di `_call_grok`. Unggah saat ini sinkron, jadi menunggu lebih lama berarti demo ikut diam.

## Perubahan kecil yang tidak diambil malam ini

Jangan menaikkan angka di `GrokCliProvider.__init__` sebagai perbaikan demo. Jangan mengubah `lexical_outcome`, label `local-rules`, atau penulisan rekaman bisnis. Perubahan kode yang lebih dulu diizinkan peta celah adalah abstain langsung di `business_query.py` untuk pertanyaan tanpa isyarat dokumen, tanpa memanggil `ask()`.
