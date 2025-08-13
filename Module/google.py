import random
import threading
import time
import signal
import sys
import os
import json
import ssl
from urllib import request, parse, error
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup

# Translation system
TRANSLATIONS = {
    "en": {
        "target_link_found": "Target link found -> href:",
        "suitable_url_not_found": "Suitable URL not found for",
        "successful_request": "Successful:",
        "site": "Site:",
        "status_code": "Status code:",
        "failed_request": "Failed:",
        "total_requests": "Total:",
        "error_occurred": "Error occurred:",
        "proxy_changed": "Proxy will be changed and continue.",
        "search_error": "Search error:",
        "ctrl_c_detected": "\n\nCtrl+C detected! Program is stopping...",
        "total_sent_requests": "Total sent requests:",
        "successful_request_count": "Successful request count:",
        "google_search_bot_starting": "Google search bot is starting...",
        "search_query": "Search query:",
        "target_url": "Target URL:",
        "thread_count": "Thread count:",
        "stop_with_ctrl_c": "Press Ctrl+C to stop.\n"
    },
    "tr": {
        "target_link_found": "Belirlenen link bulundu -> href:",
        "suitable_url_not_found": "için uygun URL bulunamadı",
        "successful_request": "Başarılı:",
        "site": "Site:",
        "status_code": "Durum kodu:",
        "failed_request": "Başarısız:",
        "total_requests": "Toplam:",
        "error_occurred": "Hata oluştu:",
        "proxy_changed": "Proxy değiştirilerek devam edilecek.",
        "search_error": "Arama hatası:",
        "ctrl_c_detected": "\n\nCtrl+C algılandı! Program durduruluyor...",
        "total_sent_requests": "Toplam gönderilen istek:",
        "successful_request_count": "Başarılı istek sayısı:",
        "google_search_bot_starting": "Google arama botu başlatılıyor...",
        "search_query": "Arama sorgusu:",
        "target_url": "Hedef URL:",
        "thread_count": "Thread sayısı:",
        "stop_with_ctrl_c": "Durdurmak için Ctrl+C tuşlarına basın.\n"
    }
}

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

def get_text(key):
    language = load_language()
    return TRANSLATIONS[language].get(key, key)

PROXY_LIST = [
    "http://M9Z7JPUKo8Vmei9g:IUuuMf4LkexA8wSn_counusy-tr_session-kZvLa1Sv_lifetime-30m_suseaming-1@geo.iproyal.com:12321"
]
NUM_THREADS = 100  # İş parçacığı sayısını artırabilirsiniz
SEARCH_QUERY = 'web trafik botu'  # Aramak istediğiniz sorgu
TARGET_URL = 'https://www.instagram.com/reel/DES86L4Oafp/'  # Aranacak ve istek yapılacak link

successful_requests = 0
total_requests = 0

proxy_index = 0
proxy_lock = threading.Lock()  # Proxy kullanımında eşzamanlı erişimi kontrol etmek için
counter_lock = threading.Lock()  # İstatistikler üzerinde eşzamanlı erişimi kontrol etmek için

# Program durdurmak için global flag
stop_flag = threading.Event()

def generate_user_agent():
    """2024 güncel User-Agent'ları - 429 hatalarını azaltmak için optimize edildi"""
    user_agents = [
        # Chrome 2024 - Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        
        # Chrome 2024 - macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        
        # Firefox 2024
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
        
        # Edge 2024
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
        
        # Safari 2024
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15",
        
        # Mobile Chrome 2024
        "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1"
    ]
    return random.choice(user_agents)

def get_next_proxy():
    global proxy_index
    with proxy_lock:
        if len(PROXY_LIST) == 0:
            return None
        proxy = PROXY_LIST[proxy_index]
        proxy_index = (proxy_index + 1) % len(PROXY_LIST)
        return proxy

