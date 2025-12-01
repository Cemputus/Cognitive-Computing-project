import React, { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
  MenuItem,
  Avatar,
  Divider,
  Chip,
} from '@mui/material'
import {
  Dashboard as DashboardIcon,
  SentimentSatisfiedAlt as SentimentIcon,
  Topic as TopicIcon,
  TrendingUp as TrendsIcon,
  Login as LoginIcon,
  Logout,
  Person,
  AdminPanelSettings,
} from '@mui/icons-material'
import { FaBrain } from 'react-icons/fa'
import { useAuth } from '../contexts/AuthContext'

const Navbar = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, isAuthenticated, isAdmin, logout } = useAuth()
  const [anchorEl, setAnchorEl] = useState(null)

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: <DashboardIcon /> },
    { label: 'Sentiment', path: '/sentiment', icon: <SentimentIcon /> },
    { label: 'Topics', path: '/topics', icon: <TopicIcon /> },
    { label: 'Trends', path: '/trends', icon: <TrendsIcon /> },
  ]

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
  }

  const handleLogout = () => {
    logout()
    handleMenuClose()
    navigate('/')
  }

  return (
    <AppBar
      position="fixed"
      sx={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
        backdropFilter: 'blur(10px)',
      }}
    >
      <Toolbar>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 1,
            cursor: 'pointer',
            mr: 4,
          }}
          onClick={() => navigate(isAuthenticated ? '/dashboard' : '/')}
        >
          <Box sx={{ fontSize: '1.8rem', display: 'flex', alignItems: 'center' }}>
            <FaBrain />
          </Box>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              fontSize: '1.5rem',
            }}
          >
            Business Intelligence
          </Typography>
        </Box>

        {isAuthenticated && (
          <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
            {navItems.map((item) => (
              <Button
                key={item.path}
                startIcon={item.icon}
                onClick={() => navigate(item.path)}
                sx={{
                  color: 'white',
                  backgroundColor:
                    location.pathname === item.path
                      ? 'rgba(255, 255, 255, 0.2)'
                      : 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.15)',
                  },
                  borderRadius: 2,
                  px: 2,
                  py: 1,
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        )}

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          {isAuthenticated ? (
            <>
              {isAdmin && (
                <Chip
                  icon={<AdminPanelSettings />}
                  label="Admin"
                  color="secondary"
                  size="small"
                />
              )}
              <IconButton
                onClick={handleMenuOpen}
                sx={{
                  color: 'white',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                <Avatar
                  sx={{
                    width: 32,
                    height: 32,
                    bgcolor: 'rgba(255, 255, 255, 0.2)',
                  }}
                >
                  {user?.name?.charAt(0).toUpperCase() || 'U'}
                </Avatar>
              </IconButton>
              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
                PaperProps={{
                  sx: {
                    mt: 1.5,
                    minWidth: 200,
                  },
                }}
              >
                <MenuItem disabled>
                  <Box>
                    <Typography variant="body2" fontWeight={600}>
                      {user?.name}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {user?.email}
                    </Typography>
                  </Box>
                </MenuItem>
                <Divider />
                <MenuItem onClick={() => { navigate('/dashboard'); handleMenuClose(); }}>
                  <Person sx={{ mr: 2 }} /> Profile
                </MenuItem>
                <MenuItem onClick={handleLogout}>
                  <Logout sx={{ mr: 2 }} /> Logout
                </MenuItem>
              </Menu>
            </>
          ) : (
            <Button
              variant="contained"
              startIcon={<LoginIcon />}
              onClick={() => navigate('/login')}
              sx={{
                bgcolor: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                '&:hover': {
                  bgcolor: 'rgba(255, 255, 255, 0.3)',
                },
              }}
            >
              Login
            </Button>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Navbar


