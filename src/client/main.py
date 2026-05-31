import sys
import getpass
from cli import storage
from cli.vault_manager import init_vault

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
                # Panggil fungsi manajer
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
            # TODO: Implementasi Mode Normal / Backup di vault_manager.py
            
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