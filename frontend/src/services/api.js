import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const apiService = {
  // Analyze sentiment for a single text
  analyzeSentiment: async (text) => {
    const response = await api.post('/sentiment/analyze', { text })
    return response.data
  },

  // Batch analyze sentiment
  batchAnalyzeSentiment: async (texts) => {
    const response = await api.post('/sentiment/batch', { texts })
    return response.data
  },

  // Get topics
  getTopics: async () => {
    const response = await api.get('/topics')
    return response.data
  },

  // Get forecast
  getForecast: async () => {
    const response = await api.get('/forecast')
    return response.data
  },

  // Get dashboard stats
  getDashboardStats: async () => {
    const response = await api.get('/dashboard/stats')
    return response.data
  },

  // Advanced Analytics
  getLocationSentiment: async (sentimentFilter = 'all') => {
    const response = await api.get(`/analytics/location-sentiment?sentiment=${sentimentFilter}`)
    return response.data
  },

  getPlatformSentiment: async (sentimentFilter = 'all') => {
    const response = await api.get(`/analytics/platform-sentiment?sentiment=${sentimentFilter}`)
    return response.data
  },

  getTopicSentiment: async (sentimentFilter = 'all') => {
    const response = await api.get(`/analytics/topic-sentiment?sentiment=${sentimentFilter}`)
    return response.data
  },

  // Export report
  exportReport: async (reportType = 'dashboard') => {
    const response = await api.post('/export/report', { type: reportType })
    return response.data
  },

  // Contact admin
  contactAdmin: async (data) => {
    const response = await api.post('/contact-admin', data)
    return response.data
  },

  // Get notifications
  getNotifications: async () => {
    const response = await api.get('/notifications')
    return response.data
  },

  // Mark notification as read
  markNotificationRead: async (notificationId) => {
    const response = await api.post('/notifications/mark-read', { id: notificationId })
    return response.data
  },
}

export default api



