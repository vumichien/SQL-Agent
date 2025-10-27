<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Setting } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import PageContent from '@/components/common/PageContent.vue'
import { useUIStore } from '@/stores/ui'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const router = useRouter()
const uiStore = useUIStore()
const authStore = useAuthStore()

const user = computed(() => authStore.user)

const handleLogout = async () => {
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
</script>

<template>
  <div class="settings-view">
    <el-container class="settings-container">
      <!-- Header -->
      <PageHeader
        :title="t('settings.title')"
        :count="0"
        count-label=""
        :show-refresh="false"
      />

      <!-- Main Content -->
      <PageContent>
        <div class="settings-content">
          <!-- User Profile Section -->
          <el-card v-if="user" class="settings-card profile-card">
            <template #header>
              <div class="card-header">
                <el-icon><User /></el-icon>
                <span>{{ t('nav.profile') }}</span>
              </div>
            </template>

            <div class="profile-content">
              <el-avatar :size="80" class="profile-avatar">
                {{ user.username ? user.username.charAt(0).toUpperCase() : 'U' }}
              </el-avatar>

              <el-descriptions :column="1" border class="profile-info">
                <el-descriptions-item :label="t('auth.username')">
                  {{ user.username }}
                </el-descriptions-item>
                <el-descriptions-item :label="t('auth.email')">
                  {{ user.email }}
                </el-descriptions-item>
                <el-descriptions-item :label="t('common.date')">
                  {{ user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A' }}
                </el-descriptions-item>
              </el-descriptions>

              <el-button
                type="danger"
                :icon="Setting"
                class="logout-button"
                @click="handleLogout"
              >
                {{ t('auth.logout') }}
              </el-button>
            </div>
          </el-card>

          <!-- Appearance Settings -->
          <el-card class="settings-card appearance-card">
            <template #header>
              <span>{{ t('settings.appearance') }}</span>
            </template>

            <el-form label-position="left" label-width="120px">
              <el-form-item :label="t('settings.theme')">
                <el-switch
                  v-model="uiStore.isDark"
                  :active-text="t('settings.darkMode')"
                  :inactive-text="t('settings.lightMode')"
                />
              </el-form-item>

              <el-form-item :label="t('settings.language')">
                <el-select v-model="uiStore.language" :placeholder="t('settings.language')">
                  <el-option :label="t('settings.languageEn')" value="en" />
                  <el-option :label="t('settings.languageJa')" value="ja" />
                </el-select>
              </el-form-item>
            </el-form>
          </el-card>

          <!-- About Section -->
          <el-card class="settings-card about-card">
            <template #header>
              <span>{{ t('settings.about') }}</span>
            </template>

            <el-descriptions :column="1" border>
              <el-descriptions-item :label="t('settings.version')">3.0.0</el-descriptions-item>
              <el-descriptions-item label="Framework">Vue 3 + TypeScript</el-descriptions-item>
              <el-descriptions-item label="UI Library">Element Plus</el-descriptions-item>
              <el-descriptions-item label="Backend">FastAPI + Vanna AI</el-descriptions-item>
            </el-descriptions>
          </el-card>
        </div>
      </PageContent>
    </el-container>
  </div>
</template>

<style scoped>
.settings-view {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.settings-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

/* Settings Content */
.settings-content {
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.settings-card {
  border-radius: 16px;
  border: 1px solid var(--el-border-color-lighter);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  overflow: hidden;
  background: #ffffff;
}

.settings-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.settings-card :deep(.el-card__header) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
  border-bottom: 1px solid var(--el-border-color-lighter);
  padding: 20px 24px;
  font-weight: 600;
  font-size: 16px;
}

.settings-card :deep(.el-card__body) {
  padding: 32px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--el-text-color-primary);
}

.card-header .el-icon {
  font-size: 20px;
  color: #667eea;
}

.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
}

.profile-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-size: 36px;
  font-weight: bold;
  color: #ffffff;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
  border: 4px solid #ffffff;
}

.profile-info {
  width: 100%;
}

.profile-info :deep(.el-descriptions__label) {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.logout-button {
  margin-top: 16px;
  background: linear-gradient(135deg, #ff4d4f 0%, #f5222d 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.4);
  padding: 10px 32px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.logout-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 77, 79, 0.5);
}

.appearance-card :deep(.el-form-item__label) {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.appearance-card :deep(.el-switch) {
  --el-switch-on-color: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Dark mode */
html.dark .settings-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

html.dark .settings-card :deep(.el-card__header) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
}

/* Responsive */
@media (max-width: 768px) {
  .settings-content {
    max-width: 100%;
  }

  .settings-card :deep(.el-card__body) {
    padding: 20px;
  }

  .profile-avatar {
    width: 70px;
    height: 70px;
    font-size: 28px;
  }
}
</style>
