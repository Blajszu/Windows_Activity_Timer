from PIL import Image, ImageTk, ImageDraw, ImageFont
import psutil
import time
import os
import json
from collections import defaultdict
import random
import glob
import win32gui
import win32process
import win32ui
import win32con

class AppTracker:
    def __init__(self, config_file="app_config.json"):
        self.app_usage = defaultdict(float)
        self.last_window = None
        self.last_time = time.time()
        self.config_file = config_file
        self.app_config = self.load_config()
        self.icon_cache = {}

    def load_config(self):
        """Ładuje konfigurację aplikacji z pliku JSON"""
        default_config = {
            "firefox.exe": {
                "name": "Mozilla Firefox",
                "custom_icon_path": "icons/firefox.png"
            },
            "chrome.exe": {
                "name": "Google Chrome",
                "custom_icon_path": "icons/chrome.png"
            },
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                with open(self.config_file, 'w') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            print(f"Błąd ładowania konfiguracji: {e}")
            return default_config

    def create_default_icon(self, size=(16, 16), name="unknown"):
        """Tworzy domyślną ikonę z pierwszą literą nazwy aplikacji"""
        img = Image.new('RGBA', (size[0] + 2, size[1] + 2), (1, 1, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Tło - kolorowy okrąg
        bg_color = random.randint(50, 200), random.randint(50, 200), random.randint(50, 200)
        draw.ellipse([(0, 0), size], fill=bg_color)
        
        # Tekst - pierwsza litera nazwy
        if name:
            letter = name[0].upper() if name else "?"
            font = None
            
            # Spróbuj załadować czcionkę
            try:
                font = ImageFont.truetype("arial.ttf", size=int(size[0]*0.6))
            except:
                try:
                    font = ImageFont.load_default()
                except:
                    pass
            
            if font:
                # Nowy sposób obliczania rozmiaru tekstu w Pillow >= 8.0.0
                left, top, right, bottom = draw.textbbox((0, 0), letter, font=font)
                text_width = right - left
                text_height = bottom - top
                
                position = (((size[0]-text_width)/2) + 1, ((size[1]-text_height)/2) - 1)
                draw.text(position, letter, font=font, fill="white")
        
        return ImageTk.PhotoImage(img)

    def get_icon(self, exe_name, icon_size=(16, 16)):
        """Pobiera ikonę dla aplikacji z pliku obrazu lub używa domyślnej"""
        if exe_name in self.icon_cache:
            return self.icon_cache[exe_name]

        app_config = self.app_config.get(exe_name.lower(), {})
        
        # Sprawdź najpierw custom_icon_path
        if 'custom_icon_path' in app_config:
            icon_path = app_config['custom_icon_path']
            if os.path.exists(icon_path):
                try:
                    img = Image.open(icon_path)
                    img = img.resize(icon_size, Image.Resampling.LANCZOS)
                    icon = ImageTk.PhotoImage(img)
                    self.icon_cache[exe_name] = icon
                    return icon
                except Exception as e:
                    print(f"Błąd wczytywania niestandardowej ikony {icon_path}: {e}")
        
        # Użyj domyślnej ikony
        icon = self.create_default_icon(icon_size, exe_name)
        self.icon_cache[exe_name] = icon
        return icon

    def get_active_window(self):
        window = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(window)
        try:
            process = psutil.Process(pid)
            exe_name = process.name()
            
            # Pobierz konfigurację aplikacji
            app_config = self.app_config.get(exe_name.lower(), {})
            name = app_config.get('name', exe_name)
            
            # Jeśli nie ma nazwy, spróbuj z tytułu okna
            if name == exe_name:
                window_title = win32gui.GetWindowText(window)
                if window_title:
                    parts = window_title.split(' - ')
                    if len(parts) > 1:
                        name = parts[-1]
            
            return {
                "name": name,
                "exe": exe_name,
                "icon": self.get_icon(exe_name)
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None

    def track(self, interval=1):
        current_window = self.get_active_window()
        current_time = time.time()

        if self.last_window and current_window:
            time_spent = current_time - self.last_time
            self.app_usage[current_window['name']] += time_spent

        self.last_window = current_window['name'] if current_window else None
        self.last_time = current_time

        return self.app_usage

    def get_top_apps(self, n=4):
        sorted_apps = sorted(self.app_usage.items(), key=lambda x: x[1], reverse=True)
        top_apps = []
        
        for app_name, time_spent in sorted_apps[:n]:
            # Znajdź exe_name dla tej aplikacji
            exe_name = None
            for exe, config in self.app_config.items():
                if config.get('name') == app_name:
                    exe_name = exe
                    break
            
            if exe_name is None:
                exe_name = app_name
                
            top_apps.append({
                "name": app_name,
                "time": self.format_time(time_spent),
                "icon": self.get_icon(exe_name),
                "exe": exe_name
            })
            
        return top_apps

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours}:{minutes:02}:{seconds:02}"