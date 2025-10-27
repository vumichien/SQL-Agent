<template>
  <div class="auth-container">
    <el-card class="auth-card" shadow="hover">
      <div class="auth-header">
        <img src="/detomo_logo.svg" alt="Detomo" class="logo" />
        <h1>{{ t('auth.createAccount') }}</h1>
        <p>{{ t('auth.registerSubtitle') }}</p>
      </div>

      <RegisterForm ref="registerFormRef" @switch-to-login="goToLogin" />
    </el-card>

    <div class="auth-footer">
      <span>© 2025 Detomo SQL AI. All rights reserved.</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import RegisterForm from '@/components/auth/RegisterForm.vue'

const { t } = useI18n()
const router = useRouter()
const registerFormRef = ref()

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 450px;
  padding: 40px 32px;
  border-radius: 16px;
}

:deep(.el-card__body) {
  padding: 0;
}

.auth-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 24px;
}

.auth-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin: 0 0 8px 0;
}

.auth-header p {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin: 0;
}

.auth-footer {
  margin-top: 24px;
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
}

/* Dark mode adjustments */
html.dark .auth-container {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

/* Responsive */
@media (max-width: 768px) {
  .auth-card {
    max-width: 100%;
    padding: 32px 24px;
  }

  .logo {
    width: 60px;
    height: 60px;
  }

  .auth-header h1 {
    font-size: 24px;
  }
}
</style>
