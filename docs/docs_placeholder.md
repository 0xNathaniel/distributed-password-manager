# Laporan

Simpan file PDF laporan di repositori dengan nama:

`13523013_13523015_13523039_Tugas4_II4021.pdf`

## Isi laporan

1. Foto anggota kelompok di cover laporan (sebagai pengganti logo).
2. Pernyataan keaslian & tanda tangan

	Kami menyatakan bahwa kode program yang dihasilkan bukan merupakan hasil
	salinan mentah (raw output) dari Generative AI, melainkan hasil
	pengembangan dan penulisan mandiri.

	[Tanda tangan Mahasiswa 1]  [Tanda tangan Mahasiswa 2]  [Tanda tangan Mahasiswa 3]

	[Nama Mahasiswa 1]  [Nama Mahasiswa 2]  [Nama Mahasiswa 3]

3. Teori singkat

	Ringkasan teori mengenai:

	- Shamir Secret Sharing
	- AES-GCM
	- KDF (Key Derivation Function)
	- CSPRNG (Cryptographically Secure PRNG)
	- Konsep relevan lainnya (termasuk bonus, jika ada)

4. Perancangan dan implementasi

	Penjelasan rancangan dan implementasi program (bukan penyalinan kode).
	Cantumkan nama file terkait pada repository untuk setiap bagian yang
	dijelaskan. Jelaskan khususnya bagian yang dibebaskan dan fitur bonus.

5. Pengujian program dan analisis hasil

	Minimal kasus uji yang harus dilaporkan:

	### i. Uji pembuatan vault
	1. Buat vault baru dengan master password valid: tunjukkan bahwa master
		key berhasil dibangkitkan, vault kosong dienkripsi, dan data awal
		disimpan.
	2. Tunjukkan pembagian master key menjadi tiga share (Skema (2,3)): local
		share, server share, recovery share.
	3. Tampilkan recovery share dalam format teks (koordinat share dan nilai).
	4. Tunjukkan bahwa server hanya menyimpan: server share, vault terenkripsi,
		nonce vault, dan metadata yang diperlukan.

	### ii. Uji penyimpanan dan perlindungan local share
	1. Tunjukkan bahwa local share tidak disimpan secara asli (plaintext).
	2. Tunjukkan local share terenkripsi menggunakan kunci turunan dari master
		password.
	3. Masukkan master password benar: local share berhasil didekripsi.
	4. Masukkan master password salah: dekripsi local share gagal atau akses
		ditolak.

	### iii. Uji akses normal
	1. Buka vault dengan master password yang benar saat server tersedia: sistem
		menggunakan kombinasi local share dan server share.
	2. Tunjukkan rekonstruksi master key dari dua share valid.
	3. Tunjukkan dekripsi vault dan tampilan isi vault.
	4. Masukkan master password salah atau share tidak valid: dekripsi gagal,
		data tidak ditampilkan.

	### iv. Uji penambahan data password
	1. Tambah data password secara manual: data tersimpan di vault.
	2. Tambah data password ter-generate menggunakan CSPRNG: password
		sesuai panjang yang diminta.
	3. Setelah penambahan, vault dienkripsi ulang dengan nonce baru dan disimpan
		ke server.
	4. Backup vault lokal juga diperbarui setelah perubahan pada mode normal.

	### v. Uji pengubahan dan penghapusan data password
	1. Ubah salah satu data: perubahan tersimpan setelah vault dienkripsi ulang.
	2. Hapus salah satu data: data tidak muncul lagi setelah vault dibuka.
	3. Pembaruan hanya dapat dilakukan pada mode normal.

	### vi. Uji penyimpanan vault di server
	1. Tunjukkan vault terenkripsi disimpan di SQLite sebagai BLOB.
	2. Tunjukkan server tidak menyimpan nama layanan, username, password, atau
		catatan sebagai baris plaintext terpisah.
	3. Tunjukkan server tidak menerima master key, local share, recovery share,
		atau isi vault dalam bentuk plaintext.

	### vii. Uji mode backup
	1. Simulasikan server tidak dapat diakses.
	2. Buka vault menggunakan master password dan recovery share: sistem
		menggunakan kombinasi local share dan recovery share.
	3. Tunjukkan penggunaan backup vault lokal terenkripsi sebagai sumber.
	4. Tunjukkan data password dapat dilihat pada mode backup.
	5. Tunjukkan bahwa penambahan/pengubahan/penghapusan data tidak dapat
		dilakukan pada mode backup.

	### viii. Uji kegagalan pemulihan
	1. Masukkan recovery share yang salah: rekonstruksi master key atau dekripsi
		vault gagal.
	2. Gunakan backup vault yang tidak sesuai atau telah dimodifikasi: dekripsi
		AES-128-GCM gagal karena validasi autentikasi tidak sesuai.
	3. Tunjukkan bahwa sistem tidak menampilkan data ketika dekripsi gagal.

	### ix. Uji kriptografi visual (bonus)
	1. Tampilkan QR code awal dari recovery share.
	2. Tampilkan dua gambar share hasil pembagian QR code.
	3. Tampilkan hasil penggabungan kedua gambar share.
	4. Tunjukkan bahwa QR code hasil penggabungan dapat dipindai dan
		menghasilkan recovery share yang sama.

6. Kesimpulan dari hasil implementasi

7. Daftar pustaka

8. Lampiran

	- Pranala repositori
	- Pranala video demo (tidak boleh menggunakan URL shortener dan tidak menuju
	  folder Google Drive; jika menggunakan Google Drive, bagikan link video
	  langsung)
	- Pembagian tugas