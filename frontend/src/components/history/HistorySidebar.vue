<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import { Search, Delete, Refresh, ChatDotRound } from '@element-plus/icons-vue'
import { useQueryStore } from '@/stores/query'
import HistoryItem from './HistoryItem.vue'

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'load-query': [id: string]
}>()

const queryStore = useQueryStore()
const searchQuery = ref('')

// Computed visible state
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// Filtered history based on search
const filteredHistory = computed(() => {
  if (!searchQuery.value.trim()) {
    return queryStore.history
  }

  const query = searchQuery.value.toLowerCase()
  return queryStore.history.filter((item) => {
    return (
      item.question.toLowerCase().includes(query) ||
      item.sql?.toLowerCase().includes(query)
    )
  })
})

// Check if a query is currently active
const isQueryActive = (id: string) => {
  return queryStore.currentQuery?.id === id
}

// Handle load query
const handleLoadQuery = (id: string) => {
  emit('load-query', id)
  // Close drawer on mobile after loading
  if (window.innerWidth < 768) {
    visible.value = false
  }
}

// Handle delete query
const handleDeleteQuery = async (id: string) => {
  try {
    await ElMessageBox.confirm(
      'This query will be permanently removed from your history.',
      'Delete this query?',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
        customClass: 'modern-delete-dialog',
        confirmButtonClass: 'modern-delete-button',
        cancelButtonClass: 'modern-cancel-button',
        center: true,
        dangerouslyUseHTMLString: true,
        showClose: false,
        autofocus: false,
        distinguishCancelAndClose: true,
        appendTo: 'body',
        lockScroll: true,
        closeOnClickModal: false,
        closeOnPressEscape: true
      }
    )

    queryStore.deleteQueryFromHistory(id)
    ElMessage({
      message: 'Query deleted successfully',
      type: 'success',
      customClass: 'modern-success-message',
      duration: 2000
    })
  } catch (error) {
    // User cancelled - no action needed
  }
}

// Handle clear all history
const handleClearAll = async () => {
  if (queryStore.history.length === 0) {
    ElMessage({
      message: 'History is already empty',
      type: 'info',
      customClass: 'modern-info-message',
      duration: 2000
    })
    return
  }

  try {
    await ElMessageBox.confirm(
      `You are about to delete <strong>${queryStore.history.length}</strong> ${queryStore.history.length === 1 ? 'query' : 'queries'}. This action cannot be undone.`,
      'Clear all history?',
      {
        confirmButtonText: 'Clear All',
        cancelButtonText: 'Cancel',
        type: 'warning',
        customClass: 'modern-delete-dialog',
        confirmButtonClass: 'modern-delete-button',
        cancelButtonClass: 'modern-cancel-button',
        center: true,
        dangerouslyUseHTMLString: true,
        showClose: false,
        autofocus: false,
        distinguishCancelAndClose: true,
        appendTo: 'body',
        lockScroll: true,
        closeOnClickModal: false,
        closeOnPressEscape: true
      }
    )

    queryStore.clearHistory()
    ElMessage({
      message: 'All history cleared',
      type: 'success',
      customClass: 'modern-success-message',
      duration: 2000
    })
  } catch (error) {
    // User cancelled - no action needed
  }
}

// Handle refresh history (load from backend)
const handleRefresh = async () => {
  try {
    await queryStore.loadHistory()
    ElMessage({
      message: 'History refreshed',
      type: 'success',
      customClass: 'modern-success-message',
      duration: 2000
    })
  } catch (error) {
    ElMessage({
      message: 'Failed to refresh history',
      type: 'error',
      customClass: 'modern-error-message',
      duration: 2000
    })
  }
}
</script>

<template>
  <el-drawer
    v-model="visible"
    title="Query History"
    direction="rtl"
    size="400px"
    :with-header="true"
    class="history-drawer"
  >
    <template #header>
      <div class="drawer-header">
        <h3>Query History</h3>
        <div class="header-actions">
          <el-tooltip content="Refresh history" placement="bottom">
            <el-button :icon="Refresh" size="small" circle @click="handleRefresh" />
          </el-tooltip>
          <el-tooltip content="Clear all" placement="bottom">
            <el-button
              :icon="Delete"
              size="small"
              circle
              type="danger"
              :disabled="queryStore.history.length === 0"
              @click="handleClearAll"
            />
          </el-tooltip>
        </div>
      </div>
    </template>

    <!-- Search bar -->
    <div class="search-container">
      <el-input
        v-model="searchQuery"
        :prefix-icon="Search"
        placeholder="Search questions or SQL..."
        clearable
        size="large"
      />
    </div>

    <!-- History count -->
    <div class="history-count">
      <span v-if="searchQuery.trim()">
        {{ filteredHistory.length }} of {{ queryStore.history.length }} queries
      </span>
      <span v-else>
        {{ queryStore.history.length }} {{ queryStore.history.length === 1 ? 'query' : 'queries' }}
      </span>
    </div>

    <!-- History list -->
    <div class="history-list">
      <!-- Empty state -->
      <div v-if="queryStore.history.length === 0" class="empty-state">
        <el-empty description="No query history yet">
          <template #image>
            <el-icon :size="80" color="var(--el-text-color-secondary)">
              <ChatDotRound />
            </el-icon>
          </template>
          <p class="empty-text">Your query history will appear here</p>
        </el-empty>
      </div>

      <!-- No search results -->
      <div v-else-if="filteredHistory.length === 0" class="empty-state">
        <el-empty description="No matching queries found">
          <el-button type="primary" @click="searchQuery = ''">Clear Search</el-button>
        </el-empty>
      </div>

      <!-- History items -->
      <div v-else class="history-items">
        <HistoryItem
          v-for="query in filteredHistory"
          :key="query.id"
          :query="query"
          :active="isQueryActive(query.id)"
          @load="handleLoadQuery"
          @delete="handleDeleteQuery"
        />
      </div>
    </div>
  </el-drawer>
