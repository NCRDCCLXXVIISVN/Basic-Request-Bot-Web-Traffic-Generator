import flet as ft
import json
import os
import subprocess
import threading
import time
import glob
from pathlib import Path
from datetime import datetime

# Language translations
TRANSLATIONS = {
    "en": {
        "title": "Request Bot Center",
        "direct_tab": "🚀 Direct Bot",
        "cookie_tab": "🍪 Cookie Bot",
        "google_tab": "🔍 Google Bot",
        "language": "Language",
        "proxy_list": "Proxy List (one per line)",
        "thread_count": "Thread Count",
        "target_url": "Target URL",
        "save_settings": "💾 Save Settings",
        "start_bot": "▶️ Start",
        "stop_bot": "⏹️ Stop",
        "logs": "📊 General Logs",
        "clear_logs": "🗑️ Clear Logs",
        "copy_logs": "📋 Copy Logs",
        "bot_logs": "📊 Bot Logs",
        "direct_logs": "📊 Direct Bot Logs",
        "cookie_logs": "📊 Cookie Bot Logs",
        "google_logs": "📊 Google Bot Logs",
        "cookie_folder": "Cookie Folder Path",
        "search_query": "Search Query",
        "use_search": "Use keyword search",
        "direct_description": "Direct Traffic Bot sends direct traffic to your target URL using proxies. Configure proxies, thread count, and target URL to start generating traffic.",
        "cookie_description": "Cookie Bot uses saved cookies to simulate real user sessions. Set cookie folder path, search query, and enable search functionality as needed.",
        "google_description": "Google Bot performs Google searches and clicks on your target URL. Configure search queries and proxies to generate organic-looking traffic.",
        "test_notice": "This is a program made for testing purposes.",
        "welcome_message": "🎯 Welcome to AOWSoftware Bot Center!\n💡 Select the bot you want, configure settings and start.",
        "folder_select": "📁 Select Folder",
        "optional": "(Optional)",
        "bot_starting": "🚀 Bot is starting...",
        "bot_started": "🚀 Bot started successfully!",
        "bot_stopped": "🛑 Bot stopped.",
        "bot_already_running": "❌ Bot is already running!",
        "bot_not_running": "⚠️ Bot is not running!",
        "bot_start_error": "❌ Error starting bot:",
        "bot_stop_error": "❌ Could not stop bot!",
        "bot_stop_error_detailed": "❌ Error stopping bot:",
        "logs_cleared": "📋 Logs cleared.",
        "successful_request": "Successful:",
        "failed_request": "Failed:",
        "status_code": "Status code:",
        "total_requests": "Total:",
        "error_occurred": "Error occurred:",
        "proxy_changed": "Proxy will be changed and continue.",
        "log_read_error": "❌ Log reading error:",
        "target_link_found": "Target link found -> href:",
        "suitable_url_not_found": "Suitable URL not found for",
        "search_error": "Search error:",
        "txt_cookie_read_error": "TXT cookie file reading error:",
        "json_cookie_read_error": "JSON cookie file reading error:",
        "html_parse_error": "HTML parse error:",
        "thread_cookie_file": "Thread",
        "cookie_file": "cookie file:",
        "no_cookie_file": "no cookie file",
        "ctrl_c_detected": "\n\nCtrl+C detected! Program is stopping...",
        "total_sent_requests": "Total sent requests:",
        "successful_request_count": "Successful request count:",
        "traffic_bot_starting": "Traffic bot is starting...",
        "target_url": "Target URL:",
        "thread_count": "Thread count:",
        "stop_with_ctrl_c": "Press Ctrl+C to stop.\n",
        "cookie_bot_starting": "Cookie Bot is starting...",
        "cookie_folder": "Cookie folder:",
        "cookie_file_count": "Cookie file count:",
        "search_usage": "Search usage:",
        "search_query": "Search query:",
        "google_search_bot_starting": "Google search bot is starting..."
    },
    "tr": {
        "title": "AOWSoftware Bot Merkezi",
        "direct_tab": "🚀 Direct Bot",
        "cookie_tab": "🍪 Cookie Bot",
        "google_tab": "🔍 Google Bot",
        "language": "Dil",
        "proxy_list": "Proxy Listesi (Her satıra bir proxy)",
        "thread_count": "Thread Sayısı",
        "target_url": "Hedef URL",
        "save_settings": "💾 Ayarları Kaydet",
        "start_bot": "▶️ Başlat",
        "stop_bot": "⏹️ Durdur",
        "logs": "📊 Genel Loglar",
        "clear_logs": "🗑️ Logları Temizle",
        "copy_logs": "📋 Logları Kopyala",
        "bot_logs": "📊 Bot Logları",
        "direct_logs": "📊 Direct Bot Logları",
        "cookie_logs": "📊 Cookie Bot Logları",
        "google_logs": "📊 Google Bot Logları",
        "cookie_folder": "Cookie Klasörü Yolu",
        "search_query": "Arama Sorgusu",
        "use_search": "Anahtar kelime ile arama kullan",
        "direct_description": "Direkt Trafik Bot, proxy'ler kullanarak hedef URL'nize direkt trafik gönderir. Trafik oluşturmaya başlamak için proxy'leri, thread sayısını ve hedef URL'yi yapılandırın.",
        "cookie_description": "Cookie Bot, gerçek kullanıcı oturumlarını simüle etmek için kaydedilmiş cookie'leri kullanır. Cookie klasör yolunu, arama sorgusunu ayarlayın ve gerektiğinde arama işlevini etkinleştirin.",
        "google_description": "Google Bot, Google aramaları yapar ve hedef URL'nizi tıklar. Organik görünümlü trafik oluşturmak için arama sorgularını ve proxy'leri yapılandırın.",
        "test_notice": "Bu bir test amaçlı yapılmış bir programdır.",
        "welcome_message": "🎯 AOWSoftware Bot Merkezi'ne hoş geldiniz!\n💡 İstediğiniz botu seçin, ayarları yapın ve başlatın.",
        "folder_select": "📁 Klasör Seç",
        "optional": "(Opsiyonel)",
        "bot_starting": "🚀 Bot başlatılıyor...",
        "bot_started": "🚀 Bot başarıyla başlatıldı!",
        "bot_stopped": "🛑 Bot durduruldu.",
        "bot_already_running": "❌ Bot zaten çalışıyor!",
        "bot_not_running": "⚠️ Bot çalışmıyor!",
        "bot_start_error": "❌ Bot başlatılırken hata:",
        "bot_stop_error": "❌ Bot durdurulamadı!",
        "bot_stop_error_detailed": "❌ Bot durdurulurken hata:",
        "logs_cleared": "📋 Loglar temizlendi.",
        "successful_request": "Başarılı:",
        "failed_request": "Başarısız:",
        "status_code": "Durum kodu:",
        "total_requests": "Toplam:",
        "error_occurred": "Hata oluştu:",
        "proxy_changed": "Proxy değiştirilerek devam edilecek.",
        "log_read_error": "❌ Log okuma hatası:",
        "target_link_found": "Belirlenen link bulundu -> href:",
        "suitable_url_not_found": "için uygun URL bulunamadı",
        "search_error": "Arama hatası:",
        "txt_cookie_read_error": "TXT cookie dosyası okuma hatası:",
        "json_cookie_read_error": "JSON cookie dosyası okuma hatası:",
        "html_parse_error": "HTML parse hatası:",
        "thread_cookie_file": "Thread",
        "cookie_file": "cookie dosyası:",
        "no_cookie_file": "cookie dosyası yok",
        "ctrl_c_detected": "\n\nCtrl+C algılandı! Program durduruluyor...",
        "total_sent_requests": "Toplam gönderilen istek:",
        "successful_request_count": "Başarılı istek sayısı:",
        "traffic_bot_starting": "Trafik botu başlatılıyor...",
        "target_url": "Hedef URL:",
        "thread_count": "Thread sayısı:",
        "stop_with_ctrl_c": "Durdurmak için Ctrl+C tuşlarına basın.\n",
        "cookie_bot_starting": "Cookie Bot başlatılıyor...",
        "cookie_folder": "Cookie klasörü:",
        "cookie_file_count": "Cookie dosya sayısı:",
        "search_usage": "Arama kullanımı:",
        "search_query": "Arama sorgusu:",
        "google_search_bot_starting": "Google arama botu başlatılıyor..."
    }
}

