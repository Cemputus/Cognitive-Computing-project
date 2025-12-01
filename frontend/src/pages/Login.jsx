import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Container,
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  InputAdornment,
  IconButton,
  Link,
  Divider,
  useTheme,
} from '@mui/material'
import {
  Email,
  Lock,
  Visibility,
  VisibilityOff,
  Business,
  Login as LoginIcon,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { FaBrain } from 'react-icons/fa'
import { useAuth } from '../contexts/AuthContext'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const theme = useTheme()
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const success = await login(email, password)
      if (success) {
        navigate('/dashboard')
      } else {
        setError('Invalid email or password')
      }
    } catch (err) {
      setError(err.message || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 4,
      }}
    >
      <Container maxWidth="xs">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Card
            sx={{
              borderRadius: 4,
              boxShadow: 24,
              overflow: 'hidden',
              maxWidth: 450,
              mx: 'auto',
            }}
          >
            {/* Header */}
            <Box
              sx={{
                background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                color: 'white',
                p: 3,
                textAlign: 'center',
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  mb: 1.5,
                  fontSize: '2.5rem',
                }}
              >
                <FaBrain />
              </Box>
              <Typography variant="h5" sx={{ fontWeight: 700, mb: 0.5 }}>
                Welcome Back
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9, fontSize: '0.875rem' }}>
                Sign in to your dashboard
              </Typography>
            </Box>

            <CardContent sx={{ p: 3 }}>
              {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                  {error}
                </Alert>
              )}

              <form onSubmit={handleSubmit}>
                <TextField
                  fullWidth
                  label="Email Address"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  size="small"
                  sx={{ mb: 2 }}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Email color="action" fontSize="small" />
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                />

                <TextField
                  fullWidth
                  label="Password"
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  size="small"
                  sx={{ mb: 2 }}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Lock color="action" />
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
                        >
                          {showPassword ? <VisibilityOff /> : <Visibility />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                />

                <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
                  <Link
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                    }}
                    sx={{ textDecoration: 'none', fontSize: '0.875rem' }}
                  >
                    Forgot Password?
                  </Link>
                </Box>

                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  size="medium"
                  disabled={loading}
                  startIcon={<LoginIcon />}
                  sx={{
                    py: 1.2,
                    fontSize: '1rem',
                    fontWeight: 600,
                    mb: 2,
                    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                    '&:hover': {
                      background: `linear-gradient(135deg, ${theme.palette.primary.dark} 0%, ${theme.palette.secondary.dark} 100%)`,
                      transform: 'translateY(-2px)',
                      boxShadow: 6,
                    },
                    transition: 'all 0.3s',
                  }}
                >
                  {loading ? 'Signing in...' : 'Sign In'}
                </Button>
              </form>

              <Divider sx={{ my: 2 }}>
                <Typography variant="caption" color="text.secondary">
                  Demo Accounts
                </Typography>
              </Divider>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mb: 2 }}>
                <Button
                  variant="outlined"
                  fullWidth
                  size="small"
                  onClick={() => {
                    setEmail('admin@business.com')
                    setPassword('admin123')
                  }}
                  startIcon={<Business sx={{ fontSize: '1rem' }} />}
                  sx={{ textTransform: 'none', fontSize: '0.875rem' }}
                >
                  Use Admin Account
                </Button>
                <Button
                  variant="outlined"
                  fullWidth
                  size="small"
                  onClick={() => {
                    setEmail('user1@business.com')
                    setPassword('user123')
                  }}
                  sx={{ textTransform: 'none', fontSize: '0.875rem' }}
                >
                  Use Demo User Account
                </Button>
              </Box>

              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">
                  Don't have an account?{' '}
                  <Link
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                    }}
                    sx={{ fontWeight: 600, fontSize: '0.875rem' }}
                  >
                    Contact Admin
                  </Link>
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </motion.div>
      </Container>
    </Box>
  )
}

export default Login

