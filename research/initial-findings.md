# Riset awal dan batas tugas

Target lokal 11 November 2026 pukul 08.00 WIB. Pengguna mengonfirmasi CTO mengizinkan dokumen dummy dan meminta riset PerkaraAI terlebih dahulu. Ketentuan detail belum boleh dianggap final.

## Sumber publik

https://perkara.ai/ — deskripsi produk dari pembuatnya, bukan audit independen. Menjelaskan penguraian berkas, pemrosesan teks/struktur, ekstraksi informasi dan penelusuran jawaban kembali ke sumber. Tampilan menyebut lima kelompok besar serta sebelas tahap/jenis artefak. Jangan menganggap setiap dokumen hanya dimasukkan ke satu folder layer. Informasi turunan dapat mempunyai hubungan ke sumber yang sama.

https://x.com/ibamarief/status/2117104412824944848 — belum terbaca langsung; fetch mendapat 403. Jangan mengklaim isi post ini sudah diverifikasi.

https://x.com/PerkaraAI — fetch langsung mendapat 403.

## Hipotesis desain untuk diuji, bukan fakta tentang implementasi internal PerkaraAI

Simpan sumber asli beserta lokasi teksnya, lalu hasil ekstraksi terstruktur dan relasi asal-usul. Pernyataan orang adalah klaim yang diatribusikan, bukan otomatis fakta yang terbukti. Premis dan sintesis harus dipisahkan dari kutipan sumber. Simpan konflik atau ketidakpastian tanpa memaksa satu versi benar. Kategori dokumen berbeda dari tingkat abstraksi informasi.

Contoh sintetis: dokumen berisi 'Menurut notulen, pilot direncanakan mulai 15 November.' Kutipan mendukung pernyataan tentang rencana, bukan bukti pilot sudah berjalan. Jika dokumen lain menyebut tanggal berbeda, tampilkan kedua klaim berikut sumbernya.

## Kandidat demo bounded

Unggah dokumen dummy, tampilkan teks sumber dan lokasi, ekstrak struktur/pernyataan, periksa klasifikasi, jelajahi hubungan antarlayer, jawab pertanyaan dengan tautan sumber. Ini rekomendasi awal yang menunggu riset, bukan persetujuan seluruh scope. Lokal berarti server/UI berjalan di Mac; inferensi online tidak boleh disebut offline. Tidak mengubah aplikasi submission sebelumnya.

## Status Grok melalui Orca

Task task_fe6c3549d45e, run run_075572b87a8d. Start awal ctx_66f66e8b1d3c gagal agent_readiness karena trust workspace submission lama; sesi telah released dan terminal ditutup. Folder baru didaftarkan di Orca, terpisah dari submission. Tidak menyetujui trust atau menjalankan model pada start gagal.
