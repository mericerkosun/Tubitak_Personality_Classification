# Kişilik Analizi Uygulaması

Bu uygulama, Big Five kişilik modelini kullanarak kullanıcıların kişilik özelliklerini analiz eden bir web uygulamasıdır.

Dataset: https://drive.google.com/file/d/1odbJSVkN40n30oNnjgiZ1Ojqm0WoR6ty/view?usp=sharing

## Özellikler

- **50 Soruluk Kapsamlı Test**: Beş temel kişilik boyutunu ölçen 50 soru
- **Kişilik Boyutları**:
  - **Dışadönüklük (Extraversion)**: Sosyal etkileşim ve enerji düzeyi
  - **Duygusal Denge (Emotional Stability)**: Stres ve duygusal kararlılık
  - **Uyumluluk (Agreeableness)**: İşbirliği ve empati
  - **Sorumluluk (Conscientiousness)**: Düzen ve planlama
  - **Açıklık (Openness)**: Yaratıcılık ve yeni deneyimlere açıklık
- **Görsel Sonuçlar**: Polar area chart ile kişilik profili görselleştirmesi
- **5 Kişilik Tipi**:
  - Analitik Düşünür
  - Sosyal Lider
  - Yaratıcı Maceracı
  - Uyumlu Destekçi
  - Organize Planlayıcı

## Teknoloji Stack

### Backend
- **FastAPI**: Modern, hızlı web framework
- **scikit-learn**: Machine learning kütüphanesi
- **KMeans Clustering**: Kişilik tiplerini belirlemek için
- **pandas & numpy**: Veri işleme
- **joblib**: Model kaydetme/yükleme

### Frontend
- **React**: Modern UI framework
- **TypeScript**: Tip güvenliği
- **Material-UI**: Modern UI bileşenleri
- **Chart.js**: Veri görselleştirme
- **Axios**: HTTP istekleri

## Kurulum ve Çalıştırma

### Backend Kurulumu

1. Backend dizinine gidin:
```bash
cd backend
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Backend'i başlatın:
```bash
python run.py
```

Backend http://localhost:8000 adresinde çalışacaktır.

### Frontend Kurulumu

1. Frontend dizinine gidin:
```bash
cd frontend
```

2. Bağımlılıkları yükleyin:
```bash
npm install
```

3. Frontend'i başlatın:
```bash
npm start
```

Frontend http://localhost:3000 adresinde çalışacaktır.

## API Endpoints

### GET /
Ana sayfa mesajı

### POST /train
Modeli eğitir (ilk çalıştırmada otomatik olarak çağrılır)

### POST /predict
Kişilik tahmini yapar
```json
{
  "questions": [3, 2, 4, 2, 3, ...] // 50 adet 1-5 arası değer
}
```

## Kullanım

1. Uygulamayı açın (http://localhost:3000)
2. 50 soruyu 1-5 arası puanlayarak cevaplayın:
   - 1: Kesinlikle Katılmıyorum
   - 2: Katılmıyorum
   - 3: Kararsızım
   - 4: Katılıyorum
   - 5: Kesinlikle Katılıyorum
3. "Analizi Tamamla" butonuna tıklayın
4. Sonuçlarınızı görüntüleyin:
   - Kişilik tipiniz
   - 5 boyutta puanlarınız
   - Görsel grafik
5. "Yeni Test Başlat" ile tekrar test yapabilirsiniz

## Model Detayları

- **Algoritma**: KMeans Clustering (5 küme)
- **Veri**: Big Five kişilik modeli veri seti
- **Özellikler**: 50 soru (her boyut için 10 soru)
- **Standardizasyon**: StandardScaler ile veri normalleştirme
- **Küme Sayısı**: 5 farklı kişilik tipi

## Geliştirme

### Backend Geliştirme
- FastAPI otomatik dokümantasyon: http://localhost:8000/docs
- Model dosyaları: `backend/model/` dizininde saklanır
- Veri dosyası: `backend/data-final.csv`

### Frontend Geliştirme
- TypeScript tip kontrolü aktif
- Material-UI tema özelleştirilebilir
- Chart.js ile görselleştirme

## Lisans

Bu proje eğitim amaçlı geliştirilmiştir. 