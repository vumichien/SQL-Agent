# TASK 28: Docker & Deployment

**Status**: Not Started
**Estimated Time**: 6-8 hours
**Dependencies**: TASK 27

## DOCKERFILES

### frontend/Dockerfile
```dockerfile
# Build stage
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
```

### docker-compose.yml (Production)
```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    
  frontend:
    build: ./frontend
    ports: ["80:80"]
    depends_on: [backend]
```

## CI/CD (GitHub Actions)
```yaml
name: Deploy
on: [push]
jobs:
  test:
    - Run tests
    - Build images
    - Deploy
```

## SUCCESS CRITERIA
- ✅ Docker images build
- ✅ Docker Compose working
- ✅ CI/CD pipeline working

**Created**: 2025-10-27
