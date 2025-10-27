<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useClipboard } from '@vueuse/core'
import { ElMessage } from 'element-plus'
import { CopyDocument, Check, CircleCheck, CircleClose } from '@element-plus/icons-vue'
import { createHighlighter } from 'shiki'

const props = defineProps<{
  sql: string
}>()

const emit = defineEmits<{
  feedback: [value: 'positive' | 'negative']
}>()

const { copy, copied } = useClipboard()
const highlightedCode = ref<string>('')
const feedbackGiven = ref<'positive' | 'negative' | null>(null)

// Initialize Shiki highlighter
const initHighlighter = async () => {
  try {
    const highlighter = await createHighlighter({
      themes: ['github-dark', 'github-light'],
      langs: ['sql']
    })

    const isDark = document.documentElement.classList.contains('dark')
    const theme = isDark ? 'github-dark' : 'github-light'

    highlightedCode.value = highlighter.codeToHtml(props.sql, {
      lang: 'sql',
      theme
    })
  } catch (error) {
    console.error('Failed to initialize syntax highlighting:', error)
    // Fallback to plain text
    highlightedCode.value = `<pre class="shiki"><code>${escapeHtml(props.sql)}</code></pre>`
  }
}

// Escape HTML for fallback
const escapeHtml = (text: string): string => {
  const map: Record<string, string> = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  }
  return text.replace(/[&<>"']/g, (m) => map[m])
}

// Handle copy to clipboard
const handleCopy = async () => {
  try {
    await copy(props.sql)
    ElMessage.success('SQL copied to clipboard')
  } catch (error) {
    ElMessage.error('Failed to copy SQL')
  }
}

// Handle feedback
const handleFeedback = (type: 'positive' | 'negative') => {
  feedbackGiven.value = type
  emit('feedback', type)
  ElMessage.success(`Feedback recorded: ${type === 'positive' ? 'Helpful' : 'Not helpful'}`)
}

// Initialize on mount
onMounted(() => {
  initHighlighter()
})

// Re-highlight when SQL changes
watch(() => props.sql, () => {
  initHighlighter()
})

// Re-highlight when theme changes
watch(
  () => document.documentElement.classList.contains('dark'),
  () => {
    initHighlighter()
  }
)
</script>

<template>
  <div class="sql-display">
    <el-card class="sql-card" shadow="never">
      <!-- Syntax highlighted SQL -->
      <div class="sql-code" v-html="highlightedCode"></div>

      <!-- Action buttons -->
      <div class="sql-actions">
        <div class="action-group">
          <!-- Copy button -->
          <el-button
            size="small"
            :icon="copied ? Check : CopyDocument"
            :type="copied ? 'success' : 'default'"
            @click="handleCopy"
          >
            {{ copied ? 'Copied!' : 'Copy' }}
          </el-button>
        </div>

        <!-- Feedback buttons -->
        <div class="action-group feedback-group">
          <el-tooltip content="Helpful" placement="top">
            <el-button
              size="small"
              :icon="CircleCheck"
              :type="feedbackGiven === 'positive' ? 'success' : 'default'"
              :disabled="feedbackGiven !== null"
              circle
              @click="handleFeedback('positive')"
            />
          </el-tooltip>
          <el-tooltip content="Not helpful" placement="top">
            <el-button
              size="small"
              :icon="CircleClose"
              :type="feedbackGiven === 'negative' ? 'danger' : 'default'"
              :disabled="feedbackGiven !== null"
              circle
              @click="handleFeedback('negative')"
            />
          </el-tooltip>
        </div>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.sql-display {
  width: 100%;
}

.sql-card {
  background-color: var(--el-fill-color-light);
  border: 1px solid var(--el-border-color);
}

.sql-code {
  border-radius: 6px;
  overflow-x: auto;
  font-family: 'Courier New', Consolas, Monaco, monospace;
  font-size: 13px;
  line-height: 1.6;
}

/* Override Shiki styles for better integration */
.sql-code :deep(pre) {
  margin: 0;
  padding: 16px;
  background-color: transparent !important;
  overflow-x: auto;
}

.sql-code :deep(code) {
  font-family: 'Courier New', Consolas, Monaco, monospace;
  font-size: 13px;
  line-height: 1.6;
}

.sql-actions {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.action-group {
  display: flex;
  gap: 8px;
  align-items: center;
}

.feedback-group {
  margin-left: auto;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .sql-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .feedback-group {
    margin-left: 0;
    justify-content: center;
  }
}
</style>
