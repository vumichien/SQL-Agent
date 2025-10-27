<script setup lang="ts">
import { ref, computed } from 'vue'
import { Delete, View, Search } from '@element-plus/icons-vue'
import type { TrainingItem } from '@/types/store'
import { ElMessageBox } from 'element-plus'

interface Props {
  data: TrainingItem[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
})

const emit = defineEmits<{
  delete: [id: string]
  view: [item: TrainingItem]
}>()

// Search
const searchQuery = ref('')

// Pagination
const currentPage = ref(1)
const pageSize = ref(10)
const pageSizes = [10, 20, 50, 100]

// Filtered and paginated data
const filteredData = computed(() => {
  if (!searchQuery.value) return props.data

  const query = searchQuery.value.toLowerCase()
  return props.data.filter((item) => {
    const typeMatch = item.training_data_type.toLowerCase().includes(query)
    const questionMatch = item.question?.toLowerCase().includes(query)
    const contentMatch = item.content?.toLowerCase().includes(query)
    const idMatch = item.id?.toLowerCase().includes(query)

    return typeMatch || questionMatch || contentMatch || idMatch
  })
})

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredData.value.slice(start, end)
})

const total = computed(() => filteredData.value.length)

// Actions
const handleDelete = async (item: TrainingItem) => {
  try {
    await ElMessageBox.confirm(
      `Are you sure you want to delete this ${item.training_data_type} training data?`,
      'Confirm Delete',
      {
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel',
        type: 'warning',
        confirmButtonClass: 'el-button--danger',
      }
    )

    emit('delete', item.id)
  } catch {
    // User cancelled
  }
}

const handleView = (item: TrainingItem) => {
  emit('view', item)
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// Type display helpers
const getTypeTag = (type: string) => {
  const typeMap: Record<string, { label: string; type: any }> = {
    sql: { label: 'SQL', type: 'success' },
    ddl: { label: 'DDL', type: 'primary' },
    documentation: { label: 'Documentation', type: 'info' },
  }
  return typeMap[type] || { label: type, type: '' }
}

const truncate = (text: string | null | undefined, maxLength = 100) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}
</script>

<template>
  <div class="training-data-table">
    <!-- Search Bar -->
    <div class="table-header">
      <el-input
        v-model="searchQuery"
        placeholder="Search training data..."
        :prefix-icon="Search"
        clearable
        style="max-width: 400px"
      />
      <div class="table-info">
        <span class="info-text">Total: {{ total }} items</span>
      </div>
    </div>

    <!-- Table -->
    <el-table
      :data="paginatedData"
      v-loading="loading"
      stripe
      border
      style="width: 100%"
      :empty-text="searchQuery ? 'No results found' : 'No training data'"
      :default-sort="{ prop: 'training_data_type', order: 'ascending' }"
    >
      <!-- ID Column -->
      <el-table-column prop="id" label="ID" width="180" sortable>
        <template #default="{ row }">
          <el-tooltip :content="row.id" placement="top">
            <span class="id-text">{{ truncate(row.id, 20) }}</span>
          </el-tooltip>
        </template>
      </el-table-column>

      <!-- Type Column -->
      <el-table-column prop="training_data_type" label="Type" width="130" sortable>
        <template #default="{ row }">
          <el-tag :type="getTypeTag(row.training_data_type).type">
            {{ getTypeTag(row.training_data_type).label }}
          </el-tag>
        </template>
      </el-table-column>

      <!-- Question Column (for SQL type) -->
      <el-table-column prop="question" label="Question" width="250" sortable>
        <template #default="{ row }">
          <div v-if="row.question" class="question-text">
            <el-tooltip :content="row.question" placement="top">
              <span>{{ truncate(row.question, 50) }}</span>
            </el-tooltip>
          </div>
          <span v-else class="empty-text">—</span>
        </template>
      </el-table-column>

      <!-- Content Column -->
      <el-table-column prop="content" label="Content" min-width="400">
        <template #default="{ row }">
          <div class="content-preview">
            <code v-if="row.content" class="content-code">{{ truncate(row.content, 150) }}</code>
            <span v-else class="empty-text">No content available</span>
          </div>
        </template>
      </el-table-column>

      <!-- Actions Column -->
      <el-table-column label="Actions" width="150" align="center" fixed="right">
        <template #default="{ row }">
          <el-button
            type="info"
            :icon="View"
            circle
            size="small"
            @click="handleView(row)"
            title="View details"
          />
          <el-button
            type="danger"
            :icon="Delete"
            circle
            size="small"
            @click="handleDelete(row)"
            title="Delete"
          />
        </template>
      </el-table-column>
    </el-table>

    <!-- Pagination -->
    <div class="table-footer">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="pageSizes"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<style scoped>
.training-data-table {
  display: flex;
  flex-direction: column;
  gap: 16px;
  height: 100%;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.table-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.info-text {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.id-text {
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  cursor: pointer;
}

.question-text {
  font-size: 13px;
  line-height: 1.5;
  color: var(--el-text-color-regular);
}

.empty-text {
  color: var(--el-text-color-placeholder);
  font-style: italic;
}

.content-preview {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.content-code {
  display: block;
  background: var(--el-fill-color-light);
  padding: 8px 12px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 12px;
  color: var(--el-color-primary);
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.table-footer {
  display: flex;
  justify-content: center;
  padding: 16px 0;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .table-header {
    flex-direction: column;
    align-items: stretch;
  }

  .table-info {
    justify-content: center;
  }
}
</style>
