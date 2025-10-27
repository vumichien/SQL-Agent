<script setup lang="ts">
import { computed } from 'vue'
import type { TrainingItem } from '@/types/store'

interface Props {
  visible: boolean
  item: TrainingItem | null
}

const props = withDefaults(defineProps<Props>(), {
  item: null,
})

const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const handleClose = () => {
  emit('update:visible', false)
}

const getTypeTag = (type: string) => {
  const typeMap: Record<string, { label: string; type: any }> = {
    sql: { label: 'SQL (Q&A)', type: 'success' },
    ddl: { label: 'DDL', type: 'primary' },
    documentation: { label: 'Documentation', type: 'info' },
  }
  return typeMap[type] || { label: type, type: '' }
}

const title = computed(() => {
  if (!props.item) return 'Training Data'
  return `Training Data - ${getTypeTag(props.item.training_data_type).label}`
})
</script>

<template>
  <el-dialog
    :model-value="visible"
    :title="title"
    width="700px"
    :before-close="handleClose"
  >
    <div v-if="item" class="training-details">
      <!-- Type Badge -->
      <div class="detail-section">
        <label class="detail-label">Type</label>
        <el-tag :type="getTypeTag(item.training_data_type).type" size="large">
          {{ getTypeTag(item.training_data_type).label }}
        </el-tag>
      </div>

      <!-- ID -->
      <div class="detail-section">
        <label class="detail-label">ID</label>
        <code class="detail-code">{{ item.id }}</code>
      </div>

      <!-- Question (for SQL type) -->
      <div v-if="item.question" class="detail-section">
        <label class="detail-label">Question</label>
        <div class="detail-content">{{ item.question }}</div>
      </div>

      <!-- Content (SQL/DDL/Documentation) -->
      <div class="detail-section">
        <label class="detail-label">
          {{ item.training_data_type === 'sql' ? 'SQL Query' : 
             item.training_data_type === 'ddl' ? 'DDL Statement' : 
             'Documentation' }}
        </label>
        <el-input
          :model-value="item.content"
          type="textarea"
          :rows="15"
          readonly
          class="readonly-textarea"
        />
      </div>
    </div>

    <div v-else class="empty-state">
      <el-empty description="No data to display" />
    </div>

    <template #footer>
      <el-button @click="handleClose">Close</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.training-details {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-label {
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.detail-content {
  padding: 12px;
  background: var(--el-fill-color-light);
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.6;
  color: var(--el-text-color-regular);
}

.detail-code {
  padding: 6px 12px;
  background: var(--el-fill-color-light);
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 12px;
  color: var(--el-color-primary);
  display: inline-block;
}

.readonly-textarea {
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
}

.readonly-textarea :deep(.el-textarea__inner) {
  background: var(--el-fill-color-light);
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 13px;
  color: var(--el-text-color-regular);
}

.empty-state {
  padding: 40px 0;
}
</style>
