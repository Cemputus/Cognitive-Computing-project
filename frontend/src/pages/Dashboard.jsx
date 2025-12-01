import React, { useEffect, useState } from 'react'
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  SentimentSatisfiedAlt,
  SentimentNeutral,
} from '@mui/icons-material'
import { apiService } from '../services/api'

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await apiService.getDashboardStats()
        setStats(data)
      } catch (err) {
        setError(err.message || 'Failed to load dashboard data')
      } finally {
        setLoading(false)
      }
    }
    fetchStats()
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

  if (error) {
    return (
      <Container>
        <Alert severity="error">{error}</Alert>
      </Container>
    )
  }

  const statCards = [
    {
      title: 'Total Reviews',
      value: stats?.total_reviews || 0,
      change: '+12%',
      icon: <SentimentSatisfiedAlt />,
      color: '#1976d2',
    },
    {
      title: 'Positive Sentiment',
      value: `${((stats?.positive_ratio || 0) * 100).toFixed(1)}%`,
      change: '+5%',
      icon: <TrendingUp />,
      color: '#2e7d32',
    },
    {
      title: 'Negative Sentiment',
      value: `${((stats?.negative_ratio || 0) * 100).toFixed(1)}%`,
      change: '-3%',
      icon: <TrendingDown />,
      color: '#d32f2f',
    },
    {
      title: 'Key Topics',
      value: stats?.topic_count || 0,
      change: '→',
      icon: <SentimentNeutral />,
      color: '#ed6c02',
    },
  ]

  return (
    <Container maxWidth="xl">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight={600}>
          Dashboard
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Welcome to your Business Intelligence Dashboard
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {statCards.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                height: '100%',
                background: `linear-gradient(135deg, ${stat.color}15 0%, ${stat.color}05 100%)`,
                border: `1px solid ${stat.color}30`,
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: `0 8px 24px ${stat.color}40`,
                },
              }}
            >
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Box>
                    <Typography color="text.secondary" gutterBottom variant="body2">
                      {stat.title}
                    </Typography>
                    <Typography variant="h4" component="div" fontWeight={700}>
                      {stat.value}
                    </Typography>
                    <Typography
                      variant="body2"
                      color={stat.change.startsWith('+') ? 'success.main' : 'text.secondary'}
                      sx={{ mt: 1 }}
                    >
                      {stat.change} from last period
                    </Typography>
                  </Box>
                  <Box
                    sx={{
                      color: stat.color,
                      fontSize: '3rem',
                      opacity: 0.8,
                    }}
                  >
                    {stat.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Box mt={4}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Grid container spacing={2} mt={1}>
              <Grid item xs={12} md={4}>
                <Card
                  sx={{
                    bgcolor: 'primary.light',
                    color: 'white',
                    cursor: 'pointer',
                    '&:hover': { bgcolor: 'primary.main' },
                  }}
                >
                  <CardContent>
                    <Typography variant="h6">Analyze Reviews</Typography>
                    <Typography variant="body2">
                      Upload or paste customer reviews for sentiment analysis
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card
                  sx={{
                    bgcolor: 'secondary.light',
                    color: 'white',
                    cursor: 'pointer',
                    '&:hover': { bgcolor: 'secondary.main' },
                  }}
                >
                  <CardContent>
                    <Typography variant="h6">View Trends</Typography>
                    <Typography variant="body2">
                      Explore sentiment trends and forecasts
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card
                  sx={{
                    bgcolor: 'success.light',
                    color: 'white',
                    cursor: 'pointer',
                    '&:hover': { bgcolor: 'success.main' },
                  }}
                >
                  <CardContent>
                    <Typography variant="h6">Topic Discovery</Typography>
                    <Typography variant="body2">
                      Identify key topics in customer feedback
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Box>
    </Container>
  )
}

export default Dashboard


