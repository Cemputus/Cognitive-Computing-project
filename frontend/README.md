# 🎨 CENAnalytics Frontend

Modern React application for the CENAnalytics Business Intelligence Platform. Built with React 18, Material-UI, and Vite for a fast, responsive, and beautiful user experience.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Development](#development)
- [Project Structure](#project-structure)
- [Components](#components)
- [Pages](#pages)
- [State Management](#state-management)
- [API Integration](#api-integration)
- [Styling](#styling)
- [Build & Deployment](#build--deployment)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The frontend is a single-page application (SPA) built with React that provides:

- **Interactive Dashboard** with real-time analytics
- **Sentiment Analysis** interface for text input
- **Topic Modeling** visualization
- **Trend Forecasting** charts
- **Report Export** with PDF download
- **User Authentication** with JWT
- **Notification System** for user alerts
- **Responsive Design** for all devices

## ✨ Features

### User Interface
- 🎨 **Material-UI Components** - Modern, accessible UI components
- 🎭 **Framer Motion** - Smooth animations and transitions
- 📊 **Recharts** - Interactive charts and graphs
- ☁️ **Word Clouds** - Visual topic representation
- 📱 **Responsive Layout** - Works on desktop, tablet, and mobile

### Functionality
- 🔐 **JWT Authentication** - Secure login and token management
- 📈 **Real-Time Analytics** - Live data updates
- 📥 **PDF Export** - Download comprehensive reports
- 🔔 **Notifications** - Real-time user notifications
- 🎯 **Filtering & Search** - Advanced data filtering
- 📊 **Multiple Visualizations** - Charts, graphs, word clouds

## 📦 Installation

### Prerequisites

- **Node.js**: 16.0 or higher
- **npm** or **yarn**: Latest version

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Verify Installation

```bash
npm run dev
```

The development server should start on `http://localhost:5173`

## 🚀 Development

### Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 📁 Project Structure

```
frontend/
├── public/
│   └── favicon.png          # App favicon
├── src/
│   ├── components/          # Reusable components
│   │   └── Navbar.jsx      # Navigation bar
│   ├── contexts/           # React contexts
│   │   ├── AuthContext.jsx # Authentication state
│   │   └── NotificationContext.jsx # Notification state
│   ├── pages/              # Page components
│   │   ├── LandingPage.jsx
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── SentimentAnalysis.jsx
│   │   ├── TopicAnalysis.jsx
│   │   ├── TrendsInsights.jsx
│   │   ├── Profile.jsx
│   │   ├── Notifications.jsx
│   │   └── About.jsx
│   ├── services/           # API services
│   │   ├── api.js         # Main API service
│   │   └── api.ts         # TypeScript definitions (optional)
│   ├── images/            # Static images
│   ├── App.jsx            # Main app component
│   ├── main.jsx           # Entry point
│   └── index.css          # Global styles
├── index.html             # HTML template
├── package.json           # Dependencies and scripts
├── vite.config.js        # Vite configuration
└── README.md             # This file
```

## 🧩 Components

### Navbar

**Location:** `src/components/Navbar.jsx`

Main navigation component with:
- Logo and branding
- Navigation links
- User menu (profile, logout)
- Notification bell icon

### AuthContext

**Location:** `src/contexts/AuthContext.jsx`

Manages authentication state:
- User login/logout
- Token storage (localStorage)
- User information
- Protected route handling

**Usage:**
```jsx
import { useAuth } from '../contexts/AuthContext'

function MyComponent() {
  const { user, login, logout, isAuthenticated } = useAuth()
  // ...
}
```

### NotificationContext

**Location:** `src/contexts/NotificationContext.jsx`

Manages notification state:
- Fetch notifications
- Mark as read
- Real-time updates

**Usage:**
```jsx
import { useNotifications } from '../contexts/NotificationContext'

function MyComponent() {
  const { notifications, fetchNotifications, markAsRead } = useNotifications()
  // ...
}
```

## 📄 Pages

### Landing Page

**Location:** `src/pages/LandingPage.jsx`

- Hero section with project overview
- Feature highlights
- Call-to-action buttons
- Public access (no authentication required)

### Login

**Location:** `src/pages/Login.jsx`

- User authentication form
- Email and password input
- Error handling
- Redirect to dashboard on success

### Dashboard

**Location:** `src/pages/Dashboard.jsx`

Main analytics dashboard with:
- **Overview Statistics**: Total reviews, sentiment distribution
- **Interactive Charts**: Bar charts, pie charts, line graphs
- **Location Analytics**: Sentiment by location
- **Platform Analytics**: Sentiment by platform
- **Topic Analytics**: Sentiment by topic
- **Export Functionality**: PDF report generation
- **Real-Time Updates**: Refresh data button
- **Filtering**: Date range, location, platform filters

**Key Features:**
- Tabbed interface for different analytics views
- Download PDF reports
- Filter and search capabilities
- Responsive grid layout

### Sentiment Analysis

**Location:** `src/pages/SentimentAnalysis.jsx`

- Single text sentiment analysis
- Batch text analysis
- Results visualization
- Confidence scores display

### Topic Analysis

**Location:** `src/pages/TopicAnalysis.jsx`

- Topic modeling visualization
- Word clouds
- Topic distribution charts
- Topic-sentiment mapping

### Trends Insights

**Location:** `src/pages/TrendsInsights.jsx`

- Trend forecasting charts
- Historical sentiment trends
- Pattern recognition
- Predictive analytics visualization

### Profile

**Location:** `src/pages/Profile.jsx`

- User profile information
- Account settings
- Activity history

### Notifications

**Location:** `src/pages/Notifications.jsx`

- Notification list
- Mark as read functionality
- Filter by type
- Real-time updates

### About

**Location:** `src/pages/About.jsx`

- Project information
- Technology stack
- Team/author information

## 🔄 State Management

### Authentication State

Managed by `AuthContext`:
- User information
- Login status
- JWT token (stored in localStorage)

### Notification State

Managed by `NotificationContext`:
- Notification list
- Unread count
- Fetch and update functions

### Local Component State

Most components use React hooks (`useState`, `useEffect`) for local state:
- Form inputs
- Loading states
- Error messages
- UI toggles

## 🔌 API Integration

### API Service

**Location:** `src/services/api.js`

Centralized API service using Axios:

```javascript
import apiService from '../services/api'

// Login
const response = await apiService.login(email, password)

// Get dashboard stats
const stats = await apiService.getDashboardStats()

// Export report
const report = await apiService.exportReport('dashboard')
```

### Available Methods

- `login(email, password)` - User authentication
- `getCurrentUser()` - Get current user info
- `analyzeSentiment(text)` - Single text analysis
- `batchAnalyzeSentiment(texts)` - Batch analysis
- `getDashboardStats()` - Dashboard statistics
- `getLocationSentiment()` - Location analytics
- `getPlatformSentiment()` - Platform analytics
- `getTopicSentiment()` - Topic analytics
- `getTopics()` - Topic modeling results
- `getForecast()` - Trend forecasts
- `exportReport(type)` - Export PDF report
- `getNotifications()` - Get notifications
- `markNotificationRead(id)` - Mark notification as read
- `submitFeedback(data)` - Submit feedback
- `contactAdmin(data)` - Contact administrator

### API Configuration

Base URL is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api'
```

Change this for production deployment.

### Error Handling

API calls include error handling:

```javascript
try {
  const response = await apiService.getDashboardStats()
  // Handle success
} catch (error) {
  // Handle error
  console.error('API Error:', error.message)
}
```

## 🎨 Styling

### Material-UI Theme

The app uses Material-UI's default theme with custom colors:

- **Primary**: Purple (#5624d0)
- **Secondary**: Custom colors for charts
- **Typography**: Roboto font family

### Global Styles

**Location:** `src/index.css`

Contains:
- CSS reset
- Global typography
- Custom utility classes

### Component Styling

Components use:
- **Material-UI `sx` prop** for inline styles
- **Material-UI `styled`** for styled components
- **CSS modules** (if needed)

## 📊 Visualizations

### Charts Library: Recharts

Used for:
- Bar charts (sentiment distribution)
- Pie charts (sentiment percentages)
- Line charts (trends over time)
- Area charts (forecast visualization)

### Word Clouds

**Library:** `react-d3-cloud`

Used in Topic Analysis page for visualizing topic keywords.

### Icons

**Library:** `@mui/icons-material` and `react-icons`

Material-UI icons and React Icons for UI elements.

## 🔒 Authentication Flow

1. User enters credentials on Login page
2. Frontend calls `/api/auth/login`
3. Backend returns JWT token
4. Token stored in localStorage
5. Token included in `Authorization` header for all API calls
6. Protected routes check authentication status
7. Token expires after 24 hours (user must re-login)

## 📥 PDF Download

The export report feature:

1. User clicks "Export Report" button
2. Frontend calls `/api/export/report`
3. Backend generates PDF and returns base64-encoded string
4. Frontend decodes base64 to binary
5. Creates Blob and triggers download
6. User receives PDF file

**Implementation:**
```javascript
const byteCharacters = atob(response.pdf)
const byteNumbers = new Array(byteCharacters.length)
for (let i = 0; i < byteCharacters.length; i++) {
  byteNumbers[i] = byteCharacters.charCodeAt(i)
}
const byteArray = new Uint8Array(byteNumbers)
const blob = new Blob([byteArray], { type: 'application/pdf' })
const url = window.URL.createObjectURL(blob)
const link = document.createElement('a')
link.href = url
link.download = response.filename
link.click()
```

## 🏗️ Build & Deployment

### Production Build

```bash
npm run build
```

Creates optimized production build in `dist/` directory.

### Build Output

- **HTML**: `dist/index.html`
- **JavaScript**: `dist/assets/*.js` (minified and chunked)
- **CSS**: `dist/assets/*.css` (minified)
- **Static Assets**: `dist/assets/*` (images, fonts)

### Deployment Options

#### Static Hosting (Netlify, Vercel, GitHub Pages)

1. Build the project: `npm run build`
2. Deploy the `dist/` directory
3. Configure redirects for SPA routing

#### Traditional Web Server (Apache, Nginx)

1. Build the project: `npm run build`
2. Copy `dist/` contents to web server directory
3. Configure server for SPA routing

### Environment Variables

Create `.env` file for environment-specific configuration:

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_NAME=CENAnalytics
```

Access in code:
```javascript
import.meta.env.VITE_API_BASE_URL
```

## 🐛 Troubleshooting

### npm install fails

**Problem:** Installation errors or timeouts

**Solution:**
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use

**Problem:** Port 5173 already in use

**Solution:**
```bash
# Change port in vite.config.js
export default {
  server: {
    port: 3000
  }
}
```

### CORS Errors

**Problem:** CORS policy errors when calling API

**Solution:**
- Ensure backend CORS is configured
- Check API base URL in `src/services/api.js`
- Verify backend is running

### Build Errors

**Problem:** Production build fails

**Solution:**
- Check for TypeScript/ESLint errors
- Verify all imports are correct
- Check for missing dependencies

### PDF Download Not Working

**Problem:** PDF doesn't download

**Solution:**
- Check browser console for errors
- Verify API response includes `pdf` and `filename`
- Ensure browser allows downloads

### Authentication Issues

**Problem:** User gets logged out frequently

**Solution:**
- Check token expiration (24 hours default)
- Verify token is stored in localStorage
- Check for token validation errors

## 📚 Dependencies

### Core

- **react** (18.2.0): UI library
- **react-dom** (18.2.0): React DOM renderer
- **react-router-dom** (6.20.0): Routing

### UI Components

- **@mui/material** (5.15.0): Material-UI components
- **@mui/icons-material** (5.15.0): Material-UI icons
- **@emotion/react** (11.11.1): CSS-in-JS
- **@emotion/styled** (11.11.0): Styled components

### Charts & Visualization

- **recharts** (2.10.3): Chart library
- **react-d3-cloud** (1.0.6): Word cloud component

### Utilities

- **axios** (1.6.2): HTTP client
- **jwt-decode** (4.0.0): JWT token decoding
- **date-fns** (2.30.0): Date utilities
- **react-icons** (4.12.0): Icon library
- **framer-motion** (10.16.16): Animation library

### Development

- **vite** (5.0.8): Build tool
- **@vitejs/plugin-react** (4.2.1): Vite React plugin

See `package.json` for complete list.

## 🎯 Best Practices

1. **Component Structure**: Keep components small and focused
2. **State Management**: Use contexts for global state, hooks for local
3. **API Calls**: Centralize in `api.js` service
4. **Error Handling**: Always handle API errors gracefully
5. **Loading States**: Show loading indicators for async operations
6. **Responsive Design**: Test on multiple screen sizes
7. **Accessibility**: Use semantic HTML and ARIA labels
8. **Performance**: Lazy load routes and optimize images

## 📞 Support

For frontend-specific issues:

1. Check browser console for errors
2. Verify API is running and accessible
3. Check network tab for failed requests
4. Review component code for issues
5. Check [main README](../README.md) for general troubleshooting

---

**Frontend Documentation** | Part of CENAnalytics Platform

Modern React application for the CENAnalytics Business Intelligence Platform. Built with React 18, Material-UI, and Vite for a fast, responsive, and beautiful user experience.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Development](#development)
- [Project Structure](#project-structure)
- [Components](#components)
- [Pages](#pages)
- [State Management](#state-management)
- [API Integration](#api-integration)
- [Styling](#styling)
- [Build & Deployment](#build--deployment)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The frontend is a single-page application (SPA) built with React that provides:

- **Interactive Dashboard** with real-time analytics
- **Sentiment Analysis** interface for text input
- **Topic Modeling** visualization
- **Trend Forecasting** charts
- **Report Export** with PDF download
- **User Authentication** with JWT
- **Notification System** for user alerts
- **Responsive Design** for all devices

## ✨ Features

### User Interface
- 🎨 **Material-UI Components** - Modern, accessible UI components
- 🎭 **Framer Motion** - Smooth animations and transitions
- 📊 **Recharts** - Interactive charts and graphs
- ☁️ **Word Clouds** - Visual topic representation
- 📱 **Responsive Layout** - Works on desktop, tablet, and mobile

### Functionality
- 🔐 **JWT Authentication** - Secure login and token management
- 📈 **Real-Time Analytics** - Live data updates
- 📥 **PDF Export** - Download comprehensive reports
- 🔔 **Notifications** - Real-time user notifications
- 🎯 **Filtering & Search** - Advanced data filtering
- 📊 **Multiple Visualizations** - Charts, graphs, word clouds

## 📦 Installation

### Prerequisites

- **Node.js**: 16.0 or higher
- **npm** or **yarn**: Latest version

### Step 1: Install Dependencies

```bash
cd frontend
npm install
```

### Step 2: Verify Installation

```bash
npm run dev
```

The development server should start on `http://localhost:5173`

## 🚀 Development

### Start Development Server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The production build will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## 📁 Project Structure

```
frontend/
├── public/
│   └── favicon.png          # App favicon
├── src/
│   ├── components/          # Reusable components
│   │   └── Navbar.jsx      # Navigation bar
│   ├── contexts/           # React contexts
│   │   ├── AuthContext.jsx # Authentication state
│   │   └── NotificationContext.jsx # Notification state
│   ├── pages/              # Page components
│   │   ├── LandingPage.jsx
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── SentimentAnalysis.jsx
│   │   ├── TopicAnalysis.jsx
│   │   ├── TrendsInsights.jsx
│   │   ├── Profile.jsx
│   │   ├── Notifications.jsx
│   │   └── About.jsx
│   ├── services/           # API services
│   │   ├── api.js         # Main API service
│   │   └── api.ts         # TypeScript definitions (optional)
│   ├── images/            # Static images
│   ├── App.jsx            # Main app component
│   ├── main.jsx           # Entry point
│   └── index.css          # Global styles
├── index.html             # HTML template
├── package.json           # Dependencies and scripts
├── vite.config.js        # Vite configuration
└── README.md             # This file
```

## 🧩 Components

### Navbar

**Location:** `src/components/Navbar.jsx`

Main navigation component with:
- Logo and branding
- Navigation links
- User menu (profile, logout)
- Notification bell icon

### AuthContext

**Location:** `src/contexts/AuthContext.jsx`

Manages authentication state:
- User login/logout
- Token storage (localStorage)
- User information
- Protected route handling

**Usage:**
```jsx
import { useAuth } from '../contexts/AuthContext'

function MyComponent() {
  const { user, login, logout, isAuthenticated } = useAuth()
  // ...
}
```

### NotificationContext

**Location:** `src/contexts/NotificationContext.jsx`

Manages notification state:
- Fetch notifications
- Mark as read
- Real-time updates

**Usage:**
```jsx
import { useNotifications } from '../contexts/NotificationContext'

function MyComponent() {
  const { notifications, fetchNotifications, markAsRead } = useNotifications()
  // ...
}
```

## 📄 Pages

### Landing Page

**Location:** `src/pages/LandingPage.jsx`

- Hero section with project overview
- Feature highlights
- Call-to-action buttons
- Public access (no authentication required)

### Login

**Location:** `src/pages/Login.jsx`

- User authentication form
- Email and password input
- Error handling
- Redirect to dashboard on success

### Dashboard

**Location:** `src/pages/Dashboard.jsx`

Main analytics dashboard with:
- **Overview Statistics**: Total reviews, sentiment distribution
- **Interactive Charts**: Bar charts, pie charts, line graphs
- **Location Analytics**: Sentiment by location
- **Platform Analytics**: Sentiment by platform
- **Topic Analytics**: Sentiment by topic
- **Export Functionality**: PDF report generation
- **Real-Time Updates**: Refresh data button
- **Filtering**: Date range, location, platform filters

**Key Features:**
- Tabbed interface for different analytics views
- Download PDF reports
- Filter and search capabilities
- Responsive grid layout

### Sentiment Analysis

**Location:** `src/pages/SentimentAnalysis.jsx`

- Single text sentiment analysis
- Batch text analysis
- Results visualization
- Confidence scores display

### Topic Analysis

**Location:** `src/pages/TopicAnalysis.jsx`

- Topic modeling visualization
- Word clouds
- Topic distribution charts
- Topic-sentiment mapping

### Trends Insights

**Location:** `src/pages/TrendsInsights.jsx`

- Trend forecasting charts
- Historical sentiment trends
- Pattern recognition
- Predictive analytics visualization

### Profile

**Location:** `src/pages/Profile.jsx`

- User profile information
- Account settings
- Activity history

### Notifications

**Location:** `src/pages/Notifications.jsx`

- Notification list
- Mark as read functionality
- Filter by type
- Real-time updates

### About

**Location:** `src/pages/About.jsx`

- Project information
- Technology stack
- Team/author information

## 🔄 State Management

### Authentication State

Managed by `AuthContext`:
- User information
- Login status
- JWT token (stored in localStorage)

### Notification State

Managed by `NotificationContext`:
- Notification list
- Unread count
- Fetch and update functions

### Local Component State

Most components use React hooks (`useState`, `useEffect`) for local state:
- Form inputs
- Loading states
- Error messages
- UI toggles

## 🔌 API Integration

### API Service

**Location:** `src/services/api.js`

Centralized API service using Axios:

```javascript
import apiService from '../services/api'

// Login
const response = await apiService.login(email, password)

// Get dashboard stats
const stats = await apiService.getDashboardStats()

// Export report
const report = await apiService.exportReport('dashboard')
```

### Available Methods

- `login(email, password)` - User authentication
- `getCurrentUser()` - Get current user info
- `analyzeSentiment(text)` - Single text analysis
- `batchAnalyzeSentiment(texts)` - Batch analysis
- `getDashboardStats()` - Dashboard statistics
- `getLocationSentiment()` - Location analytics
- `getPlatformSentiment()` - Platform analytics
- `getTopicSentiment()` - Topic analytics
- `getTopics()` - Topic modeling results
- `getForecast()` - Trend forecasts
- `exportReport(type)` - Export PDF report
- `getNotifications()` - Get notifications
- `markNotificationRead(id)` - Mark notification as read
- `submitFeedback(data)` - Submit feedback
- `contactAdmin(data)` - Contact administrator

### API Configuration

Base URL is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api'
```

Change this for production deployment.

### Error Handling

API calls include error handling:

```javascript
try {
  const response = await apiService.getDashboardStats()
  // Handle success
} catch (error) {
  // Handle error
  console.error('API Error:', error.message)
}
```

## 🎨 Styling

### Material-UI Theme

The app uses Material-UI's default theme with custom colors:

- **Primary**: Purple (#5624d0)
- **Secondary**: Custom colors for charts
- **Typography**: Roboto font family

### Global Styles

**Location:** `src/index.css`

Contains:
- CSS reset
- Global typography
- Custom utility classes

### Component Styling

Components use:
- **Material-UI `sx` prop** for inline styles
- **Material-UI `styled`** for styled components
- **CSS modules** (if needed)

## 📊 Visualizations

### Charts Library: Recharts

Used for:
- Bar charts (sentiment distribution)
- Pie charts (sentiment percentages)
- Line charts (trends over time)
- Area charts (forecast visualization)

### Word Clouds

**Library:** `react-d3-cloud`

Used in Topic Analysis page for visualizing topic keywords.

### Icons

**Library:** `@mui/icons-material` and `react-icons`

Material-UI icons and React Icons for UI elements.

## 🔒 Authentication Flow

1. User enters credentials on Login page
2. Frontend calls `/api/auth/login`
3. Backend returns JWT token
4. Token stored in localStorage
5. Token included in `Authorization` header for all API calls
6. Protected routes check authentication status
7. Token expires after 24 hours (user must re-login)

## 📥 PDF Download

The export report feature:

1. User clicks "Export Report" button
2. Frontend calls `/api/export/report`
3. Backend generates PDF and returns base64-encoded string
4. Frontend decodes base64 to binary
5. Creates Blob and triggers download
6. User receives PDF file

**Implementation:**
```javascript
const byteCharacters = atob(response.pdf)
const byteNumbers = new Array(byteCharacters.length)
for (let i = 0; i < byteCharacters.length; i++) {
  byteNumbers[i] = byteCharacters.charCodeAt(i)
}
const byteArray = new Uint8Array(byteNumbers)
const blob = new Blob([byteArray], { type: 'application/pdf' })
const url = window.URL.createObjectURL(blob)
const link = document.createElement('a')
link.href = url
link.download = response.filename
link.click()
```

## 🏗️ Build & Deployment

### Production Build

```bash
npm run build
```

Creates optimized production build in `dist/` directory.

### Build Output

- **HTML**: `dist/index.html`
- **JavaScript**: `dist/assets/*.js` (minified and chunked)
- **CSS**: `dist/assets/*.css` (minified)
- **Static Assets**: `dist/assets/*` (images, fonts)

### Deployment Options

#### Static Hosting (Netlify, Vercel, GitHub Pages)

1. Build the project: `npm run build`
2. Deploy the `dist/` directory
3. Configure redirects for SPA routing

#### Traditional Web Server (Apache, Nginx)

1. Build the project: `npm run build`
2. Copy `dist/` contents to web server directory
3. Configure server for SPA routing

### Environment Variables

Create `.env` file for environment-specific configuration:

```env
VITE_API_BASE_URL=http://localhost:5000/api
VITE_APP_NAME=CENAnalytics
```

Access in code:
```javascript
import.meta.env.VITE_API_BASE_URL
```

## 🐛 Troubleshooting

### npm install fails

**Problem:** Installation errors or timeouts

**Solution:**
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use

**Problem:** Port 5173 already in use

**Solution:**
```bash
# Change port in vite.config.js
export default {
  server: {
    port: 3000
  }
}
```

### CORS Errors

**Problem:** CORS policy errors when calling API

**Solution:**
- Ensure backend CORS is configured
- Check API base URL in `src/services/api.js`
- Verify backend is running

### Build Errors

**Problem:** Production build fails

**Solution:**
- Check for TypeScript/ESLint errors
- Verify all imports are correct
- Check for missing dependencies

### PDF Download Not Working

**Problem:** PDF doesn't download

**Solution:**
- Check browser console for errors
- Verify API response includes `pdf` and `filename`
- Ensure browser allows downloads

### Authentication Issues

**Problem:** User gets logged out frequently

**Solution:**
- Check token expiration (24 hours default)
- Verify token is stored in localStorage
- Check for token validation errors

## 📚 Dependencies

### Core

- **react** (18.2.0): UI library
- **react-dom** (18.2.0): React DOM renderer
- **react-router-dom** (6.20.0): Routing

### UI Components

- **@mui/material** (5.15.0): Material-UI components
- **@mui/icons-material** (5.15.0): Material-UI icons
- **@emotion/react** (11.11.1): CSS-in-JS
- **@emotion/styled** (11.11.0): Styled components

### Charts & Visualization

- **recharts** (2.10.3): Chart library
- **react-d3-cloud** (1.0.6): Word cloud component

### Utilities

- **axios** (1.6.2): HTTP client
- **jwt-decode** (4.0.0): JWT token decoding
- **date-fns** (2.30.0): Date utilities
- **react-icons** (4.12.0): Icon library
- **framer-motion** (10.16.16): Animation library

### Development

- **vite** (5.0.8): Build tool
- **@vitejs/plugin-react** (4.2.1): Vite React plugin

See `package.json` for complete list.

## 🎯 Best Practices

1. **Component Structure**: Keep components small and focused
2. **State Management**: Use contexts for global state, hooks for local
3. **API Calls**: Centralize in `api.js` service
4. **Error Handling**: Always handle API errors gracefully
5. **Loading States**: Show loading indicators for async operations
6. **Responsive Design**: Test on multiple screen sizes
7. **Accessibility**: Use semantic HTML and ARIA labels
8. **Performance**: Lazy load routes and optimize images

## 📞 Support

For frontend-specific issues:

1. Check browser console for errors
2. Verify API is running and accessible
3. Check network tab for failed requests
4. Review component code for issues
5. Check [main README](../README.md) for general troubleshooting

---

**Frontend Documentation** | Part of CENAnalytics Platform
