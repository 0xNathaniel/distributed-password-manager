import sys
import getpass
from cli import storage
from cli.vault_manager import init_vault, open_vault_normal, open_vault_backup

def vault_menu(username: str, vault_data: dict, master_password: str, is_backup: bool = False):
    """
    Menu interaktif di dalam vault setelah pengguna berhasil login.
    Menangani operasi CRUD untuk data password. Jika is_backup=True, operasi dibatasi (Read-Only).
    """
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
                # TODO: Implementasi Fitur Tambah Password
                print("\n[+] Fitur Tambah Password akan segera diimplementasikan.")
            
        elif pilihan == '3':
            if is_backup:
                print("[-] AKSI DITOLAK: Anda berada dalam Mode Backup. Tidak dapat mengubah data.")
            else:
                # TODO: Implementasi Fitur Ubah Password
                print("\n[+] Fitur Ubah Password akan segera diimplementasikan.")
            
        elif pilihan == '4':
            if is_backup:
                print("[-] AKSI DITOLAK: Anda berada dalam Mode Backup. Tidak dapat menghapus data.")
            else:
                # TODO: Implementasi Fitur Hapus Password
                print("\n[+] Fitur Hapus Password akan segera diimplementasikan.")
            
        elif pilihan == '5':
            print("[+] Mengunci vault dan kembali ke menu utama...")
            break
        else:
            print("[-] Pilihan tidak valid, silakan coba lagi.")

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
                    vault_data = open_vault_normal(username, password)
                    print("\n[+] BERHASIL: Otorisasi valid. Vault dibuka (Mode Normal).")
                    vault_menu(username, vault_data, password, is_backup=False)
                except Exception as e:
                    print(f"[-] {e}")
                    print("    Saran: Jika server sedang mati, silakan gunakan Mode Backup.")
            
            elif mode == '2':
                recovery_share = input("Masukkan Recovery Share Anda: ")
                try:
                    vault_data = open_vault_backup(password, recovery_share)
                    print("\n[+] BERHASIL: Rekonstruksi valid. Vault dibuka (Mode Backup).")
                    vault_menu(username, vault_data, password, is_backup=True)
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