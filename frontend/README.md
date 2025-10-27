# Detomo SQL AI - Frontend (Vue3 + TypeScript)

**Status**: ✅ TASK 15 Completed - Base Setup Done
**Version**: 3.0.0

Modern Vue 3 frontend application for Detomo SQL AI, built with TypeScript and Vite.

## Tech Stack

- **Framework**: Vue 3.5+ (Composition API with `<script setup>`)
- **Build Tool**: Vite 7.1+
- **Language**: TypeScript 5.9+ (Strict Mode)
- **UI Library**: Element Plus (TASK 16 - Not installed yet)
- **State Management**: Pinia (TASK 17 - Not installed yet)
- **Routing**: Vue Router (TASK 18 - Not installed yet)
- **Internationalization**: Vue I18n (TASK 24 - Not installed yet)
- **Code Quality**: ESLint + Prettier
- **Testing**: Vitest + Playwright (TASK 26-27 - Not installed yet)

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable Vue components
│   ├── views/            # Page components (router views)
│   ├── stores/           # Pinia stores (state management)
│   ├── router/           # Vue Router configuration
│   ├── api/              # API client and services
│   ├── types/            # TypeScript type definitions
│   ├── composables/      # Composition API composables
│   ├── assets/           # Images, fonts, static files
│   ├── styles/           # Global CSS styles
│   │   └── main.css      # Global styles
│   ├── App.vue           # Root component
│   ├── main.ts           # Application entry point
│   └── vite-env.d.ts     # Vite environment types
│
├── public/               # Static assets (served as-is)
├── dist/                 # Build output (generated)
│
├── .eslintrc.cjs         # ESLint configuration
├── .prettierrc           # Prettier configuration
├── tsconfig.json         # TypeScript config (app)
├── tsconfig.node.json    # TypeScript config (build tools)
├── vite.config.ts        # Vite configuration
├── package.json          # Dependencies and scripts
├── .env                  # Environment variables (local)
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Getting Started

### Prerequisites

- Node.js 18+ (tested with v22.18.0)
- npm 10+ (tested with v10.9.3)

### Installation

```bash
cd frontend
npm install
```

### Development

Start the development server with hot-module replacement:

```bash
npm run dev
```

The app will be available at http://localhost:5173

API requests to `/api/*` are proxied to `http://localhost:8000` (backend server).

### Build for Production

Build the app for production:

```bash
npm run build
```

Output will be in the `dist/` directory.

### Preview Production Build

Preview the production build locally:

```bash
npm run preview
```

### Code Quality

Lint and fix code:

```bash
npm run lint
```

Format code with Prettier:

```bash
npm run format
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=Detomo SQL AI
VITE_APP_VERSION=3.0.0
```

Access in code:

```typescript
import.meta.env.VITE_API_BASE_URL
```

## Configuration

### TypeScript

TypeScript is configured in strict mode with the following features:
- Strict type checking
- Unused variable warnings
- No implicit any
- Path aliases: `@/` → `src/`

### Vite

Vite configuration includes:
- Vue plugin for SFC support
- Path alias: `@` → `./src`
- API proxy: `/api` → `http://localhost:8000`
- Dev server on port 5173
- Source maps enabled in production
- Code splitting (Vue vendor chunk)

### ESLint

ESLint is configured with:
- Vue 3 recommended rules
- TypeScript recommended rules
- Prettier integration (no style conflicts)

### Code Style (Prettier)

- No semicolons
- Single quotes
- 100 character line width
- 2 space indentation

## API Integration

API calls are made to the FastAPI backend running on port 8000.

Example API client (to be implemented in TASK 19+):

```typescript
// src/api/client.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export async function query(question: string) {
  const response = await fetch(`${API_BASE_URL}/api/v0/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question })
  })
  return response.json()
}
```

## Development Workflow

1. Start backend server: `cd backend && python main.py`
2. Start frontend dev server: `cd frontend && npm run dev`
3. Open browser: http://localhost:5173
4. Make changes - hot reload will update automatically

## Next Tasks

- **TASK 16**: Element Plus Integration - UI component library
- **TASK 17**: Pinia Store Setup - State management
- **TASK 18**: Vue Router Setup - Client-side routing
- **TASK 19**: Chat Interface Components - Main UI
- **TASK 20**: SQL Display & Results Table - Query results
- **TASK 21**: Plotly Visualization - Charts
- **TASK 22**: Query History Sidebar - History management
- **TASK 23**: Training Data Management - Admin UI
- **TASK 24**: Theme & i18n - Dark mode + Japanese support
- **TASK 25**: Authentication System - Login/Register
- **TASK 26**: Frontend Testing (Vitest) - Unit tests
- **TASK 27**: E2E Testing (Playwright) - End-to-end tests
- **TASK 28**: Docker & Deployment - Production setup

## Contributing

1. Follow the TypeScript strict mode guidelines
2. Use Composition API with `<script setup>` syntax
3. Run `npm run lint` before committing
4. Write meaningful commit messages
5. Keep components small and focused

## License

ISC

---

**Last Updated**: 2025-10-27 (TASK 15 Completed)
