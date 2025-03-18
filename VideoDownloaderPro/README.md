# Video Downloader Pro

Video Downloader Pro, YouTube ve diğer popüler video platformlarından video indirmenizi sağlayan kullanıcı dostu bir masaüstü uygulamasıdır.

## Özellikler

- YouTube videolarını indirme
- Sadece ses (MP3) olarak indirme seçeneği
- İndirme ilerleme durumu gösterimi
- Kullanıcı dostu arayüz
- Özelleştirilebilir indirme konumu

## Gereksinimler

- Python 3.6 veya üzeri
- yt-dlp
- FFmpeg (ses indirme için gerekli)

## Kurulum

1. Projeyi klonlayın:
```bash
git clone https://github.com/TalhaTufanN/VideoDownloaderPro.git
cd VideoDownloaderPro
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. FFmpeg'i yükleyin:
- Windows için: [FFmpeg İndirme Sayfası](https://ffmpeg.org/download.html)
- Linux için: `sudo apt-get install ffmpeg`
- macOS için: `brew install ffmpeg`

## Kullanım

1. Programı başlatın:
```bash
python VideoDownloaderPro.py
```

2. Video URL'sini girin
3. Kaydetme konumunu seçin
4. İsterseniz "Sadece Ses (MP3)" seçeneğini işaretleyin
5. "İndir" butonuna tıklayın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir özellik dalı oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Dalınıza push yapın (`git push origin yeni-ozellik`)
5. Bir Pull Request oluşturun 