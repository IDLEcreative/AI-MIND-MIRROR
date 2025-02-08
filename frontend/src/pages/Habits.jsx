import React from 'react';
import AppLayout from '../components/Layout/AppLayout';
import {
  Container,
  Typography,
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
  Button,
  Divider,
  IconButton,
} from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const Habits = () => {
  return (
    <AppLayout>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Habits
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
        >
          New Habit
        </Button>
      </Box>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Active Habits
        </Typography>
        <List>
          <ListItem
            secondaryAction={
              <IconButton edge="end" color="primary">
                <CheckCircleIcon />
              </IconButton>
            }
          >
            <ListItemText
              primary="Example Habit"
              secondary="Daily • Not completed today"
            />
          </ListItem>
          <Divider />
          <ListItem>
            <ListItemText
              primary="No active habits"
              secondary="Click 'New Habit' to start tracking a habit"
            />
          </ListItem>
        </List>
      </Paper>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Completed Habits
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Complete habits to see them here.
        </Typography>
      </Paper>
      </Container>
    </AppLayout>
  );
};

export default Habits;
