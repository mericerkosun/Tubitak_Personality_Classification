import React, { useState } from 'react';
import { Box, Typography, Button, FormControl, InputLabel, Select, MenuItem, Grid, Paper, SelectChangeEvent, Chip } from '@mui/material';
import { Question } from '../types';

interface QuestionFormProps {
  questions: Question[];
  onSubmit: (answers: number[]) => void;
}

const QuestionForm: React.FC<QuestionFormProps> = ({ questions, onSubmit }) => {
  // State to store answers for each question
  const [answers, setAnswers] = useState<number[]>(Array(50).fill(0));
  
  // When form is submitted
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Check if all questions are answered
    if (answers.every(answer => answer !== 0)) {
      onSubmit(answers);
    } else {
      alert('Lütfen tüm soruları cevaplayın.');
    }
  };
  
  // Handle answer changes
  const handleChange = (questionIndex: number) => (event: SelectChangeEvent<number>) => {
    const newAnswers = [...answers];
    newAnswers[questionIndex] = Number(event.target.value);
    setAnswers(newAnswers);
  };

  // Group questions by category
  const groupedQuestions = questions.reduce((acc, question, index) => {
    const category = question.category || 'Other';
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push({ ...question, index });
    return acc;
  }, {} as Record<string, Array<Question & { index: number }>>);

  const categoryNames = {
    'EXT': 'Dışadönüklük (Extraversion)',
    'EST': 'Duygusal Denge (Emotional Stability)', 
    'AGR': 'Uyumluluk (Agreeableness)',
    'CSN': 'Sorumluluk (Conscientiousness)',
    'OPN': 'Açıklık (Openness)'
  };
  
  return (
    <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
      <Box component="form" onSubmit={handleSubmit}>
        <Typography variant="h5" gutterBottom color="primary">
          Kişilik Analizi Anketi
        </Typography>
        <Typography variant="body2" gutterBottom color="text.secondary" sx={{ mb: 3 }}>
          Her ifade için 1 (kesinlikle katılmıyorum) ile 5 (kesinlikle katılıyorum) arasında bir değer seçin.
        </Typography>
        
        {Object.entries(groupedQuestions).map(([category, categoryQuestions]) => (
          <Box key={category} sx={{ mb: 4 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Chip 
                label={categoryNames[category as keyof typeof categoryNames] || category} 
                color="primary" 
                variant="outlined"
                sx={{ mr: 2 }}
              />
              <Typography variant="h6" color="primary">
                ({categoryQuestions.length} soru)
              </Typography>
            </Box>
            
            <Grid container spacing={2}>
              {categoryQuestions.map((question) => (
                <Grid item xs={12} key={question.id}>
                  <FormControl fullWidth required>
                    <InputLabel id={`question-${question.index}-label`}>
                      {question.id}. {question.text}
                    </InputLabel>
                    <Select
                      labelId={`question-${question.index}-label`}
                      id={`question-${question.index}`}
                      value={answers[question.index]}
                      label={`${question.id}. ${question.text}`}
                      onChange={handleChange(question.index)}
                    >
                      <MenuItem value={0} disabled>Seçiniz</MenuItem>
                      <MenuItem value={1}>1 - Kesinlikle Katılmıyorum</MenuItem>
                      <MenuItem value={2}>2 - Katılmıyorum</MenuItem>
                      <MenuItem value={3}>3 - Kararsızım</MenuItem>
                      <MenuItem value={4}>4 - Katılıyorum</MenuItem>
                      <MenuItem value={5}>5 - Kesinlikle Katılıyorum</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              ))}
            </Grid>
          </Box>
        ))}
        
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Cevaplanan sorular: {answers.filter(answer => answer !== 0).length} / 50
          </Typography>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            size="large"
            disabled={answers.some(answer => answer === 0)}
          >
            Analizi Tamamla
          </Button>
        </Box>
      </Box>
    </Paper>
  );
};

export default QuestionForm; 