<template>
  <el-aside :width="uiStore.isSidebarCollapsed ? '64px' : '200px'" class="app-sidebar">
    <div class="sidebar-content">
      <el-menu
        :default-active="activeIndex"
        :collapse="uiStore.isSidebarCollapsed"
        :collapse-transition="false"
        class="sidebar-menu"
        router
      >
        <el-menu-item index="/chat">
          <el-icon><ChatDotRound /></el-icon>
          <template #title>{{ t('nav.chat') }}</template>
        </el-menu-item>
        <el-menu-item index="/history">
          <el-icon><Clock /></el-icon>
          <template #title>{{ t('nav.history') }}</template>
        </el-menu-item>
        <el-menu-item index="/training">
          <el-icon><Document /></el-icon>
          <template #title>{{ t('nav.training') }}</template>
        </el-menu-item>
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <template #title>{{ t('nav.settings') }}</template>
        </el-menu-item>
      </el-menu>
      
      <div class="sidebar-footer">
        <div class="collapse-btn">
          <el-button
            :icon="uiStore.isSidebarCollapsed ? Expand : Fold"
            circle
            size="small"
            @click="uiStore.toggleSidebar"
          />
        </div>
      </div>
    </div>
  </el-aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import {
  ChatDotRound,
  Clock,
  Document,
  Setting,
  Expand,
  Fold
} from '@element-plus/icons-vue'
import { useUIStore } from '@/stores/ui'

const { t } = useI18n()
const route = useRoute()
const uiStore = useUIStore()

// Get current active menu index from route
const activeIndex = computed(() => route.path)
</script>

<style scoped>
.app-sidebar {
  position: relative;
  background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
  border-right: 1px solid var(--el-border-color-light);
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.04);
  height: 100%;
  display: flex;
  flex-direction: column;
}

.sidebar-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.sidebar-menu {
  border-right: none;
  flex: 1;
  background: transparent;
  padding: 12px 8px;
  overflow-y: auto;
}

.sidebar-menu :deep(.el-menu-item) {
  border-radius: 8px;
  margin-bottom: 4px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  transform: translateX(4px);
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.sidebar-menu :deep(.el-menu-item.is-active .el-icon) {
  color: #ffffff;
}

.sidebar-footer {
  padding: 16px 0;
  border-top: 1px solid var(--el-border-color-light);
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(10px);
}

.collapse-btn {
  display: flex;
  justify-content: center;
  align-items: center;
}

.collapse-btn :deep(.el-button) {
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color);
  transition: all 0.3s ease;
}

.collapse-btn :deep(.el-button:hover) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  border-color: transparent;
  transform: scale(1.1);
}

/* Dark mode adjustments */
html.dark .app-sidebar {
  background: linear-gradient(180deg, #1a1a1a 0%, #2d2d2d 100%);
}

html.dark .sidebar-menu :deep(.el-menu-item:hover) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
}

html.dark .sidebar-footer {
  background: rgba(0, 0, 0, 0.3);
  border-top-color: rgba(255, 255, 255, 0.1);
}

/* Scrollbar for menu */
.sidebar-menu::-webkit-scrollbar {
  width: 4px;
}

.sidebar-menu::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-menu::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}
</style>
