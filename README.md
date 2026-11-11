# Studio — Görsel Editör + Yerel AI

Fotoğraf/sticker düzenleyici. Fotoğraf ekleme, katmanlar, taşıma/döndürme/ölçekleme,
kenardan boyutlandırma ve kırpma, serbest/elips/dikdörtgen bölge seçimi, yuvarlak (daire)
fotoğraf, metin (dairesel/kavisli metin dahil), şekiller, filtreler, efektler, gradyan
arka plan ve PNG/JPG/WebP dışa aktarma.

> **English:** A browser-based photo/sticker editor (layers, transforms, crop, selections, curved text, filters, export) with a natural-language assistant that turns Turkish commands into editor actions via a local Ollama model. A tiny Python server serves the UI and proxies Ollama requests to avoid CORS issues.

Ayrıca **doğal dille komut verebileceğin bir AI asistanı** var — bilgisayarına kurduğun
**Ollama** modelini kullanır.

## Nasıl çalıştırılır

1. **Ollama açık olsun.** Windows'ta sistem tepsisinde lama ikonu görünmeli.
   Bir model yoksa asistan sana uygulama içinden indirtebilir; ya da terminalde:
   ```
   ollama pull qwen3:4b
   ```
2. **`baslat.bat` dosyasına çift tıkla.**
   - Küçük bir yerel sunucu başlar ve tarayıcı otomatik açılır (http://127.0.0.1:8765).
   - Kapatmak için açılan siyah pencerede `Ctrl+C` ya da pencereyi kapat.

Python gerekir (çoğu Windows'ta vardır). Yoksa python.org'dan kur; kurulumda
"Add Python to PATH" işaretli olsun.

## Neden bir sunucu var?

Tarayıcı, güvenlik nedeniyle bir `.html` dosyasından doğrudan Ollama'ya (localhost:11434)
istek atamaz (CORS). Bu küçük sunucu iki işi yapıyor:

- Arayüzü düzgün bir web sayfası olarak sunar.
- Ollama isteklerini **sunucu tarafından** iletir (proxy). Böylece `OLLAMA_ORIGINS`
  gibi bir ayar yapmana gerek kalmaz — her şey kutudan çıktığı gibi çalışır.

## AI asistanı nasıl kullanılır

Sağdaki **✨ AI** sekmesini aç. Varsayılan motor **Ollama · PC**; uygulama açılışta
otomatik bağlanır ve modelini seçer. Kutuya ne istediğini yaz, örn:

- "arka planı gün batımı gradyanı yap, ortaya kalın beyaz YAZ başlığı ekle"
- "seçili fotoğrafı daire yap"
- "başlığı dairesel/kemer şeklinde yaz"
- "hepsini siyah-beyaz yap ve indir"

Model çıktısı editör komutlarına çevrilip tuvale uygulanır. Her AI değişikliği geri
alınabilir (Ctrl+Z).

### Model önerisi
Bu iş (Türkçe → JSON komut) için **qwen3:4b** iyi bir denge. Güçlü bir bilgisayarın
varsa `qwen3:8b` daha akıllıdır. AI sekmesindeki model listesinden seçebilirsin.

## Dosyalar
- `index.html` — editör arayüzü (sunucu bunu servis eder)
- `server.py` — yerel sunucu + Ollama proxy
- `baslat.bat` — başlatıcı (çift tıkla)
- `sticker-studio.html` — eski tek-dosya sürüm (Ollama proxy'siz; isteğe bağlı)

## Lisans

MIT. Bkz. [LICENSE](LICENSE).
