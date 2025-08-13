import flet as ft
import json
import os
import subprocess
import threading
import time
import glob
from pathlib import Path

class CookieBotGUI:
    def __init__(self):
        self.config_file = "cookie_config.json"
        self.bot_process = None
        self.is_running = False
        self.cookie_files = []
        
    def load_config(self):
        """Kaydedilmiş konfigürasyonu yükle"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "proxy_list": "http://IUuuMf4LkexA8wSn_counusy-tr_session-kZvLa1Sv_lifetime-30m_suseaming-1@geo.iproyal.com:12321:M9Z7JPUKo8Vmei9g",
            "num_threads": "100",
            "target_url": "https://aowsoftware.com/",
            "cookie_folder": "",
            "search_query": "",
            "use_search": False
        }
    
    def save_config(self, config):
        """Konfigürasyonu kaydet"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Konfigürasyon kaydedilemedi: {e}")
    
    def scan_cookie_files(self, folder_path):
        """Cookie klasöründeki dosyaları tara"""
        if not folder_path or not os.path.exists(folder_path):
            return []
        
        cookie_files = []
        # .txt dosyalarını tara
        txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
        # .json dosyalarını tara
        json_files = glob.glob(os.path.join(folder_path, "*.json"))
        
        cookie_files.extend(txt_files)
        cookie_files.extend(json_files)
        
        return sorted(cookie_files)
    
    def update_cookie_file(self, proxy_list, num_threads, target_url, cookie_folder, search_query, use_search):
        """Cookie_Search.py dosyasını güncelle"""
        try:
            # Cookie_Search.py dosyasını oku
            cookie_file_path = "Module/Cookie_Search.py"
            with open(cookie_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Proxy listesini hazırla
            proxies = [proxy.strip() for proxy in proxy_list.split('\n') if proxy.strip()]
            proxy_list_str = '[\n    "' + '",\n    "'.join(proxies) + '"\n]'
            
            # Cookie dosyalarını tara
            self.cookie_files = self.scan_cookie_files(cookie_folder)
            
            # Yeni Cookie_Search.py içeriğini oluştur
            new_content = self.generate_updated_cookie_script(
                proxy_list_str, num_threads, target_url, 
                cookie_folder, search_query, use_search
            )
            
            # Dosyayı güncelle
            with open(cookie_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        except Exception as e:
            print(f"Dosya güncellenirken hata: {e}")
            return False
    
    def generate_updated_cookie_script(self, proxy_list_str, num_threads, target_url, cookie_folder, search_query, use_search):
        """Güncellenmiş Cookie_Search.py içeriğini oluştur"""
        # String'leri güvenli bir şekilde escape et
        safe_target_url = target_url.replace("'", "\\'")
        safe_cookie_folder = cookie_folder.replace("\\", "\\\\")
        safe_search_query = search_query.replace("'", "\\'")
        
        return f'''import requests
import random
import threading
import time
import ssl
import signal
import sys
import json
import glob
import os
from http.cookiejar import MozillaCookieJar
from urllib import request, parse, error
from bs4 import BeautifulSoup

PROXY_LIST = {proxy_list_str}
NUM_THREADS = {num_threads}  # Daha fazla istek için iş parçacığı sayısını artırabilirsiniz.
TARGET_URL = \'{safe_target_url}\'  # İstek gönderilecek URL
COOKIE_FOLDER = r\'{safe_cookie_folder}\'  # Cookie dosyalarının bulunduğu klasör
SEARCH_QUERY = \'{safe_search_query}\'  # Arama sorgusu
USE_SEARCH = {str(use_search)}  # Arama kullanılacak mı?

# Başarılı istekler ve toplam istekler için global sayaçlar
successful_requests = 0
total_requests = 0

# Kilit mekanizması, çoklu iş parçacığında sayaçları güvenli bir şekilde güncellemek için gerekli
counter_lock = threading.Lock()

# Proxy'yi döngüyle kullanmak için global bir index
proxy_index = 0
# Proxy değişimini güvenli bir şekilde kontrol etmek için bir kilit
proxy_lock = threading.Lock()

# Cookie dosyalarını yükle
cookie_files = []
if COOKIE_FOLDER and os.path.exists(COOKIE_FOLDER):
    cookie_files.extend(glob.glob(os.path.join(COOKIE_FOLDER, "*.txt")))
    cookie_files.extend(glob.glob(os.path.join(COOKIE_FOLDER, "*.json")))
    cookie_files = sorted(cookie_files)

# Program durdurmak için global flag
stop_flag = threading.Event()

# Her defasında farklı user agent oluşturur
def generate_user_agent():
    random_number = random.randint(100, 999)
    return f"Mozilla/5.0 (Linux; Android 13; SM-G{{random_number}}B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"

# Proxy'yi döngü ile almak için yardımcı fonksiyon
def get_next_proxy():
    global proxy_index
    with proxy_lock:
        if len(PROXY_LIST) == 0:
            return None  # Proxy listesi boşsa None döner ve proxy olmadan devam eder
        proxy = PROXY_LIST[proxy_index]
        proxy_index = (proxy_index + 1) % len(PROXY_LIST)
        return proxy

# Cookie dosyasını thread ID'sine göre seç
def get_cookie_file_for_thread(thread_id):
    if not cookie_files:
        return None
    return cookie_files[thread_id % len(cookie_files)]

# TXT formatında çerezleri yükleme fonksiyonu
def load_cookies_txt(file_path):
    cookies = {{}}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if not line.strip() or line.startswith("#"):
                    continue  # Yorum satırlarını ve boş satırları atla
                parts = line.strip().split('\t')
                if len(parts) >= 7:
                    domain = parts[0]
                    name = parts[5]
                    value = parts[6]
                    cookies[name] = value
    except Exception as e:
        print(f"TXT cookie dosyası okuma hatası: {{e}}")
    return cookies

# JSON formatında çerezleri yükleme fonksiyonu
def load_cookies_json(file_path):
    cookies = {{}}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                for cookie in data:
                    if 'name' in cookie and 'value' in cookie:
                        cookies[cookie['name']] = cookie['value']
            elif isinstance(data, dict):
                cookies = data
    except Exception as e:
        print(f"JSON cookie dosyası okuma hatası: {{e}}")
    return cookies

# Çerezleri yükleme ana fonksiyonu
def load_cookies(file_path):
    if not file_path or not os.path.exists(file_path):
        return {{}}
    
    if file_path.endswith('.txt'):
        return load_cookies_txt(file_path)
    elif file_path.endswith('.json'):
        return load_cookies_json(file_path)
    else:
        return {{}}

# HTML'den URL alma fonksiyonu
def html_den_url_al(html, belirlenen_site):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and belirlenen_site in href:
                print(f"Belirlenen link bulundu -> href: {{href}}")
                return href
    except Exception as e:
        print(f"HTML parse hatası: {{e}}")
    return None

# Anahtar kelime arama fonksiyonu
def search_keyword(search_query, target_url, cookies):
    try:
        encoded_search_query = parse.quote(search_query)
        search_url = f"https://www.google.com/search?q={{encoded_search_query}}&num=100"
        
        proxy = get_next_proxy()
        if proxy:
            proxy_support = request.ProxyHandler({{
                "http": proxy,
                "https": proxy,
            }})
            opener = request.build_opener(proxy_support)
        else:
            opener = request.build_opener()

        opener.addheaders = [
            ("User-Agent", generate_user_agent()),
            ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"),
            ("Accept-Language", "tr"),
            ("Referer", 'https://www.google.com/')
        ]
        request.install_opener(opener)

        req = request.Request(search_url)
        response = opener.open(req, timeout=20)
        html = response.read().decode('utf-8')
        
        href = html_den_url_al(html, target_url)
        if href:
            return href
        else:
            print(f"{{search_query}} için uygun URL bulunamadı.")
            return target_url
            
    except Exception as e:
        print(f"Arama hatası: {{e}}")
        return target_url

# İstek gönderimi için her defasında farklı ping sağlar
def send_request(target_url, cookies, thread_id):
    global successful_requests, total_requests

    headers = {{
        "Cache-Control": "max-age=0",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": generate_user_agent(),
        "Accept": "application/json",
        "Sec-GPC": "1",
        "Accept-Language": "tr",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": 'https://www.google.com/'
    }}

    attempt = 0
    max_attempts = 1

    while attempt < max_attempts:
        try:
            # Proxy'yi ayarla (eğer varsa)
            proxy = get_next_proxy()
            proxies = {{"http": proxy, "https": proxy}} if proxy else None  # Proxy varsa kullan, yoksa None

            # Çerezleri 'requests' formatına dönüştür
            response = requests.get(target_url, headers=headers, cookies=cookies, proxies=proxies, timeout=20)
            
            # Toplam istek sayısını günceller
            with counter_lock:
                total_requests += 1

            # Başarılı istekleri sayar (durum kodu 200 ise)
            if response.status_code == 200:
                with counter_lock:
                    successful_requests += 1
                print(f"Başarılı: {{successful_requests}}. Site: {{target_url}}. Thread: {{thread_id}}. Durum kodu: {{response.status_code}}")
                break  # Başarılıysa döngüden çık
            else:
                print(f"Başarısız: Durum kodu: {{response.status_code}}, Thread: {{thread_id}}, Toplam: {{total_requests}}")
                break  # Durum kodu 200 değilse döngüden çık
        except Exception as e:
            attempt += 1
            print(f"Hata oluştu (Thread {{thread_id}}): {{e}}. Proxy olmadan devam edilecek.")
            if attempt >= max_attempts:
                break  # Max deneme sayısına ulaştığında döngüden çık

def worker(thread_id):
    # Bu thread için cookie dosyasını seç
    cookie_file = get_cookie_file_for_thread(thread_id)
    cookies = load_cookies(cookie_file) if cookie_file else {{}}
    
    if cookie_file:
        print(f"Thread {{thread_id}} cookie dosyası: {{os.path.basename(cookie_file)}}")
    else:
        print(f"Thread {{thread_id}} cookie dosyası yok")
    
    while not stop_flag.is_set():
        target_url = TARGET_URL
        
        # Arama kullanılacaksa
        if USE_SEARCH and SEARCH_QUERY:
            target_url = search_keyword(SEARCH_QUERY, TARGET_URL, cookies)
        
        send_request(target_url, cookies, thread_id)
        
        # stop_flag kontrolü ile birlikte sleep
        if not stop_flag.wait(random.uniform(1, 3)):
            continue
        else:
            break

def signal_handler(sig, frame):
    print("\\n\\nCtrl+C algılandı! Program durduruluyor...")
    print(f"Toplam gönderilen istek: {{total_requests}}")
    print(f"Başarılı istek sayısı: {{successful_requests}}")
    stop_flag.set()
    sys.exit(0)

def main():
    # Ctrl+C sinyalini yakala
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Cookie Bot başlatılıyor...")
    print(f"Hedef URL: {{TARGET_URL}}")
    print(f"Thread sayısı: {{NUM_THREADS}}")
    print(f"Cookie klasörü: {{COOKIE_FOLDER}}")
    print(f"Cookie dosya sayısı: {{len(cookie_files)}}")
    print(f"Arama kullanımı: {{USE_SEARCH}}")
    if USE_SEARCH:
        print(f"Arama sorgusu: {{SEARCH_QUERY}}")
    print(f"Durdurmak için Ctrl+C tuşlarına basın.\\n")

    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(i,))
        thread.daemon = True  # Ana program kapandığında thread'lerin de kapanmasını sağlar
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    main()
'''
    
    def start_bot(self, page, log_text):
        """Botu başlat"""
        if self.is_running:
            return
        
        try:
            self.is_running = True
            log_text.value += "\n🚀 Cookie Bot başlatılıyor..."
            page.update()
            
            # Bot'u subprocess ile başlat
            self.bot_process = subprocess.Popen(
                ["python", "-u", "Module/Cookie_Search.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # Log okuma thread'i başlat
            def read_logs():
                while self.is_running and self.bot_process:
                    try:
                        output = self.bot_process.stdout.readline()
                        if output:
                            log_text.value += f"\n{output.strip()}"
                            # UI güncellemesini ana thread'de yap
                            try:
                                page.update()
                            except:
                                pass
                        elif self.bot_process.poll() is not None:
                            break
                        time.sleep(0.1)  # CPU kullanımını azalt
                    except Exception as e:
                        log_text.value += f"\n❌ Log okuma hatası: {e}"
                        break
            
            threading.Thread(target=read_logs, daemon=True).start()
            
        except Exception as e:
            self.is_running = False
            log_text.value += f"\n❌ Bot başlatılırken hata: {e}"
            page.update()
    
    def stop_bot(self, page, log_text):
        """Botu durdur"""
        if not self.is_running:
            return
        
        try:
            self.is_running = False
            if self.bot_process:
                self.bot_process.terminate()
                self.bot_process = None
            
            log_text.value += "\n🛑 Cookie Bot durduruldu."
            page.update()
            
        except Exception as e:
            log_text.value += f"\n❌ Bot durdurulurken hata: {e}"
            page.update()

def main(page: ft.Page):
    page.title = "Cookie Bot Arayüzü"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = True
    
    bot_gui = CookieBotGUI()
    config = bot_gui.load_config()
    
    # UI Bileşenleri
    proxy_list_field = ft.TextField(
        label="Proxy Listesi (Her satıra bir proxy)",
        value=config.get("proxy_list", ""),
        multiline=True,
        min_lines=3,
        max_lines=8,
        width=900
    )
    
    num_threads_field = ft.TextField(
        label="Thread Sayısı",
        value=config.get("num_threads", "100"),
        width=200
    )
    
    target_url_field = ft.TextField(
        label="Hedef URL",
        value=config.get("target_url", "https://aowsoftware.com/"),
        width=600
    )
    
    cookie_folder_field = ft.TextField(
        label="Cookie Klasörü Yolu",
        value=config.get("cookie_folder", ""),
        width=500
    )
    
    search_query_field = ft.TextField(
        label="Arama Sorgusu (Opsiyonel)",
        value=config.get("search_query", ""),
        width=400
    )
    
    use_search_checkbox = ft.Checkbox(
        label="Anahtar kelime ile arama kullan",
        value=config.get("use_search", False)
    )
    
    cookie_files_text = ft.Text(
        value="Cookie dosyaları: Henüz taranmadı",
        size=12,
        color=ft.Colors.ORANGE_300
    )
    
    log_text = ft.Text(
        value="📋 Cookie Bot Arayüzü hazır.\n💡 Ayarları girin ve 'Ayarları Kaydet' butonuna basın.",
        size=12,
        color=ft.Colors.GREEN_300,
        selectable=True
    )
    
    def copy_logs(e):
        """Logları panoya kopyala"""
        try:
            page.set_clipboard(log_text.value)
            # Geçici bildirim göster
            original_value = log_text.value
            log_text.value += "\n📋 Loglar panoya kopyalandı!"
            page.update()
            time.sleep(1)
            log_text.value = original_value
            page.update()
        except Exception as ex:
            log_text.value += f"\n❌ Kopyalama hatası: {ex}"
            page.update()
    
    def clear_logs(e):
        """Logları temizle"""
        log_text.value = "📋 Loglar temizlendi."
        page.update()
    
    copy_button = ft.ElevatedButton(
        text="📋 Logları Kopyala",
        on_click=copy_logs,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=150
    )
    
    clear_logs_button = ft.ElevatedButton(
        text="🗑️ Logları Temizle",
        on_click=clear_logs,
        bgcolor=ft.Colors.ORANGE_600,
        color=ft.Colors.WHITE,
        width=150
    )
    
    def pick_cookie_folder(e):
        """Cookie klasörü seç"""
        def folder_picker_result(e: ft.FilePickerResultEvent):
            if e.path:
                cookie_folder_field.value = e.path
                # Cookie dosyalarını tara
                cookie_files = bot_gui.scan_cookie_files(e.path)
                if cookie_files:
                    file_names = [os.path.basename(f) for f in cookie_files]
                    cookie_files_text.value = f"Cookie dosyaları ({len(cookie_files)}): {', '.join(file_names[:5])}{'...' if len(file_names) > 5 else ''}"
                    cookie_files_text.color = ft.Colors.GREEN_300
                else:
                    cookie_files_text.value = "Cookie dosyaları: Klasörde .txt veya .json dosyası bulunamadı"
                    cookie_files_text.color = ft.Colors.RED_300
                page.update()
        
        folder_picker = ft.FilePicker(on_result=folder_picker_result)
        page.overlay.append(folder_picker)
        page.update()
        folder_picker.get_directory_path()
    
    def save_settings(e):
        """Ayarları kaydet ve dosyayı güncelle"""
        config = {
            "proxy_list": proxy_list_field.value,
            "num_threads": num_threads_field.value,
            "target_url": target_url_field.value,
            "cookie_folder": cookie_folder_field.value,
            "search_query": search_query_field.value,
            "use_search": use_search_checkbox.value
        }
        
        # Konfigürasyonu kaydet
        bot_gui.save_config(config)
        
        # Cookie_Search.py dosyasını güncelle
        success = bot_gui.update_cookie_file(
            proxy_list_field.value,
            num_threads_field.value,
            target_url_field.value,
            cookie_folder_field.value,
            search_query_field.value,
            use_search_checkbox.value
        )
        
        if success:
            log_text.value += "\n✅ Ayarlar kaydedildi ve Cookie_Search.py dosyası güncellendi!"
            # Cookie dosyalarını tekrar tara
            cookie_files = bot_gui.scan_cookie_files(cookie_folder_field.value)
            if cookie_files:
                file_names = [os.path.basename(f) for f in cookie_files]
                cookie_files_text.value = f"Cookie dosyaları ({len(cookie_files)}): {', '.join(file_names[:5])}{'...' if len(file_names) > 5 else ''}"
                cookie_files_text.color = ft.Colors.GREEN_300
        else:
            log_text.value += "\n❌ Ayarlar kaydedilirken hata oluştu!"
        
        page.update()
    
    def start_bot_click(e):
        """Bot başlat butonuna tıklandığında"""
        bot_gui.start_bot(page, log_text)
    
    def stop_bot_click(e):
        """Bot durdur butonuna tıklandığında"""
        bot_gui.stop_bot(page, log_text)
    
    def clear_logs(e):
        """Logları temizle"""
        log_text.value = "📋 Loglar temizlendi."
        page.update()
    
    # Butonlar
    folder_button = ft.ElevatedButton(
        text="📁 Klasör Seç",
        on_click=pick_cookie_folder,
        bgcolor=ft.Colors.PURPLE_600,
        color=ft.Colors.WHITE
    )
    
    save_button = ft.ElevatedButton(
        text="💾 Ayarları Kaydet",
        on_click=save_settings,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE
    )
    
    start_button = ft.ElevatedButton(
        text="🚀 Cookie Bot Başlat",
        on_click=start_bot_click,
        bgcolor=ft.Colors.GREEN_600,
        color=ft.Colors.WHITE
    )
    
    stop_button = ft.ElevatedButton(
        text="🛑 Cookie Bot Durdur",
        on_click=stop_bot_click,
        bgcolor=ft.Colors.RED_600,
        color=ft.Colors.WHITE
    )
    
    clear_button = ft.ElevatedButton(
        text="🗑️ Logları Temizle",
        on_click=clear_logs,
        bgcolor=ft.Colors.ORANGE_600,
        color=ft.Colors.WHITE
    )
    
    # Ana layout
    page.add(
        ft.Column([
            ft.Text("🍪 Cookie Bot Arayüzü", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
            ft.Divider(),
            
            # Ayarlar bölümü
            ft.Text("⚙️ Bot Ayarları", size=18, weight=ft.FontWeight.BOLD),
            proxy_list_field,
            ft.Row([
                num_threads_field,
                target_url_field
            ]),
            
            # Cookie ayarları
            ft.Text("🍪 Cookie Ayarları", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                cookie_folder_field,
                folder_button
            ]),
            cookie_files_text,
            
            # Arama ayarları
            ft.Text("🔍 Arama Ayarları", size=16, weight=ft.FontWeight.BOLD),
            use_search_checkbox,
            search_query_field,
            ft.Text("💡 Arama kullanılmazsa direkt hedef URL'ye istek atılır", size=10, color=ft.Colors.GREY_400),
            
            # Butonlar
            ft.Row([
                save_button,
                start_button,
                stop_button,
                clear_button
            ], spacing=10),
            
            ft.Divider(),
            
            # Log bölümü
            ft.Text("📊 Bot Durumu ve Loglar", size=18, weight=ft.FontWeight.BOLD),
            ft.Row([
                copy_button,
                clear_logs_button
            ], spacing=10),
            ft.Container(
                content=ft.Column([
                    log_text
                ], scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.Colors.GREY_900,
                padding=10,
                border_radius=5,
                height=200,
                width=950
            )
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    )

if __name__ == "__main__":
    ft.app(target=main)