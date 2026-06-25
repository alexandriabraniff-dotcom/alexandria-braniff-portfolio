/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        base: '#F7F6F2',
        surface: '#EDECEA',
        surface2: '#D5D3CB',
        text: '#111111',
        muted: '#88877F',
        coral: '#C8553D',
        'coral-dark': '#A83728',
        teal: '#555550',
        'teal-dark': '#3A3A37',
        gold: '#B8935A',
        'gold-light': '#D4B483',
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        body: ['Plus Jakarta Sans', 'sans-serif'],
        serif: ['Cormorant Garant', 'serif'],
      },
    },
  },
  plugins: [],
};
