import flet as ft
import json
import os
import subprocess
import threading
import time

class GoogleBotGUI:
    def __init__(self):
        self.config_file = "google_config.json"
        self.bot_process = None
        self.is_running = False
        
    def load_config(self):
        """Kaydedilmiş konfigürasyonu yükle"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "proxy_list": "http://M9Z7JPUKo8Vmei9g:IUuuMf4LkexA8wSn_counusy-tr_session-kZvLa1Sv_lifetime-30m_suseaming-1@geo.iproyal.com:12321",
            "num_threads": "100",
            "search_query": "web trafik botu",
            "target_url": "https://www.instagram.com/reel/DES86L4Oafp/"
        }
    
    def save_config(self, config):
        """Konfigürasyonu kaydet"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Konfigürasyon kaydedilemedi: {e}")
    
    def update_google_file(self, proxy_list, num_threads, search_query, target_url):
        """google.py dosyasını güncelle"""
        try:
            # google.py dosyasını oku
            google_file_path = "Module/google.py"
            with open(google_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Proxy listesini hazırla
            proxies = [proxy.strip() for proxy in proxy_list.split('\n') if proxy.strip()]
            proxy_list_str = '[\n    "' + '",\n    "'.join(proxies) + '"\n]'
            
            # İçeriği güncelle
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
            
            # Dosyayı güncelle
            with open(google_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            
            return True
        except Exception as e:
            print(f"Dosya güncellenirken hata: {e}")
            return False
    
    def start_bot(self, page, log_text):
        """Botu başlat"""
        if self.is_running:
            return
        
        try:
            self.is_running = True
            log_text.value += "\n🚀 Google Bot başlatılıyor..."
            page.update()
            
            # Bot'u subprocess ile başlat
            self.bot_process = subprocess.Popen(
                ["python", "Module/google.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Log okuma thread'i başlat
            def read_logs():
                while self.is_running and self.bot_process:
                    try:
                        output = self.bot_process.stdout.readline()
                        if output:
                            log_text.value += f"\n{output.strip()}"
                            page.update()
                        elif self.bot_process.poll() is not None:
                            break
                    except:
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
            
            log_text.value += "\n🛑 Google Bot durduruldu."
            page.update()
            
        except Exception as e:
            log_text.value += f"\n❌ Bot durdurulurken hata: {e}"
            page.update()

def main(page: ft.Page):
    page.title = "Google Bot Arayüzü"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 900
    page.window_height = 700
    page.window_resizable = True
    
    bot_gui = GoogleBotGUI()
    config = bot_gui.load_config()
    
    # UI Bileşenleri
    proxy_list_field = ft.TextField(
        label="Proxy Listesi (Her satıra bir proxy)",
        value=config.get("proxy_list", ""),
        multiline=True,
        min_lines=3,
        max_lines=8,
        width=800
    )
    
    num_threads_field = ft.TextField(
        label="Thread Sayısı",
        value=config.get("num_threads", "100"),
        width=200
    )
    
    search_query_field = ft.TextField(
        label="Arama Sorgusu",
        value=config.get("search_query", "web trafik botu"),
        width=400
    )
    
    target_url_field = ft.TextField(
        label="Hedef URL",
        value=config.get("target_url", "https://www.instagram.com/reel/DES86L4Oafp/"),
        width=600
    )
    
    log_text = ft.Text(
        value="📋 Google Bot Arayüzü hazır.\n💡 Ayarları girin ve 'Ayarları Kaydet' butonuna basın.",
        size=12,
        color=ft.Colors.GREEN_300
    )
    
    def save_settings(e):
        """Ayarları kaydet ve dosyayı güncelle"""
        config = {
            "proxy_list": proxy_list_field.value,
            "num_threads": num_threads_field.value,
            "search_query": search_query_field.value,
            "target_url": target_url_field.value
        }
        
        # Konfigürasyonu kaydet
        bot_gui.save_config(config)
        
        # google.py dosyasını güncelle
        success = bot_gui.update_google_file(
            proxy_list_field.value,
            num_threads_field.value,
            search_query_field.value,
            target_url_field.value
        )
        
        if success:
            log_text.value += "\n✅ Ayarlar kaydedildi ve google.py dosyası güncellendi!"
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
    save_button = ft.ElevatedButton(
        text="💾 Ayarları Kaydet",
        on_click=save_settings,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE
    )
    
    start_button = ft.ElevatedButton(
        text="🚀 Google Bot Başlat",
        on_click=start_bot_click,
        bgcolor=ft.Colors.GREEN_600,
        color=ft.Colors.WHITE
    )
    
    stop_button = ft.ElevatedButton(
        text="🛑 Google Bot Durdur",
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
            ft.Text("🔍 Google Bot Arayüzü", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
            ft.Divider(),
            
            # Ayarlar bölümü
            ft.Text("⚙️ Bot Ayarları", size=18, weight=ft.FontWeight.BOLD),
            proxy_list_field,
            ft.Row([
                num_threads_field,
                search_query_field
            ]),
            target_url_field,
            
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
            ft.Container(
                content=ft.Column([
                    log_text
                ], scroll=ft.ScrollMode.AUTO),
                bgcolor=ft.Colors.GREY_900,
                padding=10,
                border_radius=5,
                height=200,
                width=850
            )
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
    )

if __name__ == "__main__":
    ft.app(target=main)