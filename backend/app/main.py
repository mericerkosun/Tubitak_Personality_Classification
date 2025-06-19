from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from .model import PersonalityModel
from .schemas import QuestionData, PredictionResult, ModelStats, PersonalityFeatures, FeatureImportance

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# FastAPI uygulamasını oluştur
app = FastAPI(
    title="Kişilik Analizi API - Random Forest",
    description="Random Forest ile kişilik özelliklerini tahmin eden bir API",
    version="2.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm kaynaklara izin ver (üretim için değiştirilmeli)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model nesnesi oluştur
model = PersonalityModel()

# API'nin başlangıcında modeli yükle
@app.on_event("startup")
async def startup_event():
    logging.info("API başlatılıyor")
    try:
        if not model.load():
            logging.info("Random Forest modeli yüklü değil, eğitiliyor...")
            model.train()
            logging.info("Random Forest modeli eğitimi tamamlandı")
        else:
            logging.info("Random Forest modeli başarıyla yüklendi")
    except Exception as e:
        logging.error(f"Model yüklenirken hata oluştu: {str(e)}")

# Ana sayfa
@app.get("/")
async def root():
    return {"message": "Kişilik Analizi API'sine Hoş Geldiniz! (Random Forest v2.0)"}

# Labeled veri seti oluştur
@app.post("/create-labeled-dataset")
async def create_labeled_dataset():
    try:
        success = model.create_labeled_dataset()
        if success:
            return {"message": "Labeled veri seti başarıyla oluşturuldu"}
        else:
            raise HTTPException(status_code=500, detail="Labeled veri seti oluşturulamadı")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Labeled veri seti oluşturma hatası: {str(e)}")

# Modeli eğit
@app.post("/train", response_model=ModelStats)
async def train_model():
    try:
        stats = model.train()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model eğitimi başarısız: {str(e)}")

# Tahmin yap
@app.post("/predict", response_model=PredictionResult)
async def predict(data: QuestionData):
    try:
        # Geçerli veri validasyonu
        if len(data.questions) != 50:
            raise HTTPException(status_code=400, detail="Tam olarak 50 soru cevabı gereklidir")
        
        # Her cevabın 1-5 arasında olduğunu kontrol et
        for i, answer in enumerate(data.questions):
            if not (1 <= answer <= 5):
                raise HTTPException(status_code=400, detail=f"Soru {i+1} için cevap 1-5 arasında olmalıdır")
        
        # Tahmin yap
        result = model.predict(data.questions)
        
        # PersonalityFeatures objesi oluştur
        features = PersonalityFeatures(
            ext=result["features"]["ext"],
            est=result["features"]["est"], 
            agr=result["features"]["agr"],
            csn=result["features"]["csn"],
            opn=result["features"]["opn"]
        )
        
        return PredictionResult(
            features=features,
            prediction=result["prediction"],
            cluster_id=result["cluster_id"],
            confidence=result.get("confidence"),
            all_probabilities=result.get("all_probabilities")
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Geçersiz girdi: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tahmin hatası: {str(e)}")

# Feature importance'ları getir
@app.get("/feature-importance", response_model=FeatureImportance)
async def get_feature_importance():
    try:
        importance = model.get_feature_importance()
        return importance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature importance hatası: {str(e)}")

# Model bilgilerini getir
@app.get("/model-info")
async def get_model_info():
    try:
        return {
            "model_type": "Random Forest Classifier",
            "features": 50,
            "classes": 5,
            "personality_types": list(model.cluster_labels.values()),
            "dimensions": model.personality_dimensions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model bilgisi hatası: {str(e)}") 