class MainBotGUI:
    def __init__(self):
        # Direct Bot için
        self.direct_config_file = "bot_config.json"
        self.direct_process = None
        self.direct_log_text = None
        
        # Cookie Bot için
        self.cookie_config_file = "cookie_config.json"
        self.cookie_process = None
        self.cookie_is_running = False
        self.cookie_files = []
        self.cookie_log_text = None
        
        # Google Bot için
        self.google_config_file = "google_config.json"
        self.google_process = None
        self.google_is_running = False
        self.google_log_text = None
        
        # Language support
        self.current_language = self.load_language()  # Load from config
        self.translations = TRANSLATIONS
    
    def load_language(self):
        """Load language setting from config.json"""
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    config = json.load(f)
                    return config.get("language", "en")
        except:
            pass
        return "en"  # Default to English
    
    def get_text(self, key):
        return self.translations[self.current_language].get(key, key)
    
    def copy_to_clipboard(self, page, text):
        """Metni panoya kopyala"""
        try:
            page.set_clipboard(text)
            return True
        except:
            return False
    
    def change_language(self, new_language, page):
        self.current_language = new_language
        
        # Save language setting to config.json
        try:
            config = {"language": new_language}
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Language setting save error: {e}")
        
        # Update page title
        page.title = self.get_text("title")
        # Trigger UI update by recreating the main interface
        page.clean()
        main(page)
    
    # Direct Bot Methods
    def load_direct_config(self):
        """Direct bot ayarlarını yükle"""
        try:
            if os.path.exists(self.direct_config_file):
                with open(self.direct_config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return {
                        'proxy_list': config.get('proxy_list', ['']),
                        'num_threads': config.get('num_threads', 100),
                        'target_url': config.get('target_url', 'https://aowsoftware.com/')
                    }
        except:
            pass
        return {
            'proxy_list': [''],
            'num_threads': 100,
            'target_url': 'https://aowsoftware.com/'
        }
    
    def save_direct_config(self, config):
        """Direct bot ayarlarını kaydet"""
        with open(self.direct_config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def update_direct_file(self, proxy_list, num_threads, target_url):
        """Direct bot dosyasını güncelle"""
        try:
            with open('Module/direct.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # PROXY_LIST güncelle
            proxy_str = ',\n    '.join([f'"{proxy}"' for proxy in proxy_list if proxy.strip()])
            if proxy_str:
                new_proxy_list = f"PROXY_LIST = [\n    {proxy_str}\n]"
            else:
                new_proxy_list = "PROXY_LIST = []"
            
            # Regex ile değiştir
            import re
            content = re.sub(r'PROXY_LIST = \[[^\]]*\]', new_proxy_list, content, flags=re.DOTALL)
            content = re.sub(r'NUM_THREADS = \d+', f'NUM_THREADS = {num_threads}', content)
            content = re.sub(r"TARGET_URL = '[^']*'", f"TARGET_URL = '{target_url}'", content)
            
            with open('Module/direct.py', 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Direct dosya güncelleme hatası: {e}")
            return False
    
    # Cookie Bot Methods
    def load_cookie_config(self):
        """Cookie bot ayarlarını yükle"""
        if os.path.exists(self.cookie_config_file):
            try:
                with open(self.cookie_config_file, 'r', encoding='utf-8') as f:
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
    
    def save_cookie_config(self, config):
        """Cookie bot ayarlarını kaydet"""
        try:
            with open(self.cookie_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Cookie konfigürasyon kaydedilemedi: {e}")
    
    def scan_cookie_files(self, folder_path):
        """Cookie klasöründeki dosyaları tara"""
        if not folder_path or not os.path.exists(folder_path):
            return []
        
        cookie_files = []
        txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
        json_files = glob.glob(os.path.join(folder_path, "*.json"))
        
        cookie_files.extend(txt_files)
        cookie_files.extend(json_files)
        
        return sorted(cookie_files)
    
    def update_cookie_file(self, proxy_list, num_threads, target_url, cookie_folder, search_query, use_search):
        """Cookie_Search.py dosyasını güncelle"""
        try:
            cookie_file_path = "Module/Cookie_Search.py"
            with open(cookie_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            proxies = [proxy.strip() for proxy in proxy_list.split('\n') if proxy.strip()]
            proxy_list_str = '[\n    "' + '",\n    "'.join(proxies) + '"\n]'
            
            self.cookie_files = self.scan_cookie_files(cookie_folder)
            
            new_content = self.generate_updated_cookie_script(
                proxy_list_str, num_threads, target_url, 
                cookie_folder, search_query, use_search
            )
            
            with open(cookie_file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return True
        except Exception as e:
            print(f"Cookie dosya güncellenirken hata: {e}")
            return False
    
    def generate_updated_cookie_script(self, proxy_list_str, num_threads, target_url, cookie_folder, search_query, use_search):
        """Güncellenmiş Cookie_Search.py içeriğini oluştur"""
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

# Proxy\'yi döngüyle kullanmak için global bir index
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

# Proxy\'yi döngü ile almak için yardımcı fonksiyon
def get_next_proxy():
    global proxy_index
    with proxy_lock:
        if len(PROXY_LIST) == 0:
            return None  # Proxy listesi boşsa None döner ve proxy olmadan devam eder
        proxy = PROXY_LIST[proxy_index]
        proxy_index = (proxy_index + 1) % len(PROXY_LIST)
        return proxy

# Cookie dosyasını thread ID\'sine göre seç
def get_cookie_file_for_thread(thread_id):
    if not cookie_files:
        return None
    return cookie_files[thread_id % len(cookie_files)]

# TXT formatında çerezleri yükleme fonksiyonu
def load_cookies_txt(file_path):
    cookies = {{}}
    try:
        with open(file_path, \'r\', encoding=\'utf-8\') as file:
            for line in file:
                if not line.strip() or line.startswith("#"):
                    continue  # Yorum satırlarını ve boş satırları atla
                parts = line.strip().split(\'\\t\')
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
        with open(file_path, \'r\', encoding=\'utf-8\') as file:
            data = json.load(file)
            if isinstance(data, list):
                for cookie in data:
                    if \'name\' in cookie and \'value\' in cookie:
                        cookies[cookie[\'name\']] = cookie[\'value\']
            elif isinstance(data, dict):
                cookies = data
    except Exception as e:
        print(f"JSON cookie dosyası okuma hatası: {{e}}")
    return cookies

# Çerezleri yükleme ana fonksiyonu
def load_cookies(file_path):
    if not file_path or not os.path.exists(file_path):
        return {{}}
    
    if file_path.endswith(\'.txt\'):
        return load_cookies_txt(file_path)
    elif file_path.endswith(\'.json\'):
        return load_cookies_json(file_path)
    else:
        return {{}}

# HTML\'den URL alma fonksiyonu
def html_den_url_al(html, belirlenen_site):
    try:
        soup = BeautifulSoup(html, \'html.parser\')
        for link in soup.find_all(\'a\'):
            href = link.get(\'href\')
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
            ("Referer", \'https://www.google.com/\')
        ]
        request.install_opener(opener)

        req = request.Request(search_url)
        response = opener.open(req, timeout=20)
        html = response.read().decode(\'utf-8\')
        
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
        "Referer": \'https://www.google.com/\'
    }}

    attempt = 0
    max_attempts = 1

    while attempt < max_attempts:
        try:
            # Proxy\'yi ayarla (eğer varsa)
            proxy = get_next_proxy()
            proxies = {{"http": proxy, "https": proxy}} if proxy else None  # Proxy varsa kullan, yoksa None

            # Çerezleri \'requests\' formatına dönüştür
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
        thread.daemon = True  # Ana program kapandığında thread\'lerin de kapanmasını sağlar
        thread.start()
        threads.append(thread)

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
'''
    
    # Google Bot Methods
    def load_google_config(self):
        """Google bot ayarlarını yükle"""
        if os.path.exists(self.google_config_file):
            try:
                with open(self.google_config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "proxy_list": "http://M9Z7JPUKo8Vmei9g:IUuuMf4LkexA8wSn_counusy-tr_session-kZvLa1Sv_lifetime-30m_suseaming-1@geo.iproyal.com:12321",
            "num_threads": "100",
            "search_query": "web trafik botu",
            "target_url": "https://www.instagram.com/reel/DES86L4Oafp/"
        }
    
    def save_google_config(self, config):
        """Google bot ayarlarını kaydet"""
        try:
            with open(self.google_config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Google konfigürasyon kaydedilemedi: {e}")
    
    def update_google_file(self, proxy_list, num_threads, search_query, target_url):
        """google.py dosyasını güncelle"""
        try:
            google_file_path = "Module/google.py"
            with open(google_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            proxies = [proxy.strip() for proxy in proxy_list.split('\n') if proxy.strip()]
            proxy_list_str = '[\n    "' + '",\n    "'.join(proxies) + '"\n]'
            
            lines = content.split('\n')
            new_lines = []
            in_proxy_list = False
            
            for line in lines:
                if line.startswith('PROXY_LIST = ['):
                    new_lines.append(f'PROXY_LIST = {proxy_list_str}')
                    in_proxy_list = True
                elif in_proxy_list and line.strip() == ']':
                    in_proxy_list = False
                    continue
                elif in_proxy_list:
                    continue
                elif line.startswith('NUM_THREADS = '):
                    new_lines.append(f'NUM_THREADS = {num_threads}  # İş parçacığı sayısını artırabilirsiniz')
                elif line.startswith('SEARCH_QUERY = '):
                    new_lines.append(f'SEARCH_QUERY = \'{search_query}\'  # Aramak istediğiniz sorgu')
                elif line.startswith('TARGET_URL = '):
                    new_lines.append(f'TARGET_URL = \'{target_url}\'  # Aranacak ve istek yapılacak link')
                else:
                    new_lines.append(line)
            
            with open(google_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            return True
        except Exception as e:
            print(f"Google dosya güncellenirken hata: {e}")
            return False
    
    # Bot Control Methods
    def start_direct_bot(self, page, log_text):
        """Direct bot başlat"""
        print("start_direct_bot method called!")  # Debug
        if self.direct_process:
            message = f"\n{self.get_text('bot_already_running')}"
            log_text.value += message
            if hasattr(self, 'direct_log_text'):
                self.direct_log_text.value += message
            page.update()
            return
        
        try:
            print("Attempting to start direct bot subprocess...")  # Debug
            self.direct_process = subprocess.Popen(
                ['python', '-u', 'Module/direct.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,
                universal_newlines=True
            )
            print(f"Direct bot subprocess started with PID: {self.direct_process.pid}")  # Debug
            
            def read_direct_logs():
                while self.direct_process and self.direct_process.poll() is None:
                    try:
                        output = self.direct_process.stdout.readline()
                        if output and output.strip():
                            # Ana log alanına ekle
                            log_text.value += f"\n[DIRECT] {output.strip()}"
                            # Direct bot özel log alanına ekle
                            if hasattr(self, 'direct_log_text') and self.direct_log_text:
                                self.direct_log_text.value += f"\n{output.strip()}"
                            print(f"Direct bot log: {output.strip()}")  # Debug
                            try:
                                page.update()
                            except Exception as e:
                                print(f"Page update error: {e}")  # Debug
                        time.sleep(0.1)
                    except Exception as e:
                        print(f"Log reading error: {e}")  # Debug
                        break
                print("Direct bot log reading thread ended")  # Debug
            
            threading.Thread(target=read_direct_logs, daemon=True).start()
            success_message = f"\n{self.get_text('bot_started')}"
            log_text.value += success_message
            if hasattr(self, 'direct_log_text'):
                self.direct_log_text.value += success_message
            page.update()
            
        except Exception as e:
            error_message = f"\n{self.get_text('bot_start_error')} {e}"
            log_text.value += error_message
            if hasattr(self, 'direct_log_text'):
                self.direct_log_text.value += error_message
            page.update()
    
    def stop_direct_bot(self, page, log_text):
        """Direct bot durdur"""
        if self.direct_process:
            try:
                self.direct_process.terminate()
                self.direct_process = None
                stop_message = f"\n{self.get_text('bot_stopped')}"
                log_text.value += stop_message
                if hasattr(self, 'direct_log_text') and self.direct_log_text:
                    self.direct_log_text.value += stop_message
            except:
                error_message = f"\n{self.get_text('bot_stop_error')}"
                log_text.value += error_message
                if hasattr(self, 'direct_log_text') and self.direct_log_text:
                    self.direct_log_text.value += error_message
        else:
            not_running_message = f"\n{self.get_text('bot_not_running')}"
            log_text.value += not_running_message
            if hasattr(self, 'direct_log_text') and self.direct_log_text:
                self.direct_log_text.value += not_running_message
        page.update()
    
    def start_cookie_bot(self, page, log_text):
        """Cookie bot başlat"""
        if self.cookie_is_running:
            message = f"\n{self.get_text('bot_already_running')}"
            log_text.value += message
            if hasattr(self, 'cookie_log_text'):
                self.cookie_log_text.value += message
            page.update()
            return
        
        try:
            self.cookie_is_running = True
            self.cookie_process = subprocess.Popen(
                ["python", "-u", "Module/Cookie_Search.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=0,
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            def read_cookie_logs():
                while self.cookie_is_running and self.cookie_process:
                    try:
                        output = self.cookie_process.stdout.readline()
                        if output and output.strip():
                            # Ana log alanına ekle
                            log_text.value += f"\n[COOKIE] {output.strip()}"
                            # Cookie bot özel log alanına ekle
                            if hasattr(self, 'cookie_log_text') and self.cookie_log_text:
                                self.cookie_log_text.value += f"\n{output.strip()}"
                            try:
                                page.update()
                            except:
                                pass
                        elif self.cookie_process.poll() is not None:
                            break
                        time.sleep(0.1)
                    except:
                        break
            
            threading.Thread(target=read_cookie_logs, daemon=True).start()
            success_message = f"\n{self.get_text('bot_started')}"
            log_text.value += success_message
            if hasattr(self, 'cookie_log_text'):
                self.cookie_log_text.value += success_message
            page.update()
            
        except Exception as e:
            self.cookie_is_running = False
            error_message = f"\n{self.get_text('bot_start_error')} {e}"
            log_text.value += error_message
            if hasattr(self, 'cookie_log_text'):
                self.cookie_log_text.value += error_message
            page.update()
    
    def stop_cookie_bot(self, page, log_text):
        """Cookie bot durdur"""
        if not self.cookie_is_running:
            not_running_message = f"\n{self.get_text('bot_not_running')}"
            log_text.value += not_running_message
            if hasattr(self, 'cookie_log_text') and self.cookie_log_text:
                self.cookie_log_text.value += not_running_message
            page.update()
            return
        
        try:
            self.cookie_is_running = False
            if self.cookie_process:
                self.cookie_process.terminate()
                self.cookie_process = None
            
            stop_message = f"\n{self.get_text('bot_stopped')}"
            log_text.value += stop_message
            if hasattr(self, 'cookie_log_text') and self.cookie_log_text:
                self.cookie_log_text.value += stop_message
            page.update()
            
        except Exception as e:
            error_message = f"\n{self.get_text('bot_stop_error_detailed')} {e}"
            log_text.value += error_message
            page.update()
    
    def start_google_bot(self, page, log_text):
        """Google bot başlat"""
        if self.google_is_running:
            message = f"\n{self.get_text('bot_already_running')}"
            log_text.value += message
            if hasattr(self, 'google_log_text'):
                self.google_log_text.value += message
            page.update()
            return
        
        try:
            self.google_is_running = True
            self.google_process = subprocess.Popen(
                ["python", "-u", "Module/google.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,
                universal_newlines=True
            )
            
            def read_google_logs():
                while self.google_is_running and self.google_process:
                    try:
                        output = self.google_process.stdout.readline()
                        if output and output.strip():
                            # Ana log alanına ekle
                            log_text.value += f"\n[GOOGLE] {output.strip()}"
                            # Google bot özel log alanına ekle
                            if hasattr(self, 'google_log_text') and self.google_log_text:
                                self.google_log_text.value += f"\n{output.strip()}"
                            try:
                                page.update()
                            except:
                                pass
                        elif self.google_process.poll() is not None:
                            break
                        time.sleep(0.1)
                    except:
                        break
            
            threading.Thread(target=read_google_logs, daemon=True).start()
            message = f"\n{self.get_text('bot_started')}"
            log_text.value += message
            if hasattr(self, 'google_log_text'):
                self.google_log_text.value += message
            page.update()
            
        except Exception as e:
            self.google_is_running = False
            message = f"\n{self.get_text('bot_start_error')} {e}"
            log_text.value += message
            if hasattr(self, 'google_log_text'):
                self.google_log_text.value += message
            page.update()
    
    def stop_google_bot(self, page, log_text):
        """Google bot durdur"""
        if not self.google_is_running:
            message = f"\n{self.get_text('bot_not_running')}"
            log_text.value += message
            if hasattr(self, 'google_log_text') and self.google_log_text:
                self.google_log_text.value += message
            page.update()
            return
        
        try:
            self.google_is_running = False
            if self.google_process:
                self.google_process.terminate()
                self.google_process = None
            
            message = f"\n{self.get_text('bot_stopped')}"
            log_text.value += message
            if hasattr(self, 'google_log_text') and self.google_log_text:
                self.google_log_text.value += message
            page.update()
            
        except Exception as e:
            message = f"\n{self.get_text('bot_stop_error_detailed')} {e}"
            log_text.value += message
            if hasattr(self, 'google_log_text') and self.google_log_text:
                self.google_log_text.value += message
            page.update()

# Global bot_gui instance
bot_gui = None

def main(page: ft.Page):
    global bot_gui
    if bot_gui is None:
        bot_gui = MainBotGUI()
    
    page.title = bot_gui.get_text("title")
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 900
    page.window_resizable = True
    
    # Language selector
    def on_language_change(e):
        bot_gui.change_language(e.control.value, page)
    
    language_dropdown = ft.Dropdown(
        label=bot_gui.get_text("language"),
        value=bot_gui.current_language,
        options=[
            ft.dropdown.Option("en", "English"),
            ft.dropdown.Option("tr", "Türkçe")
        ],
        on_change=on_language_change,
        width=150
    )
    
    # Ana log alanı
    main_log_text = ft.Text(
        value=bot_gui.get_text("welcome_message"),
        size=12,
        color=ft.Colors.GREEN_300,
        selectable=True,
        no_wrap=False,
        expand=True
    )
    
    def clear_main_logs(e):
        """Ana logları temizle"""
        main_log_text.value = f"📋 {bot_gui.get_text('logs_cleared')}"
        page.update()
    
    # Direct Bot Tab
    def create_direct_tab():
        nonlocal main_log_text  # main_log_text'e erişim için
        direct_config = bot_gui.load_direct_config()
        
        # Direct Bot Log Text
        direct_log_text = ft.Text(
            value=f"📋 {bot_gui.get_text('direct_tab')} ready. Configure settings and start.",
            size=12,
            color=ft.Colors.GREEN_300,
            selectable=True,
            no_wrap=False,
            expand=True
        )
        bot_gui.direct_log_text = direct_log_text
        
        def clear_direct_logs(e):
            """Direct bot loglarını temizle"""
            direct_log_text.value = f"📋 {bot_gui.get_text('logs_cleared')}"
            page.update()
        
        def copy_direct_logs(e):
            """Direct bot loglarını kopyala"""
            if bot_gui.copy_to_clipboard(page, direct_log_text.value):
                main_log_text.value += "\n📋 Direct bot logları panoya kopyalandı!"
            else:
                main_log_text.value += "\n❌ Loglar kopyalanamadı!"
            page.update()
        
        direct_proxy_field = ft.TextField(
            label=bot_gui.get_text("proxy_list"),
            value='\n'.join(direct_config['proxy_list']),
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=700
        )
        
        direct_threads_field = ft.TextField(
            label=bot_gui.get_text("thread_count"),
            value=str(direct_config['num_threads']),
            width=200
        )
        
        direct_url_field = ft.TextField(
            label=bot_gui.get_text("target_url"),
            value=direct_config['target_url'],
            width=500
        )
        
        def save_direct_settings(e):
            proxy_list = [p.strip() for p in direct_proxy_field.value.split('\n') if p.strip()]
            try:
                num_threads = int(direct_threads_field.value)
            except:
                num_threads = 100
            
            config = {
                'proxy_list': proxy_list,
                'num_threads': num_threads,
                'target_url': direct_url_field.value
            }
            
            bot_gui.save_direct_config(config)
            success = bot_gui.update_direct_file(proxy_list, num_threads, direct_url_field.value)
            
            if success:
                direct_log_text.value += f"\n✅ {bot_gui.get_text('direct_tab')} settings saved!"
                main_log_text.value += f"\n✅ {bot_gui.get_text('direct_tab')} settings saved!"
            else:
                direct_log_text.value += f"\n❌ Error saving {bot_gui.get_text('direct_tab')} settings!"
                main_log_text.value += f"\n❌ Error saving {bot_gui.get_text('direct_tab')} settings!"
            page.update()
        
        def start_direct(e):
            print("Start Direct button clicked!")  # Debug log
            direct_log_text.value += f"\n🔄 {bot_gui.get_text('direct_tab')} starting..."
            main_log_text.value += f"\n🔄 {bot_gui.get_text('direct_tab')} starting..."
            page.update()
            bot_gui.start_direct_bot(page, direct_log_text)
        
        def stop_direct(e):
            bot_gui.stop_direct_bot(page, direct_log_text)
        
        return ft.Column([
            ft.Text(bot_gui.get_text("direct_tab"), size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(
                    bot_gui.get_text("direct_description"),
                    size=14,
                    color=ft.Colors.BLUE_300
                ),
                padding=10,
                bgcolor=ft.Colors.BLUE_900,
                border_radius=8
            ),
            ft.Text(bot_gui.get_text("test_notice"), size=12, color=ft.Colors.ORANGE_300, italic=True),
            ft.Divider(),
            direct_proxy_field,
            ft.Row([direct_threads_field, direct_url_field]),
            ft.Row([
                ft.ElevatedButton(bot_gui.get_text("save_settings"), on_click=save_direct_settings, bgcolor=ft.Colors.BLUE_600),
                ft.ElevatedButton(bot_gui.get_text("start_bot"), on_click=start_direct, bgcolor=ft.Colors.GREEN_600),
                ft.ElevatedButton(bot_gui.get_text("stop_bot"), on_click=stop_direct, bgcolor=ft.Colors.RED_600)
            ], spacing=10),
            ft.Divider(),
            # Direct Bot Log Bölümü
            ft.Row([
                ft.Text(bot_gui.get_text("direct_logs"), size=16, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(bot_gui.get_text("clear_logs"), on_click=clear_direct_logs, bgcolor=ft.Colors.ORANGE_600),
                ft.ElevatedButton(bot_gui.get_text("copy_logs"), on_click=copy_direct_logs, bgcolor=ft.Colors.PURPLE_600)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(
                content=ft.Column([
                    direct_log_text
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.GREY_900,
                padding=15,
                border_radius=8,
                height=200,
                expand=True
            )
        ], spacing=10)
    
    # Cookie Bot Tab
    def create_cookie_tab():
        nonlocal main_log_text  # main_log_text'e erişim için
        cookie_config = bot_gui.load_cookie_config()
        
        # Cookie Bot Log Text
        cookie_log_text = ft.Text(
            value=f"📋 {bot_gui.get_text('cookie_tab')} ready. Configure settings and start.",
            size=12,
            color=ft.Colors.GREEN_300,
            selectable=True,
            no_wrap=False,
            expand=True
        )
        bot_gui.cookie_log_text = cookie_log_text
        
        cookie_proxy_field = ft.TextField(
            label=bot_gui.get_text("proxy_list"),
            value=cookie_config.get("proxy_list", ""),
            multiline=True,
            min_lines=3,
            max_lines=8,
            width=900
        )
        
        cookie_threads_field = ft.TextField(
            label=bot_gui.get_text("thread_count"),
            value=cookie_config.get("num_threads", "100"),
            width=200
        )
        
        cookie_url_field = ft.TextField(
            label=bot_gui.get_text("target_url"),
            value=cookie_config.get("target_url", "https://aowsoftware.com/"),
            width=600
        )
        
        cookie_folder_field = ft.TextField(
            label=bot_gui.get_text("cookie_folder"),
            value=cookie_config.get("cookie_folder", ""),
            width=500
        )
        
        cookie_search_field = ft.TextField(
            label=f"{bot_gui.get_text('search_query')} {bot_gui.get_text('optional')}",
            value=cookie_config.get("search_query", ""),
            width=400
        )
        
        cookie_use_search = ft.Checkbox(
            label=bot_gui.get_text("use_search"),
            value=cookie_config.get("use_search", False)
        )
        
        cookie_files_text = ft.Text(
            value="Cookie dosyaları: Henüz taranmadı",
            size=12,
            color=ft.Colors.ORANGE_300
        )
        
        def pick_cookie_folder(e):
            def folder_picker_result(e: ft.FilePickerResultEvent):
                if e.path:
                    cookie_folder_field.value = e.path
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
        
        def clear_cookie_logs(e):
            cookie_log_text.value = ""
            page.update()
        
        def copy_cookie_logs(e):
            bot_gui.copy_to_clipboard(page, cookie_log_text.value)
        
        def save_cookie_settings(e):
            config = {
                "proxy_list": cookie_proxy_field.value,
                "num_threads": cookie_threads_field.value,
                "target_url": cookie_url_field.value,
                "cookie_folder": cookie_folder_field.value,
                "search_query": cookie_search_field.value,
                "use_search": cookie_use_search.value
            }
            
            bot_gui.save_cookie_config(config)
            success = bot_gui.update_cookie_file(
                cookie_proxy_field.value,
                cookie_threads_field.value,
                cookie_url_field.value,
                cookie_folder_field.value,
                cookie_search_field.value,
                cookie_use_search.value
            )
            
            if success:
                main_log_text.value += f"\n✅ {bot_gui.get_text('cookie_tab')} settings saved!"
                cookie_log_text.value += f"\n✅ {bot_gui.get_text('cookie_tab')} settings saved!"
                cookie_files = bot_gui.scan_cookie_files(cookie_folder_field.value)
                if cookie_files:
                    file_names = [os.path.basename(f) for f in cookie_files]
                    cookie_files_text.value = f"Cookie dosyaları ({len(cookie_files)}): {', '.join(file_names[:3])}{'...' if len(file_names) > 3 else ''}"
                    cookie_files_text.color = ft.Colors.GREEN_300
            else:
                main_log_text.value += f"\n❌ Error saving {bot_gui.get_text('cookie_tab')} settings!"
                cookie_log_text.value += f"\n❌ Error saving {bot_gui.get_text('cookie_tab')} settings!"
            page.update()
        
        def start_cookie(e):
            print("Start Cookie button clicked!")  # Debug log
            main_log_text.value += f"\n🔄 {bot_gui.get_text('cookie_tab')} starting..."
            cookie_log_text.value += f"\n🔄 {bot_gui.get_text('cookie_tab')} starting..."
            page.update()
            bot_gui.start_cookie_bot(page, main_log_text)
        
        def stop_cookie(e):
            bot_gui.stop_cookie_bot(page, main_log_text)
            cookie_log_text.value += f"\n⏹️ {bot_gui.get_text('cookie_tab')} stopped!"
            page.update()
        
        return ft.Column([
            ft.Text(bot_gui.get_text("cookie_tab"), size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(
                    bot_gui.get_text("cookie_description"),
                    size=14,
                    color=ft.Colors.BLUE_300
                ),
                padding=10,
                bgcolor=ft.Colors.BLUE_900,
                border_radius=8
            ),
            ft.Text(bot_gui.get_text("test_notice"), size=12, color=ft.Colors.ORANGE_300, italic=True),
            ft.Divider(),
            cookie_proxy_field,
            ft.Row([cookie_threads_field, cookie_url_field]),
            ft.Row([cookie_folder_field, ft.ElevatedButton(bot_gui.get_text("folder_select"), on_click=pick_cookie_folder)]),
            ft.Row([cookie_search_field, cookie_use_search]),
            cookie_files_text,
            ft.Row([
                ft.ElevatedButton(bot_gui.get_text("save_settings"), on_click=save_cookie_settings, bgcolor=ft.Colors.BLUE_600),
                ft.ElevatedButton(bot_gui.get_text("start_bot"), on_click=start_cookie, bgcolor=ft.Colors.GREEN_600),
                ft.ElevatedButton(bot_gui.get_text("stop_bot"), on_click=stop_cookie, bgcolor=ft.Colors.RED_600)
            ], spacing=10),
            ft.Divider(),
            ft.Text(bot_gui.get_text("cookie_logs"), size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(bot_gui.get_text("clear_logs"), on_click=clear_cookie_logs, bgcolor=ft.Colors.ORANGE_600),
                ft.ElevatedButton(bot_gui.get_text("copy_logs"), on_click=copy_cookie_logs, bgcolor=ft.Colors.PURPLE_600)
            ], spacing=10),
            ft.Container(
                content=ft.Column([
                    cookie_log_text
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.BLACK12,
                border_radius=8,
                padding=10,
                height=200,
                expand=True
            )
        ], spacing=10)
    
    # Google Bot Tab
    def create_google_tab():
        nonlocal main_log_text  # main_log_text'e erişim için
        google_config = bot_gui.load_google_config()
        
        # Google Bot Log Text
        google_log_text = ft.Text(
            value=f"📋 {bot_gui.get_text('google_tab')} ready. Configure settings and start.",
            size=12,
            color=ft.Colors.GREEN_300,
            selectable=True,
            no_wrap=False,
            expand=True
        )
        bot_gui.google_log_text = google_log_text
        
        google_proxy_field = ft.TextField(
            label=bot_gui.get_text("proxy_list"),
            value=google_config.get("proxy_list", ""),
            multiline=True,
            min_lines=3,
            max_lines=8,
            width=800
        )
        
        google_threads_field = ft.TextField(
            label=bot_gui.get_text("thread_count"),
            value=google_config.get("num_threads", "100"),
            width=200
        )
        
        google_search_field = ft.TextField(
            label=bot_gui.get_text("search_query"),
            value=google_config.get("search_query", "web trafik botu"),
            width=400
        )
        
        google_url_field = ft.TextField(
            label=bot_gui.get_text("target_url"),
            value=google_config.get("target_url", "https://www.instagram.com/reel/DES86L4Oafp/"),
            width=600
        )
        
        def clear_google_logs(e):
            google_log_text.value = ""
            page.update()
        
        def copy_google_logs(e):
            bot_gui.copy_to_clipboard(page, google_log_text.value)
        
        def save_google_settings(e):
            config = {
                "proxy_list": google_proxy_field.value,
                "num_threads": google_threads_field.value,
                "search_query": google_search_field.value,
                "target_url": google_url_field.value
            }
            
            bot_gui.save_google_config(config)
            success = bot_gui.update_google_file(
                google_proxy_field.value,
                google_threads_field.value,
                google_search_field.value,
                google_url_field.value
            )
            
            if success:
                main_log_text.value += f"\n✅ {bot_gui.get_text('google_tab')} settings saved!"
                google_log_text.value += f"\n✅ {bot_gui.get_text('google_tab')} settings saved!"
            else:
                main_log_text.value += f"\n❌ Error saving {bot_gui.get_text('google_tab')} settings!"
                google_log_text.value += f"\n❌ Error saving {bot_gui.get_text('google_tab')} settings!"
            page.update()
        
        def start_google(e):
            print("Start Google button clicked!")  # Debug log
            main_log_text.value += f"\n🔄 {bot_gui.get_text('google_tab')} starting..."
            google_log_text.value += f"\n🔄 {bot_gui.get_text('google_tab')} starting..."
            page.update()
            bot_gui.start_google_bot(page, main_log_text)
        
        def stop_google(e):
            bot_gui.stop_google_bot(page, main_log_text)
            google_log_text.value += f"\n⏹️ {bot_gui.get_text('google_tab')} stopped!"
            page.update()
        
        return ft.Column([
            ft.Text(bot_gui.get_text("google_tab"), size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(
                    bot_gui.get_text("google_description"),
                    size=14,
                    color=ft.Colors.BLUE_300
                ),
                padding=10,
                bgcolor=ft.Colors.BLUE_900,
                border_radius=8
            ),
            ft.Text(bot_gui.get_text("test_notice"), size=12, color=ft.Colors.ORANGE_300, italic=True),
            ft.Divider(),
            google_proxy_field,
            ft.Row([google_threads_field, google_search_field]),
            google_url_field,
            ft.Row([
                ft.ElevatedButton(bot_gui.get_text("save_settings"), on_click=save_google_settings, bgcolor=ft.Colors.BLUE_600),
                ft.ElevatedButton(bot_gui.get_text("start_bot"), on_click=start_google, bgcolor=ft.Colors.GREEN_600),
                ft.ElevatedButton(bot_gui.get_text("stop_bot"), on_click=stop_google, bgcolor=ft.Colors.RED_600)
            ], spacing=10),
            ft.Divider(),
            ft.Text(bot_gui.get_text("google_logs"), size=16, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton(bot_gui.get_text("clear_logs"), on_click=clear_google_logs, bgcolor=ft.Colors.ORANGE_600),
                ft.ElevatedButton(bot_gui.get_text("copy_logs"), on_click=copy_google_logs, bgcolor=ft.Colors.PURPLE_600)
            ], spacing=10),
            ft.Container(
                content=ft.Column([
                    google_log_text
                ], scroll=ft.ScrollMode.AUTO, expand=True),
                bgcolor=ft.Colors.BLACK12,
                border_radius=8,
                padding=10,
                height=200,
                expand=True
            )
        ], spacing=10)
    
    # Ana sayfa düzeni
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text=bot_gui.get_text("direct_tab"),
                content=ft.Container(
                    content=create_direct_tab(),
                    padding=20
                )
            ),
            ft.Tab(
                text=bot_gui.get_text("cookie_tab"),
                content=ft.Container(
                    content=create_cookie_tab(),
                    padding=20
                )
            ),
            ft.Tab(
                text=bot_gui.get_text("google_tab"),
                content=ft.Container(
                    content=create_google_tab(),
                    padding=20
                )
            )
        ],
        expand=1
    )
    
    # Ana layout - Sabit yükseklik ve pozisyon
    page.add(
        ft.Container(
            content=ft.Column([
                # Sabit header - scroll olmaz
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(bot_gui.get_text("title"), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                            language_dropdown
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Divider(),
                    ], spacing=10),
                    bgcolor=page.bgcolor,
                    padding=ft.padding.only(bottom=10)
                ),
                
                # Sekmeler - sabit
                ft.Container(
                    content=tabs,
                    padding=ft.padding.only(bottom=10)
                ),
                
                ft.Divider(),
                
                # Ana log başlığı - sabit
                ft.Container(
                    content=ft.Row([
                        ft.Text(bot_gui.get_text("logs"), size=18, weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton(bot_gui.get_text("clear_logs"), on_click=clear_main_logs, bgcolor=ft.Colors.ORANGE_600)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.only(bottom=10)
                ),
                
                # Sadece log alanı scroll olur
                ft.Container(
                    content=ft.Column([
                        main_log_text
                    ], scroll=ft.ScrollMode.AUTO, expand=True),
                    bgcolor=ft.Colors.GREY_900,
                    padding=15,
                    border_radius=8,
                    height=200,
                    expand=True
                )
            ], spacing=0),
            expand=True,
            padding=10
        )
    )

if __name__ == "__main__":
    ft.app(target=main)