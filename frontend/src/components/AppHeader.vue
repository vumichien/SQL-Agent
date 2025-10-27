<template>
  <el-header class="app-header">
    <div class="header-row">
      <div class="header-left">
        <h1 class="app-title">
          <el-icon :size="28" class="logo-icon">
            <DataAnalysis />
          </el-icon>
          {{ appTitle }}
        </h1>
      </div>
      <div class="header-right">
        <!-- Language Switcher -->
        <el-tooltip :content="t('settings.language')">
          <el-button
            class="lang-switcher"
            @click="toggleLanguage"
            circle
          >
            {{ currentLangLabel }}
          </el-button>
        </el-tooltip>

        <!-- Dark Mode Toggle -->
        <el-tooltip :content="uiStore.isDark ? t('settings.lightMode') : t('settings.darkMode')">
          <el-switch
            v-model="uiStore.isDark"
            inline-prompt
            :active-icon="Moon"
            :inactive-icon="Sunny"
          />
        </el-tooltip>

        <!-- User Profile Dropdown -->
        <el-dropdown trigger="click" @command="handleCommand">
          <el-button type="primary" :icon="User" circle />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-if="user" disabled>
                <div class="user-info">
                  <strong>{{ user.username }}</strong>
                  <small>{{ user.email }}</small>
                </div>
              </el-dropdown-item>
              <el-dropdown-item divided command="settings" :icon="Setting">
                {{ t('nav.settings') }}
              </el-dropdown-item>
              <el-dropdown-item command="logout" :icon="SwitchButton">
                {{ t('auth.logout') }}
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Moon, Sunny, User, DataAnalysis, Setting, SwitchButton } from '@element-plus/icons-vue'
import { useUIStore } from '@/stores/ui'
import { useAuthStore } from '@/stores/auth'

const { t, locale } = useI18n()
const router = useRouter()
const uiStore = useUIStore()
const authStore = useAuthStore()
const appTitle = computed(() => import.meta.env.VITE_APP_TITLE || 'Detomo SQL AI')

const user = computed(() => authStore.user)

// Current language label
const currentLangLabel = computed(() => {
  return uiStore.language === 'en' ? 'EN' : 'JA'
})

// Toggle language
const toggleLanguage = () => {
  uiStore.toggleLanguage()
}

// Handle dropdown commands
const handleCommand = async (command: string) => {
  if (command === 'settings') {
    router.push('/settings')
  } else if (command === 'logout') {
    try {
      await ElMessageBox.confirm(
        t('auth.logoutConfirm'),
        t('common.confirm'),
        {
          confirmButtonText: t('common.yes'),
          cancelButtonText: t('common.cancel'),
          type: 'warning',
        }
      )

      authStore.logout()
      ElMessage.success(t('auth.logoutSuccess'))
      router.push('/login')
    } catch {
      // User cancelled
    }
  }
}

// Watch UI store language and sync with i18n
watch(
  () => uiStore.language,
  (newLang) => {
    locale.value = newLang
  },
  { immediate: true }
)
</script>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  padding: 0 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-bottom: none;
  box-shadow: 0 2px 12px 0 rgba(102, 126, 234, 0.3);
  position: relative;
  z-index: 100;
}

.app-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
}

.header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  gap: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}


.app-title {
  margin: 0;
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 12px;
  text-shadow: 0 2px 4px rgba(0,0,0,0.2);
  letter-spacing: 0.5px;
}

.logo-icon {
  color: #ffffff;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.header-right :deep(.el-button) {
  background-color: rgba(255, 255, 255, 0.2);
  border-color: rgba(255, 255, 255, 0.3);
  color: #ffffff;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.header-right :deep(.el-button:hover) {
  background-color: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-2px);
}

.header-right :deep(.el-switch) {
  --el-switch-on-color: rgba(255, 255, 255, 0.3);
  --el-switch-off-color: rgba(255, 255, 255, 0.2);
}

.lang-switcher {
  font-weight: 600;
  font-size: 13px;
}

.user-info {
  display: flex;
  flex-direction: column;
  padding: 8px 0;
  min-width: 180px;
}

.user-info strong {
  font-size: 14px;
  color: var(--el-text-color-primary);
  font-weight: 600;
}

.user-info small {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 4px;
}

/* Responsive */
@media (max-width: 768px) {
  .app-header {
    padding: 0 16px;
  }
  
  .app-title {
    font-size: 18px;
  }
  
  .header-right {
    gap: 8px;
  }
}
</style>
