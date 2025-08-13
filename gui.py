import flet as ft
import subprocess
import os
import threading
import json

class TrafficBotGUI:
    def __init__(self):
        self.current_process = None
        self.config_file = "bot_config.json"
        self.log_text = None
        self.load_config()
    
    def load_config(self):
        """Önceki ayarları yükle"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.proxy_list = config.get('proxy_list', [''])
                    self.num_threads = config.get('num_threads', 100)
                    self.target_url = config.get('target_url', 'https://aowsoftware.com/')
            else:
                self.proxy_list = ['']
                self.num_threads = 100
                self.target_url = 'https://aowsoftware.com/'
        except:
            self.proxy_list = ['']
            self.num_threads = 100
            self.target_url = 'https://aowsoftware.com/'
    
    def save_config(self):
        """Ayarları kaydet"""
        config = {
            'proxy_list': self.proxy_list,
            'num_threads': self.num_threads,
            'target_url': self.target_url
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    
    def update_bot_file(self, file_path, proxy_list, num_threads, target_url):
        """Bot dosyasını güncelle"""
        with open(file_path, 'r', encoding='utf-8') as f:
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
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def run_bot(self, bot_type, page):
        """Bot çalıştır"""
        if self.current_process:
            page.add(ft.Text("Zaten bir bot çalışıyor! Önce durdurun.", color=ft.Colors.RED))
            page.update()
            return
        
        try:
            # Ayarları kaydet
            self.save_config()
            
            # Bot dosyasını güncelle
            file_path = 'Module/direct.py'
            
            self.update_bot_file(file_path, self.proxy_list, self.num_threads, self.target_url)
            
            # Bot çalıştır (terminal açmadan)
            self.current_process = subprocess.Popen(
                ['python', file_path],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Log okuma thread'ini başlat
            log_thread = threading.Thread(target=self.read_logs, args=(page,), daemon=True)
            log_thread.start()
            
            self.add_log(f"{bot_type.title()} bot başlatıldı!", page, ft.Colors.GREEN)
            page.update()
            
        except Exception as e:
            self.add_log(f"Hata: {str(e)}", page, ft.Colors.RED)
            page.update()
    
    def add_log(self, message, page, color=ft.Colors.WHITE):
        """Log mesajı ekle"""
        if self.log_text:
            current_value = self.log_text.value or ""
            self.log_text.value = current_value + message + "\n"
            self.log_text.update()
    
    def read_logs(self, page):
        """Bot çıktılarını oku ve log alanına ekle"""
        if not self.current_process:
            return
        
        try:
            for line in iter(self.current_process.stdout.readline, ''):
                if line:
                    self.add_log(line.strip(), page)
                if self.current_process.poll() is not None:
                    break
        except:
            pass
    
    def stop_bot(self, page):
        """Bot durdur"""
        if self.current_process:
            try:
                self.current_process.terminate()
                self.current_process = None
                self.add_log("Bot durduruldu!", page, ft.Colors.ORANGE)
            except:
                self.add_log("Bot durdurulamadı!", page, ft.Colors.RED)
        else:
            self.add_log("Çalışan bot yok!", page, ft.Colors.GREY)
        page.update()
    
    def main(self, page: ft.Page):
        page.title = "AOWSoftware Direct Traffic Bot GUI"
        page.theme_mode = ft.ThemeMode.DARK
        page.window_width = 800
        page.window_height = 700
        
        # Proxy listesi için text field
        proxy_field = ft.TextField(
            label="Proxy Listesi (Her satıra bir proxy)",
            multiline=True,
            min_lines=3,
            max_lines=5,
            value='\n'.join(self.proxy_list),
            width=700
        )
        
        # Thread sayısı
        threads_field = ft.TextField(
            label="Thread Sayısı",
            value=str(self.num_threads),
            width=200
        )
        
        # Hedef URL
        url_field = ft.TextField(
            label="Hedef URL",
            value=self.target_url,
            width=500
        )
        

        
        def update_values():
            """Değerleri güncelle"""
            self.proxy_list = [p.strip() for p in proxy_field.value.split('\n') if p.strip()]
            try:
                self.num_threads = int(threads_field.value)
            except:
                self.num_threads = 100
            self.target_url = url_field.value
        
        def on_direct_click(e):
            update_values()
            self.run_bot('direct', page)
        
        def on_stop_click(e):
            self.stop_bot(page)
        
        def on_clear_log(e):
            if self.log_text:
                self.log_text.value = ""
                self.log_text.update()
        
        # Butonlar
        direct_btn = ft.ElevatedButton(
            "Traffic Bot Başlat",
            on_click=on_direct_click,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
        )
        

        
        stop_btn = ft.ElevatedButton(
            "Bot Durdur",
            on_click=on_stop_click,
            bgcolor=ft.Colors.RED,
            color=ft.Colors.WHITE
        )
        
        clear_btn = ft.ElevatedButton(
            "Logları Temizle",
            on_click=on_clear_log,
            bgcolor=ft.Colors.GREY,
            color=ft.Colors.WHITE
        )
        
        # Log alanı
        self.log_text = ft.TextField(
            multiline=True,
            min_lines=10,
            max_lines=15,
            read_only=True,
            value="",
            width=750,
            bgcolor=ft.Colors.BLACK,
            color=ft.Colors.WHITE
        )
        
        # Sayfa düzeni
        page.add(
            ft.Text("AOWSoftware Direct Traffic Bot", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            
            ft.Text("Proxy Ayarları:", size=16, weight=ft.FontWeight.BOLD),
            proxy_field,
            
            ft.Row([
                ft.Column([
                    ft.Text("Genel Ayarlar:", size=16, weight=ft.FontWeight.BOLD),
                    threads_field,
                ]),
                ft.Column([
                    ft.Text(" "),  # Boşluk için
                    url_field,
                ])
            ]),
            
            ft.Divider(),
            
            ft.Row([
                direct_btn,
                stop_btn,
                clear_btn
            ]),
            
            ft.Divider(),
            ft.Text("Log:", size=16, weight=ft.FontWeight.BOLD),
            self.log_text,
        )

def main():
    app = TrafficBotGUI()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()