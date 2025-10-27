<script setup lang="ts">
interface Props {
  loading?: boolean
  isEmpty?: boolean
  emptyIcon?: any
  emptyTitle?: string
  emptyDescription?: string
  showEmptyAction?: boolean
  emptyActionText?: string
  emptyActionIcon?: any
}

withDefaults(defineProps<Props>(), {
  loading: false,
  isEmpty: false,
  emptyTitle: 'No data',
  emptyDescription: '',
  showEmptyAction: false,
  emptyActionText: 'Add',
})

const emit = defineEmits<{
  emptyAction: []
}>()
</script>

<template>
  <el-main class="page-content">
    <!-- Empty State -->
    <div v-if="isEmpty && !loading" class="empty-container">
      <el-empty :description="emptyTitle">
        <template #image>
          <el-icon :size="100" color="var(--el-text-color-secondary)">
            <component :is="emptyIcon" />
          </el-icon>
        </template>
        <p v-if="emptyDescription" class="empty-description">
          {{ emptyDescription }}
        </p>
        <el-button
          v-if="showEmptyAction"
          type="primary"
          :icon="emptyActionIcon"
          @click="emit('emptyAction')"
        >
          {{ emptyActionText }}
        </el-button>
      </el-empty>
    </div>

    <!-- Content Slot -->
    <div v-else class="content-wrapper">
      <slot></slot>
    </div>
  </el-main>
</template>

<style scoped>
/* Main Content */
.page-content {
  flex: 1;
  padding: 0 32px 32px 32px;
  overflow: auto;
  background: transparent;
}

.page-content :deep(.el-card) {
  border-radius: 16px;
  border: 1px solid var(--el-border-color-lighter);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.empty-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #ffffff;
  border-radius: 16px;
  padding: 60px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.empty-container .el-empty {
  padding: 40px;
}

.empty-description {
  margin: 24px 0;
  font-size: 16px;
  color: var(--el-text-color-secondary);
  line-height: 1.6;
}

.empty-container .el-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  padding: 12px 32px;
  font-size: 15px;
  font-weight: 600;
}

.empty-container .el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.content-wrapper {
  height: 100%;
}

/* Dark mode */
html.dark .empty-container {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .page-content {
    padding: 0 16px 16px 16px;
  }
}
</style>

