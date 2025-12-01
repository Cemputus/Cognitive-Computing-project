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
} from '@mui/material'
import { apiService } from '../services/api'

const TopicAnalysis = () => {
  const [topics, setTopics] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const data = await apiService.getTopics()
        setTopics(data)
      } catch (err) {
        setError(err.message || 'Failed to load topics')
      } finally {
        setLoading(false)
      }
    }
    fetchTopics()
  }, [])

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight={600}>
          Topic Analysis
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Discover key topics and themes in customer feedback
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {topics.map((topic) => (
          <Grid item xs={12} md={6} key={topic.topic_id}>
            <Card
              sx={{
                height: '100%',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
            >
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Topic {topic.topic_id + 1}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Found in {topic.review_count} reviews
                </Typography>
                <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {topic.topic_words.slice(0, 10).map((word, idx) => (
                    <Chip
                      key={idx}
                      label={`${word.word} (${(word.weight * 100).toFixed(1)}%)`}
                      size="small"
                      color={idx < 3 ? 'primary' : 'default'}
                    />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  )
}

export default TopicAnalysis


