<script setup lang="ts">
import { computed } from 'vue'
import { Delete, ChatDotRound, Clock } from '@element-plus/icons-vue'
import type { Query } from '@/types/store'

const props = defineProps<{
  query: Query
  active?: boolean
}>()

const emit = defineEmits<{
  load: [id: string]
  delete: [id: string]
}>()

// Format timestamp
const formattedTime = computed(() => {
  const date = new Date(props.query.timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  // Less than 1 minute
  if (diff < 60 * 1000) {
    return 'Just now'
  }

  // Less than 1 hour
  if (diff < 60 * 60 * 1000) {
    const minutes = Math.floor(diff / (60 * 1000))
    return `${minutes} min${minutes > 1 ? 's' : ''} ago`
  }

  // Less than 24 hours
  if (diff < 24 * 60 * 60 * 1000) {
    const hours = Math.floor(diff / (60 * 60 * 1000))
    return `${hours} hour${hours > 1 ? 's' : ''} ago`
  }

  // Less than 7 days
  if (diff < 7 * 24 * 60 * 60 * 1000) {
    const days = Math.floor(diff / (24 * 60 * 60 * 1000))
    return `${days} day${days > 1 ? 's' : ''} ago`
  }

  // Otherwise show full date
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
  })
})

// Truncate question for display
const truncatedQuestion = computed(() => {
  const maxLength = 80
  if (props.query.question.length <= maxLength) {
    return props.query.question
  }
  return props.query.question.substring(0, maxLength) + '...'
})

// Handle click to load
const handleClick = () => {
  emit('load', props.query.id)
}

// Handle delete
const handleDelete = (e: Event) => {
  e.stopPropagation() // Prevent triggering the load action
  emit('delete', props.query.id)
}
</script>

<template>
  <div :class="['history-item', { active }]" @click="handleClick">
    <div class="item-header">
      <el-icon class="item-icon">
        <ChatDotRound />
      </el-icon>
      <span class="item-time">
        <el-icon><Clock /></el-icon>
        {{ formattedTime }}
      </span>
    </div>

    <div class="item-content">
      <p class="item-question" :title="query.question">
        {{ truncatedQuestion }}
      </p>

      <div v-if="query.sql" class="item-sql">
        <code>{{ query.sql.substring(0, 60) }}{{ query.sql.length > 60 ? '...' : '' }}</code>
      </div>

      <div v-if="query.error" class="item-error">
        <el-tag type="danger" size="small">Error</el-tag>
      </div>
    </div>

    <div class="item-actions">
      <el-button
        type="danger"
        size="small"
        :icon="Delete"
        circle
        @click="handleDelete"
        class="delete-btn"
      />
    </div>
  </div>
</template>

<style scoped>
.history-item {
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: var(--el-fill-color-light);
  border: 2px solid transparent;
  position: relative;
}

.history-item:hover {
  background-color: var(--el-fill-color);
  transform: translateX(-2px);
}

.history-item.active {
  border-color: var(--el-color-primary);
  background-color: var(--el-color-primary-light-9);
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.item-icon {
  color: var(--el-color-primary);
  font-size: 18px;
}

.item-time {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.item-time .el-icon {
  font-size: 12px;
}

.item-content {
  margin-bottom: 8px;
}

.item-question {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  line-height: 1.4;
  word-break: break-word;
}

.item-sql {
  margin: 8px 0;
  padding: 6px 8px;
  background-color: var(--el-fill-color-darker);
  border-radius: 4px;
  font-size: 11px;
  font-family: 'Courier New', monospace;
  color: var(--el-text-color-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-error {
  margin-top: 6px;
}

.item-actions {
  display: flex;
  justify-content: flex-end;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.history-item:hover .item-actions {
  opacity: 1;
}

.delete-btn {
  padding: 4px;
}

/* Responsive */
@media (max-width: 768px) {
  .history-item {
    padding: 10px;
  }

  .item-question {
    font-size: 13px;
  }

  .item-actions {
    opacity: 1;
  }
}
</style>
