# TASK 15: Vue3 + Vite + TypeScript Setup

**Status**: Not Started
**Estimated Time**: 4-6 hours
**Dependencies**: TASK 13 (Monorepo structure)
**Priority**: High

---

## OVERVIEW

Initialize Vue3 project with Vite and TypeScript in `/frontend` folder. Setup development environment with ESLint, Prettier, and proper folder structure.

---

## OBJECTIVES

1. Initialize Vite + Vue3 + TypeScript project
2. Configure TypeScript with strict mode
3. Setup ESLint and Prettier
4. Create folder structure
5. Configure environment variables
6. Test build and dev server

---

## QUICK START

```bash
cd frontend

# Initialize Vite project
npm create vite@latest . -- --template vue-ts

# Install dependencies
npm install

# Install dev tools
npm install -D eslint prettier eslint-plugin-vue @typescript-eslint/parser @typescript-eslint/eslint-plugin

# Install Tailwind (optional)
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Run dev server
npm run dev  # http://localhost:5173
```

---

## FOLDER STRUCTURE

```
frontend/
├── src/
│   ├── components/      # Vue components
│   ├── views/           # Page components
│   ├── stores/          # Pinia stores (TASK 17)
│   ├── router/          # Vue Router (TASK 18)
│   ├── api/             # API client
│   ├── types/           # TypeScript types
│   ├── composables/     # Reusable composition functions
│   ├── assets/          # Static assets
│   ├── styles/          # Global styles
│   ├── App.vue
│   └── main.ts
├── public/
├── index.html
├── vite.config.ts
├── tsconfig.json
├── .eslintrc.cjs
├── .prettierrc
├── package.json
└── README.md
```

---

## KEY FILES

**vite.config.ts**:
```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

**tsconfig.json**:
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

**.env**:
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=Detomo SQL AI
```

**src/main.ts**:
```typescript
import { createApp } from 'vue'
import './styles/main.css'
import App from './App.vue'

const app = createApp(App)

app.mount('#app')
```

---

## SUCCESS CRITERIA

- ✅ Vue3 app runs on http://localhost:5173
- ✅ TypeScript compilation working
- ✅ Hot module replacement working
- ✅ Build process successful
- ✅ Folder structure created
- ✅ ESLint and Prettier configured

---

**Created**: 2025-10-27
