import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Navbar from './components/Navbar'
import LandingPage from './pages/LandingPage'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import SentimentAnalysis from './pages/SentimentAnalysis'
import TopicAnalysis from './pages/TopicAnalysis'
import TrendsInsights from './pages/TrendsInsights'
import About from './pages/About'

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth()
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

const AppRoutes = () => {
  const { isAuthenticated } = useAuth()

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
              <Navbar />
              <Box component="main" sx={{ pt: 8, pb: 4 }}>
                <Dashboard />
              </Box>
            </Box>
          </ProtectedRoute>
        }
      />
      <Route
        path="/sentiment"
        element={
          <ProtectedRoute>
            <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
              <Navbar />
              <Box component="main" sx={{ pt: 8, pb: 4 }}>
                <SentimentAnalysis />
              </Box>
            </Box>
          </ProtectedRoute>
        }
      />
      <Route
        path="/topics"
        element={
          <ProtectedRoute>
            <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
              <Navbar />
              <Box component="main" sx={{ pt: 8, pb: 4 }}>
                <TopicAnalysis />
              </Box>
            </Box>
          </ProtectedRoute>
        }
      />
      <Route
        path="/trends"
        element={
          <ProtectedRoute>
            <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
              <Navbar />
              <Box component="main" sx={{ pt: 8, pb: 4 }}>
                <TrendsInsights />
              </Box>
            </Box>
          </ProtectedRoute>
        }
      />
      <Route path="/about" element={<About />} />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App


