export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

export const formatTime = (date) => {
  return new Date(date).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  });
};

export const truncateText = (text, maxLength = 100) => {
  if (!text || text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
};

export const getMoodEmoji = (mood) => {
  const moodEmojis = {
    'very_negative': '😢',
    'negative': '😕',
    'neutral': '😐',
    'positive': '😊',
    'very_positive': '😄',
  };
  return moodEmojis[mood] || '😐';
};
