<script setup lang="ts">
export interface StatCard {
  value: number | string
  label: string
  icon: any
  iconClass: string
}

interface Props {
  stats: StatCard[]
  show?: boolean
}

withDefaults(defineProps<Props>(), {
  show: true,
})
</script>

<template>
  <div v-if="show" class="stats-section">
    <el-card
      v-for="(stat, index) in stats"
      :key="index"
      shadow="hover"
      class="stat-card"
    >
      <div class="stat-content">
        <div class="stat-icon" :class="stat.iconClass">
          <el-icon>
            <component :is="stat.icon" />
          </el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
/* Statistics Section */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  padding: 32px;
  background: transparent;
}

.stat-card {
  cursor: default;
  border-radius: 16px;
  border: 1px solid var(--el-border-color-lighter);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  overflow: hidden;
  background: #ffffff;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.stat-card :deep(.el-card__body) {
  padding: 24px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  font-weight: 500;
}

/* Icon color variations */
.total-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.today-icon {
  background: linear-gradient(135deg, #52c41a 0%, #95de64 100%);
  color: #ffffff;
}

.chart-icon {
  background: linear-gradient(135deg, #ff7a45 0%, #ff9c6e 100%);
  color: #ffffff;
}

.sql-icon {
  background: linear-gradient(135deg, #52c41a 0%, #95de64 100%);
  color: #ffffff;
}

.ddl-icon {
  background: linear-gradient(135deg, #1890ff 0%, #69c0ff 100%);
  color: #ffffff;
}

.doc-icon {
  background: linear-gradient(135deg, #722ed1 0%, #b37feb 100%);
  color: #ffffff;
}

/* Dark mode */
html.dark .stat-card {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: 1fr;
    padding: 16px;
  }
}
</style>

