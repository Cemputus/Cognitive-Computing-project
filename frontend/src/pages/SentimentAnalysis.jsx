import React, { useState } from 'react'
import {
  Container,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Box,
  Grid,
  Chip,
  CircularProgress,
  Alert,
} from '@mui/material'
import { Send as SendIcon } from '@mui/icons-material'
import { apiService } from '../services/api'

const SentimentAnalysis = () => {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const analysis = await apiService.analyzeSentiment(text)
      setResult(analysis)
    } catch (err) {
      setError(err.message || 'Failed to analyze sentiment')
    } finally {
      setLoading(false)
    }
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return 'success'
      case 'negative':
        return 'error'
      default:
        return 'default'
    }
  }

  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight={600}>
          Sentiment Analysis
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Analyze the sentiment of customer reviews and feedback
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Enter Text to Analyze
              </Typography>
              <TextField
                fullWidth
                multiline
                rows={8}
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste customer review or feedback here..."
                variant="outlined"
                sx={{ mb: 2 }}
              />
              <Button
                variant="contained"
                size="large"
                startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
                fullWidth
              >
                Analyze Sentiment
              </Button>
              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Analysis Results
              </Typography>
              {result ? (
                <Box>
                  <Box mb={3}>
                    <Chip
                      label={result.sentiment.toUpperCase()}
                      color={getSentimentColor(result.sentiment)}
                      size="large"
                      sx={{ fontSize: '1rem', fontWeight: 600, p: 2 }}
                    />
                  </Box>
                  <Grid container spacing={2}>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        Positive
                      </Typography>
                      <Typography variant="h6" color="success.main">
                        {((result.pos || result.positive || 0) * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        Neutral
                      </Typography>
                      <Typography variant="h6" color="text.secondary">
                        {((result.neu || result.neutral || 0) * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                    <Grid item xs={4}>
                      <Typography variant="body2" color="text.secondary">
                        Negative
                      </Typography>
                      <Typography variant="h6" color="error.main">
                        {((result.neg || result.negative || 0) * 100).toFixed(1)}%
                      </Typography>
                    </Grid>
                  </Grid>
                  {result.compound !== undefined && (
                    <Box mt={3}>
                      <Typography variant="body2" color="text.secondary" gutterBottom>
                        Compound Score
                      </Typography>
                      <Typography variant="h5" fontWeight={600}>
                        {result.compound.toFixed(3)}
                      </Typography>
                    </Box>
                  )}
                </Box>
              ) : (
                <Typography color="text.secondary">
                  Enter text and click "Analyze Sentiment" to see results
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}

export default SentimentAnalysis


