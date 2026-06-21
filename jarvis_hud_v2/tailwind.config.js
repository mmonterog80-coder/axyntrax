/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        sys: {
          bg: '#030712', // Abyssal dark
          panel: '#0A0F1C', // Dark slate glass
          border: '#164e63', // Cyan-900 border
          cyan: '#06b6d4', // Primary Cyan-500
          blue: '#2563eb', // Blue-600 secondary glow
          alert: '#ef4444', // Red-500 for errors
        }
      },
      animation: {
        'spin-slow': 'spin 15s linear infinite',
        'spin-reverse': 'spin-reverse 10s linear infinite',
        'spin-slow-reverse': 'spin-reverse 20s linear infinite',
        'pulse-glow': 'pulse-glow 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'blink': 'blink 1s step-end infinite',
        'data-stream': 'data-stream 2s linear infinite',
      },
      keyframes: {
        'spin-reverse': {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(-360deg)' },
        },
        'pulse-glow': {
          '0%, 100%': { opacity: 1, filter: 'drop-shadow(0 0 15px rgba(6, 182, 212, 0.7))' },
          '50%': { opacity: .7, filter: 'drop-shadow(0 0 5px rgba(6, 182, 212, 0.3))' },
        },
        'blink': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0 },
        },
        'data-stream': {
          '0%': { backgroundPosition: '0% 0%' },
          '100%': { backgroundPosition: '100% 100%' },
        }
      }
    },
  },
  plugins: [],
}
