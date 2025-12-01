import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Box } from '@mui/material'
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
  const { isAuthenticated } = useAuth()
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
            <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
              <Navbar />
              <Box component="main" sx={{ pt: 8, pb: 4 }}>
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
            <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
              <Navbar />
              <Box component="main" sx={{ pt: 8, pb: 4 }}>
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



