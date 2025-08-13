import requests
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

PROXY_LIST = [
    "http://M9Z7JPUKo8Vmei9g:IUuuMf4LkexA8wSn_counusy-tr_session-kZvLa1Sv_lifetime-30m_suseaming-1@geo.iproyal.com:12321"
]
NUM_THREADS = 100  # Daha fazla istek için iş parçacığı sayısını artırabilirsiniz.
TARGET_URL = 'https://www.instagram.com/reel/DES86L4Oafp/'  # İstek gönderilecek URL
COOKIE_FOLDER = r'C:\\Users\\Samet\\Desktop\\BOTLAR\\SATILAN SATILACAK PROJELER\\All On Web  Request Botu\\500 cookie'  # Cookie dosyalarının bulunduğu klasör
SEARCH_QUERY = 'web trafik botu'  # Arama sorgusu
USE_SEARCH = False  # Arama kullanılacak mı?

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

# Çeviri sistemi
TRANSLATIONS = {
    "en": {
        "successful": "Successful:",
        "failed": "Failed:",
        "status_code": "Status code:",
        "total": "Total:",
        "error_occurred": "Error occurred:",
        "proxy_changed": "Proxy will be changed and continue.",
        "ctrl_c_detected": "\n\nCtrl+C detected! Program is stopping...",
        "total_sent_requests": "Total sent requests:",
        "successful_request_count": "Successful request count:",
        "cookie_bot_starting": "Cookie Bot is starting...",
        "cookie_folder": "Cookie folder:",
        "cookie_file_count": "Cookie file count:",
        "search_usage": "Search usage:",
        "search_query": "Search query:",
        "target_url": "Target URL:",
        "thread_count": "Thread count:",
        "stop_with_ctrl_c": "Press Ctrl+C to stop.\n",
        "thread_cookie_file": "Thread",
        "cookie_file": "cookie file:",
        "no_cookie_file": "no cookie file",
        "txt_cookie_read_error": "TXT cookie file reading error:",
        "json_cookie_read_error": "JSON cookie file reading error:",
        "target_link_found": "Target link found -> href:",
        "suitable_url_not_found": "Suitable URL not found for",
        "search_error": "Search error:",
        "html_parse_error": "HTML parse error:"
    },
    "tr": {
        "successful": "Başarılı:",
        "failed": "Başarısız:",
        "status_code": "Durum kodu:",
        "total": "Toplam:",
        "error_occurred": "Hata oluştu:",
        "proxy_changed": "Proxy değiştirilerek devam edilecek.",
        "ctrl_c_detected": "\n\nCtrl+C algılandı! Program durduruluyor...",
        "total_sent_requests": "Toplam gönderilen istek:",
        "successful_request_count": "Başarılı istek sayısı:",
        "cookie_bot_starting": "Cookie Bot başlatılıyor...",
        "cookie_folder": "Cookie klasörü:",
        "cookie_file_count": "Cookie dosya sayısı:",
        "search_usage": "Arama kullanımı:",
        "search_query": "Arama sorgusu:",
        "target_url": "Hedef URL:",
        "thread_count": "Thread sayısı:",
        "stop_with_ctrl_c": "Durdurmak için Ctrl+C tuşlarına basın.\n",
        "thread_cookie_file": "Thread",
        "cookie_file": "cookie dosyası:",
        "no_cookie_file": "cookie dosyası yok",
        "txt_cookie_read_error": "TXT cookie dosyası okuma hatası:",
        "json_cookie_read_error": "JSON cookie dosyası okuma hatası:",
        "target_link_found": "Belirlenen link bulundu -> href:",
        "suitable_url_not_found": "için uygun URL bulunamadı",
        "search_error": "Arama hatası:",
        "html_parse_error": "HTML parse hatası:"
    }
}

# Dil ayarını yükle
def load_language():
    try:
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('language', 'tr')
    except:
        pass
    return 'tr'

# Çeviri fonksiyonu
def get_text(key):
    language = load_language()
    return TRANSLATIONS.get(language, TRANSLATIONS['tr']).get(key, key)

# Her defasında farklı user agent oluşturur
def generate_user_agent():
    random_number = random.randint(100, 999)
    return f"Mozilla/5.0 (Linux; Android 13; SM-G{random_number}B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"

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
    cookies = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if not line.strip() or line.startswith("#"):
                    continue  # Yorum satırlarını ve boş satırları atla
                parts = line.strip().split('	')
                if len(parts) >= 7:
                    domain = parts[0]
                    name = parts[5]
                    value = parts[6]
                    cookies[name] = value
    except Exception as e:
        print(f"TXT cookie dosyası okuma hatası: {e}")
    return cookies

