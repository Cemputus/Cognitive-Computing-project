import React, { createContext, useContext, useState, useEffect } from 'react'
import axios from 'axios'
import { jwtDecode } from 'jwt-decode'

const AuthContext = createContext(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)

  useEffect(() => {
    // Check for stored token on mount
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      try {
        const decoded = jwtDecode(storedToken)
        // Check if token is expired
        if (decoded.exp * 1000 > Date.now()) {
          setToken(storedToken)
          setUser(JSON.parse(storedUser))
          axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
        } else {
          // Token expired, clear storage
          localStorage.removeItem('token')
          localStorage.removeItem('user')
        }
      } catch (error) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
    }
  }, [])

  const login = async (email, password) => {
    try {
      const response = await axios.post('http://localhost:5000/api/auth/login', {
        email,
        password,
      })

      const { token: newToken, user: userData } = response.data

      setToken(newToken)
      setUser(userData)
      localStorage.setItem('token', newToken)
      localStorage.setItem('user', JSON.stringify(userData))
      axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`

      return true
    } catch (error) {
      console.error('Login error:', error)
      return false
    }
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']
  }

  const value = {
    user,
    token,
    login,
    logout,
    isAuthenticated: !!user && !!token,
    isAdmin: user?.role === 'admin',
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

