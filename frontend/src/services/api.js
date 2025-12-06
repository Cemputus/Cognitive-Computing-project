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

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
      // Network error - backend might be down
      console.error('Network Error: Backend server is not reachable')
      console.error('Make sure the backend is running on http://localhost:5000')
      error.message = 'Cannot connect to server. Please ensure the backend is running on http://localhost:5000'
    } else if (error.response) {
      // Server responded with error status
      if (error.response.status === 401) {
        // Unauthorized - token expired or invalid
        console.error('Authentication Error: Token expired or invalid')
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        error.message = 'Session expired. Please login again.'
        // Redirect to login if not already there
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      } else if (error.response.status === 404) {
        error.message = 'API endpoint not found'
      } else if (error.response.status === 500) {
        error.message = 'Server error: ' + (error.response.data?.error || 'Internal server error')
      } else {
        error.message = error.response.data?.error || error.message || 'Request failed'
      }
    } else if (error.request) {
      // Request was made but no response received
      error.message = 'No response from server. Please check if the backend is running.'
    }
    return Promise.reject(error)
  }
)

export const apiService = {
  // Analyze sentiment for a single text
  analyzeSentiment: async (text, method = 'ensemble') => {
    const response = await api.post('/sentiment/analyze', { text, method })
    return response.data
  },

  // Batch analyze sentiment
  batchAnalyzeSentiment: async (texts) => {
    const response = await api.post('/sentiment/batch', { texts })
    return response.data
  },

  // Get topics
  getTopics: async () => {
    try {
      const response = await api.get('/topics')
      // Handle both array and object responses
      if (Array.isArray(response.data)) {
        // Direct array response - empty array means no topics loaded
        if (response.data.length > 0) {
          return response.data
        } else {
          // Empty array - return error object so component can display it
          return { 
            topics: [], 
            error: 'No topics available',
            message: 'The topic model file exists but no topics could be extracted. Please ensure Milestone 2 notebook has been run successfully to regenerate the model.'
          }
        }
      } else if (response.data && typeof response.data === 'object') {
        // Object response - could have topics array or error
        if (Array.isArray(response.data.topics)) {
          if (response.data.topics.length > 0) {
            return response.data.topics // Return array directly
          } else {
            // Empty topics array - return error object so component can display it
            return { 
              topics: [], 
              error: response.data.error || response.data.message || 'No topics available',
              message: response.data.message || response.data.error
            }
          }
        } else if (response.data.error) {
          // Error object without topics array
          return { 
            topics: [], 
            error: response.data.error,
            message: response.data.message || response.data.error
          }
        } else {
          // Unknown structure - return as is
          return response.data
        }
      }
      return { topics: [], error: 'Unknown response format' }
    } catch (error) {
      // Re-throw network/HTTP errors
      throw error
    }
  },

  // Get forecast
  getForecast: async (period = '7') => {
    const response = await api.get(`/forecast?period=${period}`)
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