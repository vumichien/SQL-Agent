# TASK 16: Element Plus Integration

**Status**: Not Started
**Estimated Time**: 3-4 hours
**Dependencies**: TASK 15 (Vue3 setup)

## OVERVIEW
Integrate Element Plus UI library with auto-import and dark mode support.

## INSTALLATION
```bash
cd frontend
npm install element-plus
npm install -D unplugin-vue-components unplugin-auto-import
```

## KEY IMPLEMENTATION

**vite.config.ts** - Auto-import:
```typescript
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
})
```

**src/main.ts** - Dark mode:
```typescript
import 'element-plus/theme-chalk/dark/css-vars.css'
```

## BASE LAYOUT COMPONENTS
- AppHeader.vue
- AppSidebar.vue  
- AppMain.vue
- AppLayout.vue (combines all)

## SUCCESS CRITERIA
- ✅ Element Plus components auto-imported
- ✅ Dark mode working
- ✅ Base layout rendering
- ✅ Theme customization working

**Created**: 2025-10-27
