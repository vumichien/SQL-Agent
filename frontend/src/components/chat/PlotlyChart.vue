<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, ZoomIn, Refresh } from '@element-plus/icons-vue'
import Plotly from 'plotly.js-dist-min'

const props = defineProps<{
  figure: any // Plotly figure object from backend
}>()

const chartContainer = ref<HTMLElement | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)
const isDark = ref(document.documentElement.classList.contains('dark'))

// Resize observer for responsive charts
let resizeObserver: ResizeObserver | null = null

// Get theme-specific colors
const getThemeColors = () => {
  const dark = isDark.value
  return {
    paper_bgcolor: dark ? '#1a1a1a' : '#ffffff',
    plot_bgcolor: dark ? '#1a1a1a' : '#ffffff',
    font: {
      color: dark ? '#e5e7eb' : '#1f2937'
    },
    xaxis: {
      gridcolor: dark ? '#374151' : '#e5e7eb',
      linecolor: dark ? '#4b5563' : '#d1d5db',
      zerolinecolor: dark ? '#4b5563' : '#d1d5db'
    },
    yaxis: {
      gridcolor: dark ? '#374151' : '#e5e7eb',
      linecolor: dark ? '#4b5563' : '#d1d5db',
      zerolinecolor: dark ? '#4b5563' : '#d1d5db'
    }
  }
}

// Render or update the chart
const renderChart = async () => {
  if (!chartContainer.value || !props.figure) return

  try {
    loading.value = true
    error.value = null

    const themeColors = getThemeColors()

    // Prepare layout with theme colors
    const layout = {
      ...props.figure.layout,
      paper_bgcolor: themeColors.paper_bgcolor,
      plot_bgcolor: themeColors.plot_bgcolor,
      font: {
        ...props.figure.layout?.font,
        ...themeColors.font
      },
      xaxis: {
        ...props.figure.layout?.xaxis,
        gridcolor: themeColors.xaxis.gridcolor,
        linecolor: themeColors.xaxis.linecolor,
        zerolinecolor: themeColors.xaxis.zerolinecolor
      },
      yaxis: {
        ...props.figure.layout?.yaxis,
        gridcolor: themeColors.yaxis.gridcolor,
        linecolor: themeColors.yaxis.linecolor,
        zerolinecolor: themeColors.yaxis.zerolinecolor
      },
      autosize: true,
      margin: {
        l: 60,
        r: 40,
        t: 60,
        b: 60
      }
    }

    // Config for Plotly
    const config: Partial<Plotly.Config> = {
      responsive: true,
      displayModeBar: true,
      displaylogo: false,
      modeBarButtonsToRemove: ['lasso2d', 'select2d'] as any,
      toImageButtonOptions: {
        format: 'png',
        filename: `chart_${Date.now()}`,
        height: 800,
        width: 1200,
        scale: 2
      }
    }

    // Render the chart
    await Plotly.newPlot(
      chartContainer.value,
      props.figure.data || [],
      layout,
      config
    )

    loading.value = false
  } catch (err) {
    console.error('Failed to render Plotly chart:', err)
    error.value = 'Failed to render chart. Please try again.'
    loading.value = false
  }
}

// Handle window resize
const handleResize = () => {
  if (chartContainer.value && !loading.value && !error.value) {
    Plotly.Plots.resize(chartContainer.value)
  }
}

// Export chart as PNG
const exportChart = async () => {
  if (!chartContainer.value) return

  try {
    const imgData = await Plotly.toImage(chartContainer.value, {
      format: 'png',
      width: 1200,
      height: 800,
      scale: 2
    })

    // Create download link
    const link = document.createElement('a')
    link.href = imgData
    link.download = `chart_${Date.now()}.png`
    link.click()

    ElMessage.success('Chart exported successfully')
  } catch (err) {
    console.error('Failed to export chart:', err)
    ElMessage.error('Failed to export chart')
  }
}

// Reset zoom
const resetZoom = () => {
  if (chartContainer.value) {
    Plotly.Plots.resize(chartContainer.value)
  }
}

// Refresh chart
const refreshChart = () => {
  renderChart()
}

// Watch for theme changes
watch(
  () => document.documentElement.classList.contains('dark'),
  (newValue) => {
    isDark.value = newValue
    renderChart()
  }
)

// Watch for figure changes
watch(
  () => props.figure,
  () => {
    if (props.figure) {
      nextTick(() => {
        renderChart()
      })
    }
  },
  { deep: true }
)

// Lifecycle hooks
onMounted(async () => {
  await renderChart()

  // Setup resize observer
  if (chartContainer.value) {
    resizeObserver = new ResizeObserver(() => {
      handleResize()
    })
    resizeObserver.observe(chartContainer.value)
  }

  // Watch for theme changes via MutationObserver
  const observer = new MutationObserver(() => {
    const newIsDark = document.documentElement.classList.contains('dark')
    if (newIsDark !== isDark.value) {
      isDark.value = newIsDark
      renderChart()
    }
  })

  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
})

onBeforeUnmount(() => {
  if (resizeObserver && chartContainer.value) {
    resizeObserver.unobserve(chartContainer.value)
    resizeObserver.disconnect()
  }

  // Clean up Plotly
  if (chartContainer.value) {
    Plotly.purge(chartContainer.value)
  }
})
</script>

<template>
  <div class="plotly-chart">
    <el-card shadow="never">
      <!-- Chart actions -->
      <div class="chart-actions">
        <el-button-group>
          <el-tooltip content="Refresh chart" placement="top">
            <el-button size="small" :icon="Refresh" @click="refreshChart" :disabled="loading">
              Refresh
            </el-button>
          </el-tooltip>
          <el-tooltip content="Reset zoom" placement="top">
            <el-button size="small" :icon="ZoomIn" @click="resetZoom" :disabled="loading">
              Reset
            </el-button>
          </el-tooltip>
          <el-tooltip content="Export as PNG" placement="top">
            <el-button
              size="small"
              :icon="Download"
              type="primary"
              @click="exportChart"
              :disabled="loading || !!error"
            >
              Export
            </el-button>
          </el-tooltip>
        </el-button-group>
      </div>

      <!-- Loading state -->
      <div v-if="loading" class="chart-loading">
        <el-skeleton :rows="6" animated />
        <p class="loading-text">Rendering chart...</p>
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="chart-error">
        <el-result icon="error" :title="error">
          <template #extra>
            <el-button type="primary" @click="refreshChart">Try Again</el-button>
          </template>
        </el-result>
      </div>

      <!-- Chart container -->
      <div
        v-show="!loading && !error"
        ref="chartContainer"
        class="chart-container"
      ></div>
    </el-card>
  </div>
</template>

<style scoped>
.plotly-chart {
  width: 100%;
}

.chart-actions {
  margin-bottom: 16px;
  display: flex;
  justify-content: flex-end;
}

.chart-container {
  width: 100%;
  min-height: 400px;
  position: relative;
}

.chart-loading {
  padding: 40px;
  text-align: center;
}

.loading-text {
  margin-top: 16px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.chart-error {
  padding: 40px 20px;
}

/* Ensure Plotly renders correctly in both themes */
:deep(.plotly) {
  width: 100%;
  height: 100%;
}

:deep(.plotly .svg-container) {
  width: 100% !important;
  height: 100% !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .chart-container {
    min-height: 300px;
  }

  .chart-actions {
    justify-content: center;
  }

  .chart-actions :deep(.el-button span) {
    display: none;
  }

  .chart-actions :deep(.el-button) {
    padding: 8px;
  }
}

/* Dark mode specific adjustments */
.dark .chart-container {
  background-color: #1a1a1a;
}
</style>