</template>

<style scoped>
.history-drawer :deep(.el-drawer__header) {
  margin-bottom: 0;
  padding: 20px;
  border-bottom: 1px solid var(--el-border-color);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.drawer-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.header-actions {
  display: flex;
  gap: 8px;
}

.search-container {
  padding: 16px 20px;
  border-bottom: 1px solid var(--el-border-color);
}

.history-count {
  padding: 12px 20px;
  font-size: 13px;
  color: var(--el-text-color-secondary);
  border-bottom: 1px solid var(--el-border-color);
}

.history-list {
  padding: 16px 20px;
  height: calc(100vh - 220px);
  overflow-y: auto;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-text {
  margin-top: 16px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.history-items {
  display: flex;
  flex-direction: column;
}

/* Scrollbar styling */
.history-list::-webkit-scrollbar {
  width: 6px;
}

.history-list::-webkit-scrollbar-track {
  background: var(--el-fill-color-light);
  border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb {
  background: var(--el-border-color-darker);
  border-radius: 3px;
}

.history-list::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color-extra-light);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .history-drawer :deep(.el-drawer) {
    width: 90% !important;
  }

  .history-list {
    height: calc(100vh - 200px);
  }
}
</style>

<style>
/* Modern Delete Confirmation Dialog */
.modern-delete-dialog {
  border-radius: 16px !important;
  padding: 0 !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  max-width: 420px !important;
  width: calc(100% - 24px) !important;
  position: fixed !important;
  top: 50% !important;
  left: 50% !important;
  transform: translate(-50%, -50%) !important;
  z-index: 9999 !important;
  margin: 0 !important;
  animation: dialogSlideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
  background: #ffffff !important;
  overflow: hidden !important;
}

@keyframes dialogSlideIn {
  from {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1) translateY(0);
  }
}

/* Dialog Overlay */
.el-overlay:has(.modern-delete-dialog) {
  z-index: 9998 !important;
  background-color: rgba(0, 0, 0, 0.4) !important;
  backdrop-filter: blur(8px) !important;
  animation: overlayFadeIn 0.3s ease-out !important;
}

@keyframes overlayFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Dialog Header */
.modern-delete-dialog .el-message-box__header {
  padding: 24px 24px 0 24px !important;
  border-bottom: none !important;
  margin-bottom: 0 !important;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
  position: relative !important;
}

.modern-delete-dialog .el-message-box__header::after {
  content: '' !important;
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  right: 0 !important;
  height: 1px !important;
  background: linear-gradient(90deg, transparent 0%, #fecaca 50%, transparent 100%) !important;
}

/* Dialog Title */
.modern-delete-dialog .el-message-box__title {
  font-size: 20px !important;
  font-weight: 700 !important;
  color: #dc2626 !important;
  line-height: 1.3 !important;
  letter-spacing: -0.02em !important;
  margin: 0 !important;
  text-align: center !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 12px !important;
}

.modern-delete-dialog .el-message-box__title::before {
  content: '⚠️' !important;
  font-size: 24px !important;
  filter: drop-shadow(0 2px 4px rgba(220, 38, 38, 0.2)) !important;
}

/* Dialog Content */
.modern-delete-dialog .el-message-box__content {
  padding: 20px 24px 24px 24px !important;
  font-size: 15px !important;
  line-height: 1.5 !important;
  color: #6b7280 !important;
  text-align: center !important;
  background: #ffffff !important;
}

.modern-delete-dialog .el-message-box__message {
  padding: 0 !important;
}

.modern-delete-dialog .el-message-box__message p {
  margin: 0 !important;
  color: #6b7280 !important;
}

/* Hide default icon */
.modern-delete-dialog .el-message-box__status {
  display: none !important;
}

.modern-delete-dialog .el-message-box__container {
  display: block !important;
}

/* Dialog Buttons */
.modern-delete-dialog .el-message-box__btns {
  padding: 0 24px 24px 24px !important;
  gap: 12px !important;
  display: flex !important;
  justify-content: center !important;
  border-top: none !important;
  background: #ffffff !important;
}

/* Modern Delete Button */
.modern-delete-button {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  border: none !important;
  padding: 12px 24px !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  border-radius: 10px !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.25) !important;
  color: white !important;
  min-width: 100px !important;
  position: relative !important;
  overflow: hidden !important;
}

.modern-delete-button::before {
  content: '' !important;
  position: absolute !important;
  top: 0 !important;
  left: -100% !important;
  width: 100% !important;
  height: 100% !important;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent) !important;
  transition: left 0.5s !important;
}

