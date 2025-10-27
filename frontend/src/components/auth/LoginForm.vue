<template>
  <el-form
    ref="loginFormRef"
    :model="loginForm"
    :rules="rules"
    label-width="0"
    class="login-form"
    @submit.prevent="handleSubmit"
  >
    <el-form-item prop="username">
      <el-input
        v-model="loginForm.username"
        :placeholder="t('auth.usernamePlaceholder')"
        size="large"
        :prefix-icon="Message"
        clearable
        @keyup.enter="handleSubmit"
      >
        <template #prefix>
          <el-icon><Message /></el-icon>
        </template>
      </el-input>
    </el-form-item>

    <el-form-item prop="password">
      <el-input
        v-model="loginForm.password"
        type="password"
        :placeholder="t('auth.passwordPlaceholder')"
        size="large"
        show-password
        @keyup.enter="handleSubmit"
      >
        <template #prefix>
          <el-icon><Lock /></el-icon>
        </template>
      </el-input>
    </el-form-item>

    <el-form-item>
      <div class="form-options">
        <el-checkbox v-model="loginForm.rememberMe">
          {{ t('auth.rememberMe') }}
        </el-checkbox>
        <el-link type="primary" :underline="false" @click="$emit('forgot-password')">
          {{ t('auth.forgotPassword') }}
        </el-link>
      </div>
    </el-form-item>

    <el-form-item>
      <el-button
        type="primary"
        size="large"
        :loading="loading"
        :disabled="loading"
        native-type="submit"
        style="width: 100%"
        @click="handleSubmit"
      >
        {{ loading ? t('auth.loggingIn') : t('auth.login') }}
      </el-button>
    </el-form-item>

    <el-form-item>
      <div class="form-footer">
        <span>{{ t('auth.noAccount') }}</span>
        <el-link type="primary" :underline="false" @click="$emit('switch-to-register')">
          {{ t('auth.registerNow') }}
        </el-link>
      </div>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Message, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter, useRoute } from 'vue-router'

const { t } = useI18n()
const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

// Form ref
const loginFormRef = ref<FormInstance>()

// Form state
const loginForm = reactive({
  username: '',
  password: '',
  rememberMe: false,
})

const loading = ref(false)

// Validation rules
const rules: FormRules = {
  username: [
    {
      required: true,
      message: t('auth.usernameRequired'),
      trigger: 'blur',
    },
    {
      min: 3,
      message: t('auth.usernameMinLength'),
      trigger: ['blur', 'change'],
    },
  ],
  password: [
    {
      required: true,
      message: t('auth.passwordRequired'),
      trigger: 'blur',
    },
    {
      min: 6,
      message: t('auth.passwordMinLength'),
      trigger: ['blur', 'change'],
    },
  ],
}

// Handle form submission
const handleSubmit = async () => {
  if (!loginFormRef.value) return

  try {
    // Validate form
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    loading.value = true

    // Login
    await authStore.login(loginForm.username, loginForm.password)

    ElMessage.success(t('auth.loginSuccess'))

    // Redirect to intended page or chat
    const redirect = (route.query.redirect as string) || '/chat'
    router.push(redirect)
  } catch (error: any) {
    console.error('Login failed:', error)
    ElMessage.error(error.message || t('auth.loginFailed'))
  } finally {
    loading.value = false
  }
}

// Expose for parent component
defineExpose({
  resetForm: () => {
    loginFormRef.value?.resetFields()
  },
})

// Emits
defineEmits<{
  'switch-to-register': []
  'forgot-password': []
}>()
</script>

<style scoped>
.login-form {
  width: 100%;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.form-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  width: 100%;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-form-item:last-child) {
  margin-bottom: 0;
}
</style>
