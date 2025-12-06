import React, { useEffect, useState } from 'react'
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  IconButton,
  Alert,
  CircularProgress,
  Divider,
} from '@mui/material'
import {
  Notifications as NotificationsIcon,
  Info,
  CheckCircle,
  Warning,
  Error as ErrorIcon,
  Refresh,
  Delete,
} from '@mui/icons-material'
import { useNotifications } from '../contexts/NotificationContext'
import { motion } from 'framer-motion'

const Notifications = () => {
  const { notifications, fetchNotifications, markAsRead, deleteNotification } = useNotifications()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadNotifications = async () => {
      setLoading(true)
      await fetchNotifications()
      setLoading(false)
    }
    loadNotifications()
  }, [fetchNotifications])

  const getIcon = (type) => {
    switch (type) {
      case 'success':
        return <CheckCircle color="success" />
      case 'warning':
        return <Warning color="warning" />
      case 'error':
        return <ErrorIcon color="error" />
      default:
        return <Info color="info" />
    }
  }

  const getSeverity = (type) => {
    switch (type) {
      case 'success':
        return 'success'
      case 'warning':
        return 'warning'
      case 'error':
        return 'error'
      default:
        return 'info'
    }
  }

  const handleMarkAsRead = async (id) => {
    await markAsRead(id)
  }

  const handleDelete = async (id) => {
    await deleteNotification(id)
  }

  if (loading) {
    return (
      <Container>
        <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
          <CircularProgress />
        </Box>
      </Container>
    )
  }

  const unreadCount = notifications.filter((n) => !n.read).length

  return (
    <Container maxWidth="md">
      {/* Header */}
      <Box mb={4} display="flex" justifyContent="space-between" alignItems="center">
        <Box display="flex" alignItems="center" gap={2}>
          <NotificationsIcon sx={{ fontSize: 32, color: 'primary.main' }} />
          <Box>
            <Typography variant="h4" component="h1" fontWeight={700}>
              Notifications
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {unreadCount > 0
                ? `${unreadCount} unread notification${unreadCount > 1 ? 's' : ''}`
                : 'All caught up!'}
            </Typography>
          </Box>
        </Box>
        <IconButton onClick={fetchNotifications} color="primary">
          <Refresh />
        </IconButton>
      </Box>

      {/* Notifications List */}
      {notifications.length === 0 ? (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 8 }}>
            <NotificationsIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h6" color="text.secondary" gutterBottom>
              No notifications
            </Typography>
            <Typography variant="body2" color="text.secondary">
              You're all caught up! Check back later for updates.
            </Typography>
          </CardContent>
        </Card>
      ) : (
        <List>
          {notifications.map((notification, index) => (
            <motion.div
              key={notification.id || index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Card
                sx={{
                  mb: 2,
                  bgcolor: notification.read ? 'background.paper' : 'action.hover',
                  border: notification.read ? 'none' : `1px solid`,
                  borderColor: 'primary.main',
                  transition: 'all 0.2s',
                  '&:hover': {
                    boxShadow: 4,
                  },
                }}
              >
                <CardContent sx={{ py: 2 }}>
                  <Box display="flex" alignItems="start" gap={2}>
                    <ListItemIcon sx={{ minWidth: 40, mt: 0.5 }}>
                      {getIcon(notification.type)}
                    </ListItemIcon>
                    <Box flex={1}>
                      <Box display="flex" justifyContent="space-between" alignItems="start" mb={1}>
                        <Box flex={1}>
                          <Typography
                            variant="subtitle1"
                            fontWeight={notification.read ? 400 : 600}
                            gutterBottom
                          >
                            {notification.title || 'Notification'}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" paragraph>
                            {notification.message || notification.body || 'No message'}
                          </Typography>
                          <Box display="flex" gap={1} alignItems="center" flexWrap="wrap">
                            {notification.type && (
                              <Chip
                                label={notification.type}
                                size="small"
                                color={getSeverity(notification.type)}
                                variant="outlined"
                              />
                            )}
                            {notification.created_at && (
                              <Typography variant="caption" color="text.secondary">
                                {new Date(notification.created_at).toLocaleString()}
                              </Typography>
                            )}
                          </Box>
                        </Box>
                        <Box display="flex" gap={0.5}>
                          {!notification.read && (
                            <IconButton
                              size="small"
                              onClick={() => handleMarkAsRead(notification.id)}
                              title="Mark as read"
                            >
                              <CheckCircle fontSize="small" />
                            </IconButton>
                          )}
                          <IconButton
                            size="small"
                            onClick={() => handleDelete(notification.id)}
                            color="error"
                            title="Delete"
                          >
                            <Delete fontSize="small" />
                          </IconButton>
                        </Box>
                      </Box>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
              {index < notifications.length - 1 && <Divider />}
            </motion.div>
          ))}
        </List>
      )}

      {/* Empty State Alternative */}
      {notifications.length > 0 && unreadCount === 0 && (
        <Alert severity="success" sx={{ mt: 3 }}>
          All notifications have been read!
        </Alert>
      )}
    </Container>
  )
}

export default Notifications
