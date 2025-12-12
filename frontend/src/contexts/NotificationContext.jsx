import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { apiService } from '../services/api'
import { useAuth } from './AuthContext'

const NotificationContext = createContext(undefined)

export const useNotifications = () => {
  const context = useContext(NotificationContext)
  if (!context) {
    throw new Error('useNotifications must be used within NotificationProvider')
  }
  return context
}

export const NotificationProvider = ({ children }) => {
  const [notifications, setNotifications] = useState([])
  const [loading, setLoading] = useState(false)
  const { isAuthenticated } = useAuth()

  const fetchNotifications = useCallback(async () => {
    if (!isAuthenticated) {
      setNotifications([])
      return
    }

    try {
      setLoading(true)
      const data = await apiService.getNotifications()
      setNotifications(data.notifications || [])
    } catch (err) {
      console.error('Error fetching notifications:', err)
    } finally {
      setLoading(false)
    }
  }, [isAuthenticated])

  useEffect(() => {
    fetchNotifications()
    
    // Poll for new notifications every 30 seconds
    const interval = setInterval(() => {
      if (isAuthenticated) {
        fetchNotifications()
      }
    }, 30000)

    return () => clearInterval(interval)
  }, [fetchNotifications, isAuthenticated])

  const unreadCount = notifications.filter(n => !n.read).length

  const markAsRead = async (notificationId) => {
    try {
      await apiService.markNotificationRead(notificationId)
      setNotifications(prev =>
        prev.map(n => n.id === notificationId ? { ...n, read: true } : n)
      )
    } catch (err) {
      console.error('Error marking notification as read:', err)
    }
  }

  return (
    <NotificationContext.Provider
      value={{
        notifications,
        unreadCount,
        loading,
        fetchNotifications,
        markAsRead,
      }}
    >
      {children}
    </NotificationContext.Provider>
  )
}






