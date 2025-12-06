import React, { useEffect, useState } from 'react'
import {
  Container,
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  CircularProgress,
  Chip,
  Alert,
  LinearProgress,
  Tooltip,
  IconButton,
} from '@mui/material'
import {
  Topic as TopicIcon,
  TrendingUp,
  Refresh,
  Info,
} from '@mui/icons-material'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import { apiService } from '../services/api'
import { motion } from 'framer-motion'

const TopicAnalysis = () => {
  const [topics, setTopics] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchTopics()
  }, [])

  const fetchTopics = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await apiService.getTopics()
      
      // Handle both array and object responses
      if (Array.isArray(data)) {
        // Direct array response
        if (data.length > 0) {
          setTopics(data)
          setError(null)
        } else {
          setTopics([])
          setError('No topics available. Please ensure Milestone 2 notebook has been run.')
        }
      } else if (data && typeof data === 'object') {
        // Object response
        if (Array.isArray(data.topics)) {
          if (data.topics.length > 0) {
            setTopics(data.topics)
            setError(null)
          } else {
            // Empty topics array - show error message from backend
            setTopics([])
            setError(data.message || data.error || 'No topics available. Please ensure Milestone 2 notebook has been run.')
          }
        } else if (data.error) {
          // Error object - display the message
          setTopics([])
          setError(data.message || data.error)
        } else {
          // Unknown structure
          setTopics([])
          setError('Unknown response format from server.')
        }
      } else {
        setTopics([])
        setError('No topics data received from server.')
      }
    } catch (err) {
      console.error('Error fetching topics:', err)
      let errorMessage = 'Failed to load topics'
      let errorDetails = ''
      
      if (err.code === 'ERR_NETWORK' || err.message?.includes('Network Error') || err.message?.includes('Cannot connect')) {
        errorMessage = 'Cannot connect to server'
        errorDetails = 'Please ensure the backend is running on http://localhost:5000'
      } else if (err.response) {
        // Server responded with error status (could be 200 with error in body)
        const responseData = err.response.data
        errorMessage = responseData?.error || responseData?.message || errorMessage
        errorDetails = responseData?.message || responseData?.error || ''
        
        // If error response has topics array, check if it's empty or has data
        if (responseData?.topics && Array.isArray(responseData.topics)) {
          if (responseData.topics.length > 0) {
            setTopics(responseData.topics)
            setError(null) // Clear error if we have topics to display
          } else {
            // Empty topics array - show the error message
            setTopics([])
            setError(errorDetails || errorMessage)
          }
        } else {
          // No topics array - show error
          setTopics([])
          setError(errorDetails || errorMessage)
        }
      } else {
        errorMessage = err.message || errorMessage
        setTopics([])
        setError(errorMessage)
      }
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    )
  }

  // Prepare chart data with meaningful topic names
  const topicChartData = topics.map((topic) => ({
    name: topic.topic_name || `Topic ${topic.topic_id + 1}`,
    reviews: topic.review_count,
    words: topic.topic_words.length,
  }))

  const COLORS = ['#5624d0', '#3b82f6', '#10b981', '#f59e0b', '#ef4444']

  return (
    <Container maxWidth="xl">
      <Box mb={4} display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="h4" component="h1" gutterBottom fontWeight={700}>
            Topic Analysis
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Discover key topics and themes in customer feedback using LDA topic modeling
          </Typography>
        </Box>
        <IconButton onClick={fetchTopics} color="primary">
          <Refresh />
        </IconButton>
      </Box>

      {error && topics.length === 0 && (
        <Alert 
          severity={error.includes('Cannot connect') ? 'error' : 'warning'} 
          sx={{ mb: 3 }}
          action={
            <IconButton
              size="small"
              color="inherit"
              onClick={fetchTopics}
            >
              <Refresh />
            </IconButton>
          }
        >
          <Typography variant="body1" fontWeight={600} gutterBottom>
            {error.includes('Cannot connect') ? 'Connection Error' : 
             error.includes('Version Mismatch') ? 'Model Version Mismatch' :
             'No Topics Available'}
          </Typography>
          <Typography variant="body2" component="div" sx={{ whiteSpace: 'pre-line' }}>
            {error}
          </Typography>
          {error.includes('Cannot connect') && (
            <Typography variant="caption" display="block" sx={{ mt: 1 }}>
              Make sure the backend server is running. You can start it by running: <code>python backend_api.py</code> in the backend directory.
            </Typography>
          )}
        </Alert>
      )}

      {topics.length === 0 && !loading && !error && (
        <Card>
          <CardContent>
            <Box textAlign="center" py={4}>
              <Typography variant="h6" color="text.secondary" gutterBottom>
                No Topics Available
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Please ensure Milestone 2 notebook has been run to generate topic models.
              </Typography>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Topic Distribution Chart */}
      {topics.length > 0 && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h6" fontWeight={600} gutterBottom mb={3}>
              Topic Distribution
            </Typography>
            <Box height={300}>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={topicChartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <RechartsTooltip
                    contentStyle={{
                      backgroundColor: 'rgba(255, 255, 255, 0.95)',
                      border: '1px solid #e5e7eb',
                      borderRadius: 8,
                    }}
                  />
                  <Legend />
                  <Bar dataKey="reviews" fill="#5624d0" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Topic Cards */}
      <Grid container spacing={3}>
        {topics.map((topic, index) => (
          <Grid item xs={12} md={6} lg={4} key={topic.topic_id}>
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -8 }}
            >
              <Card
                sx={{
                  height: '100%',
                  borderLeft: `4px solid ${COLORS[index % COLORS.length]}`,
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-8px)',
                    boxShadow: 8,
                  },
                }}
              >
                <CardContent>
                  <Box display="flex" alignItems="center" gap={2} mb={2}>
                    <Box
                      sx={{
                        bgcolor: `${COLORS[index % COLORS.length]}15`,
                        p: 1.5,
                        borderRadius: 2,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                      }}
                    >
                      <TopicIcon sx={{ color: COLORS[index % COLORS.length], fontSize: 28 }} />
                    </Box>
                    <Box flex={1}>
                      <Typography variant="h6" fontWeight={600}>
                        {topic.topic_name || `Topic ${topic.topic_id + 1}`}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {topic.review_count} reviews
                      </Typography>
                    </Box>
                  </Box>

                  <Box sx={{ mt: 3 }}>
                    <Typography variant="body2" fontWeight={600} gutterBottom color="text.secondary">
                      Top Keywords
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                      {topic.topic_words.slice(0, 8).map((word, idx) => (
                        <Tooltip
                          key={idx}
                          title={`Weight: ${(word.weight * 100).toFixed(2)}%`}
                          arrow
                        >
                          <Chip
                            label={word.word}
                            size="small"
                            sx={{
                              bgcolor: idx < 3 ? `${COLORS[index % COLORS.length]}20` : 'grey.100',
                              color: idx < 3 ? COLORS[index % COLORS.length] : 'text.primary',
                              fontWeight: idx < 3 ? 600 : 400,
                              fontSize: '0.75rem',
                              '&:hover': {
                                bgcolor: idx < 3 ? `${COLORS[index % COLORS.length]}30` : 'grey.200',
                              },
                            }}
                          />
                        </Tooltip>
                      ))}
                    </Box>

                    {/* Word weights visualization */}
                    <Box sx={{ mt: 2 }}>
                      {topic.topic_words.slice(0, 5).map((word, idx) => (
                        <Box key={idx} sx={{ mb: 1 }}>
                          <Box display="flex" justifyContent="space-between" mb={0.5}>
                            <Typography variant="caption" fontWeight={500}>
                              {word.word}
                            </Typography>
                            <Typography variant="caption" color="text.secondary">
                              {(word.weight * 100).toFixed(1)}%
                            </Typography>
                          </Box>
                          <LinearProgress
                            variant="determinate"
                            value={word.weight * 100}
                            sx={{
                              height: 6,
                              borderRadius: 3,
                              bgcolor: 'grey.200',
                              '& .MuiLinearProgress-bar': {
                                bgcolor: COLORS[index % COLORS.length],
                                borderRadius: 3,
                              },
                            }}
                          />
                        </Box>
                      ))}
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>
        ))}
      </Grid>

      {/* Info Card */}
      {topics.length > 0 && (
        <Card sx={{ mt: 4, bgcolor: 'info.light', color: 'info.contrastText' }}>
          <CardContent>
            <Box display="flex" alignItems="start" gap={2}>
              <Info sx={{ fontSize: 32, flexShrink: 0 }} />
              <Box>
                <Typography variant="h6" fontWeight={600} gutterBottom>
                  About Topic Modeling
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  Topics are discovered using Latent Dirichlet Allocation (LDA), an unsupervised machine learning
                  algorithm that identifies hidden themes in text data. Each topic represents a collection of words
                  that frequently appear together, helping you understand the main themes in customer feedback.
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      )}
    </Container>
  )
}

export default TopicAnalysis
