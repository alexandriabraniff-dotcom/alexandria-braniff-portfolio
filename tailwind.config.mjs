/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        base: '#0E0E10',
        surface: '#1A1A1E',
        surface2: '#252529',
        text: '#F5F5F3',
        muted: '#A1A1AA',
        coral: '#FF6F61',
        'coral-dark': '#E85A4C',
        teal: '#2DD4BF',
        'teal-dark': '#1BB8A5',
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        body: ['Plus Jakarta Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
