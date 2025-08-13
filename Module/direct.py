import urllib.request
import random
import threading
import time
import ssl
import signal
import sys
import os
import json

PROXY_LIST = [
    "http://M9Z7JPUKo8Vmei9g:IUuuMf4LkexA8wSn_counusy-tr_session-kZvLa1Sv_lifetime-30m_suseaming-1@geo.iproyal.com:12321"
]
NUM_THREADS = 100  # Daha fazla istek için iş parçacığı sayısını artırabilirsiniz.
TARGET_URL = 'https://aowsoftware.com/'  # İstek gönderilecek URL'yi girin

# Başarılı istekler ve toplam istekler için global sayaçlar
successful_requests = 0
total_requests = 0

# Kilit mekanizması, çoklu iş parçacığında sayaçları güvenli bir şekilde güncellemek için gerekli
counter_lock = threading.Lock()

# Proxy'yi döngüyle kullanmak için global bir index
proxy_index = 0
# Proxy değişimini güvenli bir şekilde kontrol etmek için bir kilit
proxy_lock = threading.Lock()

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
        "traffic_bot_starting": "Traffic bot is starting...",
        "target_url": "Target URL:",
        "thread_count": "Thread count:",
        "stop_with_ctrl_c": "Press Ctrl+C to stop.\n"
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
        "traffic_bot_starting": "Trafik botu başlatılıyor...",
        "target_url": "Hedef URL:",
        "thread_count": "Thread sayısı:",
        "stop_with_ctrl_c": "Durdurmak için Ctrl+C tuşlarına basın.\n"
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
            return None
        proxy = PROXY_LIST[proxy_index]
        proxy_index = (proxy_index + 1) % len(PROXY_LIST)
        return proxy

# İstek gönderimi için her defasında farklı ping sağlar
def send_request(target_url):
    global successful_requests, total_requests
    ssl._create_default_https_context = ssl._create_unverified_context

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
    retry_delay = 0  # Bekleme süresi (saniye) başarısızlık durumunda

    while attempt < max_attempts:
        try:
            # Proxy'yi ayarlayın (eğer varsa)
            proxy = get_next_proxy()
            if proxy:
                proxy_support = urllib.request.ProxyHandler({
                    "http": proxy,
                    "https": proxy,
                })
                opener = urllib.request.build_opener(proxy_support)
            else:
                opener = urllib.request.build_opener()

            # Headers'ı ayarlayın
            opener.addheaders = [(key, value) for key, value in headers.items()]

            # İstek gönderimi
            request = urllib.request.Request(target_url, headers=dict(headers))
            response = opener.open(request, timeout=20)
            
            # Toplam istek sayısını günceller
            with counter_lock:
                total_requests += 1

            # Başarılı istekleri sayar (durum kodu 200 ise)
            if response.getcode() == 200:
                with counter_lock:
                    successful_requests += 1
                print(f"{get_text('successful')} {successful_requests}. Site: {target_url}. {get_text('status_code')} {response.getcode()}")
                break  # Başarılıysa döngüden çık
            else:
                print(f"{get_text('failed')} {get_text('status_code')} {response.getcode()}, {get_text('total')} {total_requests}")
                break  # Durum kodu 200 değilse döngüden çık
        except Exception as e:
            attempt += 1
            print(f"{get_text('error_occurred')} {e}. {get_text('proxy_changed')}")
            if attempt >= max_attempts:
                break  # Max deneme sayısına ulaştığında döngüden çık

def worker():
    while not stop_flag.is_set():
        send_request(TARGET_URL)
        # stop_flag kontrolü ile birlikte sleep
        if not stop_flag.wait(random.uniform(1, 3)):
            continue
        else:
            break

def signal_handler(sig, frame):
    print(get_text('ctrl_c_detected'))
    print(f"{get_text('total_sent_requests')} {total_requests}")
    print(f"{get_text('successful_request_count')} {successful_requests}")
    stop_flag.set()
    sys.exit(0)

def main():
    # Ctrl+C sinyalini yakala
    signal.signal(signal.SIGINT, signal_handler)
    
    print(get_text('traffic_bot_starting'))
    print(f"{get_text('target_url')} {TARGET_URL}")
    print(f"{get_text('thread_count')} {NUM_THREADS}")
    print(get_text('stop_with_ctrl_c'))
    
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=worker)
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
