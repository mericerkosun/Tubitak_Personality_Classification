import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from joblib import dump, load
import os
from typing import List, Dict, Any

class PersonalityModel:
    def __init__(self):
        self.rf_model = None
        self.scaler = None
        self.model_path = "model/rf_model.joblib"
        self.scaler_path = "model/scaler.joblib"
        self.labeled_data_path = "clustered_dataset.csv"
        self.data_path = "data-final.csv"
        
        # Kişilik boyutları ve küme etiketleri
        self.personality_dimensions = ['EXT', 'EST', 'AGR', 'CSN', 'OPN']
        self.cluster_labels = {
            0: "Analitik Düşünür",
            1: "Sosyal Lider", 
            2: "Yaratıcı Maceracı",
            3: "Uyumlu Destekçi",
            4: "Organize Planlayıcı"
        }
    
    def load(self) -> bool:
        """Kaydedilmiş Random Forest modelini ve scaler'ı yükle"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.rf_model = load(self.model_path)
                self.scaler = load(self.scaler_path)
                return True
            return False
        except Exception as e:
            print(f"Model yüklenirken hata: {e}")
            return False
    
    def create_labeled_dataset(self) -> bool:
        """KMeans ile clustering yaparak labeled veri seti oluştur"""
        try:
            print("📊 Labeled veri seti oluşturuluyor...")
            
            # 1. Veriyi oku
            df = pd.read_csv(self.data_path, sep="\t")
            print(f"Toplam veri sayısı: {len(df)}")
            
            # 2. Eksik verileri temizle
            df = df.dropna()
            print(f"Temizlenen veri sayısı: {len(df)}")
            
            # 3. Sadece 50 soruyu al
            df_questions = df.iloc[:, :50]
            
            # 4. Veriyi standardize et
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(df_questions)
            
            # 5. KMeans ile clustering yap
            kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            
            # 6. Labeled veri setini oluştur
            labeled_df = df_questions.copy()
            labeled_df['personality_type'] = labels
            
            # 7. Labeled veri setini kaydet
            os.makedirs(os.path.dirname(self.labeled_data_path), exist_ok=True)
            labeled_df.to_csv(self.labeled_data_path, index=False)
            
            print(f"✅ Labeled veri seti kaydedildi: {self.labeled_data_path}")
            print(f"Label dağılımı:")
            for label, count in pd.Series(labels).value_counts().sort_index().items():
                print(f"  {self.cluster_labels.get(label, f'Küme {label}')}: {count} kişi")
            
            return True
            
        except Exception as e:
            print(f"Labeled veri seti oluşturulurken hata: {e}")
            return False
    
    def train(self) -> Dict[str, Any]:
        """Random Forest modelini eğit ve kaydet"""
        try:
            # 1. Labeled veri seti var mı kontrol et
            if not os.path.exists(self.labeled_data_path):
                raise Exception(f"Labeled veri seti bulunamadı: {self.labeled_data_path}")
            
            # 2. Labeled veri setini yükle
            print("📚 Labeled veri seti yükleniyor...")
            df = pd.read_csv(self.labeled_data_path)
            
            # 3. Features ve target'ı ayır
            X = df.iloc[:, :50]  # İlk 50 sütun (sorular)
            y = df['ClusterLabel']  # Son sütun (label)
            
            # 4. Train-test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # 5. Veriyi standardize et
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # 6. Random Forest modeli oluştur ve eğit
            print("🌲 Random Forest modeli eğitiliyor...")
            self.rf_model = RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1
            )
            
            self.rf_model.fit(X_train_scaled, y_train)
            
            # 7. Model performansını değerlendir
            y_pred = self.rf_model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, target_names=[
                self.cluster_labels[i] for i in range(5)
            ])
            
            # 8. Modeli ve scaler'ı kaydet
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            dump(self.rf_model, self.model_path)
            dump(self.scaler, self.scaler_path)
            
            print("✅ Random Forest modeli ve scaler başarıyla kaydedildi.")
            print(f"🎯 Model doğruluğu: {accuracy:.4f}")
            print(f"📊 Detaylı rapor:\n{report}")
            
            return {
                "accuracy": accuracy,
                "classification_report": report,
                "model_type": "Random Forest"
            }
            
        except Exception as e:
            raise Exception(f"Model eğitimi başarısız: {e}")
    
    def predict(self, answers: List[float]) -> Dict[str, Any]:
        """Verilen cevaplara göre kişilik tahmini yap"""
        try:
            if self.rf_model is None or self.scaler is None:
                raise ValueError("Model yüklenmemiş. Önce modeli yükleyin veya eğitin.")
            
            if len(answers) != 50:
                raise ValueError("Tam olarak 50 soru cevabı gereklidir")
            
            # Cevapları numpy array'e çevir
            answers_array = np.array(answers).reshape(1, -1)
            
            # Veriyi standardize et
            answers_scaled = self.scaler.transform(answers_array)
            
            # Tahmin yap
            prediction = self.rf_model.predict(answers_scaled)[0]
            prediction_proba = self.rf_model.predict_proba(answers_scaled)[0]
            
            # Kişilik özelliklerini hesapla (her boyut için ortalama)
            features = {}
            for i, dim in enumerate(self.personality_dimensions):
                start_idx = i * 10
                end_idx = start_idx + 10
                dim_scores = answers[start_idx:end_idx]
                features[dim.lower()] = float(np.mean(dim_scores))
            
            # Güven skorları
            confidence_scores = {}
            for i, label in enumerate(self.cluster_labels.values()):
                confidence_scores[label] = float(prediction_proba[i])
            
            return {
                "features": features,
                "prediction": self.cluster_labels.get(prediction, f"Küme {prediction}"),
                "cluster_id": int(prediction),
                "confidence": float(prediction_proba[prediction]),
                "all_probabilities": confidence_scores
            }
            
        except Exception as e:
            raise Exception(f"Tahmin hatası: {e}")
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Random Forest'ın feature importance'larını döndür"""
        try:
            if self.rf_model is None:
                raise ValueError("Model yüklenmemiş")
            
            # Feature importance'ları al
            importances = self.rf_model.feature_importances_
            
            # Soru bazında importance
            feature_importance = {}
            for i in range(50):
                dim_idx = i // 10
                question_idx = (i % 10) + 1
                dim_name = self.personality_dimensions[dim_idx]
                feature_importance[f"{dim_name}{question_idx}"] = float(importances[i])
            
            # Boyut bazında ortalama importance
            dimension_importance = {}
            for i, dim in enumerate(self.personality_dimensions):
                start_idx = i * 10
                end_idx = start_idx + 10
                dim_importance = np.mean(importances[start_idx:end_idx])
                dimension_importance[dim] = float(dim_importance)
            
            return {
                "question_importance": feature_importance,
                "dimension_importance": dimension_importance
            }
            
        except Exception as e:
            raise Exception(f"Feature importance hatası: {e}")