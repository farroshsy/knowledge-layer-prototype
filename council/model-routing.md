# Pembagian model Grok

Daftar CLI terverifikasi pada 10 Nov 2026 lewat `grok models` dengan akun grok.com: grok-4.7 (default), grok-4.7-build-fast, grok-4.6, grok-4.5. Ini ketersediaan, bukan benchmark relatif biaya/latensi/akurasi. User mengizinkan pemilihan model sesuai kebutuhan dan beberapa agent independen untuk task yang sama.

- grok-4.7: business process A dan B, keputusan arsitektur, semantic query contract, review adversarial dan security/data-integrity decisions. Sesi A/B yang sudah berjalan tetap dipertahankan, tidak direstart hanya demi label model.
- grok-4.7-build-fast: pekerjaan terisolasi dengan output jelas seperti drafting evaluation cases atau dokumentasi. Hasilnya direview sebelum digunakan sebagai oracle. Scope kecil bukan berarti boleh melewatkan pemeriksaan.
- grok-4.6/grok-4.5: tidak dipilih hanya karena lebih lama. Belum ada bukti manfaat memakai mereka untuk tugas ini.

Batasi write ownership. Jangan menambah banyak penulis pada file yang sama; tambahkan reviewer atau analisis independen jika perlu paralel. Hindari puluhan agent dengan brief identik yang tidak punya output atau keputusan berbeda. Persetujuan beberapa model tidak menggantikan pengujian. Satu model yang baik dalam coding tidak otomatis baik dalam klasifikasi runtime.

Model runtime aplikasi perlu dievaluasi terpisah dari model development. Catat model/method, error, waktu dan ukuran konteks jika tersedia. Jangan ganti provider produksi/default aplikasi secara diam-diam mengikuti pilihan worker. Eskalasi dari fast ke model utama jika hasil tidak valid, kontradiksi tidak terselesaikan, atau perlu perubahan desain/keamanan; hentikan iterasi tak terbatas.
