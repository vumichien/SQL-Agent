<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import MessageList from '@/components/chat/MessageList.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
import HistorySidebar from '@/components/history/HistorySidebar.vue'
import { queryAPI } from '@/api/query'
import { useQueryStore } from '@/stores/query'
import type { QueryResponse } from '@/types/api'

const { t } = useI18n()
const queryStore = useQueryStore()

// History sidebar state
const showHistory = ref(false)

// Messages in current conversation
const messages = ref<Array<{ type: 'user' | 'assistant'; data: any }>>([])

// Loading state
const loading = ref(false)

// Handle sending a question
const handleSend = async (question: string) => {
  if (!question.trim() || loading.value) return

  // Add user message
  messages.value.push({
    type: 'user',
    data: question,
  })

  loading.value = true

  try {
    // Call API
    const response = await queryAPI.sendQuery(question)

    // Add assistant response
    messages.value.push({
      type: 'assistant',
      data: response,
    })

    // Save to query store
    queryStore.addQuery({
      id: response.id || `query-${Date.now()}`,
      question: response.question,
      sql: response.sql,
      results: response.results,
      chart: response.visualization,
      timestamp: Date.now(),
    })

    if (response.error) {
      ElMessage.error(response.error)
    } else {
      ElMessage.success(t('chat.querySuccess'))
    }
  } catch (error: any) {
    console.error('Query error:', error)

    // Add error message
    messages.value.push({
      type: 'assistant',
      data: {
        id: `error-${Date.now()}`,
        question,
        sql: '',
        results: null,
        visualization: null,
        error: error.message || t('chat.queryError'),
      } as QueryResponse,
    })
  } finally {
    loading.value = false
  }
}

// Handle selecting a suggested question
const handleSelectQuestion = (question: string) => {
  handleSend(question)
}

// Handle loading query from history
const handleLoadQuery = async (id: string) => {
  try {
    const query = queryStore.history.find((q) => q.id === id)
    if (!query) {
      ElMessage.error(t('history.queryNotFound'))
      return
    }

    // Clear current messages
    messages.value = []

    // Add user message
    messages.value.push({
      type: 'user',
      data: query.question,
    })

    // Add assistant response
    messages.value.push({
      type: 'assistant',
      data: {
        id: query.id,
        question: query.question,
        sql: query.sql || '',
        results: query.results,
        visualization: query.chart,
        error: query.error || null,
      } as QueryResponse,
    })

    // Set as current query
    queryStore.currentQuery = query

    ElMessage.success(t('history.loadSuccess'))
  } catch (error: any) {
    console.error('Load query error:', error)
    ElMessage.error(t('history.loadError'))
  }
}

// Toggle history sidebar
const toggleHistory = () => {
  showHistory.value = !showHistory.value
}

// Handle new chat
const handleNewChat = () => {
  messages.value = []
  queryStore.currentQuery = null
  ElMessage.success(t('chat.newChatSuccess'))
}
</script>

<template>
  <div class="chat-view">
    <div class="chat-container">
      <!-- Message List -->
      <MessageList
        :messages="messages"
        :loading="loading"
        @select-question="handleSelectQuestion"
      />

      <!-- Chat Input -->
      <ChatInput :loading="loading" @send="handleSend" />

      <!-- New Chat Button -->
      <button
        class="new-chat-btn"
        @click="handleNewChat"
        :title="t('chat.newChat')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 5v14M5 12h14"/>
        </svg>
      </button>

      <!-- History Toggle Button -->
      <button
        class="history-toggle-btn"
        @click="toggleHistory"
        :title="t('history.title')"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span v-if="queryStore.history.length > 0" class="history-badge">
          {{ queryStore.history.length > 99 ? '99+' : queryStore.history.length }}
        </span>
      </button>

      <!-- History Sidebar -->
      <HistorySidebar
        v-model="showHistory"
        @load-query="handleLoadQuery"
      />
    </div>
  </div>
</template>

<style scoped>
.chat-view {
  height: 100%;
  width: 100%;
  position: relative;
}

.chat-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.new-chat-btn {
  position: fixed;
  bottom: 190px;
  right: 32px;
  z-index: 999;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: #ffffff;
  color: #667eea;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.12),
    0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.new-chat-btn svg {
  width: 24px;
  height: 24px;
}

.new-chat-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 24px rgba(102, 126, 234, 0.25),
    0 0 0 1px rgba(102, 126, 234, 0.2);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.new-chat-btn:active {
  transform: translateY(0);
}

.history-toggle-btn {
  position: fixed;
  bottom: 120px;
  right: 32px;
  z-index: 999;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: none;
  background: #ffffff;
  color: #667eea;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.12),
    0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.history-toggle-btn svg {
  width: 24px;
  height: 24px;
}

.history-toggle-btn:hover {
  transform: translateY(-2px);
  box-shadow: 
    0 8px 24px rgba(102, 126, 234, 0.25),
    0 0 0 1px rgba(102, 126, 234, 0.2);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.history-toggle-btn:active {
  transform: translateY(0);
}

.history-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 22px;
  height: 22px;
  padding: 0 6px;
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
  border-radius: 11px;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #ffffff;
  box-shadow: 0 2px 8px rgba(245, 87, 108, 0.4);
}

/* Dark mode adjustments */
html.dark .new-chat-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #8b9ef9;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

html.dark .new-chat-btn:hover {
  background: linear-gradient(135deg, #8b9ef9 0%, #9d7fc0 100%);
  color: white;
}

html.dark .history-toggle-btn {
  background: rgba(255, 255, 255, 0.1);
  color: #8b9ef9;
  box-shadow: 
    0 4px 16px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

html.dark .history-toggle-btn:hover {
  background: linear-gradient(135deg, #8b9ef9 0%, #9d7fc0 100%);
  color: white;
}

html.dark .history-badge {
  border-color: rgba(26, 26, 26, 0.9);
}

/* Responsive */
@media (max-width: 768px) {
  .new-chat-btn {
    bottom: 165px;
    right: 20px;
    width: 50px;
    height: 50px;
  }
  
  .new-chat-btn svg {
    width: 22px;
    height: 22px;
  }
  
  .history-toggle-btn {
    bottom: 100px;
    right: 20px;
    width: 50px;
    height: 50px;
  }
  
  .history-toggle-btn svg {
    width: 22px;
    height: 22px;
  }
  
  .history-badge {
    min-width: 20px;
    height: 20px;
    font-size: 10px;
    padding: 0 5px;
  }
}
</style>
