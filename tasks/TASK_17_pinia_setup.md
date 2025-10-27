# TASK 17: Pinia Store Setup

**Status**: Not Started  
**Estimated Time**: 4-6 hours
**Dependencies**: TASK 15 (Vue3 setup)

## OVERVIEW
Setup Pinia for state management with TypeScript support and persistence.

## INSTALLATION
```bash
npm install pinia
npm install pinia-plugin-persistedstate
```

## STORES TO CREATE

### 1. useAuthStore (src/stores/auth.ts)
```typescript
interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

Actions: login(), logout(), register(), refreshToken()
```

### 2. useQueryStore (src/stores/query.ts)
```typescript
interface QueryState {
  currentQuery: Query | null
  history: Query[]
  isLoading: boolean
}

Actions: sendQuery(), loadHistory(), clearHistory()
```

### 3. useTrainingStore (src/stores/training.ts)
```typescript
interface TrainingState {
  trainingData: TrainingItem[]
  count: number
}

Actions: fetchTraining(), addTraining(), removeTraining()
```

### 4. useUIStore (src/stores/ui.ts)
```typescript
interface UIState {
  theme: 'light' | 'dark'
  language: 'en' | 'ja'
  sidebarCollapsed: boolean
}

Actions: toggleTheme(), setLanguage(), toggleSidebar()
```

## MAIN.TS
```typescript
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
```

## SUCCESS CRITERIA
- ✅ All stores functional
- ✅ State persistence working
- ✅ TypeScript types correct
- ✅ Reactivity working

**Created**: 2025-10-27
