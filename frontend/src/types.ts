export interface Question {
  id: number;
  text: string;
  category?: string;
}

export interface PersonalityFeatures {
  ext: number;  // Extraversion
  est: number;  // Emotional Stability
  agr: number;  // Agreeableness
  csn: number;  // Conscientiousness
  opn: number;  // Openness
}

export interface PredictionResult {
  features: PersonalityFeatures;
  prediction: string;
  cluster_id: number;
  confidence?: number;  // Random Forest için güven skoru
  all_probabilities?: { [key: string]: number };  // Tüm sınıflar için olasılıklar
} 