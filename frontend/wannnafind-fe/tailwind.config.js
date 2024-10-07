/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx,scss}',  // Adjust the path as necessary for your project structure
    './src/index.html',
    './src/header/header.component.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

