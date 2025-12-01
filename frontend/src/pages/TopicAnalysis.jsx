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
      const data = await apiService.getTopics()
      setTopics(data)
      setError(null)
    } catch (err) {
      setError(err.message || 'Failed to load topics')
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

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {topics.length === 0 && !loading && (
        <Card>
          <CardContent>
            <Typography variant="body1" color="text.secondary" textAlign="center" py={4}>
              No topics available. Run Milestone 2 notebook to generate topic models.
            </Typography>
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
