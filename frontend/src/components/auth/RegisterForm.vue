<template>
  <el-form
    ref="registerFormRef"
    :model="registerForm"
    :rules="rules"
    label-width="0"
    class="register-form"
    @submit.prevent="handleSubmit"
  >
    <el-form-item prop="email">
      <el-input
        v-model="registerForm.email"
        :placeholder="t('auth.emailPlaceholder')"
        size="large"
        clearable
        @keyup.enter="handleSubmit"
      >
        <template #prefix>
          <el-icon><Message /></el-icon>
        </template>
      </el-input>
    </el-form-item>

    <el-form-item prop="username">
      <el-input
        v-model="registerForm.username"
        :placeholder="t('auth.usernamePlaceholder')"
        size="large"
        clearable
        @keyup.enter="handleSubmit"
      >
        <template #prefix>
          <el-icon><User /></el-icon>
        </template>
      </el-input>
    </el-form-item>

    <el-form-item prop="password">
      <el-input
        v-model="registerForm.password"
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

    <el-form-item prop="confirmPassword">
      <el-input
        v-model="registerForm.confirmPassword"
        type="password"
        :placeholder="t('auth.confirmPasswordPlaceholder')"
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
      <el-alert
        v-if="passwordStrength"
        :title="passwordStrength.message"
        :type="passwordStrength.type"
        :closable="false"
        show-icon
      />
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
        {{ loading ? t('auth.registering') : t('auth.register') }}
      </el-button>
    </el-form-item>

    <el-form-item>
      <div class="form-footer">
        <span>{{ t('auth.haveAccount') }}</span>
        <el-link type="primary" :underline="false" @click="$emit('switch-to-login')">
          {{ t('auth.loginNow') }}
        </el-link>
      </div>
    </el-form-item>
  </el-form>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { Message, Lock, User } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const authStore = useAuthStore()
const router = useRouter()

// Form ref
const registerFormRef = ref<FormInstance>()

// Form state
const registerForm = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
})

const loading = ref(false)

// Password strength indicator
const passwordStrength = computed(() => {
  const password = registerForm.password
  if (!password) return null

  let strength = 0
  let message = ''
  let type: 'success' | 'warning' | 'error' | 'info' = 'info'

  // Check length
  if (password.length >= 8) strength++
  if (password.length >= 12) strength++

  // Check complexity
  if (/[a-z]/.test(password)) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^a-zA-Z0-9]/.test(password)) strength++

  if (strength <= 2) {
    message = t('auth.passwordWeak')
    type = 'error'
  } else if (strength <= 4) {
    message = t('auth.passwordMedium')
    type = 'warning'
  } else {
    message = t('auth.passwordStrong')
    type = 'success'
  }

  return { message, type, strength }
})

// Custom validator for password confirmation
const validateConfirmPassword = (_rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error(t('auth.confirmPasswordRequired')))
  } else if (value !== registerForm.password) {
    callback(new Error(t('auth.passwordMismatch')))
  } else {
    callback()
  }
}

// Validation rules
const rules: FormRules = {
  email: [
    {
      required: true,
      message: t('auth.emailRequired'),
      trigger: 'blur',
    },
    {
      type: 'email',
      message: t('auth.emailInvalid'),
      trigger: ['blur', 'change'],
    },
  ],
  username: [
    {
      required: true,
      message: t('auth.usernameRequired'),
      trigger: 'blur',
    },
    {
      min: 3,
      max: 20,
      message: t('auth.usernameLength'),
      trigger: ['blur', 'change'],
    },
    {
      pattern: /^[a-zA-Z0-9_]+$/,
      message: t('auth.usernameInvalid'),
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
  confirmPassword: [
    {
      required: true,
      validator: validateConfirmPassword,
      trigger: ['blur', 'change'],
    },
  ],
}

// Handle form submission
const handleSubmit = async () => {
  if (!registerFormRef.value) return

  try {
    // Validate form
    const valid = await registerFormRef.value.validate()
    if (!valid) return

    loading.value = true

    // Register (this will auto-login after success)
    await authStore.register(
      registerForm.email,
      registerForm.username,
      registerForm.password
    )

    ElMessage.success(t('auth.registerSuccess'))

    // Redirect to chat
    router.push('/chat')
  } catch (error: any) {
    console.error('Registration failed:', error)
    ElMessage.error(error.message || t('auth.registerFailed'))
  } finally {
    loading.value = false
  }
}

// Expose for parent component
defineExpose({
  resetForm: () => {
    registerFormRef.value?.resetFields()
  },
})

// Emits
defineEmits<{
  'switch-to-login': []
}>()
</script>

<style scoped>
.register-form {
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
