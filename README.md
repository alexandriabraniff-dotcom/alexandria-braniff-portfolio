# Alexandria Braniff — Portfolio Website

Personal portfolio website for Alexandria Braniff, web developer based in Adelaide, South Australia.

## Tech Stack

- **Framework**: [Astro](https://astro.build/) v4
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) v3 with custom design tokens
- **Fonts**: Syne (display) + Plus Jakarta Sans (body) via Google Fonts
- **Deployment**: [Vercel](https://vercel.com/)
- **Contact form**: [Formspree](https://formspree.io/)

---

## Local Development

### Requirements

- Node.js 18 or higher
- pnpm (recommended) — install with `npm install -g pnpm`

### Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/alexandria-braniff-portfolio.git
cd alexandria-braniff-portfolio

# Install dependencies
pnpm install

# Start dev server
pnpm dev
```

The site will be available at `http://localhost:4321`.

---

## Build and Deploy

### Build for production

```bash
pnpm build
```

Output goes to `./dist/`.

### Preview the production build locally

```bash
pnpm preview
```

### Deploy to Vercel

**Option 1 — Vercel CLI:**

```bash
npm install -g vercel
vercel
```

Follow the prompts. On subsequent deploys, run `vercel --prod`.

**Option 2 — Import from GitHub:**

1. Push the repo to GitHub.
2. Go to [vercel.com/new](https://vercel.com/new).
3. Import the GitHub repository.
4. Vercel auto-detects Astro — no additional config needed.
5. Click Deploy.

---

## Placeholders to Fill In

Before going live, complete the following:

### 1. Contact form endpoint

Open `src/pages/contact.astro` and replace `YOUR_FORM_ID` in the form `action` attribute with your actual Formspree form ID:

```html
<!-- Find this line: -->
<form action="https://formspree.io/f/YOUR_FORM_ID" ...>

<!-- Replace YOUR_FORM_ID with your real ID, e.g.: -->
<form action="https://formspree.io/f/xabcdefg" ...>
```

To get a form ID: sign up at [formspree.io](https://formspree.io), create a new form, and copy the endpoint ID.

### 2. Project screenshots

Add project images to `public/images/projects/`. The expected filenames are:

- `public/images/projects/beachside-jiujitsu.jpg` — real project (priority)
- `public/images/projects/local-bakery.jpg`
- `public/images/projects/independent-boutique.jpg`
- `public/images/projects/trades-business.jpg`
- `public/images/projects/restaurant-bar.jpg`
- `public/images/projects/health-wellness-studio.jpg`

Recommended dimensions: 1280x720px (16:9 ratio). JPG or WebP both work.

### 3. Portfolio coming soon entries

5 placeholder entries in `src/data/projects.json` are ready for real projects. See "Adding a new project" below.

### 4. Site URL

Once you have a custom domain, update `astro.config.mjs`:

```js
export default defineConfig({
  integrations: [tailwind()],
  site: 'https://your-actual-domain.com', // Update this
});
```

---

## Adding a New Portfolio Project

Open `src/data/projects.json` and add a new entry to the array. A complete entry looks like this:

```json
{
  "id": "your-project-slug",
  "name": "Client Business Name",
  "blurb": "A short one-line description under 60 characters.",
  "image": "/images/projects/your-project-slug.jpg",
  "url": "https://their-live-site.com",
  "comingSoon": false,
  "detail": {
    "business": "A paragraph about the client's business and what they needed.",
    "built": "What tech you used and how you built it.",
    "notable": "What makes this project stand out or an interesting build note."
  }
}
```

**Key rules:**
- `id` must be unique and URL-safe (lowercase, hyphens only)
- `image` path must match a file in `public/images/projects/`
- `comingSoon: false` means the card is fully interactive with modal support
- `comingSoon: true` renders a styled placeholder card — set `url: null` and `detail: null`

To replace a coming-soon placeholder with a real project, simply update the relevant entry: set `comingSoon: false`, add the real `url` and `detail` fields, and add the project image to `public/images/projects/`.
