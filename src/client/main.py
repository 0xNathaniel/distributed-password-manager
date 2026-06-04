import sys
import getpass
from cli import storage
from cli.vault_manager import (
    init_vault, 
    open_vault_normal, 
    open_vault_backup,
    generate_secure_password,
    update_vault
)
from cli.visual_crypto import generate_visual_shares

def vault_menu(username: str, vault_data: dict, master_password: str, is_backup: bool = False, master_key: bytes = None):
    while True:
        mode_status = "[MODE BACKUP - READ ONLY]" if is_backup else "[MODE NORMAL]"
        print(f"\n=== Vault Menu ({username}) {mode_status} ===")
        print("1. Lihat Semua Password")
        print("2. Tambah Password Baru")
        print("3. Ubah Password")
        print("4. Hapus Password")
        print("5. Kunci Vault (Kembali ke Menu Utama)")
        
        pilihan = input("Pilih menu (1-5): ")
        
        if pilihan == '1':
            print("\n[+] Menampilkan data password yang tersimpan:")
            if not vault_data:
                print("Vault Anda masih kosong.")
            else:
                print("-" * 40)
                for service, credentials in vault_data.items():
                    print(f"Layanan : {service}")
                    print(f"Username: {credentials.get('username')}")
                    print(f"Password: {credentials.get('password')}")
                    print(f"Catatan : {credentials.get('catatan', '-')}")
                    print("-" * 40)
                    
        elif pilihan == '2':
            if is_backup:
                print("[-] AKSI DITOLAK: Anda berada dalam Mode Backup. Tidak dapat menambah data.")
            else:
                print("\n[+] Tambah Data Password Baru")
                service = input("Nama Layanan (misal: GitHub): ")
                if service in vault_data:
                    print(f"[-] Layanan {service} sudah ada. Silakan gunakan menu Ubah Password.")
                    continue
                    
                user_id = input("Username / Email: ")
                
                print("Pilih metode password:")
                print("a. Input manual")
                print("b. Generate otomatis (CSPRNG)")
                metode = input("Pilihan (a/b): ").lower()
                
                pwd = ""
                if metode == 'b':
                    panjang_str = input("Masukkan panjang password (minimal 4, tekan enter untuk 16): ")
                    panjang = int(panjang_str) if panjang_str.isdigit() else 16
                    pwd = generate_secure_password(max(4, panjang))
                    print(f"[!] Password dibangkitkan: {pwd}")
                else:
                    pwd = getpass.getpass("Masukkan password: ")
                    
                catatan = input("Catatan (opsional): ")
                
                vault_data[service] = {
                    "username": user_id,
                    "password": pwd,
                    "catatan": catatan
                }
                
                try:
                    update_vault(username, vault_data, master_key)
                    print(f"[+] Berhasil menambahkan akun untuk {service} dan vault telah disinkronisasi.")
                except Exception as e:
                    print(f"[-] Gagal menyimpan pembaruan: {e}")
                    del vault_data[service]
            
        elif pilihan == '3':
            if is_backup:
                print("[-] AKSI DITOLAK: Anda berada dalam Mode Backup. Tidak dapat mengubah data.")
            else:
                print("\n[+] Ubah Data Password")
                service = input("Masukkan Nama Layanan yang ingin diubah: ")
                
                if service not in vault_data:
                    print(f"[-] Layanan '{service}' tidak ditemukan di vault.")
                    continue
                    
                print(f"Data saat ini untuk {service}:")
                print(f"Username: {vault_data[service].get('username')}")
                print(f"Catatan : {vault_data[service].get('catatan', '-')}")
                
                print("\nApa yang ingin diubah?")
                print("1. Username/Email")
                print("2. Password")
                print("3. Catatan")
                print("4. Batal")
                
                ubah_pilihan = input("Pilih (1-4): ")
                
                old_data = vault_data[service].copy()
                
                if ubah_pilihan == '1':
                    vault_data[service]['username'] = input("Username / Email baru: ")
                elif ubah_pilihan == '2':
                    print("Pilih metode password baru:")
                    print("a. Input manual")
                    print("b. Generate otomatis (CSPRNG)")
                    metode = input("Pilihan (a/b): ").lower()
                    
                    if metode == 'b':
                        panjang_str = input("Masukkan panjang password (minimal 4, tekan enter untuk 16): ")
                        panjang = int(panjang_str) if panjang_str.isdigit() else 16
                        pwd = generate_secure_password(max(4, panjang))
                        print(f"[!] Password baru dibangkitkan: {pwd}")
                        vault_data[service]['password'] = pwd
                    else:
                        vault_data[service]['password'] = getpass.getpass("Masukkan password baru: ")
                elif ubah_pilihan == '3':
                    vault_data[service]['catatan'] = input("Catatan baru: ")
                elif ubah_pilihan == '4':
                    continue
                else:
                    print("[-] Pilihan tidak valid.")
                    continue
                    
                try:
                    update_vault(username, vault_data, master_key)
                    print(f"[+] Berhasil mengubah data untuk '{service}'. Vault telah disinkronisasi.")
                except Exception as e:
                    print(f"[-] Gagal menyimpan pembaruan ke server: {e}")
                    vault_data[service] = old_data
            
        elif pilihan == '4':
            if is_backup:
                print("[-] AKSI DITOLAK: Anda berada dalam Mode Backup. Tidak dapat menghapus data.")
            else:
                print("\n[+] Hapus Data Password")
                service = input("Masukkan Nama Layanan yang ingin dihapus: ")
                
                if service not in vault_data:
                    print(f"[-] Layanan '{service}' tidak ditemukan di vault.")
                    continue
                    
                konfirmasi = input(f"Apakah Anda yakin ingin menghapus data untuk '{service}'? (y/n): ").lower()
                
                if konfirmasi == 'y':
                    old_data = vault_data.pop(service)
                    
                    try:
                        update_vault(username, vault_data, master_key)
                        print(f"[+] Berhasil menghapus data '{service}'. Vault telah disinkronisasi.")
                    except Exception as e:
                        print(f"[-] Gagal menghapus data di server: {e}")
                        vault_data[service] = old_data
                else:
                    print("[-] Penghapusan dibatalkan.")
        elif pilihan == '5':
            print("\n[+] Mengunci vault. Kembali ke Menu Utama.")
            break
        else:
            print("[-] Pilihan tidak valid.")

