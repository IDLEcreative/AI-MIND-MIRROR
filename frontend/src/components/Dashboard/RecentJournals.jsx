import React from 'react';
import { Link } from 'react-router-dom';
import { formatDate, truncateText, getMoodEmoji } from '../../utils/formatters';

const RecentJournals = ({ entries }) => {
  if (!entries?.length) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No journal entries yet.</p>
        <Link
          to="/journal"
          className="mt-4 inline-block text-mind-blue hover:text-mind-blue/90"
        >
          Write your first entry
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {entries.map((entry) => (
        <div
          key={entry.id}
          className="bg-white p-4 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center space-x-2">
                <span className="text-2xl" role="img" aria-label={`Mood: ${entry.mood}`}>
                  {getMoodEmoji(entry.mood)}
                </span>
                <span className="text-sm text-gray-500">
                  {formatDate(entry.created_at)}
                </span>
              </div>
              <p className="mt-2 text-gray-700">{truncateText(entry.entry_text)}</p>
              {entry.ai_reflection && (
                <div className="mt-2 text-sm text-gray-600 italic">
                  "{truncateText(entry.ai_reflection, 120)}"
                </div>
              )}
            </div>
          </div>
          <div className="mt-3 flex justify-end">
            <Link
              to={`/journal/${entry.id}`}
              className="text-mind-blue hover:text-mind-blue/90 text-sm font-medium"
            >
              Read more →
            </Link>
          </div>
        </div>
      ))}
    </div>
  );
};

export default RecentJournals;
