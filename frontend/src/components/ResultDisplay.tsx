import React from 'react';
import { Box, Typography, Paper, Grid, Divider, Button, LinearProgress, Chip } from '@mui/material';
import { PredictionResult } from '../types';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, RadialLinearScale } from 'chart.js';
import { PolarArea } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(RadialLinearScale, ArcElement, Tooltip, Legend);

interface ResultDisplayProps {
  result: PredictionResult | null;
  onReset: () => void;
}

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, onReset }) => {
  if (!result) return null;
  
  // Prepare personality traits for the chart
  const chartData = {
    labels: [
      'Dışadönüklük',
      'Duygusal Denge',
      'Uyumluluk',
      'Sorumluluk',
      'Açıklık'
    ],
    datasets: [
      {
        label: 'Kişilik Özellikleri',
        data: [
          result.features.ext,
          result.features.est,
          result.features.agr,
          result.features.csn,
          result.features.opn
        ],
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)'
        ],
        borderWidth: 1
      }
    ]
  };

  // Personality type descriptions
  const personalityDescriptions: {[key: string]: string} = {
    'Analitik Düşünür': 'Detaylara odaklanan, sistematik düşünen ve problem çözme konusunda yetenekli bir kişiliğe sahipsiniz.',
    'Sosyal Lider': 'İnsanlarla iletişim kurmakta başarılı, liderlik özelliklerine sahip ve sosyal bir kişiliğiniz var.',
    'Yaratıcı Maceracı': 'Yenilikçi, yaratıcı düşünce yapısına sahip ve yeni deneyimlere açık bir kişiliğiniz bulunuyor.',
    'Uyumlu Destekçi': 'Empati kurabilen, işbirlikçi ve başkalarının ihtiyaçlarını önemseyen bir kişiliğe sahipsiniz.',
    'Organize Planlayıcı': 'Düzenli, planlı ve sorumluluk sahibi bir yaklaşımla hayata bakan bir kişiliğiniz var.'
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Box>
        <Typography variant="h4" gutterBottom color="primary" align="center">
          Kişilik Analizi Sonucu
        </Typography>
        <Divider sx={{ mb: 3 }} />
        
        <Grid container spacing={4}>
          <Grid item xs={12} md={6}>
            <Box sx={{ height: 300 }}>
              <PolarArea data={chartData} options={{ maintainAspectRatio: false }} />
            </Box>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="h5" color="secondary" sx={{ mr: 2 }}>
                Kişilik Tipiniz: {result.prediction}
              </Typography>
              {result.confidence && (
                <Chip 
                  label={`Güven: %${(result.confidence * 100).toFixed(1)}`}
                  color="primary"
                  variant="outlined"
                />
              )}
            </Box>
            
            <Typography variant="body1" paragraph>
              {personalityDescriptions[result.prediction] || 'Bu kişilik tipi için henüz açıklama mevcut değil.'}
            </Typography>
            
            <Typography variant="subtitle1" gutterBottom sx={{ mt: 2 }}>
              Kişilik Özellikleri Puanları:
            </Typography>
            
            <Typography variant="body2">
              <strong>Dışadönüklük (Extraversion):</strong> {result.features.ext.toFixed(2)} / 5
            </Typography>
            <Typography variant="body2">
              <strong>Duygusal Denge (Emotional Stability):</strong> {result.features.est.toFixed(2)} / 5
            </Typography>
            <Typography variant="body2">
              <strong>Uyumluluk (Agreeableness):</strong> {result.features.agr.toFixed(2)} / 5
            </Typography>
            <Typography variant="body2">
              <strong>Sorumluluk (Conscientiousness):</strong> {result.features.csn.toFixed(2)} / 5
            </Typography>
            <Typography variant="body2">
              <strong>Açıklık (Openness):</strong> {result.features.opn.toFixed(2)} / 5
            </Typography>
          </Grid>
        </Grid>
        
        {/* Random Forest Güven Skorları */}
        {result.all_probabilities && (
          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom color="primary">
              Tüm Kişilik Tipleri için Olasılıklar (Random Forest)
            </Typography>
            <Grid container spacing={2}>
              {Object.entries(result.all_probabilities)
                .sort(([,a], [,b]) => b - a)
                .map(([type, probability]) => (
                <Grid item xs={12} sm={6} md={4} key={type}>
                  <Box sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2" fontWeight={type === result.prediction ? 'bold' : 'normal'}>
                        {type}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        %{(probability * 100).toFixed(1)}
                      </Typography>
                    </Box>
                    <LinearProgress 
                      variant="determinate" 
                      value={probability * 100}
                      color={type === result.prediction ? 'primary' : 'secondary'}
                      sx={{ height: 8, borderRadius: 4 }}
                    />
                  </Box>
                </Grid>
              ))}
            </Grid>
          </Box>
        )}
        
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Button
            variant="contained"
            color="primary"
            onClick={onReset}
          >
            Yeni Test Başlat
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default ResultDisplay; 