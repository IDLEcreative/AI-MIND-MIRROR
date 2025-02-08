import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const options = {
  responsive: true,
  plugins: {
    legend: {
      display: false,
    },
    tooltip: {
      mode: 'index',
      intersect: false,
    },
  },
  scales: {
    y: {
      min: -1,
      max: 1,
      ticks: {
        callback: (value) => {
          const labels = {
            1: 'Very Positive',
            0.5: 'Positive',
            0: 'Neutral',
            '-0.5': 'Negative',
            '-1': 'Very Negative',
          };
          return labels[value] || '';
        },
      },
    },
  },
  interaction: {
    intersect: false,
    mode: 'index',
  },
};

const MoodChart = ({ data }) => {
  const chartData = {
    labels: data.map(d => d.date),
    datasets: [
      {
        label: 'Mood',
        data: data.map(d => d.sentiment),
        borderColor: 'rgb(99, 102, 241)',
        backgroundColor: 'rgba(99, 102, 241, 0.1)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-sm border border-gray-100">
      <h3 className="text-lg font-medium text-gray-900 mb-4">Mood Trends</h3>
      <div className="h-64">
        <Line options={options} data={chartData} />
      </div>
    </div>
  );
};

export default MoodChart;
