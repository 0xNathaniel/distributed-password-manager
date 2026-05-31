import sys

def main_menu():
    while True:
        print("\n=== Distributed Password Manager ===")
        print("1. Buat Vault Baru (Inisialisasi)")
        print("2. Buka Vault (Mode Normal / Backup)")
        print("3. Keluar")
        
        pilihan = input("Pilih menu (1/2/3): \n>")
        
        if pilihan == '1':
            print("\n[+] Memulai pembuatan vault baru...")
            # TODO: Implementasi alur input master password, generate share, dll.
        elif pilihan == '2':
            print("\n[+] Mengakses vault...")
            # TODO: Implementasi alur dekripsi local share, fetch server, dll.
        elif pilihan == '3':
            print("Keluar dari program. Sampai jumpa!")
            sys.exit(0)
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nKeluar dari program.")
        sys.exit(0)