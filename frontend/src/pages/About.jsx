import React from 'react'
import { Container, Card, CardContent, Typography, Box, Grid } from '@mui/material'

const About = () => {
  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight={600}>
          About
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom fontWeight={600}>
                Small Business Intelligence Analyst
              </Typography>
              <Typography variant="body1" paragraph>
                A cognitive computing system designed to help small businesses in Kampala, Uganda
                understand customer sentiment, identify market trends, and make data-driven decisions.
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Features
              </Typography>
              <Typography variant="body2" component="ul">
                <li>Sentiment Analysis</li>
                <li>Topic Modeling</li>
                <li>Trend Forecasting</li>
                <li>Knowledge Graphs</li>
                <li>Predictive Analytics</li>
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Cognitive Pillars
              </Typography>
              <Typography variant="body2" component="ul">
                <li>Understand: NLP and sentiment analysis</li>
                <li>Reason: Knowledge graphs and ML models</li>
                <li>Learn: Active feedback and model updates</li>
                <li>Interact: Modern React interface</li>
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}

export default About