def main_menu():
    while True:
        print("\n=== Distributed Password Manager ===")
        is_init = storage.is_initialized()
        
        if not is_init:
            print("1. Buat Vault Baru (Inisialisasi)")
        else:
            print("2. Buka Vault (Mode Normal / Backup)")
            
        print("3. Keluar")
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == '1' and not is_init:
            print("\n[+] Memulai pembuatan vault baru...")
            username = input("Masukkan username Anda: ")
            password = getpass.getpass("Masukkan master password: ")
            confirm_password = getpass.getpass("Konfirmasi master password: ")
            
            if password != confirm_password:
                print("[-] Password tidak cocok. Dibatalkan.")
                continue
            
            try:
                recovery_share = init_vault(username, password)
                
                print("\n[!] VAULT BERHASIL DIBUAT!")
                print("="*50)
                print("RECOVERY SHARE ANDA:")
                print(recovery_share)
                print("="*50)
                print("[!] PERINGATAN KELANGSUNGAN HIDUP VAULT ANDA:")
                print("Simpan recovery share ini di tempat yang aman (copy-paste).")
                print("Jika server mati dan Anda kehilangan share ini, vault tidak bisa dibuka!")

                print("\n[+] Memproses Kriptografi Visual untuk Recovery Share...")
                s1, s2, comb = generate_visual_shares(recovery_share, f"recovery_{username}")
                print("[!] Berhasil! 3 file gambar telah dibuat di direktori saat ini:")
                print(f"    - {s1} (Simpan di tempat A)")
                print(f"    - {s2} (Simpan di tempat B)")
                print(f"    - {comb} (Simulasi penggabungan, coba scan QR-nya!)")
                print("="*50)
            except Exception as e:
                print(f"[-] Terjadi kesalahan saat inisialisasi: {e}")
                
        elif pilihan == '2' and is_init:
            print("\n[+] Mengakses vault...")
            print("Pilih mode akses:")
            print("1. Mode Normal (Koneksi ke Server)")
            print("2. Mode Backup (Darurat / Offline)")
            mode = input("Masukkan pilihan (1/2): ")
            
            if mode not in ['1', '2']:
                print("[-] Pilihan mode tidak valid. Dibatalkan.")
                continue
            
            username = input("Masukkan username Anda: ")
            password = getpass.getpass("Masukkan master password: ")
            
            if mode == '1':
                try:
                    vault_data, master_key = open_vault_normal(username, password)
                    print("\n[+] BERHASIL: Otorisasi valid. Vault dibuka (Mode Normal).")
                    vault_menu(username, vault_data, password, is_backup=False, master_key=master_key)
                except Exception as e:
                    print(f"[-] {e}")
                    print("    Saran: Jika server sedang mati, silakan gunakan Mode Backup.")
            
            elif mode == '2':
                recovery_share = input("Masukkan Recovery Share Anda: ")
                try:
                    vault_data = open_vault_backup(password, recovery_share)
                    print("\n[+] BERHASIL: Rekonstruksi valid. Vault dibuka (Mode Backup).")
                    vault_menu(username, vault_data, password, is_backup=True, master_key=None)
                except Exception as e:
                    print(f"[-] {e}")
            
        elif pilihan == '3':
            print("Keluar dari program. Sampai jumpa!")
            sys.exit(0)
            
        else:
            print("[-] Pilihan tidak valid atau menu belum tersedia.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nKeluar dari program.")
        sys.exit(0)