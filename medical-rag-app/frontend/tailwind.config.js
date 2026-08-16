/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      // Design tokens - same palette used across the whole app.
      colors: {
        teal: {
          900: "#0b3f38",
          700: "#0f6e63",
          500: "#2e9e8f",
          100: "#e3f2ef",
        },
        bg: "#f4f7f7",
        surface: "#ffffff",
        ink: "#16302c",
        "ink-soft": "#5b7370",
        border: "#d8e4e2",
        amber: {
          DEFAULT: "#c48a2b",
          bg: "#fbf1de",
        },
      },
      fontFamily: {
        display: ["var(--font-display)", "sans-serif"],
        body: ["var(--font-body)", "sans-serif"],
        mono: ["var(--font-mono)", "monospace"],
      },
      keyframes: {
        "draw-ecg": {
          "0%": { strokeDashoffset: "220" },
          "55%": { strokeDashoffset: "0" },
          "100%": { strokeDashoffset: "-220" },
        },
      },
      animation: {
        "draw-ecg": "draw-ecg 2.4s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};
