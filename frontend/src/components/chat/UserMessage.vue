<script setup lang="ts">
import { User } from '@element-plus/icons-vue'

defineProps<{
  question: string
}>()
</script>

<template>
  <div class="user-message">
    <el-avatar :size="40" class="avatar">
      <el-icon><User /></el-icon>
    </el-avatar>
    <div class="message-content">
      <p class="message-text">{{ question }}</p>
    </div>
  </div>
</template>

<style scoped>
.user-message {
  display: flex;
  gap: 12px;
  padding: 20px;
  align-items: flex-start;
  flex-direction: row-reverse;
  animation: slideInRight 0.4s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.avatar {
  flex-shrink: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  border: 2px solid #ffffff;
}

.message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 18px 18px 4px 18px;
  padding: 14px 18px;
  max-width: 70%;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
  position: relative;
}

.message-content::before {
  content: '';
  position: absolute;
  bottom: 0;
  right: -8px;
  width: 0;
  height: 0;
  border-left: 8px solid #764ba2;
  border-top: 8px solid transparent;
}

.message-text {
  margin: 0;
  color: #ffffff;
  font-size: 15px;
  line-height: 1.6;
  word-wrap: break-word;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .user-message {
    padding: 12px;
  }
  
  .message-content {
    max-width: 85%;
    padding: 12px 16px;
  }
  
  .message-text {
    font-size: 14px;
  }
}
</style>
