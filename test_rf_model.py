#!/usr/bin/env python3
"""
Random Forest Kişilik Modeli Test Scripti
"""

from backend.app.model import PersonalityModel
import numpy as np
import json

def test_model():
    print("🌲 Random Forest Kişilik Modeli Test Ediliyor...")
    
    # Model oluştur ve yükle
    model = PersonalityModel()
    
    if not model.load():
        print("❌ Model yüklenemedi!")
        return
    
    print("✅ Model başarıyla yüklendi")
    
    # Test verileri
    test_cases = [
        {
            "name": "Yüksek Dışadönüklük",
            "answers": [5, 4, 5, 4, 5, 4, 5, 4, 5, 4] + [3] * 40
        },
        {
            "name": "Yüksek Sorumluluk", 
            "answers": [3] * 30 + [5, 4, 5, 4, 5, 4, 5, 4, 5, 4] + [3] * 10
        },
        {
            "name": "Dengeli Profil",
            "answers": [3, 3, 3, 3, 3] * 10
        }
    ]
    
    print("\n📊 Test Sonuçları:")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}:")
        
        try:
            result = model.predict(test_case['answers'])
            
            print(f"   Tahmin: {result['prediction']}")
            print(f"   Güven: %{result['confidence']*100:.1f}")
            print(f"   Küme ID: {result['cluster_id']}")
            
            print("   Kişilik Özellikleri:")
            for dim, score in result['features'].items():
                print(f"     {dim.upper()}: {score:.2f}")
                
            print("   Tüm Olasılıklar:")
            for personality, prob in sorted(result['all_probabilities'].items(), 
                                          key=lambda x: x[1], reverse=True):
                print(f"     {personality}: %{prob*100:.1f}")
                
        except Exception as e:
            print(f"   ❌ Hata: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Test tamamlandı!")

if __name__ == "__main__":
    test_model() 