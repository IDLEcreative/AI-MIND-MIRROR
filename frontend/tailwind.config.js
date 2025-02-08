/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
    './public/index.html',
  ],
  theme: {
    extend: {
      colors: {
        'mind-blue': '#2563eb',
        'mind-purple': '#7c3aed',
        'mind-mint': '#2dd4bf',
      },
    },
  },
  plugins: [],
}
