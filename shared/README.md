# Shared - Common Types and Constants

**Status**: Not Started

This directory will contain shared code between backend and frontend.

## Purpose

- TypeScript type definitions shared between frontend and backend
- Constants used across the application
- Common utilities that don't belong to frontend or backend specifically

## Planned Structure

```
shared/
├── types/
│   ├── api.ts           # API request/response types
│   ├── database.ts      # Database schema types
│   ├── query.ts         # Query-related types
│   └── user.ts          # User types
├── constants/
│   ├── routes.ts        # API route constants
│   ├── config.ts        # Shared configuration
│   └── errors.ts        # Error codes/messages
└── utils/
    └── validators.ts    # Shared validation functions
```

## Usage

### In Backend (Python)

For backend, types will be defined using Pydantic models.
This folder serves mainly as a reference.

### In Frontend (TypeScript)

```typescript
import type { QueryResponse } from '@/shared/types/api'
import { API_ROUTES } from '@/shared/constants/routes'
```

## Next Steps

Types will be added as needed during:
- TASK_14: Backend Refactor (Pydantic models)
- TASK_15: Vue3 Setup (TypeScript types)
- TASK_17: Pinia Stores (State types)
