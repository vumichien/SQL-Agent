<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  loading?: boolean
}>()

const emit = defineEmits<{
  send: [question: string]
}>()

const inputValue = ref('')

const handleSend = () => {
  const question = inputValue.value.trim()
  if (question && !props.loading) {
    emit('send', question)
    inputValue.value = ''
  }
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    handleSend()
  }
}
</script>

<template>
  <div class="chat-input">
    <div class="input-wrapper">
      <el-input
        v-model="inputValue"
        type="textarea"
        :rows="1"
        :autosize="{ minRows: 1, maxRows: 4 }"
        :disabled="loading"
        :placeholder="t('chat.inputPlaceholder')"
        resize="none"
        class="input-field"
        @keydown="handleKeyDown"
      />
      <button
        :disabled="!inputValue.trim() || loading"
        class="send-button"
        @click="handleSend"
      >
        <svg v-if="!loading" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M22 2L11 13"></path>
          <path d="M22 2L15 22L11 13L2 9L22 2Z"></path>
        </svg>
        <div v-else class="spinner"></div>
      </button>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  padding: 24px;
  background: transparent;
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: #ffffff;
  border-radius: 28px;
  padding: 8px 8px 8px 20px;
  box-shadow: 
    0 2px 12px rgba(0, 0, 0, 0.08),
    0 0 0 1px rgba(0, 0, 0, 0.04);
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  box-shadow: 
    0 4px 24px rgba(102, 126, 234, 0.15),
    0 0 0 2px rgba(102, 126, 234, 0.3);
  transform: translateY(-1px);
}

.input-field {
  flex: 1;
  min-width: 0;
}

.input-field :deep(.el-textarea__inner) {
  padding: 10px 0;
  font-size: 15px;
  line-height: 1.5;
  border: none;
  background: transparent;
  box-shadow: none;
  resize: none;
  color: var(--el-text-color-primary);
}

.input-field :deep(.el-textarea__inner:focus) {
  border: none;
  box-shadow: none;
  outline: none;
}

.input-field :deep(.el-textarea__inner::placeholder) {
  color: var(--el-text-color-placeholder);
}

.send-button {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.send-button svg {
  width: 20px;
  height: 20px;
  transform: rotate(45deg);
  transition: transform 0.2s ease;
}

.send-button:hover:not(:disabled) {
  transform: scale(1.08);
  box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4);
}

.send-button:hover:not(:disabled) svg {
  transform: rotate(45deg) translateX(1px) translateY(-1px);
}

.send-button:active:not(:disabled) {
  transform: scale(0.95);
}

.send-button:disabled {
  background: #e5e7eb;
  cursor: not-allowed;
  opacity: 0.5;
  box-shadow: none;
}

.send-button:disabled svg {
  opacity: 0.5;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Dark mode adjustments */
html.dark .input-wrapper {
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 
    0 2px 12px rgba(0, 0, 0, 0.3),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

html.dark .input-wrapper:focus-within {
  box-shadow: 
    0 4px 24px rgba(102, 126, 234, 0.3),
    0 0 0 2px rgba(102, 126, 234, 0.5);
}

html.dark .input-field :deep(.el-textarea__inner) {
  color: #ffffff;
}

html.dark .send-button:disabled {
  background: rgba(255, 255, 255, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .chat-input {
    padding: 16px;
  }
  
  .input-wrapper {
    padding: 6px 6px 6px 16px;
  }
  
  .input-field :deep(.el-textarea__inner) {
    padding: 8px 0;
    font-size: 14px;
  }
  
  .send-button {
    width: 40px;
    height: 40px;
  }
  
  .send-button svg {
    width: 18px;
    height: 18px;
  }
}
</style>
