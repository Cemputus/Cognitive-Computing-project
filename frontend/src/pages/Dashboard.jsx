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
  Tabs,
  Tab,
  FormControl,
  Select,
  MenuItem,
  InputLabel,
  Chip,
  IconButton,
  Tooltip,
  Snackbar,
  TextField,
} from '@mui/material'
import {
  TrendingUp,
  TrendingDown,
  SentimentSatisfiedAlt,
  SentimentNeutral,
  LocationOn,
  Topic as TopicIcon,
  Public,
  Refresh,
  Download,
  FilterList,
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
  LineChart,
  Line,
  Area,
  AreaChart,
} from 'recharts'
import { apiService } from '../services/api'
import { motion } from 'framer-motion'
import { useNotifications } from '../contexts/NotificationContext'

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [locationData, setLocationData] = useState(null)
  const [platformData, setPlatformData] = useState(null)
  const [topicData, setTopicData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Filter states for each visualization
  const [locationFilter, setLocationFilter] = useState('all')
  const [platformFilter, setPlatformFilter] = useState('all')
  const [topicFilter, setTopicFilter] = useState('all')
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' })
  const [searchQuery, setSearchQuery] = useState('')
  const { fetchNotifications } = useNotifications()

  const COLORS = {
    positive: '#10b981',
    negative: '#ef4444',
    neutral: '#6b7280',
  }

  useEffect(() => {
    fetchAllData()
  }, [])

  useEffect(() => {
    fetchLocationData()
  }, [locationFilter])

  useEffect(() => {
    fetchPlatformData()
  }, [platformFilter])

  useEffect(() => {
    fetchTopicData()
  }, [topicFilter])

  const fetchAllData = async () => {
    try {
      setLoading(true)
      const [statsData, locData, platData, topData] = await Promise.all([
        apiService.getDashboardStats(),
        apiService.getLocationSentiment('all'),
        apiService.getPlatformSentiment('all'),
        apiService.getTopicSentiment('all'),
      ])
      setStats(statsData)
      setLocationData(locData)
      setPlatformData(platData)
      setTopicData(topData)
      setError(null)
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const fetchLocationData = async () => {
    try {
      const data = await apiService.getLocationSentiment(locationFilter)
      console.log('Location data:', data)
      console.log('Location filter:', locationFilter)
      setLocationData(data)
    } catch (err) {
      console.error('Error fetching location data:', err)
    }
  }

  const fetchPlatformData = async () => {
    try {
      const data = await apiService.getPlatformSentiment(platformFilter)
      setPlatformData(data)
    } catch (err) {
      console.error('Error fetching platform data:', err)
    }
  }

  const fetchTopicData = async () => {
    try {
      const data = await apiService.getTopicSentiment(topicFilter)
      setTopicData(data)
    } catch (err) {
      console.error('Error fetching topic data:', err)
    }
  }

  const handleRefresh = () => {
    fetchAllData()
    fetchLocationData()
    fetchPlatformData()
    fetchTopicData()
  }

  const handleExportReport = async () => {
    try {
      const response = await apiService.exportReport('dashboard')
      
      // Refresh notifications to get new ones
      await fetchNotifications()
      
      // Show success message
      setSnackbar({
        open: true,
        message: 'Report exported successfully! A copy has been sent to ensubuga019@gmail.com',
        severity: 'success'
      })
    } catch (err) {
      setSnackbar({
        open: true,
        message: 'Failed to export report: ' + (err.message || 'Unknown error'),
        severity: 'error'
      })
    }
  }

  if (loading && !stats) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    )
  }

  if (error && !stats) {
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
      color: '#5624d0',
    },
    {
      title: 'Positive Sentiment',
      value: `${((stats?.positive_ratio || 0) * 100).toFixed(1)}%`,
      change: '+5%',
      icon: <TrendingUp />,
      color: '#10b981',
    },
    {
      title: 'Negative Sentiment',
      value: `${((stats?.negative_ratio || 0) * 100).toFixed(1)}%`,
      change: '-3%',
      icon: <TrendingDown />,
      color: '#ef4444',
    },
    {
      title: 'Key Topics',
      value: stats?.topic_count || 0,
      change: '→',
      icon: <TopicIcon />,
      color: '#f59e0b',
    },
  ]

  // Prepare location chart data with percentage distribution
  // When filter is applied, show percentage of all filtered sentiment from each location
  const locationChartData = (locationData?.locations || []).slice(0, 10).map((loc) => {
    if (locationFilter !== 'all') {
      // Use snake_case from backend response
      const pctKey = `pct_of_all_${locationFilter}`
      const value = loc[pctKey] !== undefined ? Number(loc[pctKey]) : 0
      return {
        name: loc.location || 'Unknown',
        Value: value,
        Total: Number(loc.total) || 0,
      }
    }
    return {
      name: loc.location || 'Unknown',
      Positive: Number(loc.positive_pct) || 0,
      Negative: Number(loc.negative_pct) || 0,
      Neutral: Number(loc.neutral_pct) || 0,
      Total: Number(loc.total) || 0,
      pctOfAllPositive: Number(loc.pct_of_all_positive) || 0,
      pctOfAllNegative: Number(loc.pct_of_all_negative) || 0,
      pctOfAllNeutral: Number(loc.pct_of_all_neutral) || 0,
    }
  }).filter(item => {
    if (searchQuery) {
      return item.name.toLowerCase().includes(searchQuery.toLowerCase())
    }
    return true
  })
  
  console.log('Location chart data prepared:', locationChartData.length, 'items, filter:', locationFilter)

  // Prepare platform chart data with percentage distribution
  // When filter is applied, show percentage of all filtered sentiment from each platform
  const platformChartData = (platformData?.platforms || []).map((plat) => {
    if (platformFilter !== 'all') {
      // Use snake_case from backend response
      const pctKey = `pct_of_all_${platformFilter}`
      const value = plat[pctKey] !== undefined ? Number(plat[pctKey]) : 0
      return {
        name: plat.platform || 'Unknown',
        Value: value,
        Total: Number(plat.total) || 0,
      }
    }
    return {
      name: plat.platform || 'Unknown',
      Positive: Number(plat.positive_pct) || 0,
      Negative: Number(plat.negative_pct) || 0,
      Neutral: Number(plat.neutral_pct) || 0,
      Total: Number(plat.total) || 0,
      pctOfAllPositive: Number(plat.pct_of_all_positive) || 0,
      pctOfAllNegative: Number(plat.pct_of_all_negative) || 0,
      pctOfAllNeutral: Number(plat.pct_of_all_neutral) || 0,
    }
  }).filter(item => {
    if (searchQuery) {
      return item.name.toLowerCase().includes(searchQuery.toLowerCase())
    }
    return true
  })

  // Prepare topic chart data with meaningful names
  // When filter is applied, show percentage of all filtered sentiment from each topic
  const topicChartData = (topicData?.topics || []).map((topic) => {
    const topicName = topic.topic_name || `Topic ${topic.topic}`
    if (topicFilter !== 'all') {
      // Use snake_case from backend response
      const pctKey = `pct_of_all_${topicFilter}`
      const value = topic[pctKey] !== undefined ? Number(topic[pctKey]) : 0
      return {
        name: topicName,
        Value: value,
        Total: Number(topic.total) || 0,
      }
    }
    return {
      name: topicName,
      Positive: Number(topic.positive_pct) || 0,
      Negative: Number(topic.negative_pct) || 0,
      Neutral: Number(topic.neutral_pct) || 0,
      Total: Number(topic.total) || 0,
      pctOfAllPositive: Number(topic.pct_of_all_positive) || 0,
      pctOfAllNegative: Number(topic.pct_of_all_negative) || 0,
      pctOfAllNeutral: Number(topic.pct_of_all_neutral) || 0,
    }
  }).filter(item => {
    if (searchQuery) {
      return item.name.toLowerCase().includes(searchQuery.toLowerCase())
    }
    return true
  })

  // Location pie chart data
  const locationPieData = locationData?.locations?.slice(0, 5).map((loc) => ({
    name: loc.location,
    value: loc.total,
  })) || []

  // Platform pie chart data
  const platformPieData = platformData?.platforms?.map((plat) => ({
    name: plat.platform,
    value: plat.total,
  })) || []

  return (
    <Container maxWidth="xl">
      {/* Header */}
      <Box mb={4} display="flex" justifyContent="space-between" alignItems="center">
        <Box>
          <Typography variant="h4" component="h1" gutterBottom fontWeight={700}>
            Analytics Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Comprehensive business intelligence insights and sentiment analysis
          </Typography>
        </Box>
        <Box display="flex" gap={1}>
          <Tooltip title="Refresh Data">
            <IconButton onClick={handleRefresh} color="primary">
              <Refresh />
            </IconButton>
          </Tooltip>
          <Tooltip title="Export Report">
            <IconButton onClick={handleExportReport} color="primary">
              <Download />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} mb={4}>
        {statCards.map((stat, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
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
                      <Typography color="text.secondary" gutterBottom variant="body2" fontWeight={500}>
                        {stat.title}
                      </Typography>
                      <Typography variant="h4" component="div" fontWeight={700} color={stat.color}>
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
            </motion.div>
          </Grid>
        ))}
      </Grid>

      {/* Location-Based Sentiment Analysis */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
            <Box display="flex" alignItems="center" gap={2}>
              <LocationOn color="primary" sx={{ fontSize: 32 }} />
              <Box>
                <Typography variant="h5" fontWeight={600}>
                  Sentiment by Location
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Analyze customer sentiment across different locations
                </Typography>
              </Box>
            </Box>
            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel>Filter Sentiment</InputLabel>
              <Select
                value={locationFilter}
                label="Filter Sentiment"
                onChange={(e) => setLocationFilter(e.target.value)}
                startAdornment={<FilterList sx={{ mr: 1, fontSize: 18 }} />}
              >
                <MenuItem value="all">All Sentiments</MenuItem>
                <MenuItem value="positive">Positive Only</MenuItem>
                <MenuItem value="negative">Negative Only</MenuItem>
                <MenuItem value="neutral">Neutral Only</MenuItem>
              </Select>
            </FormControl>
          </Box>

          {locationChartData.length === 0 ? (
            <Box p={4} textAlign="center">
              <Typography variant="body1" color="text.secondary">
                No data available for the selected filter. Try selecting a different sentiment or check back later.
              </Typography>
            </Box>
          ) : (
          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Box height={400}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={locationChartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis
                      dataKey="name"
                      angle={-45}
                      textAnchor="end"
                      height={100}
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis tick={{ fontSize: 12 }} />
                    <RechartsTooltip
                      contentStyle={{
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        border: '1px solid #e5e7eb',
                        borderRadius: 8,
                      }}
                      formatter={(value, name, props) => {
                        if (locationFilter !== 'all') {
                          return [`${typeof value === 'number' ? value.toFixed(1) : value}% of all ${locationFilter} reviews`, name]
                        }
                        return [typeof value === 'number' ? value.toFixed(1) + '%' : value + '%', name]
                      }}
                    />
                    <Legend />
                    {locationFilter === 'all' ? (
                      <>
                        <Bar dataKey="Positive" fill={COLORS.positive} radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Negative" fill={COLORS.negative} radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Neutral" fill={COLORS.neutral} radius={[4, 4, 0, 0]} />
                      </>
                    ) : (
                      <Bar 
                        dataKey="Value" 
                        fill={COLORS[locationFilter]} 
                        radius={[4, 4, 0, 0]}
                        name={`% of All ${locationFilter.charAt(0).toUpperCase() + locationFilter.slice(1)}`}
                      />
                    )}
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box height={400}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={locationPieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {locationPieData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={['#5624d0', '#3b82f6', '#10b981', '#f59e0b', '#ef4444'][index % 5]} />
                      ))}
                    </Pie>
                    <RechartsTooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            </Grid>
          </Grid>
          )}

          {locationData?.summary && (
            <Box mt={2}>
              <Box display="flex" gap={2} flexWrap="wrap" mb={1}>
                <Chip
                  label={`Total Locations: ${locationData.summary.total_locations}`}
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label={`Total Reviews: ${locationData.summary.total_reviews.toLocaleString()}`}
                  color="primary"
                  variant="outlined"
                />
                {locationFilter !== 'all' && (
                  <Chip
                    label={`Filter: ${locationFilter}`}
                    color="secondary"
                    variant="outlined"
                  />
                )}
              </Box>
              {locationFilter !== 'all' && locationData.summary[`total_${locationFilter}`] > 0 && (
                <Typography variant="body2" color="text.secondary" mt={1}>
                  <strong>Distribution:</strong> Showing what percentage of all {locationFilter} reviews come from each location.
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Platform-Based Sentiment Analysis */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
            <Box display="flex" alignItems="center" gap={2}>
              <Public color="primary" sx={{ fontSize: 32 }} />
              <Box>
                <Typography variant="h5" fontWeight={600}>
                  Sentiment by Platform
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Compare sentiment across social media platforms and sources
                </Typography>
              </Box>
            </Box>
            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel>Filter Sentiment</InputLabel>
              <Select
                value={platformFilter}
                label="Filter Sentiment"
                onChange={(e) => setPlatformFilter(e.target.value)}
                startAdornment={<FilterList sx={{ mr: 1, fontSize: 18 }} />}
              >
                <MenuItem value="all">All Sentiments</MenuItem>
                <MenuItem value="positive">Positive Only</MenuItem>
                <MenuItem value="negative">Negative Only</MenuItem>
                <MenuItem value="neutral">Neutral Only</MenuItem>
              </Select>
            </FormControl>
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Box height={400}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={platformChartData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="name" tick={{ fontSize: 12 }} angle={-45} textAnchor="end" height={100} />
                    <YAxis tick={{ fontSize: 12 }} />
                    <RechartsTooltip
                      contentStyle={{
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        border: '1px solid #e5e7eb',
                        borderRadius: 8,
                      }}
                      formatter={(value, name, props) => {
                        if (platformFilter !== 'all') {
                          return [`${typeof value === 'number' ? value.toFixed(1) : value}% of all ${platformFilter} reviews`, name]
                        }
                        return [typeof value === 'number' ? value.toFixed(1) + '%' : value + '%', name]
                      }}
                    />
                    <Legend />
                    {platformFilter === 'all' ? (
                      <>
                        <Bar dataKey="Positive" fill={COLORS.positive} radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Negative" fill={COLORS.negative} radius={[4, 4, 0, 0]} />
                        <Bar dataKey="Neutral" fill={COLORS.neutral} radius={[4, 4, 0, 0]} />
                      </>
                    ) : (
                      <Bar 
                        dataKey="Value" 
                        fill={COLORS[platformFilter]} 
                        radius={[4, 4, 0, 0]}
                        name={`% of All ${platformFilter.charAt(0).toUpperCase() + platformFilter.slice(1)}`}
                      />
                    )}
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box height={400}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={platformPieData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      outerRadius={120}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {platformPieData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={['#5624d0', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'][index % 6]}
                        />
                      ))}
                    </Pie>
                    <RechartsTooltip />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            </Grid>
          </Grid>

          {platformData?.summary && (
            <Box mt={2}>
              <Box display="flex" gap={2} flexWrap="wrap" mb={1}>
                <Chip
                  label={`Total Platforms: ${platformData.summary.total_platforms}`}
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label={`Total Reviews: ${platformData.summary.total_reviews.toLocaleString()}`}
                  color="primary"
                  variant="outlined"
                />
                {platformFilter !== 'all' && (
                  <Chip
                    label={`Filter: ${platformFilter}`}
                    color="secondary"
                    variant="outlined"
                  />
                )}
              </Box>
              {platformFilter !== 'all' && platformData.summary[`total_${platformFilter}`] > 0 && (
                <Typography variant="body2" color="text.secondary" mt={1}>
                  <strong>Distribution:</strong> Showing what percentage of all {platformFilter} reviews come from each platform.
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>

      {/* Topic-Based Sentiment Analysis */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
            <Box display="flex" alignItems="center" gap={2}>
              <TopicIcon color="primary" sx={{ fontSize: 32 }} />
              <Box>
                <Typography variant="h5" fontWeight={600}>
                  Sentiment by Topic
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Analyze sentiment distribution across different discussion topics
                </Typography>
              </Box>
            </Box>
            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel>Filter Sentiment</InputLabel>
              <Select
                value={topicFilter}
                label="Filter Sentiment"
                onChange={(e) => setTopicFilter(e.target.value)}
                startAdornment={<FilterList sx={{ mr: 1, fontSize: 18 }} />}
              >
                <MenuItem value="all">All Sentiments</MenuItem>
                <MenuItem value="positive">Positive Only</MenuItem>
                <MenuItem value="negative">Negative Only</MenuItem>
                <MenuItem value="neutral">Neutral Only</MenuItem>
              </Select>
            </FormControl>
          </Box>

          <Box height={400}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topicChartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis type="number" tick={{ fontSize: 12 }} />
                <YAxis dataKey="name" type="category" tick={{ fontSize: 12 }} width={100} />
                <RechartsTooltip
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    border: '1px solid #e5e7eb',
                    borderRadius: 8,
                  }}
                  formatter={(value, name, props) => {
                    if (topicFilter !== 'all') {
                      return [`${typeof value === 'number' ? value.toFixed(1) : value}% of all ${topicFilter} reviews`, name]
                    }
                    return [typeof value === 'number' ? value.toFixed(1) + '%' : value + '%', name]
                  }}
                />
                <Legend />
                {topicFilter === 'all' ? (
                  <>
                    <Bar dataKey="Positive" fill={COLORS.positive} radius={[0, 4, 4, 0]} />
                    <Bar dataKey="Negative" fill={COLORS.negative} radius={[0, 4, 4, 0]} />
                    <Bar dataKey="Neutral" fill={COLORS.neutral} radius={[0, 4, 4, 0]} />
                  </>
                ) : (
                  <Bar 
                    dataKey="Value" 
                    fill={COLORS[topicFilter]} 
                    radius={[0, 4, 4, 0]}
                    name={`% of All ${topicFilter.charAt(0).toUpperCase() + topicFilter.slice(1)}`}
                  />
                )}
              </BarChart>
            </ResponsiveContainer>
          </Box>

          {topicData?.summary && (
            <Box mt={2}>
              <Box display="flex" gap={2} flexWrap="wrap" mb={1}>
                <Chip
                  label={`Total Topics: ${topicData.summary.total_topics}`}
                  color="primary"
                  variant="outlined"
                />
                <Chip
                  label={`Total Reviews: ${topicData.summary.total_reviews.toLocaleString()}`}
                  color="primary"
                  variant="outlined"
                />
                {topicFilter !== 'all' && (
                  <Chip
                    label={`Filter: ${topicFilter}`}
                    color="secondary"
                    variant="outlined"
                  />
                )}
              </Box>
              {topicFilter !== 'all' && topicData.summary[`total_${topicFilter}`] > 0 && (
                <Typography variant="body2" color="text.secondary" mt={1}>
                  <strong>Distribution:</strong> Showing what percentage of all {topicFilter} reviews come from each topic.
                </Typography>
              )}
            </Box>
          )}
        </CardContent>
      </Card>
    </Container>
  )
}

export default Dashboard
