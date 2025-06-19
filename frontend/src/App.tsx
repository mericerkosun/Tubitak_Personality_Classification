import React, { useState } from 'react';
import { Container, Box, Typography, AppBar, Toolbar, CssBaseline, ThemeProvider, createTheme, Alert } from '@mui/material';
import QuestionForm from './components/QuestionForm';
import ResultDisplay from './components/ResultDisplay';
import { questions } from './questions';
import { predictPersonality } from './api';
import { PredictionResult } from './types';

// Theme colors
const theme = createTheme({
  palette: {
    primary: {
      main: '#3f51b5',
    },
    secondary: {
      main: '#f50057',
    },
  },
});

function App() {
  // State to store prediction results
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // When form is submitted
  const handleSubmit = async (answers: number[]) => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Form gönderiliyor, cevap sayısı:', answers.length);
      const prediction = await predictPersonality(answers);
      console.log('Tahmin alındı:', prediction);
      setResult(prediction);
    } catch (err: any) {
      const errorMessage = err.message || 'Sonuçları alırken bir hata oluştu. Lütfen daha sonra tekrar deneyin.';
      setError(errorMessage);
      console.error('Uygulama hatası:', err);
    } finally {
      setLoading(false);
    }
  };

  // Reset the test
  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Kişilik Analizi Uygulaması (Random Forest v2.0)
          </Typography>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="md">
        <Box sx={{ my: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom align="center" color="primary">
            Kişilik Analizi Testi
          </Typography>
          
          <Typography variant="body1" paragraph align="center">
            Bu test, beş temel kişilik özelliğinizi ölçerek kişilik tipinizi belirlemeye yardımcı olur.
            Random Forest algoritması ile %88.7 doğruluk oranında tahmin yapar.
          </Typography>
          
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              <Typography variant="body2">
                <strong>Hata:</strong> {error}
              </Typography>
              <Typography variant="caption" display="block" sx={{ mt: 1 }}>
                API Durumu: http://localhost:8000 - Lütfen backend sunucusunun çalıştığından emin olun.
              </Typography>
            </Alert>
          )}
          
          {loading ? (
            <Box sx={{ textAlign: 'center', my: 4 }}>
              <Typography variant="h6" gutterBottom>
                Random Forest modeli analiz yapıyor...
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Lütfen bekleyin, sonuçlarınız hazırlanıyor.
              </Typography>
            </Box>
          ) : result ? (
            <ResultDisplay result={result} onReset={handleReset} />
          ) : (
            <QuestionForm questions={questions} onSubmit={handleSubmit} />
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App; 