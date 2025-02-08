import React from 'react';
import { Link } from 'react-router-dom';
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

const HabitOverview = ({ habits }) => {
  if (!habits?.length) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No habits tracked yet.</p>
        <Link
          to="/habits"
          className="mt-4 inline-block text-mind-blue hover:text-mind-blue/90"
        >
          Start tracking habits
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {habits.map((habit) => (
        <div
          key={habit.id}
          className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
        >
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium text-gray-900">{habit.name}</h4>
              <p className="text-sm text-gray-500">{habit.description}</p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="text-green-500 flex items-center">
                <CheckCircleIcon className="w-5 h-5 mr-1" />
                <span className="text-sm font-medium">{habit.completed_count}</span>
              </div>
              <div className="text-red-500 flex items-center">
                <XCircleIcon className="w-5 h-5 mr-1" />
                <span className="text-sm font-medium">{habit.missed_count}</span>
              </div>
            </div>
          </div>
          <div className="mt-3">
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-mind-blue rounded-full h-2 transition-all"
                style={{
                  width: `${(habit.completed_count / (habit.completed_count + habit.missed_count)) * 100}%`,
                }}
              />
            </div>
          </div>
        </div>
      ))}
      <div className="text-right">
        <Link
          to="/habits"
          className="text-mind-blue hover:text-mind-blue/90 text-sm font-medium"
        >
          View all habits →
        </Link>
      </div>
    </div>
  );
};

export default HabitOverview;
