<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useTrainingStore } from '@/stores/training'
import { useI18n } from 'vue-i18n'
import { Refresh, Plus, InfoFilled } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import StatsCards, { type StatCard } from '@/components/common/StatsCards.vue'
import PageContent from '@/components/common/PageContent.vue'
import TrainingDataTable from '@/components/training/TrainingDataTable.vue'
import AddTrainingModal from '@/components/training/AddTrainingModal.vue'
import ViewTrainingModal from '@/components/training/ViewTrainingModal.vue'
import type { TrainRequest } from '@/types/api'
import type { TrainingItem } from '@/types/store'

const { t } = useI18n()
const trainingStore = useTrainingStore()

// Modal visibility
const addModalVisible = ref(false)
const viewModalVisible = ref(false)
const selectedItem = ref<TrainingItem | null>(null)

// Load training data on mount
onMounted(async () => {
  await trainingStore.fetchTrainingData()
})

// Handle add training data
const handleAdd = () => {
  addModalVisible.value = true
}

// Handle submit new training data
const handleSubmit = async (data: TrainRequest) => {
  try {
    await trainingStore.addTrainingData(data)
    addModalVisible.value = false
  } catch (error) {
    console.error('Failed to add training data:', error)
  }
}

// Handle view training data
const handleView = (item: TrainingItem) => {
  selectedItem.value = item
  viewModalVisible.value = true
}

// Handle delete training data
const handleDelete = async (id: string) => {
  try {
    await trainingStore.removeTrainingData(id)
  } catch (error) {
    console.error('Failed to delete training data:', error)
  }
}

// Handle refresh
const handleRefresh = async () => {
  await trainingStore.fetchTrainingData()
}

// Get statistics
const stats = computed(() => {
  const data = trainingStore.trainingData
  return {
    total: data.length,
    sql: data.filter((item) => item.training_data_type === 'sql').length,
    ddl: data.filter((item) => item.training_data_type === 'ddl').length,
    documentation: data.filter((item) => item.training_data_type === 'documentation').length,
  }
})

// Stats cards configuration
const statsCards = computed<StatCard[]>(() => [
  {
    value: stats.value.sql,
    label: t('training.sqlPairs'),
    icon: InfoFilled,
    iconClass: 'sql-icon'
  },
  {
    value: stats.value.ddl,
    label: t('training.ddlStatements'),
    icon: InfoFilled,
    iconClass: 'ddl-icon'
  },
  {
    value: stats.value.documentation,
    label: t('training.documentation'),
    icon: InfoFilled,
    iconClass: 'doc-icon'
  }
])
</script>

<template>
  <div class="training-view">
    <el-container class="training-container">
      <!-- Header -->
      <PageHeader
        :title="t('training.title')"
        :count="stats.total"
        count-label="items"
        :loading="trainingStore.isLoading"
        :show-refresh="true"
        :refresh-icon="Refresh"
        :show-primary-action="true"
        :primary-action-icon="Plus"
        @refresh="handleRefresh"
        @primary-action="handleAdd"
      >
        <template #refresh-text>{{ t('common.refresh') }}</template>
        <template #primary-action-text>{{ t('training.addData') }}</template>
      </PageHeader>

      <!-- Statistics Cards -->
      <StatsCards :stats="statsCards" />

      <!-- Main Content -->
      <PageContent
        :loading="trainingStore.isLoading"
        :is-empty="!trainingStore.isLoading && trainingStore.trainingData.length === 0"
        :empty-icon="InfoFilled"
        :empty-title="t('training.noData')"
        empty-description="Add DDL, documentation, or SQL examples to improve accuracy"
        :show-empty-action="true"
        :empty-action-text="t('training.addData')"
        :empty-action-icon="Plus"
        @empty-action="handleAdd"
      >
        <!-- Training Data Table -->
        <TrainingDataTable
          :data="trainingStore.trainingData"
          :loading="trainingStore.isLoading"
          @delete="handleDelete"
          @view="handleView"
        />
      </PageContent>
    </el-container>

    <!-- Add Training Modal -->
    <AddTrainingModal
      v-model:visible="addModalVisible"
      :loading="trainingStore.isLoading"
      @submit="handleSubmit"
    />

    <!-- View Training Modal -->
    <ViewTrainingModal
      v-model:visible="viewModalVisible"
      :item="selectedItem"
    />
  </div>
</template>

<style scoped>
.training-view {
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.training-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

</style>
