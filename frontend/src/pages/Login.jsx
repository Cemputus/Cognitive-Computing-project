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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material'
import {
  Email,
  Lock,
  Visibility,
  VisibilityOff,
  Business,
  Login as LoginIcon,
  Send,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { FaBrain } from 'react-icons/fa'
import { useAuth } from '../contexts/AuthContext'
import { apiService } from '../services/api'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [contactDialogOpen, setContactDialogOpen] = useState(false)
  const [contactName, setContactName] = useState('')
  const [contactEmail, setContactEmail] = useState('')
  const [contactSubject, setContactSubject] = useState('')
  const [contactMessage, setContactMessage] = useState('')
  const [contactLoading, setContactLoading] = useState(false)
  const [contactSuccess, setContactSuccess] = useState(false)
  const navigate = useNavigate()
  const theme = useTheme()
  const { login } = useAuth()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const success = await login(email.trim(), password)
      if (success) {
        navigate('/dashboard')
      } else {
        setError('Invalid email or password')
      }
    } catch (err) {
      console.error('Login error in component:', err)
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
              borderRadius: 3,
              boxShadow: 12,
              overflow: 'hidden',
              maxWidth: 380,
              mx: 'auto',
            }}
          >
            {/* Header */}
            <Box
              sx={{
                background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
                color: 'white',
                p: 2,
                textAlign: 'center',
              }}
            >
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  mb: 1,
                  fontSize: '2rem',
                }}
              >
                <FaBrain />
              </Box>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 0.25 }}>
                Welcome Back
              </Typography>
              <Typography variant="caption" sx={{ opacity: 0.9, fontSize: '0.75rem' }}>
                Sign in to your dashboard
              </Typography>
            </Box>

            <CardContent sx={{ p: 2.5 }}>
              {error && (
                <Alert severity="error" sx={{ mb: 2, py: 0.5, fontSize: '0.875rem' }}>
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
                  sx={{ mb: 1.5 }}
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
                  sx={{ mb: 1.5 }}
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <Lock color="action" fontSize="small" />
                      </InputAdornment>
                    ),
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton
                          onClick={() => setShowPassword(!showPassword)}
                          edge="end"
                          size="small"
                        >
                          {showPassword ? <VisibilityOff fontSize="small" /> : <Visibility fontSize="small" />}
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                  variant="outlined"
                />

                <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1.5 }}>
                  <Link
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                    }}
                    sx={{ textDecoration: 'none', fontSize: '0.75rem' }}
                  >
                    Forgot Password?
                  </Link>
                </Box>

                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  size="small"
                  disabled={loading}
                  startIcon={<LoginIcon fontSize="small" />}
                  sx={{
                    py: 1,
                    fontSize: '0.875rem',
                    fontWeight: 600,
                    mb: 1.5,
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

              <Divider sx={{ my: 1.5 }}>
                <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
                  Demo Accounts
                </Typography>
              </Divider>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.75, mb: 1.5 }}>
                <Button
                  variant="outlined"
                  fullWidth
                  size="small"
                  onClick={() => {
                    setEmail('admin@business.com')
                    setPassword('admin123')
                  }}
                  startIcon={<Business sx={{ fontSize: '0.875rem' }} />}
                  sx={{ textTransform: 'none', fontSize: '0.75rem', py: 0.75 }}
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
                  sx={{ textTransform: 'none', fontSize: '0.75rem', py: 0.75 }}
                >
                  Use Demo User Account
                </Button>
              </Box>

              <Box sx={{ textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary" sx={{ fontSize: '0.7rem' }}>
                  Don't have an account?{' '}
                  <Link
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()
                      setContactDialogOpen(true)
                    }}
                    sx={{ fontWeight: 600, fontSize: '0.7rem', cursor: 'pointer' }}
                  >
                    Contact Admin
                  </Link>
                </Typography>
              </Box>

              {/* Contact Admin Dialog */}
              <Dialog
                open={contactDialogOpen}
                onClose={() => {
                  setContactDialogOpen(false)
                  setContactSuccess(false)
                  setContactName('')
                  setContactEmail('')
                  setContactSubject('')
                  setContactMessage('')
                }}
                maxWidth="sm"
                fullWidth
              >
                <DialogTitle>
                  <Box display="flex" alignItems="center" gap={1}>
                    <Email color="primary" />
                    <Typography variant="h6">Contact Administrator</Typography>
                  </Box>
                </DialogTitle>
                <DialogContent>
                  {contactSuccess ? (
                    <Alert severity="success" sx={{ mb: 2 }}>
                      Your message has been sent to the administrator. They will get back to you soon.
                    </Alert>
                  ) : (
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
                      <TextField
                        label="Your Name"
                        fullWidth
                        value={contactName}
                        onChange={(e) => setContactName(e.target.value)}
                        required
                      />
                      <TextField
                        label="Your Email"
                        type="email"
                        fullWidth
                        value={contactEmail}
                        onChange={(e) => setContactEmail(e.target.value)}
                        required
                      />
                      <TextField
                        label="Subject"
                        fullWidth
                        value={contactSubject}
                        onChange={(e) => setContactSubject(e.target.value)}
                        required
                      />
                      <TextField
                        label="Message"
                        fullWidth
                        multiline
                        rows={4}
                        value={contactMessage}
                        onChange={(e) => setContactMessage(e.target.value)}
                        required
                      />
                    </Box>
                  )}
                </DialogContent>
                <DialogActions>
                  <Button
                    onClick={() => {
                      setContactDialogOpen(false)
                      setContactSuccess(false)
                      setContactName('')
                      setContactEmail('')
                      setContactSubject('')
                      setContactMessage('')
                    }}
                  >
                    {contactSuccess ? 'Close' : 'Cancel'}
                  </Button>
                  {!contactSuccess && (
                    <Button
                      onClick={async () => {
                        if (!contactName || !contactEmail || !contactSubject || !contactMessage) {
                          setError('Please fill in all fields')
                          return
                        }
                        try {
                          setContactLoading(true)
                          await apiService.contactAdmin({
                            name: contactName,
                            email: contactEmail,
                            subject: contactSubject,
                            message: contactMessage,
                          })
                          setContactSuccess(true)
                        } catch (err) {
                          setError('Failed to send message. Please try again.')
                        } finally {
                          setContactLoading(false)
                        }
                      }}
                      variant="contained"
                      startIcon={<Send />}
                      disabled={contactLoading}
                    >
                      {contactLoading ? 'Sending...' : 'Send Message'}
                    </Button>
                  )}
                </DialogActions>
              </Dialog>
            </CardContent>
          </Card>
        </motion.div>
      </Container>
    </Box>
  )
}

export default Login
