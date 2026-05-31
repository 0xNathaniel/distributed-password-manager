import sys
import getpass
from cli import storage
from cli.vault_manager import init_vault, open_vault_normal

def vault_menu(username: str, vault_data: dict, master_password: str):
    while True:
        print(f"\n=== Vault Menu ({username}) ===")
        print("1. Lihat Semua Password")
        print("2. Tambah Password Baru")
        print("3. Ubah Password")
        print("4. Hapus Password")
        print("5. Kunci Vault (Kembali ke Menu Utama)")
        
        pilihan = input("Pilih menu (1-5): \n> ")
        
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
            print("\n[+] Fitur Tambah Password akan segera diimplementasikan.")
            
        elif pilihan == '3':
            print("\n[+] Fitur Ubah Password akan segera diimplementasikan.")
            
        elif pilihan == '4':
            print("\n[+] Fitur Hapus Password akan segera diimplementasikan.")
            
        elif pilihan == '5':
            print("[+] Mengunci vault dan kembali ke menu utama...")
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
        
        pilihan = input("Pilih menu: \n> ")
        
        if pilihan == '1' and not is_init:
            print("\n[+] Memulai pembuatan vault baru...")
            username = input("Masukkan username Anda: \n> ")
            password = getpass.getpass("Masukkan master password: \n> ")
            confirm_password = getpass.getpass("Konfirmasi master password: \n> ")

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
            username = input("Masukkan username Anda: \n> ")
            password = getpass.getpass("Masukkan master password: \n> ")

            try:
                vault_data = open_vault_normal(username, password)
                print("\n[+] BERHASIL: Otorisasi valid. Vault dibuka.")
                vault_menu(username, vault_data, password)
            
            except Exception as e:
                print(f"[-] {e}")
            
        elif pilihan == '3':
            print("Keluar dari program.")
            sys.exit(0)
            
        else:
            print("[-] Pilihan tidak valid.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nKeluar dari program.")
        sys.exit(0)