# JSON formatında çerezleri yükleme fonksiyonu
def load_cookies_json(file_path):
    cookies = {}
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
        print(f"JSON cookie dosyası okuma hatası: {e}")
    return cookies

# Çerezleri yükleme ana fonksiyonu
def load_cookies(file_path):
    if not file_path or not os.path.exists(file_path):
        return {}
    
    if file_path.endswith('.txt'):
        return load_cookies_txt(file_path)
    elif file_path.endswith('.json'):
        return load_cookies_json(file_path)
    else:
        return {}

# HTML'den URL alma fonksiyonu
def html_den_url_al(html, belirlenen_site):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and belirlenen_site in href:
                print(f"Belirlenen link bulundu -> href: {href}")
                return href
    except Exception as e:
        print(f"HTML parse hatası: {e}")
    return None

# Anahtar kelime arama fonksiyonu
def search_keyword(search_query, target_url, cookies):
    try:
        encoded_search_query = parse.quote(search_query)
        search_url = f"https://www.google.com/search?q={encoded_search_query}&num=100"
        
        proxy = get_next_proxy()
        if proxy:
            proxy_support = request.ProxyHandler({
                "http": proxy,
                "https": proxy,
            })
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
            print(f"{search_query} için uygun URL bulunamadı.")
            return target_url
            
    except Exception as e:
        print(f"Arama hatası: {e}")
        return target_url

# İstek gönderimi için her defasında farklı ping sağlar
def send_request(target_url, cookies, thread_id):
    global successful_requests, total_requests

    headers = {
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
    }

    attempt = 0
    max_attempts = 1

    while attempt < max_attempts:
        try:
            # Proxy'yi ayarla (eğer varsa)
            proxy = get_next_proxy()
            proxies = {"http": proxy, "https": proxy} if proxy else None  # Proxy varsa kullan, yoksa None

            # Çerezleri 'requests' formatına dönüştür
            response = requests.get(target_url, headers=headers, cookies=cookies, proxies=proxies, timeout=20)
            
            # Toplam istek sayısını günceller
            with counter_lock:
                total_requests += 1

            # Başarılı istekleri sayar (durum kodu 200 ise)
            if response.status_code == 200:
                with counter_lock:
                    successful_requests += 1
                print(f"Başarılı: {successful_requests}. Site: {target_url}. Thread: {thread_id}. Durum kodu: {response.status_code}")
                break  # Başarılıysa döngüden çık
            else:
                print(f"Başarısız: Durum kodu: {response.status_code}, Thread: {thread_id}, Toplam: {total_requests}")
                break  # Durum kodu 200 değilse döngüden çık
        except Exception as e:
            attempt += 1
            print(f"Hata oluştu (Thread {thread_id}): {e}. Proxy olmadan devam edilecek.")
            if attempt >= max_attempts:
                break  # Max deneme sayısına ulaştığında döngüden çık

def worker(thread_id):
    # Bu thread için cookie dosyasını seç
    cookie_file = get_cookie_file_for_thread(thread_id)
    cookies = load_cookies(cookie_file) if cookie_file else {}
    
    if cookie_file:
        print(f"Thread {thread_id} cookie dosyası: {os.path.basename(cookie_file)}")
    else:
        print(f"Thread {thread_id} cookie dosyası yok")
    
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
    print("\n\nCtrl+C algılandı! Program durduruluyor...")
    print(f"Toplam gönderilen istek: {total_requests}")
    print(f"Başarılı istek sayısı: {successful_requests}")
    stop_flag.set()
    sys.exit(0)

def main():
    # Ctrl+C sinyalini yakala
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"Cookie Bot başlatılıyor...")
    print(f"Hedef URL: {TARGET_URL}")
    print(f"Thread sayısı: {NUM_THREADS}")
    print(f"Cookie klasörü: {COOKIE_FOLDER}")
    print(f"Cookie dosya sayısı: {len(cookie_files)}")
    print(f"Arama kullanımı: {USE_SEARCH}")
    if USE_SEARCH:
        print(f"Arama sorgusu: {SEARCH_QUERY}")
    print(f"Durdurmak için Ctrl+C tuşlarına basın.\n")

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
