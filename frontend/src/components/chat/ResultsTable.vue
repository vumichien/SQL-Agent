<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, Search } from '@element-plus/icons-vue'
import type { QueryResults } from '@/types/api'

const props = defineProps<{
  results: QueryResults
}>()

// Pagination
const currentPage = ref(1)
const pageSize = ref(10)
const pageSizes = [10, 20, 50, 100]

// Search/Filter
const searchQuery = ref('')

// Convert data from array of arrays to array of objects for El-Table
const tableData = computed(() => {
  const data = props.results.data.map((row) => {
    const obj: Record<string, any> = {}
    props.results.columns.forEach((col, index) => {
      obj[col] = row[index]
    })
    return obj
  })

  // Apply search filter
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    return data.filter((row) => {
      return Object.values(row).some((value) =>
        String(value).toLowerCase().includes(query)
      )
    })
  }

  return data
})

// Paginated data
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return tableData.value.slice(start, end)
})

// Total items (after filtering)
const totalItems = computed(() => tableData.value.length)

// Handle page size change
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

// Handle page change
const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// Export to CSV
const exportCSV = () => {
  try {
    // Create CSV content
    const headers = props.results.columns.join(',')
    const rows = tableData.value.map((row) => {
      return props.results.columns
        .map((col) => {
          const value = row[col]
          // Escape quotes and wrap in quotes if contains comma
          if (value === null || value === undefined) return ''
          const stringValue = String(value)
          if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
            return `"${stringValue.replace(/"/g, '""')}"`
          }
          return stringValue
        })
        .join(',')
    })

    const csv = [headers, ...rows].join('\n')

    // Create blob and download
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const link = document.createElement('a')
    const url = URL.createObjectURL(blob)

    link.setAttribute('href', url)
    link.setAttribute('download', `query_results_${Date.now()}.csv`)
    link.style.visibility = 'hidden'

    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)

    ElMessage.success('CSV exported successfully')
  } catch (error) {
    console.error('Failed to export CSV:', error)
    ElMessage.error('Failed to export CSV')
  }
}

// Handle search
const handleSearch = () => {
  currentPage.value = 1
}

// Clear search
const clearSearch = () => {
  searchQuery.value = ''
  currentPage.value = 1
}
</script>

<template>
  <div class="results-table">
    <el-card shadow="never">
      <!-- Header with search and export -->
      <div class="table-header">
        <div class="search-container">
          <el-input
            v-model="searchQuery"
            :prefix-icon="Search"
            placeholder="Search in results..."
            clearable
            @input="handleSearch"
            @clear="clearSearch"
            style="max-width: 300px"
          />
        </div>
        <div class="header-actions">
          <el-button
            type="primary"
            :icon="Download"
            size="small"
            @click="exportCSV"
            :disabled="totalItems === 0"
          >
            Export CSV
          </el-button>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="totalItems === 0 && searchQuery.trim()" class="empty-state">
        <el-empty description="No results found matching your search">
          <el-button type="primary" @click="clearSearch">Clear Search</el-button>
        </el-empty>
      </div>

      <div v-else-if="totalItems === 0" class="empty-state">
        <el-empty description="No data returned from query" />
      </div>

      <!-- Table -->
      <div v-else class="table-container">
        <el-table
          :data="paginatedData"
          stripe
          border
          style="width: 100%"
          :default-sort="{ prop: results.columns[0], order: 'ascending' }"
          height="500"
        >
          <el-table-column
            v-for="column in results.columns"
            :key="column"
            :prop="column"
            :label="column"
            :sortable="true"
            min-width="150"
            show-overflow-tooltip
          >
            <template #default="{ row }">
              <span class="cell-content">{{ formatValue(row[column]) }}</span>
            </template>
          </el-table-column>
        </el-table>

        <!-- Pagination -->
        <div class="pagination-container">
          <div class="pagination-info">
            Showing {{ ((currentPage - 1) * pageSize) + 1 }} to
            {{ Math.min(currentPage * pageSize, totalItems) }} of {{ totalItems }} results
            <span v-if="searchQuery.trim()" class="filter-badge">
              (filtered from {{ results.rowCount }} total)
            </span>
          </div>
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="pageSizes"
            :total="totalItems"
            layout="sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            background
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts">
// Format cell values
function formatValue(value: any): string {
  if (value === null || value === undefined) {
    return 'NULL'
  }
  if (typeof value === 'boolean') {
    return value ? 'TRUE' : 'FALSE'
  }
  if (typeof value === 'number') {
    // Format numbers with thousand separators
    return value.toLocaleString()
  }
  return String(value)
}
</script>

<style scoped>
.results-table {
  width: 100%;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  gap: 16px;
  flex-wrap: wrap;
}

.search-container {
  flex: 1;
  min-width: 200px;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.table-container {
  width: 100%;
}

.cell-content {
  word-break: break-word;
}

.pagination-container {
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.pagination-info {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.filter-badge {
  color: var(--el-color-primary);
  font-weight: 500;
}

.empty-state {
  padding: 40px 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .table-header {
    flex-direction: column;
    align-items: stretch;
  }

  .search-container {
    width: 100%;
  }

  .search-container :deep(.el-input) {
    max-width: 100% !important;
  }

  .header-actions {
    width: 100%;
    justify-content: stretch;
  }

  .header-actions .el-button {
    flex: 1;
  }

  .pagination-container {
    flex-direction: column;
    align-items: center;
  }

  .pagination-info {
    text-align: center;
    width: 100%;
  }

  /* Adjust table for mobile */
  .table-container :deep(.el-table) {
    font-size: 12px;
  }

  .table-container :deep(.el-table th),
  .table-container :deep(.el-table td) {
    padding: 8px 4px;
  }
}

/* Dark mode adjustments */
.dark .empty-state {
  background-color: var(--el-bg-color);
}
</style>
