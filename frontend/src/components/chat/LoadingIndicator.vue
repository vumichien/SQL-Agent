<script setup lang="ts">
import { Loading } from '@element-plus/icons-vue'
// Loading indicator with typing animation
</script>

<template>
  <div class="loading-indicator">
    <el-avatar :size="40" class="avatar">
      <el-icon><Loading /></el-icon>
    </el-avatar>
    <div class="loading-content">
      <div class="typing-dots">
        <span></span>
        <span></span>
        <span></span>
      </div>
      <p class="loading-text">Generating SQL query...</p>
    </div>
  </div>
</template>

<style scoped>
.loading-indicator {
  display: flex;
  gap: 12px;
  padding: 20px;
  align-items: flex-start;
  animation: fadeIn 0.4s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.avatar {
  flex-shrink: 0;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
  border: 2px solid #ffffff;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.loading-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #ffffff;
  border-radius: 16px;
  padding: 16px 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--el-border-color-lighter);
}

.typing-dots {
  display: flex;
  gap: 6px;
  align-items: center;
}

.typing-dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  animation: typing 1.4s infinite ease-in-out;
  box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%,
  60%,
  100% {
    opacity: 0.3;
    transform: scale(0.7) translateY(0);
  }
  30% {
    opacity: 1;
    transform: scale(1.1) translateY(-5px);
  }
}

.loading-text {
  margin: 0;
  color: var(--el-text-color-regular);
  font-size: 14px;
  font-weight: 500;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Dark mode adjustments */
html.dark .loading-content {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}
</style>
