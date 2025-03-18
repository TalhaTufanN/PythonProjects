import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import sys
import time  # Zaman bilgisini almak için
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
    label_status.config(text=f"İndirme durumu: {progress}%")

def reset_fields():
    entry_url.delete(0, tk.END)
    var_audio.set(False)

# Tkinter arayüzü
root = tk.Tk()
root.title("Video Downloader Pro")
root.geometry("400x300+750+300")
root.minsize(400,300)

# Icon'u ayarla
try:
    icon_path = resource_path("icon.ico")
    root.iconbitmap(icon_path)
except Exception as e:
    print(f"İcon yüklenirken hata oluştu: {e}")

# URL giriş alanı
tk.Label(root, text="Video URL:").pack(pady=5)
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

# Kayıt yeri seçme butonu
tk.Label(root, text="Kaydetme Konumu:").pack(pady=5)
entry_path = tk.Entry(root, width=50)
entry_path.pack(pady=5)
tk.Button(root, text="Gözat", command=browse_folder).pack(pady=5)

# MP3 veya Video seçimi
var_audio = tk.BooleanVar()
tk.Checkbutton(root, text="Sadece Ses (MP3)", variable=var_audio).pack(pady=5)

# İndirme butonu
tk.Button(root, text="İndir", command=start_download).pack(pady=5)

# İndirme durumu
label_status = tk.Label(root, text="İndirme durumu: 0%")
label_status.pack(pady=10)

root.mainloop()
