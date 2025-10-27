<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  count?: number
  countLabel?: string
  loading?: boolean
  showRefresh?: boolean
  refreshIcon?: any
  showPrimaryAction?: boolean
  primaryActionText?: string
  primaryActionIcon?: any
  showDangerAction?: boolean
  dangerActionText?: string
  dangerActionIcon?: any
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  countLabel: 'items',
  loading: false,
  showRefresh: true,
  showPrimaryAction: false,
  primaryActionText: 'Add',
  showDangerAction: false,
  dangerActionText: 'Delete',
})

const emit = defineEmits<{
  refresh: []
  primaryAction: []
  dangerAction: []
}>()

const countText = computed(() => {
  return `${props.count} ${props.countLabel}`
})
</script>

<template>
  <el-header class="page-header">
    <div class="header-left">
      <h2>{{ title }}</h2>
      <el-tag v-if="countLabel" type="info" size="large">{{ countText }}</el-tag>
    </div>
    <div class="header-right">
      <el-button
        v-if="showRefresh"
        :icon="refreshIcon"
        @click="emit('refresh')"
        :loading="loading"
        title="Refresh"
      >
        <slot name="refresh-text">Refresh</slot>
      </el-button>
      <el-button
        v-if="showPrimaryAction"
        type="primary"
        :icon="primaryActionIcon"
        @click="emit('primaryAction')"
      >
        <slot name="primary-action-text">{{ primaryActionText }}</slot>
      </el-button>
      <el-button
        v-if="showDangerAction"
        type="danger"
        :icon="dangerActionIcon"
        @click="emit('dangerAction')"
      >
        <slot name="danger-action-text">{{ dangerActionText }}</slot>
      </el-button>
    </div>
  </el-header>
</template>

<style scoped>
/* Header */
.page-header {
  background: #ffffff;
  border-bottom: 1px solid var(--el-border-color-lighter);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  height: 80px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-left h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-left .el-tag {
  font-weight: 600;
  font-size: 14px;
}

.header-right {
  display: flex;
  gap: 12px;
}

.header-right .el-button {
  font-weight: 500;
}

.header-right .el-button--primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

.header-right .el-button--primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.header-right .el-button--danger {
  background: linear-gradient(135deg, #ff4d4f 0%, #f5222d 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(255, 77, 79, 0.4);
  transition: all 0.3s ease;
}

.header-right .el-button--danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 77, 79, 0.5);
}

/* Dark mode */
html.dark .page-header {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    height: auto;
    gap: 16px;
    padding: 16px;
  }

  .header-left,
  .header-right {
    width: 100%;
  }

  .header-right {
    justify-content: flex-end;
  }
}
</style>

