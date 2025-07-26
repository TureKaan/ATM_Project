#Gerekli modülleri içe aktarıyoruz
import json #Kullanıcı verilerini saklamak için JSON formatını kullanacağız
from datetime import datetime # Tarih ve saat modülü içe aktarılıyor
from colorama import init, Fore, Style
init(autoreset=True) # Renklerin her print'ten sonra sıfırlanmasını sağlar

# İşlem geçmişine kayıt fonksiyonu
def add_to_log(username,action):
    """
    Kullanıcının işlem geçmişine tarih-saat bilgisiyle kayıt ekler.
    Her kullanıcı için ayrı bir log dosyası tutulur.
    """
    log_file_name = f"{username}_log.txt" # Her kullanıcıya özel log dosyası
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Şu anki tarih - saat
    log_entry = f"[{timestamp}] {action}" # Log formatı

    # Log dosyasına yaz
    with open(log_file_name, "a") as file:
        file.write(log_entry + "\n")

#Kullanıcı verilerinin saklanacağı JSON dosyası adı
users_file = "users.json"

# Program başında kullanıcı verilerini yükleme
try:
    with open(users_file, "r") as file: #Dosyayı okuma modunda açıyoruz
        users = json.load(file) # JSON verilerini Python sözlüğüne yüklüyoruz
except FileNotFoundError:
    users = {} #Eğer dosya yoksa, boş bir sözlük başlatıyoruz
    with open(users_file, "w") as file:
        json.dump(users, file, indent=4) #indent=4 düzenli yazdırır

#Kullanıcı verilerini kaydetme fonksiyonu
def save_users():
    """Tüm kullanıcı verilerini JSON dosyasına kaydeder"""
    with open(users_file,"w") as file:
        json.dump(users,file, indent=4) # Verileri dosyaya kaydet


def register_user():
    """Yeni kullanıcı oluşturur"""
    username = input("Yeni kullanıcı adı:")
    if username in users:
        print("Bu kullanıcı zaten var.")
        return

    password = input("Şifre:")
    is_admin_input = input ("Yönetici mi? (E/H):").lower()
    is_admin = True if is_admin_input == "e" else False

    #Kullanıcıyı sözlüğe ekleme
    users[username] = {
        "password": password,
        "balance": 0,
        "is_admin": is_admin
    }

    save_users() # Değişiklikleri JSON dosyasına kaydet
    print(f" {username} başarıyla kaydedildi.")

#KULLACINI GİRİŞİ

def login_user():
    """Var olan bir kullanıcı ile sisteme giriş yapar"""
    username = input("Kullanıcı adı:").strip()
    if username not in users:
        print(Fore.RED + "Kullanıcı bulunamadı.")
        return None # Kullanıcı yoksa None döndür

    for attempt in range(3,0,-1): # 3 deneme hakkı
        password = input("Şifre: ").strip()

        # DEBUG AMAÇLI SATIR
        print(Fore.YELLOW + f"[DEBUG] Girilen şifre : '{password}'")
        print(Fore.YELLOW + f"[DEBUG] Kayıtlı şifre: '{users[username]['password']}'")

        if password == users[username]["password"].strip():
            print(Fore.GREEN + f"Hoşgeldiniz {username}!")
            return username # Doğru giriş - kullanıcı adını döndür
        else:
            print(Fore.RED + f"Yanlış şifre Kalan deneme hakkı: {attempt-1}")

    print(Fore.RED +"3 kez hatalı giriş. Çıkılıyor.")
    return None #3 hatalı giriş sonrası None döndür

#YÖNETİCİ PANELİ
def admin_panel():
    """Yöneticiler için kullanıcı yönetimi ekranı"""
    while True:
        print(Fore.MAGENTA + "\n Yönetici Paneli")
        print("1. Tüm kullanıcıları listele")
        print("2. Kullanıcı sil")
        print("3. Kullanıcının şifresini sıfırla") # Yeni özellik
        print("4. Çıkış")

        choice = input("Seçiminiz: ")
        if choice == "1":
            # Tüm kullanıcıları listele
            print(" Kayıtlı Kulanıcılar:")
            for user in users:
                print(f"- {user} (Admin: {users[user]['is_admin']})")
        elif choice == "2":
            #Kullanıcı Silme
            user_to_delete = input("Silinecek kullanıcı adı: ")
            if user_to_delete in users:
                del users[user_to_delete] # Kullanıcıyı sil
                save_users() # JSON dosyasına kaydet
                print(f" {user_to_delete} silindi.")
            else:
                print(" Kullanıcı bulunamadı.")
        elif choice == "3":
            # Şifre sıfırlama
            target_user = input(" Şifresi sıfırlanacak kullanıcı adı:")
            if target_user in users:
                new_password = input(" Yeni şifre:")
                users[target_user]["password"] = new_password
                save_users() # Değişiklikleri kaydet
                print(f" {target_user} kullanıcısının şifresi değiştirildi.")
                add_to_log(target_user, f"Admin tarafından şifre sıfırlandı")
            else:
                print(" Kullanıcı bulunmadı.")
        elif choice == "4":
            print(". Yöetici panelinden çıkılıyor.")
            break # Yönetici panelinden çık
        else:
            print("Geçersiz seçim.")

