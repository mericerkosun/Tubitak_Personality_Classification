from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class QuestionData(BaseModel):
    questions: List[float]  # 1-5 arası float değerler

class PersonalityFeatures(BaseModel):
    ext: float  # Extraversion
    est: float  # Emotional Stability (Neuroticism)
    agr: float  # Agreeableness
    csn: float  # Conscientiousness
    opn: float  # Openness

class PredictionResult(BaseModel):
    features: PersonalityFeatures
    prediction: str
    cluster_id: int
    confidence: Optional[float] = None  # Random Forest için güven skoru
    all_probabilities: Optional[Dict[str, float]] = None  # Tüm sınıflar için olasılıklar

class ModelStats(BaseModel):
    accuracy: Optional[float] = None
    classification_report: str
    model_type: Optional[str] = None

class FeatureImportance(BaseModel):
    question_importance: Dict[str, float]  # Her soru için importance
    dimension_importance: Dict[str, float]  # Her boyut için ortalama importance 