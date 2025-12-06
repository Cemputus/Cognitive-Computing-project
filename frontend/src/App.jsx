import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Box, CircularProgress } from '@mui/material'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { NotificationProvider } from './contexts/NotificationContext'
import Navbar from './components/Navbar'
import LandingPage from './pages/LandingPage'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import SentimentAnalysis from './pages/SentimentAnalysis'
import TopicAnalysis from './pages/TopicAnalysis'
import TrendsInsights from './pages/TrendsInsights'
import About from './pages/About'
import Profile from './pages/Profile'
import Notifications from './pages/Notifications'

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth()
  
  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh' }}>
        <CircularProgress />
      </Box>
    )
  }
  
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

const AppRoutes = () => {
  const { isAuthenticated } = useAuth()

  return (
    <Routes>
      <Route
        path="/"
        element={
          <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
            <LandingPage />
          </Box>
        }
      />
      <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
          <Box sx={{ minHeight: '100vh', bgcolor: '#f5f7fa', overflow: 'hidden' }}>
            <Navbar />
            <Box component="main" sx={{ pt: 8, pb: 4, minHeight: 'calc(100vh - 64px)' }}>
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
          <Box sx={{ minHeight: '100vh', bgcolor: '#f5f7fa', overflow: 'hidden' }}>
            <Navbar />
            <Box component="main" sx={{ pt: 8, pb: 4, minHeight: 'calc(100vh - 64px)' }}>
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
          <Box sx={{ minHeight: '100vh', bgcolor: '#f5f7fa', overflow: 'hidden' }}>
            <Navbar />
            <Box component="main" sx={{ pt: 8, pb: 4, minHeight: 'calc(100vh - 64px)' }}>
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
          <Box sx={{ minHeight: '100vh', bgcolor: '#f5f7fa', overflow: 'hidden' }}>
            <Navbar />
            <Box component="main" sx={{ pt: 8, pb: 4, minHeight: 'calc(100vh - 64px)' }}>
              <TrendsInsights />
            </Box>
          </Box>
          </ProtectedRoute>
        }
      />
      <Route
        path="/about"
        element={
          <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
            <Navbar />
            <Box component="main" sx={{ pt: 8, pb: 4 }}>
              <About />
            </Box>
          </Box>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
          <Box sx={{ minHeight: '100vh', bgcolor: '#f5f7fa', overflow: 'hidden' }}>
            <Navbar />
            <Box component="main" sx={{ pt: 8, pb: 4, minHeight: 'calc(100vh - 64px)' }}>
              <Profile />
            </Box>
          </Box>
          </ProtectedRoute>
        }
      />
      <Route
        path="/notifications"
        element={
          <ProtectedRoute>
          <Box sx={{ minHeight: '100vh', bgcolor: '#f5f7fa', overflow: 'hidden' }}>
            <Navbar />
            <Box component="main" sx={{ pt: 8, pb: 4, minHeight: 'calc(100vh - 64px)' }}>
              <Notifications />
            </Box>
          </Box>
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <NotificationProvider>
        <AppRoutes />
      </NotificationProvider>
    </AuthProvider>
  )
}

export default App