# KULLANICI PANELİ

# Normal kullanıcı ATM Menüsü
def user_panel(username):
    """Kullanıcının bakiye ve işlemlerini yönetir"""
    balance = users[username]["balance"] # Mevut bakiye yükleniyor
    while True:
        print(Fore.BLUE + "\n--- ATM Menü ---")
        print("1. Bakiye GÖrüntüleme")
        print("2. Para Yatır")
        print("3. Para Çek")
        print("4. Para Transfer Et (Havale)") # Transfer seçeneği
        print("5. İşlem Geçmişini Görüntüle")
        print("6. Çıkış")

        choice = input("Seçiminiz: ")
        if choice == "1":
            print(f" Mevcut bakiye: {balance} TL")
            add_to_log(username, "Bakiye görüntülendi") # Log kaydı
        elif choice == "2":
            #Para Yatırma
            amount = float(input(" Yatırılacak tutar:"))
            if amount > 0:
                balance += amount
                print(Fore.GREEN + f" {amount} TL yatırıldı. Yeni bakiye: {balance} TL ")
                add_to_log(username, f"{amount} TL yatırıldı") # Log kaydı
            else:
                print("Geçerli bir tutar girin.")
        elif choice == "3":
            #Para çekme
            amount = float(input("Çekilen tutar:"))
            if amount > 0 and amount <= balance:
                balance -= amount
                print(Fore.RED + f"{amount} TL çekildi. Yeni bakiye {balance} TL")
                add_to_log(username, f"{amount} TL çekildi") # Log kaydı
            elif amount > balance:
                print("Yetersiz bakiye!")
            else:
                print("Geçerli bir tutar girin.")
        elif choice == "4":
            # Para transferi
            recipient = input(" Transfer edilecek kullanıcı adı:")
            if recipient not in users:
                print(" Hedef kullanıcı bulunamadı.")
                continue # Menüye dön
            amount = float(input(" Transer edilecek tutar:"))
            if amount > 0 and amount <= balance:
                balance -= amount # Gönderen bakiyeden düş
                users[recipient]["balance"] += amount # Alıcıya ekle
                print(f" {recipient} kullanıcına {amount} TL transfer edildi.")
                # Log kaydı hem gönderen hem alıcı için
                add_to_log(username, f"{recipient} kullanıcına {amount} TL transfer edildi.")
                add_to_log(recipient, f"{username} kullanıcısından {amount} TL alındı")
            else:
                print(" Geçerli bir tutar girin veya bakiyeniz yetesiz")
        elif choice == "5":
            # İşlem geçmişi
            print("\n İşlem Geçmişi:")
            log_file_name = f"{username}_log.txt"
            try:
                with open(log_file_name, "r") as file:
                    print(file.read())
            except FileNotFoundError:
                print("Henüz işlem geçmişiniz yok.")
        elif choice == "6":
            # Çıkış
            users[username]["balance"] = balance #Bakiyeyi kaydet
            save_users() # JSON'a kaydet
            print("Çıkış yapılıyor.")
            break
        else:
            print("Geçersiz seçim.")

#Ana Menü
while True:
    print(Fore.CYAN + "\n╔══════════════════════╗")
    print(Fore.CYAN + "║     ATM SİSTEMİ      ║")
    print(Fore.CYAN + "╠══════════════════════╣")
    print(Fore.YELLOW + "║ 1. Giriş Yap         ║")
    print("║ 2. Kayıt Ol          ║")
    print("║ 3. Çıkış             ║")
    print(Fore.CYAN + "╚══════════════════════╝")

    main_choice = input("Seçiminiz: ")
    if main_choice == "1":
        user = login_user()
        if user:
            if users[user]["is_admin"]:
                admin_panel() # Yönetici ise admin paneline yönlendir
            else:
                user_panel(user) # Normal kullanıcı menüsüne yönlendir
    elif main_choice == "2":
        register_user() # Yeni kullanıcı kaydı
    elif main_choice == "3":
        print(" GÖrüşmek üzere!")
        break
    else:
        print(" Geçersiz seçim.")