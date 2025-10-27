<script setup lang="ts">
import { Document, Grid, TrendCharts, ChatDotRound } from '@element-plus/icons-vue'
import type { QueryResponse } from '@/types/api'
import SQLDisplay from './SQLDisplay.vue'
import ResultsTable from './ResultsTable.vue'
import PlotlyChart from './PlotlyChart.vue'

defineProps<{
  message: QueryResponse
}>()

// Handle SQL feedback
const handleSQLFeedback = (feedback: 'positive' | 'negative') => {
  console.log('SQL feedback:', feedback)
  // TODO: Send feedback to backend API in future task
}
</script>

<template>
  <div class="assistant-message">
    <el-avatar :size="40" class="avatar">
      <el-icon><ChatDotRound /></el-icon>
    </el-avatar>
    <div class="message-content">
      <!-- Error state -->
      <el-alert
        v-if="message.error"
        type="error"
        :title="message.error"
        :closable="false"
        show-icon
      />

      <!-- SQL Display -->
      <div v-if="message.sql && !message.error" class="sql-section">
        <div class="section-header">
          <el-icon><Document /></el-icon>
          <span>Generated SQL</span>
        </div>
        <SQLDisplay :sql="message.sql" @feedback="handleSQLFeedback" />
      </div>

      <!-- Results Display -->
      <div v-if="message.results && !message.error" class="results-section">
        <div class="section-header">
          <el-icon><Grid /></el-icon>
          <span>Query Results</span>
        </div>
        <ResultsTable :results="message.results" />
      </div>

      <!-- Visualization -->
      <div v-if="message.visualization" class="chart-section">
        <div class="section-header">
          <el-icon><TrendCharts /></el-icon>
          <span>Visualization</span>
        </div>
        <PlotlyChart :figure="message.visualization" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.assistant-message {
  display: flex;
  gap: 12px;
  padding: 20px;
  align-items: flex-start;
  animation: slideInLeft 0.4s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.avatar {
  flex-shrink: 0;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  box-shadow: 0 4px 12px rgba(240, 147, 251, 0.3);
  border: 2px solid #ffffff;
}

.message-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 85%;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  margin-bottom: 12px;
  font-size: 15px;
  padding: 8px 12px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
  border-radius: 8px;
  border-left: 3px solid #667eea;
}

.section-header .el-icon {
  color: #667eea;
  font-size: 18px;
}

.sql-section,
.results-section,
.chart-section {
  animation: fadeInUp 0.5s ease-out;
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--el-border-color-lighter);
  transition: all 0.3s ease;
}

.sql-section:hover,
.results-section:hover,
.chart-section:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.placeholder {
  text-align: center;
  color: var(--el-text-color-secondary);
  padding: 40px;
}

/* Dark mode adjustments */
html.dark .sql-section,
html.dark .results-section,
html.dark .chart-section {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

html.dark .section-header {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
}

/* Responsive */
@media (max-width: 768px) {
  .assistant-message {
    padding: 12px;
  }
  
  .message-content {
    max-width: 95%;
    gap: 16px;
  }
  
  .sql-section,
  .results-section,
  .chart-section {
    padding: 16px;
  }
}
</style>