def html_den_url_al(html, belirlenen_site):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Hedef URL'den domain ve path bilgilerini çıkar
    from urllib.parse import urlparse
    parsed_target = urlparse(belirlenen_site)
    target_domain = parsed_target.netloc.lower()
    target_path = parsed_target.path.lower()
    
    # Instagram reel ID'sini çıkar
    reel_id = None
    if '/reel/' in target_path:
        reel_id = target_path.split('/reel/')[-1].rstrip('/')
    
    print(f"[DEBUG] Aranan domain: {target_domain}, path: {target_path}, reel_id: {reel_id}")
    
    for link in soup.find_all('a'):
        href = link.get('href')
        if not href:
            continue
            
        # URL'yi temizle ve normalize et
        href_lower = href.lower()
        
        # Farklı eşleştirme yöntemleri
        match_found = False
        
        # 1. Tam URL eşleşmesi
        if belirlenen_site.lower() in href_lower:
            match_found = True
            print(f"[DEBUG] Tam URL eşleşmesi bulundu")
        
        # 2. Domain ve reel ID eşleşmesi
        elif target_domain in href_lower and reel_id and reel_id in href_lower:
            match_found = True
            print(f"[DEBUG] Domain ve reel ID eşleşmesi bulundu")
        
        # 3. Instagram domain ve path eşleşmesi
        elif 'instagram.com' in href_lower and target_path in href_lower:
            match_found = True
            print(f"[DEBUG] Instagram domain ve path eşleşmesi bulundu")
        
        # 4. Sadece reel ID eşleşmesi (Instagram için)
        elif 'instagram.com' in href_lower and '/reel/' in href_lower and reel_id and reel_id in href_lower:
            match_found = True
            print(f"[DEBUG] Instagram reel ID eşleşmesi bulundu")
        
        if match_found:
            print(f"{get_text('target_link_found')} {href}")
            return href
    
    print(f"[DEBUG] Hiçbir eşleşme bulunamadı. Aranan: {belirlenen_site}")
    return None

def send_request(target_url):
    global successful_requests, total_requests
    headers = {
        "Cache-Control": "max-age=0",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": generate_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Sec-GPC": "1",
        "Accept-Language": "tr",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": 'https://www.google.com/'
    }

    attempt = 0
    max_attempts = 3

    while attempt < max_attempts:
        try:
            # SSL context oluştur
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
            
            proxy = get_next_proxy()
            if proxy:
                proxy_support = request.ProxyHandler({
                    "http": proxy,
                    "https": proxy,
                })
                https_handler = request.HTTPSHandler(context=ssl_context)
                opener = request.build_opener(proxy_support, https_handler)
            else:
                https_handler = request.HTTPSHandler(context=ssl_context)
                opener = request.build_opener(https_handler)

            opener.addheaders = [(key, value) for key, value in headers.items()]
            request.install_opener(opener)

            req = request.Request(target_url, headers=dict(headers))
            response = opener.open(req, timeout=20)
            
            with counter_lock:
                total_requests += 1

            if response.getcode() == 200:
                with counter_lock:
                    successful_requests += 1
                print(f"{get_text('successful_request')} {successful_requests}. {get_text('site')} {target_url}. {get_text('status_code')} {response.getcode()}")
                break
            else:
                print(f"{get_text('failed_request')} {get_text('status_code')} {response.getcode()}, {get_text('total_requests')} {total_requests}")
                break
        except ssl.SSLError as e:
            attempt += 1
            print(f"[ERROR] SSL Hatası: {e}")
            print(f"[INFO] SSL hatası nedeniyle bekleme...")
            time.sleep(random.uniform(10, 20))
            if attempt >= max_attempts:
                break
        except error.URLError as e:
            attempt += 1
            error_reason = str(e.reason).lower()
            if 'ssl' in error_reason or 'unexpected_eof' in error_reason or 'eof occurred' in error_reason:
                print(f"[ERROR] SSL/EOF Hatası: {e.reason}")
                print(f"[INFO] SSL hatası nedeniyle bekleme...")
                time.sleep(random.uniform(10, 20))
            else:
                print(f"{get_text('error_occurred')} {e}. {get_text('proxy_changed')}")
                time.sleep(random.uniform(2, 5))
            if attempt >= max_attempts:
                break
        except Exception as e:
            attempt += 1
            error_msg = str(e).lower()
            if 'ssl' in error_msg or 'unexpected_eof' in error_msg or 'eof occurred' in error_msg:
                print(f"[ERROR] SSL/EOF Hatası: {e}")
                print(f"[INFO] SSL hatası nedeniyle bekleme...")
                time.sleep(random.uniform(10, 20))
            else:
                print(f"{get_text('error_occurred')} {e}. {get_text('proxy_changed')}")
                time.sleep(random.uniform(2, 5))
            if attempt >= max_attempts:
                break

# 429 hatası için global değişkenler
rate_limit_delay = 5  # Başlangıç bekleme süresi
max_rate_limit_delay = 300  # Maksimum bekleme süresi (5 dakika)
consecutive_429_errors = 0  # Ardışık 429 hatası sayısı
last_429_time = 0  # Son 429 hatası zamanı