.modern-delete-button:hover {
  background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.35) !important;
}

.modern-delete-button:hover::before {
  left: 100% !important;
}

.modern-delete-button:active {
  transform: translateY(0) !important;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3) !important;
}

/* Modern Cancel Button */
.modern-cancel-button {
  background: #f8fafc !important;
  border: 1px solid #e2e8f0 !important;
  color: #64748b !important;
  padding: 12px 24px !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  border-radius: 10px !important;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
  min-width: 100px !important;
}

.modern-cancel-button:hover {
  background: #f1f5f9 !important;
  border-color: #cbd5e1 !important;
  color: #475569 !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

.modern-cancel-button:active {
  transform: translateY(0) !important;
  box-shadow: none !important;
}

/* Success Message */
.modern-success-message {
  border-radius: 12px !important;
  padding: 16px 20px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  box-shadow: 0 8px 25px rgba(16, 185, 129, 0.15) !important;
  border: 1px solid rgba(16, 185, 129, 0.2) !important;
  background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%) !important;
  color: #065f46 !important;
}

.modern-success-message .el-message__icon {
  color: #10b981 !important;
}

/* Info Message */
.modern-info-message {
  border-radius: 12px !important;
  padding: 16px 20px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15) !important;
  border: 1px solid rgba(102, 126, 234, 0.2) !important;
  background: linear-gradient(135deg, #eef2ff 0%, #e0e7ff 100%) !important;
  color: #3730a3 !important;
}

.modern-info-message .el-message__icon {
  color: #6366f1 !important;
}

/* Error Message */
.modern-error-message {
  border-radius: 12px !important;
  padding: 16px 20px !important;
  font-size: 14px !important;
  font-weight: 500 !important;
  box-shadow: 0 8px 25px rgba(239, 68, 68, 0.15) !important;
  border: 1px solid rgba(239, 68, 68, 0.2) !important;
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%) !important;
  color: #991b1b !important;
}

.modern-error-message .el-message__icon {
  color: #ef4444 !important;
}

/* Dark Mode */
html.dark .modern-delete-dialog {
  background: #1e293b !important;
  border-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5) !important;
}

html.dark .modern-delete-dialog .el-message-box__header {
  background: linear-gradient(135deg, #2d1b1b 0%, #3d1f1f 100%) !important;
}

html.dark .modern-delete-dialog .el-message-box__title {
  color: #fca5a5 !important;
}

html.dark .modern-delete-dialog .el-message-box__content {
  background: #1e293b !important;
  color: #cbd5e1 !important;
}

html.dark .modern-delete-dialog .el-message-box__message p {
  color: #cbd5e1 !important;
}

html.dark .modern-delete-dialog .el-message-box__btns {
  background: #1e293b !important;
}

html.dark .modern-cancel-button {
  background: #334155 !important;
  border-color: #475569 !important;
  color: #e2e8f0 !important;
}

html.dark .modern-cancel-button:hover {
  background: #475569 !important;
  border-color: #64748b !important;
  color: #f1f5f9 !important;
}

html.dark .modern-success-message {
  background: linear-gradient(135deg, #064e3b 0%, #065f46 100%) !important;
  border-color: rgba(16, 185, 129, 0.3) !important;
  color: #a7f3d0 !important;
}

html.dark .modern-info-message {
  background: linear-gradient(135deg, #312e81 0%, #3730a3 100%) !important;
  border-color: rgba(99, 102, 241, 0.3) !important;
  color: #c7d2fe !important;
}

html.dark .modern-error-message {
  background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%) !important;
  border-color: rgba(239, 68, 68, 0.3) !important;
  color: #fecaca !important;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .modern-delete-dialog {
    max-width: calc(100% - 16px) !important;
    margin: 0 8px !important;
  }
  
  .modern-delete-dialog .el-message-box__header {
    padding: 20px 20px 0 20px !important;
  }
  
  .modern-delete-dialog .el-message-box__title {
    font-size: 18px !important;
  }
  
  .modern-delete-dialog .el-message-box__content {
    padding: 16px 20px 20px 20px !important;
    font-size: 14px !important;
  }
  
  .modern-delete-dialog .el-message-box__btns {
    padding: 0 20px 20px 20px !important;
    flex-direction: column !important;
    gap: 10px !important;
  }
  
  .modern-delete-button,
  .modern-cancel-button {
    width: 100% !important;
    padding: 14px 24px !important;
  }
}
</style>
