import React, { useState, useEffect } from 'react';
import AppLayout from '../components/Layout/AppLayout';
import { useAuth } from '../context/AuthContext';
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Tab,
  Tabs,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Chip,
  Stack,
  LinearProgress,
} from '@mui/material';
import axios from 'axios';

const Analytics = () => {
  const { user } = useAuth();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [insights, setInsights] = useState(null);
  const [synthesizedInsights, setSynthesizedInsights] = useState(null);

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch all agent insights at once
        const response = await axios.get('/api/agents/orchestrate', {
          headers: { Authorization: `Bearer ${user?.token}` }
        });

        setInsights(response.data.agent_insights);
        setSynthesizedInsights(response.data.synthesized_insights);
      } catch (err) {
        setError(err.response?.data?.message || 'Failed to fetch insights');
      } finally {
        setLoading(false);
      }
    };

    fetchInsights();
  }, [tabValue, user]);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <AppLayout>
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Analytics
      </Typography>
      
      {synthesizedInsights && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>Holistic Overview</Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="primary">Key Themes</Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap">
                {synthesizedInsights.themes.map((theme, i) => (
                  <Chip key={i} label={theme} color="primary" variant="outlined" />
                ))}
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" color="secondary">Focus Areas</Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap">
                {synthesizedInsights.focus_areas.map((area, i) => (
                  <Chip key={i} label={area} color="secondary" variant="outlined" />
                ))}
              </Stack>
            </Grid>
          </Grid>
        </Paper>
      )}

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Well-being" />
          <Tab label="Growth" />
          <Tab label="Patterns" />
        </Tabs>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {loading ? (
          <Grid item xs={12}>
            <LinearProgress />
          </Grid>
        ) : error ? (
          <Grid item xs={12}>
            <Alert severity="error">{error}</Alert>
          </Grid>
        ) : insights ? (
          <>
            {/* Well-being View */}
            {tabValue === 0 && (
              <>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>Emotional Health</Typography>
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2">Forecast</Typography>
                        <Typography>{insights.emotional_forecasts.forecast}</Typography>
                      </Box>
                      <Box>
                        <Typography variant="subtitle2">Well-being Metrics</Typography>
                        <Typography>{insights.well_being_insights.summary}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>Self-Compassion</Typography>
                      <Typography>{insights.compassion_guidance.message}</Typography>
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2">Suggested Practices</Typography>
                        <Typography>{insights.compassion_guidance.practices.join(', ')}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              </>
            )}

            {/* Growth View */}
            {tabValue === 1 && (
              <>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>Habit Development</Typography>
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2">Current Progress</Typography>
                        <Typography>{insights.habit_insights.progress}</Typography>
                      </Box>
                      <Box>
                        <Typography variant="subtitle2">Behavior Change</Typography>
                        <Typography>{insights.behavior_insights.recommendations}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>Growth Catalysts</Typography>
                      <Typography>{insights.catalyst_insights.opportunities}</Typography>
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2">Next Steps</Typography>
                        <Typography>{insights.catalyst_insights.next_steps}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              </>
            )}

            {/* Patterns View */}
            {tabValue === 2 && (
              <>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>Journal Analysis</Typography>
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="subtitle2">Key Patterns</Typography>
                        <Typography>{insights.journal_analysis.patterns}</Typography>
                      </Box>
                      <Box>
                        <Typography variant="subtitle2">Deep Insights</Typography>
                        <Typography>{insights.reflection_insights.deep_patterns}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" gutterBottom>Life Narrative</Typography>
                      <Typography>{insights.life_narrative.summary}</Typography>
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2">Emerging Themes</Typography>
                        <Typography>{insights.life_narrative.themes.join(', ')}</Typography>
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              </>
            )}
          </>
        ) : null}
      </Grid>
      </Container>
    </AppLayout>
  );
};

export default Analytics;
