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
  Button,
  IconButton,
  Tooltip,
  Tabs,
  Tab,
  Divider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
} from 'recharts'
import {
  TrendingUp,
  TrendingDown,
  Refresh,
  Download,
  Insights,
  ShowChart,
  Assessment,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { apiService } from '../services/api'

const TrendsInsights = () => {
  const [forecast, setForecast] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [tabValue, setTabValue] = useState(0)
  const [chartType, setChartType] = useState('line')
  const [forecastPeriod, setForecastPeriod] = useState('7')

  useEffect(() => {
    fetchForecast()
  }, [forecastPeriod])

  const fetchForecast = async () => {
    try {
      setLoading(true)
      const data = await apiService.getForecast(forecastPeriod)
      if (data && (data.forecast_dates || data.forecast)) {
        setForecast(data)
        setError(null)
      } else if (data && data.error) {
        // Handle user-friendly error message from backend
        const errorMsg = data.message || data.error
        setError(errorMsg)
      } else {
        setError('Forecast data is not yet available. The predictive analytics are still being processed.')
      }
    } catch (err) {
      console.error('Forecast error:', err)
      // Handle error response with user-friendly message
      if (err.response && err.response.data) {
        const errorData = err.response.data
        const errorMsg = errorData.message || errorData.error || 'Unable to load forecast data at this time.'
        setError(errorMsg)
      } else {
        setError('Unable to load forecast data. Please try again later.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handlePeriodChange = (event) => {
    setForecastPeriod(event.target.value)
  }

  const handleExport = () => {
    if (!forecast) return
    
    const csvContent = [
      'Date,Moving Average,Linear Trend,ARIMA Forecast',
      ...(forecast.forecast_dates || []).map((date, idx) => {
        const ma = forecast.ma_forecast?.[idx] || 0
        const trend = forecast.trend_forecast?.[idx] || 0
        const arima = forecast.arima_forecast?.[idx] || 0
        return `${date},${ma},${trend},${arima}`
      })
    ].join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `forecast_data_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
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

  const chartData = forecast && forecast.forecast_dates
    ? forecast.forecast_dates.map((date, idx) => ({
        date: new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        fullDate: date,
        ma_forecast: forecast.ma_forecast?.[idx] || 0,
        trend_forecast: forecast.trend_forecast?.[idx] || 0,
        arima_forecast: forecast.arima_forecast?.[idx] || 0,
        actual: forecast.actual_sentiment?.[idx] || null,
      }))
    : []

  const getTrendIcon = () => {
    if (!forecast) return null
    const direction = forecast.trend_direction
    if (direction === 'INCREASING') {
      return <TrendingUp color="success" sx={{ fontSize: 32 }} />
    } else if (direction === 'DECREASING') {
      return <TrendingDown color="error" sx={{ fontSize: 32 }} />
    }
    return <ShowChart color="info" sx={{ fontSize: 32 }} />
  }

  const getTrendColor = () => {
    if (!forecast) return 'default'
    const direction = forecast.trend_direction
    if (direction === 'INCREASING') return 'success'
    if (direction === 'DECREASING') return 'error'
    return 'default'
  }

  return (
    <Container maxWidth="xl">
      <Box mb={4} display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="h4" component="h1" gutterBottom fontWeight={700}>
            Trends & Insights
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Predictive insights and sentiment trend forecasting powered by advanced ML models
          </Typography>
        </Box>
        <Box display="flex" gap={2} alignItems="center">
          <FormControl size="small" sx={{ minWidth: 180 }}>
            <InputLabel id="forecast-period-label">Forecast Period</InputLabel>
            <Select
              labelId="forecast-period-label"
              id="forecast-period-select"
              value={forecastPeriod}
              label="Forecast Period"
              onChange={handlePeriodChange}
            >
              <MenuItem value="7">7 Days</MenuItem>
              <MenuItem value="30">30 Days</MenuItem>
              <MenuItem value="months">Months (Last Year)</MenuItem>
              <MenuItem value="years">Years (All Data)</MenuItem>
              <MenuItem value="overall">Overall (All Data)</MenuItem>
            </Select>
          </FormControl>
          <Tooltip title="Refresh Data">
            <IconButton onClick={fetchForecast} color="primary">
              <Refresh />
            </IconButton>
          </Tooltip>
          <Tooltip title="Export Forecast Data">
            <span>
              <IconButton onClick={handleExport} color="primary" disabled={!forecast}>
                <Download />
              </IconButton>
            </span>
          </Tooltip>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {forecast ? (
        <Grid container spacing={3}>
          {/* Key Metrics Cards */}
          <Grid item xs={12} md={4}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Card
                sx={{
                  height: '100%',
                  background: 'linear-gradient(135deg, #5624d015 0%, #5624d005 100%)',
                  border: '1px solid #5624d030',
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 8,
                  },
                }}
              >
                <CardContent>
                  <Box display="flex" alignItems="center" gap={2} mb={2}>
                    {getTrendIcon()}
                    <Box>
                      <Typography variant="h6" gutterBottom fontWeight={600}>
                        Trend Direction
                      </Typography>
                      <Chip
                        label={forecast.trend_direction || 'STABLE'}
                        color={getTrendColor()}
                        sx={{ fontSize: '0.875rem', fontWeight: 600 }}
                      />
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    Overall sentiment trend based on historical data analysis
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>

          <Grid item xs={12} md={4}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              <Card
                sx={{
                  height: '100%',
                  background: 'linear-gradient(135deg, #10b98115 0%, #10b98105 100%)',
                  border: '1px solid #10b98130',
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 8,
                  },
                }}
              >
                <CardContent>
                  <Typography variant="h6" gutterBottom fontWeight={600}>
                    Current Sentiment
                  </Typography>
                  <Typography variant="h3" color="success.main" fontWeight={700}>
                    {forecast.current_sentiment ? (forecast.current_sentiment * 100).toFixed(1) : '0.0'}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Current positive sentiment ratio
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>

          <Grid item xs={12} md={4}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <Card
                sx={{
                  height: '100%',
                  background: 'linear-gradient(135deg, #3b82f615 0%, #3b82f605 100%)',
                  border: '1px solid #3b82f630',
                  transition: 'all 0.3s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 8,
                  },
                }}
              >
                <CardContent>
                  <Typography variant="h6" gutterBottom fontWeight={600}>
                    Forecasted Average
                  </Typography>
                  <Typography variant="h3" color="info.main" fontWeight={700}>
                    {forecast.forecast_avg ? (forecast.forecast_avg * 100).toFixed(1) : '0.0'}%
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Predicted positive sentiment ratio (next 7 days)
                  </Typography>
                </CardContent>
              </Card>
            </motion.div>
          </Grid>

          {/* Forecast Chart */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                  <Box>
                    <Typography variant="h6" gutterBottom fontWeight={600}>
                      Sentiment Trend Forecast
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Multi-model forecasting using Moving Average, Linear Trend, and ARIMA
                    </Typography>
                  </Box>
                  <Box display="flex" gap={1}>
                    <Button
                      size="small"
                      variant={chartType === 'line' ? 'contained' : 'outlined'}
                      onClick={() => setChartType('line')}
                      startIcon={<ShowChart />}
                    >
                      Line
                    </Button>
                    <Button
                      size="small"
                      variant={chartType === 'area' ? 'contained' : 'outlined'}
                      onClick={() => setChartType('area')}
                      startIcon={<Assessment />}
                    >
                      Area
                    </Button>
                  </Box>
                </Box>

                <Box mb={2} display="flex" gap={1} flexWrap="wrap">
                  <Chip
                    label={`Trend: ${forecast.trend_direction || 'STABLE'}`}
                    color={getTrendColor()}
                    sx={{ fontSize: '0.875rem', fontWeight: 600 }}
                  />
                  <Chip
                    label={`Forecast Period: ${
                      forecastPeriod === 'overall' ? 'Overall' :
                      forecastPeriod === 'months' ? 'Last 12 Months' :
                      forecastPeriod === 'years' ? 'All Years' :
                      forecastPeriod === '30' ? '30 Days' :
                      '7 Days'
                    } (${chartData.length} data points)`}
                    variant="outlined"
                    sx={{ fontSize: '0.875rem' }}
                  />
                  {forecast.ma_accuracy && (
                    <Chip
                      label={`MA Accuracy: ${(forecast.ma_accuracy * 100).toFixed(1)}%`}
                      variant="outlined"
                      color="info"
                      sx={{ fontSize: '0.875rem' }}
                    />
                  )}
                </Box>

                <ResponsiveContainer width="100%" height={450}>
                  {chartType === 'line' ? (
                    <LineChart data={chartData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis 
                        dataKey="date" 
                        tick={{ fontSize: 12 }}
                        angle={-45}
                        textAnchor="end"
                        height={80}
                      />
                      <YAxis 
                        tick={{ fontSize: 12 }}
                        domain={[0, 1]}
                        tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                      />
                      <RechartsTooltip
                        formatter={(value) => `${(Number(value) * 100).toFixed(1)}%`}
                        contentStyle={{
                          backgroundColor: 'rgba(255, 255, 255, 0.95)',
                          border: '1px solid #e5e7eb',
                          borderRadius: 8,
                        }}
                      />
                      <Legend />
                      {forecast.ma_forecast && (
                        <Line
                          type="monotone"
                          dataKey="ma_forecast"
                          stroke="#1976d2"
                          strokeWidth={3}
                          dot={{ r: 4 }}
                          name="Moving Average"
                        />
                      )}
                      {forecast.trend_forecast && (
                        <Line
                          type="monotone"
                          dataKey="trend_forecast"
                          stroke="#2e7d32"
                          strokeWidth={3}
                          dot={{ r: 4 }}
                          name="Linear Trend"
                        />
                      )}
                      {forecast.arima_forecast && (
                        <Line
                          type="monotone"
                          dataKey="arima_forecast"
                          stroke="#9c27b0"
                          strokeWidth={3}
                          dot={{ r: 4 }}
                          name="ARIMA"
                        />
                      )}
                      {forecast.actual_sentiment && (
                        <Line
                          type="monotone"
                          dataKey="actual"
                          stroke="#f59e0b"
                          strokeWidth={2}
                          strokeDasharray="5 5"
                          dot={{ r: 3 }}
                          name="Actual (Historical)"
                        />
                      )}
                    </LineChart>
                  ) : (
                    <AreaChart data={chartData}>
                      <defs>
                        <linearGradient id="colorMa" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#1976d2" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#1976d2" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorTrend" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#2e7d32" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#2e7d32" stopOpacity={0}/>
                        </linearGradient>
                        <linearGradient id="colorArima" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#9c27b0" stopOpacity={0.8}/>
                          <stop offset="95%" stopColor="#9c27b0" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis 
                        dataKey="date" 
                        tick={{ fontSize: 12 }}
                        angle={-45}
                        textAnchor="end"
                        height={80}
                      />
                      <YAxis 
                        tick={{ fontSize: 12 }}
                        domain={[0, 1]}
                        tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                      />
                      <RechartsTooltip
                        formatter={(value) => `${(Number(value) * 100).toFixed(1)}%`}
                        contentStyle={{
                          backgroundColor: 'rgba(255, 255, 255, 0.95)',
                          border: '1px solid #e5e7eb',
                          borderRadius: 8,
                        }}
                      />
                      <Legend />
                      {forecast.ma_forecast && (
                        <Area
                          type="monotone"
                          dataKey="ma_forecast"
                          stroke="#1976d2"
                          fillOpacity={1}
                          fill="url(#colorMa)"
                          name="Moving Average"
                        />
                      )}
                      {forecast.trend_forecast && (
                        <Area
                          type="monotone"
                          dataKey="trend_forecast"
                          stroke="#2e7d32"
                          fillOpacity={1}
                          fill="url(#colorTrend)"
                          name="Linear Trend"
                        />
                      )}
                      {forecast.arima_forecast && (
                        <Area
                          type="monotone"
                          dataKey="arima_forecast"
                          stroke="#9c27b0"
                          fillOpacity={1}
                          fill="url(#colorArima)"
                          name="ARIMA"
                        />
                      )}
                    </AreaChart>
                  )}
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>

          {/* Model Comparison */}
          {forecast.ma_forecast && forecast.trend_forecast && forecast.arima_forecast && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom fontWeight={600}>
                    Model Comparison
                  </Typography>
                  <Typography variant="body2" color="text.secondary" mb={3}>
                    Compare forecast accuracy across different predictive models
                  </Typography>
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={[
                      {
                        name: 'Moving Average',
                        value: forecast.ma_forecast?.[forecast.ma_forecast.length - 1] || 0,
                      },
                      {
                        name: 'Linear Trend',
                        value: forecast.trend_forecast?.[forecast.trend_forecast.length - 1] || 0,
                      },
                      {
                        name: 'ARIMA',
                        value: forecast.arima_forecast?.[forecast.arima_forecast.length - 1] || 0,
                      },
                    ]}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                      <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                      <YAxis 
                        tick={{ fontSize: 12 }}
                        domain={[0, 1]}
                        tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
                      />
                      <RechartsTooltip
                        formatter={(value) => `${(Number(value) * 100).toFixed(1)}%`}
                        contentStyle={{
                          backgroundColor: 'rgba(255, 255, 255, 0.95)',
                          border: '1px solid #e5e7eb',
                          borderRadius: 8,
                        }}
                      />
                      <Bar 
                        dataKey="value" 
                        radius={[4, 4, 0, 0]}
                        fill="#5624d0"
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
          )}

          {/* Insights Section */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" gap={2} mb={2}>
                  <Insights color="primary" sx={{ fontSize: 32 }} />
                  <Typography variant="h6" fontWeight={600}>
                    Key Insights
                  </Typography>
                </Box>
                <Box component="ul" sx={{ pl: 2, m: 0 }}>
                  <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {forecast.trend_direction === 'INCREASING' 
                      ? 'Sentiment is trending upward, indicating positive customer feedback growth.'
                      : forecast.trend_direction === 'DECREASING'
                      ? 'Sentiment is trending downward, suggesting areas for improvement.'
                      : 'Sentiment remains stable, maintaining consistent customer feedback levels.'}
                  </Typography>
                  <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    Forecast models predict sentiment changes over the next 7 days based on historical patterns.
                  </Typography>
                  <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    Multiple models (MA, Linear Trend, ARIMA) provide robust predictions through ensemble forecasting.
                  </Typography>
                  <Typography component="li" variant="body2" color="text.secondary">
                    Use these insights to proactively address customer concerns and capitalize on positive trends.
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Recommendations */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" gap={2} mb={2}>
                  <Assessment color="primary" sx={{ fontSize: 32 }} />
                  <Typography variant="h6" fontWeight={600}>
                    Recommendations
                  </Typography>
                </Box>
                <Box component="ul" sx={{ pl: 2, m: 0 }}>
                  {forecast.trend_direction === 'INCREASING' ? (
                    <>
                      <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        Continue current strategies that are driving positive sentiment.
                      </Typography>
                      <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        Leverage positive feedback for marketing and customer testimonials.
                      </Typography>
                      <Typography component="li" variant="body2" color="text.secondary">
                        Monitor for potential saturation points in positive sentiment growth.
                      </Typography>
                    </>
                  ) : forecast.trend_direction === 'DECREASING' ? (
                    <>
                      <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        Investigate root causes of declining sentiment through detailed analysis.
                      </Typography>
                      <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        Implement immediate customer service improvements and feedback loops.
                      </Typography>
                      <Typography component="li" variant="body2" color="text.secondary">
                        Focus on addressing the most common negative feedback themes.
                      </Typography>
                    </>
                  ) : (
                    <>
                      <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        Maintain consistent service quality to preserve current sentiment levels.
                      </Typography>
                      <Typography component="li" variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                        Identify opportunities for incremental improvements.
                      </Typography>
                      <Typography component="li" variant="body2" color="text.secondary">
                        Continue monitoring trends for early detection of changes.
                      </Typography>
                    </>
                  )}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      ) : (
        <Card>
          <CardContent>
            <Box textAlign="center" py={6}>
              <ShowChart sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
              <Typography variant="h6" color="text.secondary" gutterBottom>
                {error ? 'Forecast Data Not Available' : 'Loading Forecast Data...'}
              </Typography>
              {error ? (
                <Box sx={{ maxWidth: 600, mx: 'auto', mt: 2 }}>
                  <Alert severity="info" sx={{ mb: 2 }}>
                    <Typography variant="body1" sx={{ fontWeight: 500, mb: 1 }}>
                      Forecast Data Not Available
                    </Typography>
                    <Typography variant="body2">
                      {error}
                    </Typography>
                  </Alert>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                    Predictive analytics will appear here once the analysis is complete.
                  </Typography>
                </Box>
              ) : (
                <>
                  <Typography variant="body2" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto', mt: 1 }}>
                    Loading forecast data from Milestone 2 output...
                  </Typography>
                  <CircularProgress sx={{ mt: 3 }} />
                </>
              )}
            </Box>
          </CardContent>
        </Card>
      )}
    </Container>
  )
}

export default TrendsInsights
