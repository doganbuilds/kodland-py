/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Montserrat", "sans-serif"],
      },
      colors: {
        dark: "#1a1a1a",
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
