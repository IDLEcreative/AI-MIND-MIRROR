import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { journalAPI, habitsAPI, analyticsAPI } from '../api/client';
import AppLayout from '../components/Layout/AppLayout';
import StatCard from '../components/Dashboard/StatCard';
import RecentJournals from '../components/Dashboard/RecentJournals';
import HabitOverview from '../components/Dashboard/HabitOverview';
import MoodChart from '../components/Dashboard/MoodChart';
import {
  BookOpenIcon,
  CheckCircleIcon,
  ChartBarIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';
import { toast } from 'react-hot-toast';

const Dashboard = () => {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    journalCount: 0,
    habitCount: 0,
    completionRate: 0,
    averageMood: 0,
  });
  const [recentJournals, setRecentJournals] = useState([]);
  const [activeHabits, setActiveHabits] = useState([]);
  const [moodData, setMoodData] = useState([]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [journalStats, habitStats, moodTrends] = await Promise.all([
          analyticsAPI.getJournalStats(),
          analyticsAPI.getHabitStats(),
          analyticsAPI.getMoodTrends(),
        ]);

        setStats({
          journalCount: journalStats.data.total_entries,
          habitCount: habitStats.data.total_habits,
          completionRate: habitStats.data.completion_rate,
          averageMood: moodTrends.data.average_sentiment,
        });

        const [journals, habits] = await Promise.all([
          journalAPI.getEntries(),
          habitsAPI.getHabits(),
        ]);

        setRecentJournals(journals.data.slice(0, 3));
        setActiveHabits(habits.data.slice(0, 3));
        setMoodData(moodTrends.data.trends);
      } catch (error) {
        toast.error('Failed to load dashboard data');
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <AppLayout>
        <div className="flex items-center justify-center min-h-screen">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-mind-blue" />
        </div>
      </AppLayout>
    );
  }

  return (
    <AppLayout>
      <div className="py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
          <h1 className="text-2xl font-semibold text-gray-900">
            Welcome back, {user?.name}!
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Here's an overview of your journey
          </p>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
          {/* Stats Grid */}
          <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              title="Journal Entries"
              value={stats.journalCount}
              icon={BookOpenIcon}
            />
            <StatCard
              title="Active Habits"
              value={stats.habitCount}
              icon={CheckCircleIcon}
              color="mind-purple"
            />
            <StatCard
              title="Habit Completion"
              value={`${Math.round(stats.completionRate)}%`}
              icon={ChartBarIcon}
              trend={stats.completionRate - 70} // Compare with baseline of 70%
              color="mind-mint"
            />
            <StatCard
              title="Average Mood"
              value={stats.averageMood > 0 ? 'Positive' : stats.averageMood < 0 ? 'Negative' : 'Neutral'}
              icon={SparklesIcon}
              color={stats.averageMood > 0 ? 'green-500' : stats.averageMood < 0 ? 'red-500' : 'gray-500'}
            />
          </div>

          {/* Mood Chart */}
          <div className="mt-8">
            <MoodChart data={moodData} />
          </div>

          {/* Two Column Layout */}
          <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
            {/* Recent Journal Entries */}
            <div>
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Recent Journal Entries
              </h2>
              <RecentJournals entries={recentJournals} />
            </div>

            {/* Active Habits */}
            <div>
              <h2 className="text-lg font-medium text-gray-900 mb-4">
                Habit Tracking
              </h2>
              <HabitOverview habits={activeHabits} />
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  );
};

export default Dashboard;
