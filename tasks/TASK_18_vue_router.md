# TASK 18: Vue Router Setup

**Status**: Not Started
**Estimated Time**: 3-4 hours  
**Dependencies**: TASK 17 (Pinia stores)

## OVERVIEW
Setup Vue Router with authentication guards and route transitions.

## INSTALLATION
```bash
npm install vue-router@4
```

## ROUTES
```typescript
const routes = [
  { path: '/', redirect: '/chat' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { 
    path: '/chat', 
    component: ChatView,
    meta: { requiresAuth: true }
  },
  {
    path: '/history',
    component: HistoryView, 
    meta: { requiresAuth: true }
  },
  {
    path: '/training',
    component: TrainingView,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    component: SettingsView,
    meta: { requiresAuth: true }
  },
  { path: '/:pathMatch(.*)*', component: NotFoundView }
]
```

## AUTH GUARD
```typescript
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})
```

## SUCCESS CRITERIA
- ✅ All routes working
- ✅ Protected routes working
- ✅ Navigation guards functional
- ✅ Smooth transitions

**Created**: 2025-10-27
