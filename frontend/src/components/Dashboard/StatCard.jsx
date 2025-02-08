import React from 'react';

const StatCard = ({ title, value, icon: Icon, trend, color = 'mind-blue' }) => {
  return (
    <div className={`p-6 bg-white rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {Icon && (
            <div className={`p-3 rounded-full bg-${color}/10`}>
              <Icon className={`w-6 h-6 text-${color}`} />
            </div>
          )}
          <div>
            <p className="text-sm font-medium text-gray-600">{title}</p>
            <h3 className="text-2xl font-bold text-gray-900">{value}</h3>
          </div>
        </div>
        {trend && (
          <div className={`flex items-center ${
            trend > 0 ? 'text-green-500' : trend < 0 ? 'text-red-500' : 'text-gray-500'
          }`}>
            {trend > 0 ? '↑' : trend < 0 ? '↓' : '−'}
            <span className="ml-1 text-sm font-medium">
              {Math.abs(trend)}%
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default StatCard;
