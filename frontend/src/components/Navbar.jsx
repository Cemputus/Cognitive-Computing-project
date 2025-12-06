import React, { useState, useEffect } from 'react'
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
  Container,
  InputBase,
  alpha,
  Badge,
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
  Settings,
  Search,
  NotificationsNone,
  Menu as MenuIcon,
  Info,
} from '@mui/icons-material'
import { useAuth } from '../contexts/AuthContext'
import { useNotifications } from '../contexts/NotificationContext'
import { useSearch } from '../contexts/SearchContext'
import logoImage from '../images/CENAnalytics logo.png'

const Navbar = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, isAuthenticated, isAdmin, logout } = useAuth()
  const { unreadCount } = useNotifications()
  const { searchQuery, updateSearchQuery } = useSearch()
  const [anchorEl, setAnchorEl] = useState(null)
  const [scrolled, setScrolled] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  // Handle scroll for floating effect
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const navItems = [
    { label: 'Dashboard', path: '/dashboard', icon: <DashboardIcon fontSize="small" /> },
    { label: 'Sentiment', path: '/sentiment', icon: <SentimentIcon fontSize="small" /> },
    { label: 'Topics', path: '/topics', icon: <TopicIcon fontSize="small" /> },
    { label: 'Trends', path: '/trends', icon: <TrendsIcon fontSize="small" /> },
    { label: 'About', path: '/about', icon: <Info fontSize="small" /> },
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

  const isActive = (path) => location.pathname === path

  return (
    <AppBar
      position="fixed"
      sx={{
        background: scrolled
          ? 'rgba(255, 255, 255, 0.98)'
          : 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px)',
        boxShadow: scrolled
          ? '0 4px 20px rgba(0,0,0,0.08)'
          : '0 2px 8px rgba(0,0,0,0.04)',
        transition: 'all 0.3s ease',
        borderBottom: '1px solid rgba(0,0,0,0.05)',
        zIndex: 1300,
      }}
    >
      <Container maxWidth="xl">
        <Toolbar
          disableGutters
          sx={{
            minHeight: { xs: 56, sm: 64 },
            py: 1,
            justifyContent: 'space-between',
          }}
        >
          {/* Logo */}
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1.5,
              cursor: 'pointer',
              mr: { xs: 2, md: 4 },
              flexShrink: 0,
            }}
            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/')}
          >
            <Box
              component="img"
              src={logoImage}
              alt="CENAnalytics"
              sx={{
                height: { xs: 32, sm: 36 },
                width: 'auto',
              }}
            />
            <Typography
              variant="h6"
              sx={{
                fontWeight: 700,
                fontSize: { xs: '1.1rem', sm: '1.25rem' },
                color: 'text.primary',
                display: { xs: 'none', sm: 'block' },
                ml: 1,
              }}
            >
              CENAnalytics
            </Typography>
          </Box>

          {/* Navigation Items - Desktop */}
          {isAuthenticated && (
            <Box
              sx={{
                flexGrow: 1,
                display: { xs: 'none', md: 'flex' },
                gap: 0.5,
                mx: 2,
              }}
            >
              {navItems.map((item) => (
                <Button
                  key={item.path}
                  startIcon={item.icon}
                  onClick={() => navigate(item.path)}
                  sx={{
                    color: isActive(item.path) ? 'primary.main' : 'text.secondary',
                    backgroundColor: isActive(item.path)
                      ? alpha('#5624d0', 0.08)
                      : 'transparent',
                    fontWeight: isActive(item.path) ? 600 : 500,
                    borderRadius: 2,
                    px: 2,
                    py: 0.75,
                    fontSize: '0.9375rem',
                    textTransform: 'none',
                    '&:hover': {
                      backgroundColor: isActive(item.path)
                        ? alpha('#5624d0', 0.12)
                        : alpha('#5624d0', 0.05),
                      color: 'primary.main',
                    },
                    transition: 'all 0.2s ease',
                  }}
                >
                  {item.label}
                </Button>
              ))}
            </Box>
          )}

          {/* Search Bar - Desktop */}
          {isAuthenticated && (
            <Box
              sx={{
                display: { xs: 'none', md: 'flex' },
                position: 'relative',
                borderRadius: 2,
                backgroundColor: alpha('#000', 0.04),
                '&:hover': {
                  backgroundColor: alpha('#000', 0.06),
                },
                marginRight: 2,
                width: { md: '300px', lg: '400px' },
                transition: 'all 0.2s ease',
              }}
            >
              <Box
                sx={{
                  padding: '8px 12px',
                  height: '100%',
                  position: 'absolute',
                  pointerEvents: 'none',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'text.secondary',
                }}
              >
                <Search fontSize="small" />
              </Box>
              <InputBase
                placeholder="Search analytics..."
                value={searchQuery}
                onChange={(e) => updateSearchQuery(e.target.value)}
                sx={{
                  color: 'text.primary',
                  width: '100%',
                  pl: '40px',
                  pr: '12px',
                  py: '8px',
                  fontSize: '0.9375rem',
                }}
              />
            </Box>
          )}

          {/* Right Side Actions */}
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              gap: 1,
              flexShrink: 0,
            }}
          >
            {isAuthenticated ? (
              <>
                {/* Notifications */}
                <IconButton
                  onClick={() => navigate('/notifications')}
                  sx={{
                    color: isActive('/notifications') ? 'primary.main' : 'text.secondary',
                    '&:hover': {
                      backgroundColor: alpha('#5624d0', 0.08),
                      color: 'primary.main',
                    },
                    display: { xs: 'none', sm: 'flex' },
                  }}
                >
                  <Badge badgeContent={unreadCount} color="error">
                    <NotificationsNone />
                  </Badge>
                </IconButton>

                {/* Admin Badge */}
                {isAdmin && (
                  <Chip
                    icon={<AdminPanelSettings fontSize="small" />}
                    label="Admin"
                    size="small"
                    sx={{
                      bgcolor: alpha('#5624d0', 0.1),
                      color: 'primary.main',
                      fontWeight: 600,
                      display: { xs: 'none', sm: 'flex' },
                      '& .MuiChip-icon': {
                        color: 'primary.main',
                      },
                    }}
                  />
                )}

                {/* User Menu */}
                <IconButton
                  onClick={handleMenuOpen}
                  sx={{
                    color: 'text.primary',
                    '&:hover': {
                      backgroundColor: alpha('#5624d0', 0.08),
                    },
                  }}
                >
                  <Avatar
                    sx={{
                      width: 36,
                      height: 36,
                      bgcolor: 'primary.main',
                      fontSize: '0.875rem',
                      fontWeight: 600,
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
                      minWidth: 240,
                      boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
                      borderRadius: 2,
                      border: '1px solid rgba(0,0,0,0.05)',
                    },
                  }}
                  transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                  anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                >
                  <MenuItem disabled sx={{ py: 1.5 }}>
                    <Box>
                      <Typography variant="body2" fontWeight={600} color="text.primary">
                        {user?.name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {user?.email}
                      </Typography>
                    </Box>
                  </MenuItem>
                  <Divider />
                  <MenuItem
                    onClick={() => {
                      navigate('/profile')
                      handleMenuClose()
                    }}
                    sx={{ py: 1.25 }}
                  >
                    <Person sx={{ mr: 2, fontSize: 20 }} /> Profile
                  </MenuItem>
                  <MenuItem
                    onClick={() => {
                      navigate('/dashboard')
                      handleMenuClose()
                    }}
                    sx={{ py: 1.25 }}
                  >
                    <Settings sx={{ mr: 2, fontSize: 20 }} /> Settings
                  </MenuItem>
                  <Divider />
                  <MenuItem onClick={handleLogout} sx={{ py: 1.25, color: 'error.main' }}>
                    <Logout sx={{ mr: 2, fontSize: 20 }} /> Logout
                  </MenuItem>
                </Menu>

                {/* Mobile Menu Button */}
                <IconButton
                  onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                  sx={{
                    color: 'text.primary',
                    display: { xs: 'flex', md: 'none' },
                  }}
                >
                  <MenuIcon />
                </IconButton>
              </>
            ) : (
              <Button
                variant="contained"
                startIcon={<LoginIcon />}
                onClick={() => navigate('/login')}
                sx={{
                  bgcolor: 'primary.main',
                  color: 'white',
                  fontWeight: 600,
                  px: 2.5,
                  '&:hover': {
                    bgcolor: 'primary.dark',
                    boxShadow: '0 4px 12px rgba(86, 36, 208, 0.3)',
                  },
                }}
              >
                Login
              </Button>
            )}
          </Box>
        </Toolbar>

        {/* Mobile Menu */}
        {isAuthenticated && mobileMenuOpen && (
          <Box
            sx={{
              display: { xs: 'flex', md: 'none' },
              flexDirection: 'column',
              gap: 0.5,
              px: 2,
              pb: 2,
              borderTop: '1px solid rgba(0,0,0,0.05)',
            }}
          >
            {navItems.map((item) => (
              <Button
                key={item.path}
                startIcon={item.icon}
                onClick={() => {
                  navigate(item.path)
                  setMobileMenuOpen(false)
                }}
                fullWidth
                sx={{
                  justifyContent: 'flex-start',
                  color: isActive(item.path) ? 'primary.main' : 'text.secondary',
                  backgroundColor: isActive(item.path)
                    ? alpha('#5624d0', 0.08)
                    : 'transparent',
                  fontWeight: isActive(item.path) ? 600 : 500,
                  borderRadius: 2,
                  py: 1.25,
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        )}
      </Container>
    </AppBar>
  )
}

export default Navbar
