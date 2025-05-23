# Growth Copilot

E-ticaret sitenizin performansını ölçen, günlük strateji önerileri üreten ve GPT tabanlı analizler sunan bir otomasyon projesidir.

## Özellikler
- Shopify ve Meta API'lerinden otomatik veri çekme
- JSON ve Excel formatında veri sunumu
- FAISS + OpenAI Embedding ile semantik arama (RAG)
- Otomatik veri güncelleme (GitHub Actions ile)
- Güvenli secrets yönetimi (GitHub Secrets)

## Kurulum
1. Gerekli environment variable'ları GitHub Secrets veya .env dosyasına ekleyin
2. `config.py` dosyasını düzenleyin (örnekler dosyada mevcut)
3. API anahtarlarınızı asla doğrudan kodda tutmayın

## Klasör Yapısı
- Data/: JSON veri dosyaları
- Vectors/: FAISS index ve embedding dosyaları
- Meta_Marketing_API/: Meta Marketing veri çekme scripti
- Meta_Insights_API/: Meta Insights veri çekme scripti
- Shopify_Admin_API/: Shopify veri çekme scripti
- .well-known/: GPT Plugin entegrasyon dosyaları
- .github/workflows/: Otomasyon scriptleri 