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
  Paper,
  Divider,
  IconButton,
  Tooltip,
} from '@mui/material'
import {
  Send as SendIcon,
  ContentCopy,
  Refresh,
  TrendingUp,
  TrendingDown,
  SentimentSatisfiedAlt,
  SentimentNeutral,
  SentimentDissatisfied,
} from '@mui/icons-material'
import {
  RadialBarChart,
  RadialBar,
  ResponsiveContainer,
  Legend,
  Cell,
  Tooltip as RechartsTooltip,
} from 'recharts'
import { apiService } from '../services/api'
import { motion } from 'framer-motion'

const SentimentAnalysis = () => {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])

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
      // Add to history
      setHistory([{ text, result: analysis, timestamp: new Date() }, ...history.slice(0, 4)])
    } catch (err) {
      setError(err.message || 'Failed to analyze sentiment')
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setText('')
    setResult(null)
    setError(null)
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(text)
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

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case 'positive':
        return <SentimentSatisfiedAlt sx={{ fontSize: 32 }} />
      case 'negative':
        return <SentimentDissatisfied sx={{ fontSize: 32 }} />
      default:
        return <SentimentNeutral sx={{ fontSize: 32 }} />
    }
  }

  // Prepare radial chart data
  const radialData = result
    ? [
        {
          name: 'Positive',
          value: ((result.pos ?? result.positive ?? 0) * 100).toFixed(1),
          fill: '#10b981',
        },
        {
          name: 'Neutral',
          value: ((result.neu ?? result.neutral ?? 0) * 100).toFixed(1),
          fill: '#6b7280',
        },
        {
          name: 'Negative',
          value: ((result.neg ?? result.negative ?? 0) * 100).toFixed(1),
          fill: '#ef4444',
        },
      ]
    : []

  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight={700}>
          Sentiment Analysis
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Analyze the sentiment of customer reviews and feedback using advanced NLP models
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Input Section */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6" fontWeight={600}>
                  Enter Text to Analyze
                </Typography>
                <Box display="flex" gap={1}>
                  <Tooltip title="Clear">
                    <IconButton size="small" onClick={handleClear}>
                      <Refresh fontSize="small" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Copy">
                    <IconButton size="small" onClick={handleCopy} disabled={!text}>
                      <ContentCopy fontSize="small" />
                    </IconButton>
                  </Tooltip>
                </Box>
              </Box>
              <Divider sx={{ mb: 2 }} />
              <TextField
                fullWidth
                multiline
                rows={10}
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste customer review or feedback here...

