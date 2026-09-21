/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        paper: "#f5f8f7",
        ink: "#173330",
        line: "#dbe8e5",
        teal: {
          50: "#edf7f5",
          100: "#d8eeea",
          500: "#2c6f67",
          600: "#245d57",
          700: "#1c4c47",
        },
        "risk-low": "#4c7a4a",
        "risk-lowBg": "#eaf4e8",
        "risk-mid": "#b8862e",
        "risk-midBg": "#fff6df",
        "risk-high": "#b3452f",
        "risk-highBg": "#fcece8",
      },
      fontFamily: {
        display: ["Georgia", "serif"],
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
