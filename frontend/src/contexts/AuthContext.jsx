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
  const [loading, setLoading] = useState(true)

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
    setLoading(false)
  }, [])

  const login = async (email, password) => {
    try {
      console.log('Attempting login with:', { email, passwordLength: password?.length })
      
      const response = await axios.post('http://localhost:5000/api/auth/login', {
        email: email.trim(),
        password: password,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      })

      console.log('Login response:', response.status, response.data)

      if (response.data && response.data.token) {
        const { token: newToken, user: userData } = response.data

        setToken(newToken)
        setUser(userData)
        localStorage.setItem('token', newToken)
        localStorage.setItem('user', JSON.stringify(userData))
        axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`

        return true
      } else {
        console.error('No token in response:', response.data)
        return false
      }
    } catch (error) {
      console.error('Login error:', error)
      if (error.response) {
        console.error('Error response:', error.response.status, error.response.data)
        throw new Error(error.response.data?.error || 'Login failed')
      } else if (error.request) {
        console.error('No response received:', error.request)
        throw new Error('Cannot connect to server. Please check if backend is running.')
      } else {
        throw new Error(error.message || 'Login failed')
      }
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
    loading,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