Example:
'Great service! Very fast delivery in Kampala. Highly recommend!'"
                variant="outlined"
                sx={{ mb: 2 }}
              />
              <Button
                variant="contained"
                size="large"
                startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SendIcon />}
                onClick={handleAnalyze}
                disabled={loading || !text.trim()}
                fullWidth
                sx={{
                  py: 1.5,
                  fontWeight: 600,
                  fontSize: '1rem',
                }}
              >
                {loading ? 'Analyzing...' : 'Analyze Sentiment'}
              </Button>
              {error && (
                <Alert severity="error" sx={{ mt: 2 }}>
                  {error}
                </Alert>
              )}
            </CardContent>
          </Card>

          {/* History */}
          {history.length > 0 && (
            <Card sx={{ mt: 3 }}>
              <CardContent>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  Recent Analyses
                </Typography>
                <Divider sx={{ mb: 2 }} />
                <Box sx={{ maxHeight: 300, overflowY: 'auto' }}>
                  {history.map((item, idx) => (
                    <Paper
                      key={idx}
                      sx={{
                        p: 2,
                        mb: 1.5,
                        bgcolor: 'grey.50',
                        cursor: 'pointer',
                        '&:hover': {
                          bgcolor: 'grey.100',
                        },
                      }}
                      onClick={() => {
                        setText(item.text)
                        setResult(item.result)
                      }}
                    >
                      <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
                        <Chip
                          label={item.result.sentiment}
                          size="small"
                          color={getSentimentColor(item.result.sentiment)}
                          sx={{ fontWeight: 600 }}
                        />
                        <Typography variant="caption" color="text.secondary">
                          {item.timestamp.toLocaleTimeString()}
                        </Typography>
                      </Box>
                      <Typography
                        variant="body2"
                        sx={{
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          display: '-webkit-box',
                          WebkitLineClamp: 2,
                          WebkitBoxOrient: 'vertical',
                        }}
                      >
                        {item.text}
                      </Typography>
                    </Paper>
                  ))}
                </Box>
              </CardContent>
            </Card>
          )}
        </Grid>

        {/* Results Section */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Analysis Results
              </Typography>
              <Divider sx={{ mb: 3 }} />
              {result ? (
                <Box>
                  {/* Sentiment Badge */}
                  <Box mb={3} textAlign="center">
                    <motion.div
                      initial={{ scale: 0.8, opacity: 0 }}
                      animate={{ scale: 1, opacity: 1 }}
                      transition={{ duration: 0.3 }}
                    >
                      <Box
                        sx={{
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: 2,
                          p: 3,
                          borderRadius: 3,
                          bgcolor: `${getSentimentColor(result.sentiment)}.light`,
                          border: `2px solid`,
                          borderColor: `${getSentimentColor(result.sentiment)}.main`,
                        }}
                      >
                        {getSentimentIcon(result.sentiment)}
                        <Box>
                          <Typography variant="h4" fontWeight={700} color={`${getSentimentColor(result.sentiment)}.main`}>
                            {result.sentiment.toUpperCase()}
                          </Typography>
                          {result.confidence && (
                            <Typography variant="body2" color="text.secondary">
                              Confidence: {(result.confidence * 100).toFixed(1)}%
                            </Typography>
                          )}
                        </Box>
                      </Box>
                    </motion.div>
                  </Box>

                  {/* Sentiment Scores */}
                  <Grid container spacing={2} mb={3}>
                    <Grid item xs={4}>
                      <Paper
                        sx={{
                          p: 2,
                          textAlign: 'center',
                          bgcolor: '#10b98115',
                          border: '1px solid #10b98130',
                          borderRadius: 2,
                        }}
                      >
                        <Typography variant="body2" color="text.secondary" gutterBottom fontWeight={500}>
                          Positive
                        </Typography>
                        <Typography variant="h5" color="success.main" fontWeight={700}>
                          {(() => {
                            const posValue = result.pos ?? result.positive ?? 0
                            return (posValue * 100).toFixed(1)
                          })()}%
                        </Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={4}>
                      <Paper
                        sx={{
                          p: 2,
                          textAlign: 'center',
                          bgcolor: '#6b728015',
                          border: '1px solid #6b728030',
                          borderRadius: 2,
                        }}
                      >
                        <Typography variant="body2" color="text.secondary" gutterBottom fontWeight={500}>
                          Neutral
                        </Typography>
                        <Typography variant="h5" color="text.secondary" fontWeight={700}>
                          {(() => {
                            const neuValue = result.neu ?? result.neutral ?? 0
                            return (neuValue * 100).toFixed(1)
                          })()}%
                        </Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={4}>
                      <Paper
                        sx={{
                          p: 2,
                          textAlign: 'center',
                          bgcolor: '#ef444415',
                          border: '1px solid #ef444430',
                          borderRadius: 2,
                        }}
                      >
                        <Typography variant="body2" color="text.secondary" gutterBottom fontWeight={500}>
                          Negative
                        </Typography>
                        <Typography variant="h5" color="error.main" fontWeight={700}>
                          {(() => {
                            const negValue = result.neg ?? result.negative ?? 0
                            return (negValue * 100).toFixed(1)
                          })()}%
                        </Typography>
                      </Paper>
                    </Grid>
                  </Grid>

                  {/* Radial Chart */}
                  <Box height={250} mb={3}>
                    <ResponsiveContainer width="100%" height="100%">
                      <RadialBarChart
                        cx="50%"
                        cy="50%"
                        innerRadius="40%"
                        outerRadius="80%"
                        data={radialData}
                        startAngle={90}
                        endAngle={-270}
                      >
                        <RadialBar dataKey="value" cornerRadius={8} />
                        <Legend
                          iconSize={12}
                          layout="vertical"
                          verticalAlign="middle"
                          align="right"
                          wrapperStyle={{ fontSize: '0.875rem' }}
                        />
                        <RechartsTooltip
                          contentStyle={{
                            backgroundColor: 'rgba(255, 255, 255, 0.95)',
                            border: '1px solid #e5e7eb',
                            borderRadius: 8,
                          }}
                        />
                      </RadialBarChart>
                    </ResponsiveContainer>
                  </Box>

                  {/* Compound Score */}
                  {result.compound !== undefined && (
                    <Paper
                      sx={{
                        p: 2,
                        bgcolor: 'primary.light',
                        color: 'white',
                        borderRadius: 2,
                      }}
                    >
                      <Typography variant="body2" gutterBottom sx={{ opacity: 0.9 }}>
                        Compound Score
                      </Typography>
                      <Box display="flex" alignItems="center" gap={1}>
                        <Typography variant="h4" fontWeight={700}>
                          {result.compound.toFixed(3)}
                        </Typography>
                        {result.compound > 0.05 ? (
                          <TrendingUp sx={{ fontSize: 28 }} />
                        ) : result.compound < -0.05 ? (
                          <TrendingDown sx={{ fontSize: 28 }} />
                        ) : null}
                      </Box>
                      <Typography variant="caption" sx={{ opacity: 0.8, mt: 0.5, display: 'block' }}>
                        Range: -1 (very negative) to +1 (very positive)
                      </Typography>
                    </Paper>
                  )}

                  {/* Additional Details */}
                  {result.method && (
                    <Box mt={2}>
                      <Chip
                        label={`Method: ${result.method}`}
                        size="small"
                        variant="outlined"
                        sx={{ mr: 1 }}
                      />
                      {result.methods_used && (
                        <Chip
                          label={`Methods: ${result.methods_used}`}
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  )}
                </Box>
              ) : (
                <Box
                  sx={{
                    textAlign: 'center',
                    py: 8,
                    color: 'text.secondary',
                  }}
                >
                  <SentimentSatisfiedAlt sx={{ fontSize: 64, mb: 2, opacity: 0.3 }} />
                  <Typography variant="body1" fontWeight={500}>
                    Enter text and click "Analyze Sentiment" to see results
                  </Typography>
                  <Typography variant="body2" sx={{ mt: 1, opacity: 0.7 }}>
                    Our advanced NLP models will analyze the sentiment and provide detailed insights
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}

export default SentimentAnalysis
