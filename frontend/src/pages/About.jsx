import React from 'react'
import {
  Container,
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material'
import {
  Analytics,
  TrendingUp,
  Insights,
  Security,
  Speed,
  Support,
  Psychology,
  AutoAwesome,
} from '@mui/icons-material'
import { motion } from 'framer-motion'

const About = () => {
  const features = [
    {
      icon: <Analytics sx={{ fontSize: 40, color: '#5624d0' }} />,
      title: 'Real-Time Analytics',
      description: 'Get instant insights into customer sentiment and feedback trends with advanced data processing.',
    },
    {
      icon: <TrendingUp sx={{ fontSize: 40, color: '#10b981' }} />,
      title: 'Predictive Forecasting',
      description: 'Leverage machine learning models to predict future sentiment trends and market behavior.',
    },
    {
      icon: <Insights sx={{ fontSize: 40, color: '#f59e0b' }} />,
      title: 'Topic Discovery',
      description: 'Automatically identify and categorize key themes in customer feedback using LDA topic modeling.',
    },
    {
      icon: <Psychology sx={{ fontSize: 40, color: '#3b82f6' }} />,
      title: 'Cognitive Intelligence',
      description: 'Powered by four cognitive pillars: Understand, Reason, Learn, and Interact.',
    },
    {
      icon: <Security sx={{ fontSize: 40, color: '#ef4444' }} />,
      title: 'Secure & Private',
      description: 'Enterprise-grade security with JWT authentication and data encryption.',
    },
    {
      icon: <Speed sx={{ fontSize: 40, color: '#8b5cf6' }} />,
      title: 'High Performance',
      description: 'Optimized for speed with efficient algorithms and real-time processing capabilities.',
    },
  ]

  const pillars = [
    {
      name: 'Understand',
      description: 'Natural Language Processing to interpret unstructured text from reviews and social media',
      color: '#5624d0',
    },
    {
      name: 'Reason',
      description: 'Knowledge graphs and ML models to analyze sentiment, extract trends, and generate insights',
      color: '#3b82f6',
    },
    {
      name: 'Learn',
      description: 'Active feedback loops and model refinement based on new data and user interactions',
      color: '#10b981',
    },
    {
      name: 'Interact',
      description: 'Modern React interface with intuitive dashboards and interactive visualizations',
      color: '#f59e0b',
    },
  ]

  return (
    <Container maxWidth="lg">
      <Box mb={6} textAlign="center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Typography variant="h3" component="h1" gutterBottom fontWeight={700}>
            About CENAnalytics
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 800, mx: 'auto', mt: 2 }}>
            A comprehensive cognitive computing system designed to help small businesses in Kampala, Uganda
            understand customer sentiment, identify market trends, and make data-driven decisions.
          </Typography>
        </motion.div>
      </Box>

      {/* Features Grid */}
      <Box mb={6}>
        <Typography variant="h5" fontWeight={600} gutterBottom mb={3}>
          Key Features
        </Typography>
        <Grid container spacing={3}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={6} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -8 }}
              >
                <Card
                  sx={{
                    height: '100%',
                    transition: 'all 0.3s',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 8,
                    },
                  }}
                >
                  <CardContent>
                    <Box mb={2}>{feature.icon}</Box>
                    <Typography variant="h6" fontWeight={600} gutterBottom>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Cognitive Pillars */}
      <Box mb={6}>
        <Typography variant="h5" fontWeight={600} gutterBottom mb={3}>
          Cognitive Computing Pillars
        </Typography>
        <Grid container spacing={3}>
          {pillars.map((pillar, index) => (
            <Grid item xs={12} md={6} key={index}>
              <motion.div
                initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.15 }}
              >
                <Card
                  sx={{
                    height: '100%',
                    borderLeft: `4px solid ${pillar.color}`,
                    transition: 'all 0.3s',
                    '&:hover': {
                      boxShadow: 6,
                      transform: 'translateX(4px)',
                    },
                  }}
                >
                  <CardContent>
                    <Box display="flex" alignItems="center" gap={2} mb={2}>
                      <Chip
                        label={pillar.name}
                        sx={{
                          bgcolor: `${pillar.color}15`,
                          color: pillar.color,
                          fontWeight: 700,
                          fontSize: '1rem',
                          height: 36,
                        }}
                      />
                    </Box>
                    <Typography variant="body1" color="text.secondary">
                      {pillar.description}
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Technology Stack */}
      <Card>
        <CardContent>
          <Typography variant="h5" fontWeight={600} gutterBottom mb={3}>
            Technology Stack
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom color="primary">
                Frontend
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="React 18" secondary="Modern UI framework" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="Material-UI" secondary="Component library" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="Framer Motion" secondary="Animations" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="Recharts" secondary="Data visualization" />
                </ListItem>
              </List>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom color="primary">
                Backend
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="Flask" secondary="REST API framework" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="Python" secondary="Core language" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="JWT" secondary="Authentication" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="Pandas/NumPy" secondary="Data processing" />
                </ListItem>
              </List>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" gutterBottom color="primary">
                AI/ML
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="VADER/TextBlob" secondary="Sentiment analysis" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="Gensim LDA" secondary="Topic modeling" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="NetworkX" secondary="Knowledge graphs" />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <AutoAwesome fontSize="small" />
                  </ListItemIcon>
                  <ListItemText primary="scikit-learn" secondary="ML models" />
                </ListItem>
              </List>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Contact/Support */}
      <Box mt={6} textAlign="center">
        <Card sx={{ bgcolor: 'primary.main', color: 'white' }}>
          <CardContent sx={{ py: 4 }}>
            <Support sx={{ fontSize: 48, mb: 2 }} />
            <Typography variant="h5" fontWeight={600} gutterBottom>
              Need Help?
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.9, mb: 3 }}>
              Our support team is here to help you get the most out of the platform
            </Typography>
            <Chip
              label="Contact Support"
              sx={{
                bgcolor: 'rgba(255,255,255,0.2)',
                color: 'white',
                fontWeight: 600,
                cursor: 'pointer',
                '&:hover': {
                  bgcolor: 'rgba(255,255,255,0.3)',
                },
              }}
            />
          </CardContent>
        </Card>
      </Box>
    </Container>
  )
}

export default About
