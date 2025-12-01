import React, { useEffect, useState } from 'react'
import {
  Container,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Grid,
  Chip,
} from '@mui/material'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { apiService } from '../services/api'

const TrendsInsights = () => {
  const [forecast, setForecast] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchForecast = async () => {
      try {
        const data = await apiService.getForecast()
        setForecast(data)
      } catch (err) {
        setError(err.message || 'Failed to load forecast data')
      } finally {
        setLoading(false)
      }
    }
    fetchForecast()
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

  const chartData = forecast
    ? forecast.forecast_dates.map((date, idx) => ({
        date: new Date(date).toLocaleDateString(),
        ma_forecast: forecast.ma_forecast[idx],
        trend_forecast: forecast.trend_forecast?.[idx],
        arima_forecast: forecast.arima_forecast?.[idx],
      }))
    : []

  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight={600}>
          Trends & Insights
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Predictive insights and sentiment trend forecasting
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {forecast && (
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Sentiment Trend Forecast
                </Typography>
                <Box mb={2}>
                  <Chip
                    label={`Trend: ${forecast.trend_direction}`}
                    color={
                      forecast.trend_direction === 'INCREASING'
                        ? 'success'
                        : forecast.trend_direction === 'DECREASING'
                        ? 'error'
                        : 'default'
                    }
                    sx={{ fontSize: '1rem', fontWeight: 600 }}
                  />
                </Box>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line
                      type="monotone"
                      dataKey="ma_forecast"
                      stroke="#1976d2"
                      strokeWidth={2}
                      name="Moving Average"
                    />
                    {forecast.trend_forecast && (
                      <Line
                        type="monotone"
                        dataKey="trend_forecast"
                        stroke="#2e7d32"
                        strokeWidth={2}
                        name="Linear Trend"
                      />
                    )}
                    {forecast.arima_forecast && (
                      <Line
                        type="monotone"
                        dataKey="arima_forecast"
                        stroke="#9c27b0"
                        strokeWidth={2}
                        name="ARIMA"
                      />
                    )}
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Current Status
                </Typography>
                <Typography variant="h4" color="primary">
                  {(forecast.current_sentiment * 100).toFixed(1)}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Current positive sentiment ratio
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Forecasted Average
                </Typography>
                <Typography variant="h4" color="secondary">
                  {(forecast.forecast_avg * 100).toFixed(1)}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Predicted positive sentiment ratio (next 7 days)
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Container>
  )
}

export default TrendsInsights


