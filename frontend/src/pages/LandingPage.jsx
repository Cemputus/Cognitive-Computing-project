import React from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Container,
  Box,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  useTheme,
  alpha,
} from '@mui/material'
import {
  Analytics,
  TrendingUp,
  Insights,
  Speed,
  Security,
  Support,
  BarChart,
  SentimentSatisfiedAlt,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { FaShieldAlt, FaRocket } from 'react-icons/fa'
import Navbar from '../components/Navbar'

const LandingPage = () => {
  const navigate = useNavigate()
  const theme = useTheme()

  const features = [
    {
      icon: <Analytics sx={{ fontSize: 40 }} />,
      title: 'Real-Time Analytics',
      description: 'Get instant insights into customer sentiment and feedback trends',
      color: '#1976d2',
    },
    {
      icon: <TrendingUp sx={{ fontSize: 40 }} />,
      title: 'Trend Forecasting',
      description: 'Predict future sentiment trends with advanced ML models',
      color: '#2e7d32',
    },
    {
      icon: <Insights sx={{ fontSize: 40 }} />,
      title: 'Topic Discovery',
      description: 'Automatically identify key themes in customer feedback',
      color: '#ed6c02',
    },
    {
      icon: <Speed sx={{ fontSize: 40 }} />,
      title: 'Lightning Fast',
      description: 'Process thousands of reviews in seconds',
      color: '#9c27b0',
    },
    {
      icon: <Security sx={{ fontSize: 40 }} />,
      title: 'Secure & Private',
      description: 'Your data is protected with enterprise-grade security',
      color: '#d32f2f',
    },
    {
      icon: <Support sx={{ fontSize: 40 }} />,
      title: '24/7 Support',
      description: 'Get help whenever you need it with our support team',
      color: '#0288d1',
    },
  ]

  const stats = [
    { number: '85%', label: 'Accuracy', icon: <BarChart /> },
    { number: '5K+', label: 'Reviews Analyzed', icon: <SentimentSatisfiedAlt /> },
    { number: '100+', label: 'Businesses', icon: <FaRocket /> },
    { number: '24/7', label: 'Available', icon: <FaShieldAlt /> },
  ]

  return (
    <>
      <Navbar />
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default', pt: 8 }}>
        {/* Hero Section */}
        <Box
        sx={{
          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
          color: 'white',
          py: 12,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'url("data:image/svg+xml,%3Csvg width=\'60\' height=\'60\' viewBox=\'0 0 60 60\' xmlns=\'http://www.w3.org/2000/svg\'%3E%3Cg fill=\'none\' fill-rule=\'evenodd\'%3E%3Cg fill=\'%23ffffff\' fill-opacity=\'0.05\'%3E%3Cpath d=\'M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z\'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")',
            opacity: 0.3,
          }}
        />
        <Container maxWidth="lg">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Typography
              variant="h1"
              component="h1"
              sx={{
                fontSize: { xs: '2.5rem', md: '4rem' },
                fontWeight: 800,
                mb: 2,
                textAlign: 'center',
              }}
            >
              CENAnalytics
              <br />
              <Box component="span" sx={{ color: alpha('#fff', 0.9) }}>
                Business Intelligence Made Simple
              </Box>
            </Typography>
            <Typography
              variant="h5"
              sx={{
                textAlign: 'center',
                mb: 4,
                color: alpha('#fff', 0.9),
                maxWidth: '700px',
                mx: 'auto',
              }}
            >
              Understand your customers better with AI-powered sentiment analysis
              and predictive insights for small businesses in Kampala
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, flexWrap: 'wrap' }}>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/login')}
                  sx={{
                    bgcolor: 'white',
                    color: theme.palette.primary.main,
                    px: 4,
                    py: 1.5,
                    fontSize: '1.1rem',
                    fontWeight: 600,
                    '&:hover': {
                      bgcolor: alpha('#fff', 0.9),
                      transform: 'translateY(-2px)',
                      boxShadow: 6,
                    },
                    transition: 'all 0.3s',
                  }}
                >
                  Get Started
                </Button>
              </motion.div>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="outlined"
                  size="large"
                  onClick={() => navigate('/about')}
                  sx={{
                    borderColor: 'white',
                    color: 'white',
                    px: 4,
                    py: 1.5,
                    fontSize: '1.1rem',
                    fontWeight: 600,
                    '&:hover': {
                      borderColor: alpha('#fff', 0.9),
                      bgcolor: alpha('#fff', 0.1),
                    },
                  }}
                >
                  Learn More
                </Button>
              </motion.div>
            </Box>
          </motion.div>
        </Container>
      </Box>

      {/* Stats Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Grid container spacing={4}>
          {stats.map((stat, index) => (
            <Grid item xs={6} md={3} key={index}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card
                  sx={{
                    textAlign: 'center',
                    p: 3,
                    height: '100%',
                    background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.1)} 0%, ${alpha(theme.palette.secondary.main, 0.1)} 100%)`,
                    border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                    transition: 'all 0.3s',
                    '&:hover': {
                      transform: 'translateY(-8px)',
                      boxShadow: 6,
                    },
                  }}
                >
                  <CardContent>
                    <Box
                      sx={{
                        fontSize: '2.5rem',
                        fontWeight: 800,
                        color: theme.palette.primary.main,
                        mb: 1,
                      }}
                    >
                      {stat.number}
                    </Box>
                    <Typography variant="h6" color="text.secondary">
                      {stat.label}
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* Features Section */}
      <Box sx={{ bgcolor: alpha(theme.palette.primary.main, 0.02), py: 10 }}>
        <Container maxWidth="lg">
          <Typography
            variant="h2"
            component="h2"
            sx={{
              textAlign: 'center',
              fontWeight: 700,
              mb: 2,
              color: theme.palette.text.primary,
            }}
          >
            Powerful Features
          </Typography>
          <Typography
            variant="h6"
            sx={{
              textAlign: 'center',
              color: 'text.secondary',
              mb: 6,
              maxWidth: '600px',
              mx: 'auto',
            }}
          >
            Everything you need to understand your customers and grow your business
          </Typography>
          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} md={4} key={index}>
                <motion.div
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ y: -8 }}
                >
                  <Card
                    sx={{
                      height: '100%',
                      p: 3,
                      border: `1px solid ${alpha(feature.color, 0.2)}`,
                      transition: 'all 0.3s',
                      '&:hover': {
                        transform: 'translateY(-8px)',
                        boxShadow: 8,
                        borderColor: feature.color,
                      },
                    }}
                  >
                    <Box
                      sx={{
                        color: feature.color,
                        mb: 2,
                        display: 'flex',
                        alignItems: 'center',
                      }}
                    >
                      {feature.icon}
                    </Box>
                    <Typography variant="h5" sx={{ fontWeight: 600, mb: 1 }}>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </Card>
                </motion.div>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box
        sx={{
          background: `linear-gradient(135deg, ${theme.palette.primary.dark} 0%, ${theme.palette.secondary.dark} 100%)`,
          color: 'white',
          py: 10,
        }}
      >
        <Container maxWidth="md">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6 }}
          >
            <Typography
              variant="h3"
              component="h2"
              sx={{ textAlign: 'center', fontWeight: 700, mb: 2 }}
            >
              Ready to Get Started?
            </Typography>
            <Typography
              variant="h6"
              sx={{
                textAlign: 'center',
                mb: 4,
                color: alpha('#fff', 0.9),
              }}
            >
              Join hundreds of businesses using our platform to understand their customers
            </Typography>
            <Box sx={{ display: 'flex', justifyContent: 'center' }}>
              <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={() => navigate('/login')}
                  sx={{
                    bgcolor: 'white',
                    color: theme.palette.primary.main,
                    px: 6,
                    py: 2,
                    fontSize: '1.2rem',
                    fontWeight: 600,
                    '&:hover': {
                      bgcolor: alpha('#fff', 0.9),
                      transform: 'translateY(-2px)',
                      boxShadow: 8,
                    },
                  }}
                >
                  Start Free Trial
                </Button>
              </motion.div>
            </Box>
          </motion.div>
        </Container>
      </Box>
      </Box>
    </>
  )
}

export default LandingPage



