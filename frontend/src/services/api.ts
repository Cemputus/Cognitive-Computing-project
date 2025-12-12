import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral'
  compound: number
  pos: number
  neu: number
  neg: number
  text: string
}

export interface TopicResult {
  topic_id: number
  topic_words: Array<{ word: string; weight: number }>
  review_count: number
}

export interface ForecastResult {
  current_sentiment: number
  forecast_avg: number
  trend_direction: 'INCREASING' | 'DECREASING' | 'STABLE'
  forecast_dates: string[]
  ma_forecast: number[]
  trend_forecast?: number[]
  arima_forecast?: number[]
}

export const apiService = {
  // Analyze sentiment for a single text
  analyzeSentiment: async (text: string): Promise<SentimentResult> => {
    const response = await api.post('/sentiment/analyze', { text })
    return response.data
  },

  // Batch analyze sentiment
  batchAnalyzeSentiment: async (
    texts: string[]
  ): Promise<SentimentResult[]> => {
    const response = await api.post('/sentiment/batch', { texts })
    return response.data
  },

  // Get topics
  getTopics: async (): Promise<TopicResult[]> => {
    const response = await api.get('/topics')
    return response.data
  },

  // Get forecast
  getForecast: async (): Promise<ForecastResult> => {
    const response = await api.get('/forecast')
    return response.data
  },

  // Get dashboard stats
  getDashboardStats: async () => {
    const response = await api.get('/dashboard/stats')
    return response.data
  },
}

export default api
















const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral'
  compound: number
  pos: number
  neu: number
  neg: number
  text: string
}

export interface TopicResult {
  topic_id: number
  topic_words: Array<{ word: string; weight: number }>
  review_count: number
}

export interface ForecastResult {
  current_sentiment: number
  forecast_avg: number
  trend_direction: 'INCREASING' | 'DECREASING' | 'STABLE'
  forecast_dates: string[]
  ma_forecast: number[]
  trend_forecast?: number[]
  arima_forecast?: number[]
}

export const apiService = {
  // Analyze sentiment for a single text
  analyzeSentiment: async (text: string): Promise<SentimentResult> => {
    const response = await api.post('/sentiment/analyze', { text })
    return response.data
  },

  // Batch analyze sentiment
  batchAnalyzeSentiment: async (
    texts: string[]
  ): Promise<SentimentResult[]> => {
    const response = await api.post('/sentiment/batch', { texts })
    return response.data
  },

  // Get topics
  getTopics: async (): Promise<TopicResult[]> => {
    const response = await api.get('/topics')
    return response.data
  },

  // Get forecast
  getForecast: async (): Promise<ForecastResult> => {
    const response = await api.get('/forecast')
    return response.data
  },

  // Get dashboard stats
  getDashboardStats: async () => {
    const response = await api.get('/dashboard/stats')
    return response.data
  },
}

export default api



















