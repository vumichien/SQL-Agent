<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import UserMessage from './UserMessage.vue'
import AssistantMessage from './AssistantMessage.vue'
import LoadingIndicator from './LoadingIndicator.vue'
import EmptyState from './EmptyState.vue'

const props = defineProps<{
  messages: Array<{ type: 'user' | 'assistant'; data: any }>
  loading?: boolean
}>()

const emit = defineEmits<{
  selectQuestion: [question: string]
}>()

const messagesContainer = ref<HTMLElement | null>(null)

// Auto-scroll to bottom when new messages arrive
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// Watch for message changes
watch(
  () => [props.messages.length, props.loading],
  () => {
    scrollToBottom()
  },
  { deep: true }
)

const handleSelectQuestion = (question: string) => {
  emit('selectQuestion', question)
}
</script>

<template>
  <div ref="messagesContainer" class="message-list">
    <!-- Empty state when no messages -->
    <EmptyState
      v-if="messages.length === 0 && !loading"
      @select-question="handleSelectQuestion"
    />

    <!-- Messages -->
    <div v-else class="messages-container">
      <template v-for="(message, index) in messages" :key="index">
        <UserMessage v-if="message.type === 'user'" :question="message.data" />
        <AssistantMessage
          v-else-if="message.type === 'assistant'"
          :message="message.data"
        />
      </template>

      <!-- Loading indicator -->
      <LoadingIndicator v-if="loading" />
    </div>
  </div>
</template>

<style scoped>
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  background: linear-gradient(180deg, rgba(248, 249, 250, 0.5) 0%, rgba(255, 255, 255, 0.8) 100%);
  display: flex;
  flex-direction: column;
  position: relative;
}

.message-list::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(102, 126, 234, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 90% 80%, rgba(118, 75, 162, 0.03) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

.messages-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
  z-index: 1;
}

/* Scrollbar styling */
.message-list::-webkit-scrollbar {
  width: 10px;
}

.message-list::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.02);
  border-radius: 5px;
}

.message-list::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 5px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

.message-list::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #5568d3 0%, #653a8b 100%);
  border-radius: 5px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

/* Dark mode adjustments */
html.dark .message-list {
  background: linear-gradient(180deg, rgba(26, 26, 26, 0.8) 0%, rgba(45, 45, 45, 0.9) 100%);
}

html.dark .message-list::before {
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(102, 126, 234, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 90% 80%, rgba(118, 75, 162, 0.05) 0%, transparent 50%);
}

html.dark .message-list::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
}

/* Responsive */
@media (max-width: 768px) {
  .message-list {
    padding: 16px;
  }
  
  .messages-container {
    gap: 6px;
  }
}
</style>
