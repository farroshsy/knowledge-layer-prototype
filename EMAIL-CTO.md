# Draf surel

Salin subjek dan isi di bawah ini. Surel belum dikirim.

## Subjek

Prototipe notebook operasional untuk tinjauan

## Isi

Yth. Bapak/Ibu,

Saya menyampaikan prototipe notebook operasional untuk ditinjau. Prototipe ini menyimpan dua sumber secara terpisah: rekaman bisnis yang diisi orang, dan berkas yang diunggah. Pertanyaan hanya dijawab dari baris yang sudah tersimpan. Jika barisnya tidak ada, atau para penilai tidak sepakat, sistem menolak menjawab.

Produk dijalankan secara lokal dengan Rails 7.0.10, Ruby 3.3.2, dan PostgreSQL. Panduan perintahnya ada di berkas PENGGUNAAN.md pada repositori. Ringkasnya, dari folder ops-notebook:

    export RBENV_VERSION=3.3.2
    export SDKROOT="$(xcrun --sdk macosx --show-sdk-path)"
    bundle install
    bin/rails db:prepare
    bin/ops

Setelah server berjalan, buka http://127.0.0.1:3000 dan pilih Buka contoh produk. Halaman yang dapat dilewati berurutan adalah Dump, Pemetaan, Proses, Analisis, Keputusan, Verifikasi, dan Tanya.

Yang sudah dapat dicoba pada teks polos: pemecahan berkas, penentuan jenis oleh isi, baris berjudul, bentrok yang tetap terlihat, serta pembedaan rencana dan kejadian. Nama berkas dicatat sebagai penanda dan tidak menentukan jenis.

Yang belum tersedia, dan tidak saya klaim: pembacaan PDF, OCR, dokumen kantor berdesain, transkrip audio atau video, pemotongan berkas besar, model bahasa, antrian latar, serta akun pengguna. Docker Compose juga belum disediakan.

Kode dan naskah penjelasan ada pada pull request berikut:

https://github.com/farroshsy/knowledge-layer-prototype/pull/1

Repositorinya privat. Saya siap menunjukkan alurnya langsung bila diperlukan.

Hormat saya,
Farros
