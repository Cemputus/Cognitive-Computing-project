import React from 'react'
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Chip,
} from '@mui/material'
import {
  Business,
  Psychology,
  Timeline,
  Insights,
  Analytics,
  Security,
} from '@mui/icons-material'

const About = () => {
  const features = [
    {
      icon: <Analytics sx={{ fontSize: 40 }} />,
      title: 'Advanced Analytics',
      description: 'Comprehensive sentiment analysis using multiple ML models including VADER, TextBlob, and Transformer-based approaches.',
    },
    {
      icon: <Psychology sx={{ fontSize: 40 }} />,
      title: 'Cognitive Computing',
      description: 'Leveraging cognitive computing principles to understand and reason about customer feedback patterns.',
    },
    {
      icon: <Timeline sx={{ fontSize: 40 }} />,
      title: 'Trend Forecasting',
      description: 'Predictive analytics and sentiment trend forecasting powered by advanced machine learning models.',
    },
    {
      icon: <Insights sx={{ fontSize: 40 }} />,
      title: 'Topic Modeling',
      description: 'Discover key topics and themes in customer feedback using LDA (Latent Dirichlet Allocation) topic modeling.',
    },
    {
      icon: <Business sx={{ fontSize: 40 }} />,
      title: 'Business Intelligence',
      description: 'Real-time business intelligence insights to help make data-driven decisions.',
    },
    {
      icon: <Security sx={{ fontSize: 40 }} />,
      title: 'Secure & Reliable',
      description: 'Enterprise-grade security with JWT authentication and secure data handling.',
    },
  ]

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header */}
      <Box textAlign="center" mb={6}>
        <Typography variant="h3" component="h1" gutterBottom fontWeight={700} sx={{ mb: 2 }}>
          About Business Intelligence Analyst
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 800, mx: 'auto' }}>
          A comprehensive cognitive computing platform for analyzing customer sentiment,
          discovering insights, and forecasting trends from business reviews.
        </Typography>
      </Box>

      {/* Mission Statement */}
      <Card sx={{ mb: 6, bgcolor: 'primary.main', color: 'white' }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h5" gutterBottom fontWeight={600}>
            Our Mission
          </Typography>
          <Typography variant="body1" sx={{ fontSize: '1.1rem', lineHeight: 1.8 }}>
            To empower businesses with intelligent sentiment analysis and predictive insights,
            enabling them to understand customer feedback, identify trends, and make data-driven
            decisions that drive growth and customer satisfaction.
          </Typography>
        </CardContent>
      </Card>

      {/* Features */}
      <Box mb={6}>
        <Typography variant="h4" component="h2" gutterBottom fontWeight={600} textAlign="center" mb={4}>
          Key Features
        </Typography>
        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 4,
                  },
                }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ color: 'primary.main', mb: 2 }}>
                    {feature.icon}
                  </Box>
                  <Typography variant="h6" gutterBottom fontWeight={600}>
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Technology Stack */}
      <Card sx={{ mb: 6 }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h5" gutterBottom fontWeight={600} mb={3}>
            Technology Stack
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom fontWeight={600} color="primary">
                Frontend
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
                <Chip label="React" color="primary" variant="outlined" />
                <Chip label="Material-UI" color="primary" variant="outlined" />
                <Chip label="Recharts" color="primary" variant="outlined" />
                <Chip label="Axios" color="primary" variant="outlined" />
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom fontWeight={600} color="primary">
                Backend
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
                <Chip label="Python" color="secondary" variant="outlined" />
                <Chip label="Flask" color="secondary" variant="outlined" />
                <Chip label="Gensim" color="secondary" variant="outlined" />
                <Chip label="Pandas" color="secondary" variant="outlined" />
                <Chip label="NumPy" color="secondary" variant="outlined" />
              </Box>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom fontWeight={600} color="primary">
                Machine Learning
              </Typography>
              <Box display="flex" flexWrap="wrap" gap={1}>
                <Chip label="VADER" color="success" variant="outlined" />
                <Chip label="TextBlob" color="success" variant="outlined" />
                <Chip label="Transformers" color="success" variant="outlined" />
                <Chip label="LDA" color="success" variant="outlined" />
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* System Architecture */}
      <Card>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h5" gutterBottom fontWeight={600} mb={3}>
            System Architecture
          </Typography>
          <Typography variant="body1" paragraph>
            The Business Intelligence Analyst platform is built on a modern, scalable architecture
            that separates concerns between frontend and backend components:
          </Typography>
          <Box component="ul" sx={{ pl: 4, '& li': { mb: 2 } }}>
            <li>
              <Typography variant="body1">
                <strong>Frontend:</strong> React-based single-page application providing an intuitive
                user interface for data visualization and interaction.
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                <strong>Backend API:</strong> RESTful Flask API handling sentiment analysis, topic modeling,
                and predictive analytics.
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                <strong>Data Processing:</strong> Python-based data pipeline for cleaning, preprocessing,
                and analyzing customer review data.
              </Typography>
            </li>
            <li>
              <Typography variant="body1">
                <strong>ML Models:</strong> Ensemble approach combining multiple sentiment analysis
                methods and LDA topic modeling for comprehensive insights.
              </Typography>
            </li>
          </Box>
        </CardContent>
      </Card>
    </Container>
  )
}

export default About
