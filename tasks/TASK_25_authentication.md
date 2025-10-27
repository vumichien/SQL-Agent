# TASK 25: Authentication System

**Status**: Not Started
**Estimated Time**: 10-12 hours
**Dependencies**: TASK 14, 18

## PAGES

### LoginView.vue
- Login form (El-Form)
- Email + password
- "Remember me" checkbox
- Link to register

### RegisterView.vue
- Register form
- Email + username + password
- Password confirmation
- Validation

## JWT HANDLING
```typescript
// src/api/auth.ts
export const authAPI = {
  async login(username, password) {
    const { data } = await axios.post('/api/v0/auth/login', {
      username, password
    })
    return data.access_token
  }
}
```

## SUCCESS CRITERIA
- ✅ Login/register working
- ✅ JWT stored securely
- ✅ Protected routes working
- ✅ Token refresh working

**Created**: 2025-10-27