# Token bucket rate limiting
class TokenBucket:
    def __init__(self, capacity=10, refill_rate=1):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def consume(self, tokens=1):
        with self.lock:
            now = time.time()
            # Token'ları yenile
            elapsed = now - self.last_refill
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
            self.last_refill = now
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def wait_for_token(self, tokens=1):
        while not self.consume(tokens):
            wait_time = tokens / self.refill_rate
            print(f"[INFO] Token bucket boş, {wait_time:.1f}s bekleniyor...")
            time.sleep(min(wait_time, 5))

# Token Bucket Nedir?
# Token bucket, rate limiting (hız sınırlama) algoritmasıdır.
# Bir kova gibi düşünün: belirli hızda token (jeton) dolar, istek yaparken token harcanır.
# Kova boşsa beklemek gerekir. Bu sayede API rate limit'lerini aşmayız.
# 
# Avantajları:
# - Ani istek patlamalarına izin verir (kova doluysa)
# - Sürekli hız kontrolü sağlar
# - 429 hatalarını önler
#
# Her thread için bağımsız token bucket kullanacağız
# Bu sayede threadler birbirini engellemez

# Thread-local storage için
import threading
thread_local_data = threading.local()

def get_thread_token_bucket():
    """Her thread için bağımsız token bucket döndürür"""
    if not hasattr(thread_local_data, 'token_bucket'):
        # Her thread için ayrı token bucket (daha küçük kapasiteli ama hızlı)
        thread_local_data.token_bucket = TokenBucket(capacity=5, refill_rate=1.0)
    return thread_local_data.token_bucket

def handle_429_error(response=None):
    """429 hatası için gelişmiş exponential backoff ve Retry-After header kontrolü"""
    global rate_limit_delay, consecutive_429_errors, last_429_time
    
    consecutive_429_errors += 1
    current_time = time.time()
    last_429_time = current_time
    
    # Retry-After header kontrolü
    retry_after = None
    if response and hasattr(response, 'headers'):
        retry_after = response.headers.get('Retry-After')
        if retry_after:
            try:
                # Retry-After saniye cinsinden olabilir
                retry_after_seconds = int(retry_after)
                print(f"[INFO] Server Retry-After header: {retry_after_seconds} saniye")
                if retry_after_seconds <= 600:  # Maksimum 10 dakika
                    print(f"[INFO] Retry-After header'a göre {retry_after_seconds} saniye bekleniyor...")
                    time.sleep(retry_after_seconds)
                    return retry_after_seconds
            except ValueError:
                # Retry-After HTTP-date formatında olabilir, şimdilik göz ardı et
                pass
    
    # Exponential backoff: Her 429 hatasında bekleme süresini artır
    base_delay = min(5 * (2 ** (consecutive_429_errors - 1)), max_rate_limit_delay)
    
    # Rastgele jitter ekle (±30%) - daha fazla randomness
    jitter = random.uniform(0.7, 1.3)
    actual_delay = base_delay * jitter
    
    print(f"[WARNING] 429 Too Many Requests hatası! Ardışık hata: {consecutive_429_errors}")
    print(f"[INFO] {actual_delay:.1f} saniye bekleniyor (exponential backoff)...")
    
    time.sleep(actual_delay)
    
    return actual_delay

def reset_rate_limit_if_needed():
    """Başarılı istekten sonra rate limit ayarlarını sıfırla"""
    global rate_limit_delay, consecutive_429_errors
    
    # Eğer son 429 hatasından 5 dakika geçtiyse ayarları sıfırla
    if time.time() - last_429_time > 300:
        if consecutive_429_errors > 0:
            print(f"[INFO] Rate limit ayarları sıfırlanıyor (5 dakika geçti)")
            consecutive_429_errors = 0
            rate_limit_delay = 5

