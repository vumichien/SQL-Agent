<script setup lang="ts">
import { computed } from 'vue'
import { useQueryStore } from '@/stores/query'
import { useI18n } from 'vue-i18n'
import { Clock, Refresh, Delete, TrendCharts } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import PageHeader from '@/components/common/PageHeader.vue'
import StatsCards, { type StatCard } from '@/components/common/StatsCards.vue'
import PageContent from '@/components/common/PageContent.vue'

const { t } = useI18n()
const queryStore = useQueryStore()

// Get history statistics
const stats = computed(() => {
  const history = queryStore.history
  return {
    total: history.length,
    today: history.filter(q => {
      const date = new Date(q.timestamp)
      const today = new Date()
      return date.toDateString() === today.toDateString()
    }).length,
    withCharts: history.filter(q => q.chart).length
  }
})

// Stats cards configuration
const statsCards = computed<StatCard[]>(() => [
  {
    value: stats.value.total,
    label: t('history.totalQueries', { count: '' }).replace('queries', 'Total Queries'),
    icon: Clock,
    iconClass: 'total-icon'
  },
  {
    value: stats.value.today,
    label: "Today's Queries",
    icon: Clock,
    iconClass: 'today-icon'
  },
  {
    value: stats.value.withCharts,
    label: 'With Visualizations',
    icon: TrendCharts,
    iconClass: 'chart-icon'
  }
])

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
  } catch {
    // User cancelled - no action needed
  }
}

// Handle delete single query
const handleDelete = async (id: string) => {
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
  } catch {
    // User cancelled - no action needed
  }
}

// Format date
const formatDate = (timestamp: number) => {
  return new Date(timestamp).toLocaleString()
}
</script>

<template>
  <div class="history-view">
    <el-container class="history-container">
      <!-- Header -->
      <PageHeader
        :title="t('history.title')"
        :count="stats.total"
        :count-label="t('history.items')"
        :show-refresh="true"
        :refresh-icon="Refresh"
        :show-danger-action="queryStore.history.length > 0"
        :danger-action-icon="Delete"
        @refresh="queryStore.loadHistory"
        @danger-action="handleClearAll"
      >
        <template #refresh-text>{{ t('common.refresh') }}</template>
        <template #danger-action-text>{{ t('history.clearAll') }}</template>
      </PageHeader>

      <!-- Statistics Cards -->
      <StatsCards :stats="statsCards" />

      <!-- Main Content -->
      <PageContent
        :is-empty="queryStore.history.length === 0"
        :empty-icon="Clock"
        :empty-title="t('history.noHistory')"
        empty-description="Your past queries will appear here. Start asking questions in the Chat!"
      >
        <!-- History List -->
        <div class="history-list">
          <el-card
            v-for="query in queryStore.history"
            :key="query.id"
            class="history-card"
            shadow="hover"
          >
            <div class="history-item">
              <div class="history-header">
                <div class="history-question">
                  {{ query.question }}
                </div>
                <el-button
                  type="danger"
                  :icon="Delete"
                  circle
                  size="small"
                  @click="handleDelete(query.id)"
                />
              </div>
              <div class="history-meta">
                <el-tag size="small" type="info">
                  <el-icon><Clock /></el-icon>
                  {{ formatDate(query.timestamp) }}
                </el-tag>
                <el-tag v-if="query.chart" size="small" type="success">
                  <el-icon><TrendCharts /></el-icon>
                  Has Chart
                </el-tag>
              </div>
              <div v-if="query.sql" class="history-sql">
                <code>{{ query.sql }}</code>
              </div>
            </div>
          </el-card>
        </div>
      </PageContent>
    </el-container>
  </div>
</template>

<style scoped>
.history-view {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.history-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

/* History List */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-card {
  border-radius: 16px;
  border: 1px solid var(--el-border-color-lighter);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
  background: #ffffff;
}

.history-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.history-card :deep(.el-card__body) {
  padding: 24px;
}

.history-item {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.history-question {
  flex: 1;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  line-height: 1.5;
}

.history-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.history-meta .el-tag {
  display: flex;
  align-items: center;
  gap: 4px;
}

.history-sql {
  background: var(--el-fill-color-light);
  border-radius: 8px;
  padding: 12px 16px;
  border-left: 3px solid #667eea;
}

.history-sql code {
  font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
  font-size: 13px;
  color: var(--el-text-color-regular);
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-all;
}

/* Dark mode */
html.dark .history-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

html.dark .history-sql {
  background: rgba(255, 255, 255, 0.05);
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
