# Growth Copilot

E-ticaret sitenizin performansını ölçen, günlük strateji önerileri üreten ve GPT tabanlı analizler sunan bir otomasyon projesidir.

## Özellikler
- Shopify ve Meta API'lerinden otomatik veri çekme
- Parquet formatında veri sunumu
- Otomatik veri güncelleme (GitHub Actions ile)
- Güvenli secrets yönetimi (GitHub Secrets ve .env)
- ChatGPT Plus ve özel GPT entegrasyonu
- Incremental veri çekme sistemi

## Kurulum
Projenin hem lokalde hem de GitHub Actions üzerinde çalışabilmesi için API anahtarları ve diğer hassas bilgiler farklı yöntemlerle yönetilir:

1.  **Lokal Geliştirme/Test:**
    -   `.envs` klasörü altında `.env` uzantılı dosyalar oluşturun (örneğin `.envs/meta.env`).
    -   Gerekli tüm API değişkenlerini (Token, ID, Secret vb.) bu dosyalara `ANAHTAR=DEĞER` formatında ekleyin.
    -   Bu dosyalar `.gitignore` ile takip edilmez ve güvenliğiniz için paylaşılmamalıdır.

2.  **GitHub Actions:**
    -   GitHub projenizin ayarlarına gidin (`Settings` -> `Secrets and variables` -> `Actions`).
    -   Kullanılan tüm API değişkenlerini (Account ID, App ID, App Secret, Marketing Token vb.) GitHub Secrets olarak ekleyin.
    -   `config_*.py` dosyaları, çalışma ortamına göre otomatik olarak `.env` dosyasından (lokal) veya GitHub Secrets'tan (GitHub Actions) bilgileri alacaktır.

3.  Gerekli Python paketlerini yükleyin:
    ```bash
    pip install -r requirements.txt
    ```
4.  `Config` klasöründeki ilgili `config_*.py` dosyalarını (özellikle GitHub için sabit ID'ler veya lokal için özel ayarlar gerekiyorsa) ihtiyacınıza göre gözden geçirin.

## Klasör Yapısı
- Data/
  - API_Data/: API'lerden çekilen Parquet veri dosyaları
    - Meta/
      - meta_daily.parquet
    - Shopify/
      - Shopify_Data_Daily.parquet
- Config/: Yapılandırma dosyaları (Ortama göre yükleme mantığı içerir)
  - config_meta.py
  - config_shopify.py
  - config_openai.py
- .envs/: Lokal environment variable dosyaları (gitignoreed)
  - meta.env
  - shopify.env
  - openai.env
- Launch_Local/: Lokal ortamda .env dosyalarını yükleyen yardımcı scriptler
  - launch_local_meta.py
  - launch_local_shopify.py
  - launch_local_openai.py
- Meta_Marketing_API/: Meta Marketing veri çekme scripti
  - fetch_meta_daily.py
- Shopify_Admin_API/: Shopify veri çekme scripti
- fetch_shopify_daily.py
- .github/workflows/: GitHub Actions otomasyon scriptleri
  - Meta/
    - fetch_meta_daily.yml
  - Shopify/
    - fetch_shopify_daily.yml

## Kullanım
1. Veriler her sabah 06:00'da (TR saati) otomatik olarak güncellenir (GitHub Actions cron schedule).
2. Script, mevcut Parquet dosyasındaki en son tarihi kontrol eder ve yalnızca eksik günlerin verisini çeker (incremental).
3. Çekilen ve güncellenen Parquet veri dosyaları (örneğin `Data/API_Data/Meta/meta_daily.parquet`), GitHub repository'sine commitlenir.
4. Parquet veri dosyaları ChatGPT Plus ve özel GPT'nize "Import URL" ile yüklenerek analiz edilebilir.
5. ChatGPT, verileri analiz ederek stratejiler üretebilir. 