def anahtar_kelimeyi_ara():
    """Gelişmiş 429 hata yönetimi ile Google arama"""
    global consecutive_429_errors
    
    # Thread-local token bucket kontrolü - her thread kendi bucket'ını kullanır
    thread_bucket = get_thread_token_bucket()
    thread_bucket.wait_for_token()
    
    # Arama sorgusunu UTF-8'e kodlayarak sorunları çözebiliriz
    encoded_search_query = parse.quote(SEARCH_QUERY)
    search_url = f"https://www.google.com/search?q={encoded_search_query}&num=100"
    
    max_retries = 5  # Maksimum deneme sayısı
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # Rate limit kontrolü
            reset_rate_limit_if_needed()
            
            # Eğer çok fazla 429 hatası varsa ekstra bekleme
            if consecutive_429_errors >= 3:
                extra_delay = random.uniform(10, 30)
                print(f"[INFO] Çok fazla 429 hatası nedeniyle ekstra {extra_delay:.1f}s bekleniyor...")
                time.sleep(extra_delay)
            
            # SSL context oluştur
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
            
            proxy = get_next_proxy()
            if proxy:
                proxy_support = request.ProxyHandler({
                    "http": proxy,
                    "https": proxy,
                })
                https_handler = request.HTTPSHandler(context=ssl_context)
                opener = request.build_opener(proxy_support, https_handler)
            else:
                https_handler = request.HTTPSHandler(context=ssl_context)
                opener = request.build_opener(https_handler)

            # 2024 güncel ve gerçekçi headers - 429 hatalarını azaltmak için optimize edildi
            opener.addheaders = [
                ("User-Agent", generate_user_agent()),
                ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"),
                ("Accept-Language", "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"),
                ("Accept-Encoding", "gzip, deflate, br, zstd"),
                ("Cache-Control", "max-age=0"),
                ("Sec-Ch-Ua", '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"'),
                ("Sec-Ch-Ua-Mobile", "?0"),
                ("Sec-Ch-Ua-Platform", '"Windows"'),
                ("Sec-Fetch-Dest", "document"),
                ("Sec-Fetch-Mode", "navigate"),
                ("Sec-Fetch-Site", "none"),
                ("Sec-Fetch-User", "?1"),
                ("Upgrade-Insecure-Requests", "1"),
                ("Connection", "keep-alive"),
                ("DNT", "1"),
                ("Referer", "https://www.google.com/")
            ]
            request.install_opener(opener)

            req = request.Request(search_url)
            response = opener.open(req, timeout=30)  # Timeout'u artır
            
            # HTTP status code kontrolü
            status_code = response.getcode()
            
            if status_code == 429:
                print(f"[WARNING] HTTP 429 Too Many Requests alındı!")
                handle_429_error(response)
                retry_count += 1
                continue
            elif status_code == 503:
                print(f"[WARNING] HTTP 503 Service Unavailable alındı!")
                delay = random.uniform(30, 60)
                print(f"[INFO] {delay:.1f} saniye bekleniyor...")
                time.sleep(delay)
                retry_count += 1
                continue
            elif status_code != 200:
                print(f"[WARNING] Beklenmeyen HTTP status code: {status_code}")
                retry_count += 1
                time.sleep(random.uniform(5, 15))
                continue
            
            # Başarılı istek - Gzip/deflate decode problemi için güvenli okuma
            try:
                # Response'u oku ve encoding'i kontrol et
                raw_data = response.read()
                
                # Content-Encoding header'ını kontrol et
                content_encoding = response.headers.get('Content-Encoding', '').lower()
                
                if content_encoding == 'gzip':
                    import gzip
                    html = gzip.decompress(raw_data).decode('utf-8', errors='ignore')
                elif content_encoding == 'deflate':
                    import zlib
                    html = zlib.decompress(raw_data).decode('utf-8', errors='ignore')
                elif content_encoding == 'br':
                    try:
                        import brotli
                        html = brotli.decompress(raw_data).decode('utf-8', errors='ignore')
                    except ImportError:
                        # Brotli modülü yoksa normal decode dene
                        html = raw_data.decode('utf-8', errors='ignore')
                else:
                    # Normal decode, hataları ignore et
                    html = raw_data.decode('utf-8', errors='ignore')
                    
            except Exception as decode_error:
                print(f"[WARNING] Response decode hatası: {decode_error}")
                # Fallback: latin-1 ile decode dene
                try:
                    html = response.read().decode('latin-1')
                except:
                    print(f"[ERROR] Response decode edilemedi, atlanıyor...")
                    retry_count += 1
                    continue
            
            # Rate limit ayarlarını sıfırla (başarılı istek)
            if consecutive_429_errors > 0:
                print(f"[SUCCESS] Başarılı istek sonrası rate limit sıfırlandı")
                consecutive_429_errors = 0
                rate_limit_delay = 5
            
            href = html_den_url_al(html, TARGET_URL)
            if href:
                send_request(href)
            else:
                print(f"{get_text('suitable_url_not_found')} {SEARCH_QUERY}.")
            
            # Başarılı işlem sonrası normal bekleme
            base_delay = random.uniform(3, 8)
            print(f"[INFO] Normal bekleme: {base_delay:.1f} saniye")
            time.sleep(base_delay)
            break  # Başarılı olduğu için döngüden çık
            
        except error.HTTPError as e:
            if e.code == 429:
                print(f"[ERROR] HTTPError 429 Too Many Requests!")
                # HTTPError nesnesini response olarak geçir
                handle_429_error(e)
                retry_count += 1
            elif e.code == 503:
                print(f"[ERROR] HTTPError 503 Service Unavailable!")
                # 503 için de Retry-After header kontrolü
                retry_after = e.headers.get('Retry-After') if hasattr(e, 'headers') else None
                if retry_after:
                    try:
                        delay = int(retry_after)
                        print(f"[INFO] Server Retry-After: {delay} saniye")
                        time.sleep(min(delay, 300))  # Maksimum 5 dakika
                    except ValueError:
                        delay = random.uniform(30, 60)
                        print(f"[INFO] {delay:.1f} saniye bekleniyor...")
                        time.sleep(delay)
                else:
                    delay = random.uniform(30, 60)
                    print(f"[INFO] {delay:.1f} saniye bekleniyor...")
                    time.sleep(delay)
                retry_count += 1
            else:
                print(f"[ERROR] HTTPError {e.code}: {e.reason}")
                retry_count += 1
                time.sleep(random.uniform(5, 15))
        except error.URLError as e:
            error_reason = str(e.reason).lower()
            if 'ssl' in error_reason or 'unexpected_eof' in error_reason or 'eof occurred' in error_reason:
                print(f"[ERROR] SSL Hatası: {e.reason}")
                print(f"[INFO] SSL hatası nedeniyle uzun bekleme...")
                time.sleep(random.uniform(15, 30))
            else:
                print(f"[ERROR] URLError: {e.reason}")
                time.sleep(random.uniform(5, 15))
            retry_count += 1
        except ssl.SSLError as e:
            print(f"[ERROR] SSL Hatası: {e}")
            print(f"[INFO] SSL hatası nedeniyle uzun bekleme...")
            time.sleep(random.uniform(20, 40))
            retry_count += 1
        except Exception as e:
            error_msg = str(e).lower()
            if '429' in error_msg or 'too many requests' in error_msg:
                print(f"[ERROR] 429 hatası tespit edildi: {e}")
                handle_429_error()
                retry_count += 1
                # Proxy değiştir ve devam et
                proxy = get_next_proxy()
                if proxy:
                    print(f"[INFO] Proxy değiştiriliyor: {proxy[:50]}...")
                time.sleep(random.uniform(5, 10))
            elif 'ssl' in error_msg or 'unexpected_eof' in error_msg or 'eof occurred' in error_msg:
                print(f"[ERROR] SSL/EOF Hatası: {e}")
                print(f"[INFO] SSL hatası nedeniyle uzun bekleme...")
                time.sleep(random.uniform(15, 30))
                retry_count += 1
            else:
                print(f"{get_text('search_error')} {e}")
                retry_count += 1
                time.sleep(random.uniform(2, 8))
    
    # Tüm denemeler başarısız oldu
    if retry_count >= max_retries:
        print(f"[ERROR] {max_retries} deneme sonrası başarısız! Uzun bekleme...")
        long_delay = random.uniform(60, 120)
        print(f"[INFO] {long_delay:.1f} saniye bekleniyor...")
        time.sleep(long_delay)


def worker():
    while not stop_flag.is_set():
        anahtar_kelimeyi_ara()
        
        # 429 hatası durumuna göre adaptif bekleme
        if consecutive_429_errors > 0:
            # 429 hatası varsa daha uzun bekle
            adaptive_delay = random.uniform(20, 40) + (consecutive_429_errors * 5)
            print(f"[INFO] Worker adaptif bekleme: {adaptive_delay:.1f}s (429 hatası nedeniyle)")
            if stop_flag.wait(adaptive_delay):
                break
        else:
            # Normal bekleme süresi
            normal_delay = random.uniform(10, 15)
            if stop_flag.wait(normal_delay):
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
    
    print(get_text('google_search_bot_starting'))
    print(f"{get_text('search_query')} {SEARCH_QUERY}")
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
