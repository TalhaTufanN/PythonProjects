import yt_dlp
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
import time  # Zaman bilgisini almak için
import json
import requests
from PIL import Image, ImageTk
from io import BytesIO

def resource_path(relative_path):
    """ PyInstaller ile paketlendiğinde dosya yollarını yönetmek için yardımcı fonksiyon. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_icon_from_url(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        photo = ImageTk.PhotoImage(image)
        return photo
    except Exception as e:
        print(f"İcon yüklenirken hata oluştu: {e}")
        return None

def load_last_folder():
    """ Son kullanılan klasörü yükler. """
    try:
        if os.path.exists('settings.json'):
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return settings.get('last_folder', '')
    except Exception as e:
        print(f"Ayarlar yüklenirken hata oluştu: {e}")
    return ''

def save_last_folder(folder_path):
    """ Son kullanılan klasörü kaydeder. """
    try:
        settings = {'last_folder': folder_path}
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ayarlar kaydedilirken hata oluştu: {e}")

def downloader(video_url, save_path, audio_only=False, progress_callback=None):
    def hook(d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes')
            downloaded_bytes = d.get('downloaded_bytes')
            if total_bytes and downloaded_bytes:
                progress = int(downloaded_bytes / total_bytes * 100)
                progress_callback(progress)
        elif d['status'] == 'finished':
            progress_callback(100)

    ydl_opts = {
        'format': 'bestaudio/best' if audio_only else 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }] if audio_only else [],
        'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        'progress_hooks': [hook]
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'İsimsiz video')
            downloaded_file_path = ydl.prepare_filename(info_dict) 

            # İndirilen dosyanın zaman bilgisini güncelle
            current_time = time.time()
            os.utime(downloaded_file_path, (current_time, current_time))

        messagebox.showinfo("Başarılı", f"Başarıyla indirildi: {video_title}")
        reset_fields()
    except Exception as e:
        messagebox.showerror("Hata", f"İndirilemedi: {e}")
        reset_fields()

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder_selected)
        save_last_folder(folder_selected)

def start_download():
    video_url = entry_url.get()
    save_path = entry_path.get()
    audio_only = var_audio.get()
    if video_url and save_path:
        label_status.config(text="İndirme durumu: 0%")
        threading.Thread(target=downloader, args=(video_url, save_path, audio_only, update_progress)).start()
    else:
        messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurunuz.")

def update_progress(progress):
    progress_bar['value'] = progress
    label_status.config(text=f"İndirme durumu: {progress}%")

def reset_fields():
    entry_url.delete(0, tk.END)
    var_audio.set(False)
    progress_bar['value'] = 0
    label_status.config(text="İndirme durumu: 0%")

# Tkinter arayüzü
root = tk.Tk()
root.title("Video Downloader Pro")
root.geometry("500x450+750+300")
root.minsize(500, 450)

# Stil ayarları
style = ttk.Style()
style.configure('TButton', padding=5)
style.configure('TLabel', padding=5)
style.configure('TEntry', padding=5)

# Icon'u ayarla
try:
    icon_path = resource_path("icon.ico")
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"İcon yüklenirken hata oluştu: {e}")

# Ana frame
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# URL giriş alanı
url_frame = ttk.Frame(main_frame)
url_frame.pack(fill=tk.X, pady=5)
ttk.Label(url_frame, text="Video URL:").pack(side=tk.LEFT)
entry_url = ttk.Entry(url_frame, width=50)
entry_url.pack(side=tk.LEFT, padx=5)

# Kayıt yeri seçme alanı
path_frame = ttk.Frame(main_frame)
path_frame.pack(fill=tk.X, pady=5)
ttk.Label(path_frame, text="Kaydetme Konumu:").pack(side=tk.LEFT)
entry_path = ttk.Entry(path_frame, width=50)
entry_path.pack(side=tk.LEFT, padx=5)
ttk.Button(path_frame, text="Gözat", command=browse_folder).pack(side=tk.LEFT)

# Son kullanılan klasörü yükle
last_folder = load_last_folder()
if last_folder and os.path.exists(last_folder):
    entry_path.insert(0, last_folder)

# MP3 veya Video seçimi
var_audio = tk.BooleanVar()
ttk.Checkbutton(main_frame, text="Sadece Ses (MP3)", variable=var_audio).pack(pady=5)

# İndirme butonu
ttk.Button(main_frame, text="İndir", command=start_download).pack(pady=10)

# Progress bar
progress_frame = ttk.Frame(main_frame)
progress_frame.pack(fill=tk.X, pady=5)
progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
progress_bar.pack(fill=tk.X)

# İndirme durumu
label_status = ttk.Label(main_frame, text="İndirme durumu: 0%")
label_status.pack(pady=5)

root.mainloop()
