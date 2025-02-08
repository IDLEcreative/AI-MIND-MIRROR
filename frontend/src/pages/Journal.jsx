import React from 'react';
import AppLayout from '../components/Layout/AppLayout';
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
} from '@mui/material';

const Journal = () => {
  return (
    <AppLayout>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Journal
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          New Entry
        </Typography>
        <TextField
          fullWidth
          multiline
          rows={4}
          placeholder="Write your thoughts..."
          sx={{ mb: 2 }}
        />
        <Button variant="contained" color="primary">
          Save Entry
        </Button>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Recent Entries
        </Typography>
        <Typography variant="body1" color="text.secondary">
          No journal entries yet. Start writing to see your entries here.
        </Typography>
      </Paper>
      </Container>
    </AppLayout>
  );
};

export default Journal;
