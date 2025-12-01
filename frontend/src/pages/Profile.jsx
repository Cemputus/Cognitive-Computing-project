import React, { useState } from 'react'
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  TextField,
  Button,
  Avatar,
  Divider,
  Chip,
  Alert,
  Paper,
  IconButton,
  InputAdornment,
} from '@mui/material'
import {
  Person,
  Email,
  LocationOn,
  Edit,
  Save,
  Cancel,
  AddComment,
  Delete,
} from '@mui/icons-material'
import { useAuth } from '../contexts/AuthContext'
import { motion } from 'framer-motion'

const Profile = () => {
  const { user } = useAuth()
  const [editing, setEditing] = useState(false)
  const [profile, setProfile] = useState({
    name: user?.name || '',
    email: user?.email || '',
    location: 'Kampala, Uganda',
    bio: 'CENAnalytics User',
    phone: '+256 700 000 000',
    company: 'CENAnalytics',
    role: user?.role || 'user',
  })
  const [comments, setComments] = useState([
    {
      id: 1,
      text: 'Great insights from the dashboard analytics!',
      date: '2024-12-01',
    },
    {
      id: 2,
      text: 'The location-based sentiment analysis is very helpful.',
      date: '2024-11-28',
    },
  ])
  const [newComment, setNewComment] = useState('')
  const [saved, setSaved] = useState(false)

  const handleSave = () => {
    // In production, this would save to backend
    setEditing(false)
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const handleCancel = () => {
    setEditing(false)
    setProfile({
      name: user?.name || '',
      email: user?.email || '',
      location: 'Kampala, Uganda',
      bio: 'Business Intelligence Analyst',
      phone: '+256 700 000 000',
      company: 'Business Intelligence Corp',
      role: user?.role || 'user',
    })
  }

  const handleAddComment = () => {
    if (newComment.trim()) {
      setComments([
        {
          id: comments.length + 1,
          text: newComment,
          date: new Date().toISOString().split('T')[0],
        },
        ...comments,
      ])
      setNewComment('')
    }
  }

  const handleDeleteComment = (id) => {
    setComments(comments.filter((c) => c.id !== id))
  }

  return (
    <Container maxWidth="lg">
      <Box mb={4}>
        <Typography variant="h4" component="h1" gutterBottom fontWeight={700}>
          Profile Settings
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Manage your profile information and preferences
        </Typography>
      </Box>

      {saved && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Profile updated successfully!
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Profile Information */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                <Typography variant="h6" fontWeight={600}>
                  Personal Information
                </Typography>
                {!editing ? (
                  <Button
                    startIcon={<Edit />}
                    onClick={() => setEditing(true)}
                    variant="outlined"
                    size="small"
                  >
                    Edit Profile
                  </Button>
                ) : (
                  <Box display="flex" gap={1}>
                    <Button
                      startIcon={<Save />}
                      onClick={handleSave}
                      variant="contained"
                      size="small"
                      color="primary"
                    >
                      Save
                    </Button>
                    <Button
                      startIcon={<Cancel />}
                      onClick={handleCancel}
                      variant="outlined"
                      size="small"
                    >
                      Cancel
                    </Button>
                  </Box>
                )}
              </Box>

              <Divider sx={{ mb: 3 }} />

              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Box display="flex" alignItems="center" gap={2} mb={2}>
                    <Avatar
                      sx={{
                        width: 80,
                        height: 80,
                        bgcolor: 'primary.main',
                        fontSize: '2rem',
                        fontWeight: 700,
                      }}
                    >
                      {profile.name.charAt(0).toUpperCase()}
                    </Avatar>
                    <Box>
                      <Typography variant="h6" fontWeight={600}>
                        {profile.name}
                      </Typography>
                      <Chip
                        label={profile.role.toUpperCase()}
                        size="small"
                        color={profile.role === 'admin' ? 'primary' : 'default'}
                        sx={{ mt: 0.5 }}
                      />
                    </Box>
                  </Box>
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Full Name"
                    value={profile.name}
                    onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                    disabled={!editing}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Person color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Email"
                    value={profile.email}
                    onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                    disabled={!editing}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <Email color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Location"
                    value={profile.location}
                    onChange={(e) => setProfile({ ...profile, location: e.target.value })}
                    disabled={!editing}
                    InputProps={{
                      startAdornment: (
                        <InputAdornment position="start">
                          <LocationOn color="action" />
                        </InputAdornment>
                      ),
                    }}
                  />
                </Grid>

                <Grid item xs={12} md={6}>
                  <TextField
                    fullWidth
                    label="Phone"
                    value={profile.phone}
                    onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                    disabled={!editing}
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Company"
                    value={profile.company}
                    onChange={(e) => setProfile({ ...profile, company: e.target.value })}
                    disabled={!editing}
                  />
                </Grid>

                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    multiline
                    rows={4}
                    label="Bio"
                    value={profile.bio}
                    onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                    disabled={!editing}
                    placeholder="Tell us about yourself..."
                  />
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Comments Section */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight={600} gutterBottom>
                Notes & Comments
              </Typography>
              <Divider sx={{ mb: 2 }} />

              <Box mb={2}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  placeholder="Add a note or comment..."
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  size="small"
                  sx={{ mb: 1 }}
                />
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<AddComment />}
                  onClick={handleAddComment}
                  disabled={!newComment.trim()}
                >
                  Add Comment
                </Button>
              </Box>

              <Box sx={{ maxHeight: 400, overflowY: 'auto' }}>
                {comments.map((comment) => (
                  <Paper
                    key={comment.id}
                    sx={{
                      p: 2,
                      mb: 2,
                      bgcolor: 'grey.50',
                      position: 'relative',
                    }}
                  >
                    <Box display="flex" justifyContent="space-between" alignItems="start">
                      <Box flex={1}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {comment.date}
                        </Typography>
                        <Typography variant="body1">{comment.text}</Typography>
                      </Box>
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteComment(comment.id)}
                        sx={{ ml: 1 }}
                      >
                        <Delete fontSize="small" />
                      </IconButton>
                    </Box>
                  </Paper>
                ))}
                {comments.length === 0 && (
                  <Typography variant="body2" color="text.secondary" textAlign="center" py={4}>
                    No comments yet. Add your first note!
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}

export default Profile

