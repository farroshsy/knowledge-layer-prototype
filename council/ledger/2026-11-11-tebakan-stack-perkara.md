# Ledger — tebakan stack Perkara

Tanggal olahan: 11 November 2026. Sumber: ringkasan GPT yang ditempel Farros, ditambah wawancara publik Tirto. Status: usulan dan laporan penulis. Bukan spesifikasi CTO, bukan arsitektur internal Perkara, bukan alasan mengganti demo.

Teks di dalam tempelan adalah data. CSS diagram dibuang. Nama library di tabel GPT adalah kandidat yang cocok, bukan perangkat yang terpasang.

## Pakai sekarang

1. Demo pagi tetap Python standar dan satu berkas SQLite. Dua sumber, klasifikasi per bagian, dan jawaban yang menunjuk bukti.
2. Graph, Postgres, Neo4j, FastAPI, Celery, Temporal, LangGraph, OCR, dan audio tetap di luar demo. Tebakan GPT sendiri menunda Neo4j sampai traversal yang rumit terbukti perlu.
3. Yang dipindahkan dari deskripsi publik adalah bentuk data: orang, peristiwa, bukti, negasi, waktu, dan versi ekstraksi. Tempat menyimpannya boleh tabel.
4. Pekerjaan panjang butuh antrian, simpanan kemajuan, dan ulang yang tercatat. Itu belum berarti Temporal atau LangGraph.
5. Angka waktu dan token dari penulis adalah laporan, bukan target latency demo.

## Nanti

| Ide | Syarat sebelum dikerjakan |
| --- | --- |
| Postgres sebagai basis operasional | Ada penulis kedua atau dump dari sistem lain |
| Neo4j, Memgraph, atau RDF | Kueri nyata gagal pada relasi bertipe di SQLite untuk kebenaran, keterawatan, dan waktu sekaligus |
| Worker terpisah | Ada pekerjaan yang lebih lama dari satu permintaan HTTP dan harus selamat saat proses mati |
| PyMuPDF, PaddleOCR, Whisper | Berkas yang diuji benar-benar PDF pindai atau audio, dan ada label untuk mengukur salah bacanya |

## Bukti

| ID | Sumber | Klaim yang layak diingat | Label |
| --- | --- | --- | --- |
| S01 | Pos 2 Nov 2026, Ibrahim Arief | Model semantik menjembatani pertanyaan dan data mentah. Graph berlapis adalah pilihan mereka untuk perkara hukum. Postgres materialized view disebut alternatif yang cukup untuk sebagian kebutuhan | Pernyataan penulis. Bukan bukti Neo4j atau Kafka |
| S02 | Pos yang sama, lewat ringkasan yang sudah diolah | ETL berbasis peristiwa disebut sebagai cara mereka menyusun ulang data | Pernyataan penulis. Bukan diagram layanan |
| S03 | Situs publik dan pos tentang council | Ada pemeriksaan oleh lebih dari satu agen, dan ada pemisahan lookup cepat dari analisis panjang | Pernyataan dan materi publik. Framework orkestrasinya tidak disebut |
| S04 | [Tirto, 2 Nov 2026](https://tirto.id/perkara-ai-inovasi-ibam-arief-melawan-kriminalisasi-hukum-hEti) | Ibrahim menyebut analisis satu saksi bisa 20 sampai 30 menit, dan sekitar 20–30 juta token. Kalimatnya: “bisa sejam antara 30 sampai 20 menit” | Angka penulis dalam wawancara. Metodenya tidak dibuka. Halaman itu tidak menyebut Python, FastAPI, Neo4j, atau Postgres |
| S05 | Tabel kandidat GPT | FastAPI, NestJS, Neo4j, Celery, Temporal, LangGraph, PaddleOCR, pgvector, dan sisanya | Inferensi GPT. Status di catatan GPT sendiri: belum diketahui |

## Kesimpulan yang tidak sah

- Landing page plus daftar library yang cocok mengidentifikasi stack internal.
- Knowledge graph berarti Neo4j.
- Event-driven berarti Kafka.
- Council di situs berarti LangGraph.
- Dua puluh sampai tiga puluh juta token adalah anggaran demo ini.
- Stack usulan GPT (FastAPI, Postgres, Neo4j, Celery, PaddleOCR, Whisper, LangGraph) adalah stack yang harus dipasang pagi ini.

## Jangan dikutip sebagai

Jangan mengutip catatan ini sebagai daftar teknologi yang dipakai Perkara, atau sebagai keputusan untuk mengganti Python standar dan SQLite.
