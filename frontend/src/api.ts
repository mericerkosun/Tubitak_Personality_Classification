import axios from 'axios';
import { PredictionResult } from './types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// API ile kişilik tahmini yapmak için
export const predictPersonality = async (answers: number[]): Promise<PredictionResult> => {
  try {
    console.log('API isteği gönderiliyor:', { url: `${API_URL}/predict`, answers: answers.length });
    
    const response = await axios.post(`${API_URL}/predict`, {
      questions: answers
    });
    
    console.log('API yanıtı alındı:', response.data);
    return response.data;
  } catch (error: any) {
    console.error('API hatası detayları:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status,
      url: `${API_URL}/predict`
    });
    
    if (error.response) {
      // Server responded with error status
      throw new Error(`API Hatası (${error.response.status}): ${error.response.data?.detail || 'Bilinmeyen hata'}`);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('API sunucusuna ulaşılamıyor. Lütfen sunucunun çalıştığından emin olun.');
    } else {
      // Something else happened
      throw new Error(`İstek hatası: ${error.message}`);
    }
  }
}; 