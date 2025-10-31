<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const emit = defineEmits<{
  selectQuestion: [question: string]
}>()

// Suggested questions in multiple languages
const suggestions = [
  { text: 'How many customers are there?', icon: '' },
  { text: 'What are the total sales by country?', icon: '' },
  { text: '顧客数を教えてください', icon: '' },
  { text: '国別の総売上を表示してください', icon: '' },
  { text: '従業員とその役職をリストアップ', icon: '' }
]

const handleQuestionClick = (question: string) => {
  emit('selectQuestion', question)
}
</script>

<template>
  <div class="empty-state">
    <div class="icon">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        <circle cx="9" cy="10" r="1" fill="currentColor"></circle>
        <circle cx="12" cy="10" r="1" fill="currentColor"></circle>
        <circle cx="15" cy="10" r="1" fill="currentColor"></circle>
      </svg>
    </div>
    <h2>{{ t('chat.welcomeTitle') }}</h2>
    <p>{{ t('chat.welcomeMessage') }}</p>

    <!-- Suggestion Pills -->
    <div class="suggestions">
      <button
        v-for="(suggestion, index) in suggestions"
        :key="index"
        class="suggestion-pill"
        @click="handleQuestionClick(suggestion.text)"
      >
        <span class="suggestion-icon">{{ suggestion.icon }}</span>
        <span class="suggestion-text">{{ suggestion.text }}</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 20px;
  text-align: center;
  height: 100%;
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.icon {
  width: 120px;
  height: 120px;
  margin-bottom: 32px;
  position: relative;
  animation: float 3s ease-in-out infinite;
}

.icon::before {
  content: '';
  position: absolute;
  inset: -20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.15));
  border-radius: 50%;
  filter: blur(20px);
  animation: pulse 2s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.1);
  }
}

.icon svg {
  width: 100%;
  height: 100%;
  stroke: url(#gradient);
  position: relative;
  z-index: 1;
}

.icon svg path,
.icon svg circle {
  stroke: #667eea;
}

h2 {
  margin: 0 0 16px 0;
  font-size: 42px;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -1px;
  line-height: 1.2;
}

p {
  margin: 0 0 40px 0;
  color: var(--el-text-color-secondary);
  font-size: 20px;
  line-height: 1.6;
  max-width: 600px;
  font-weight: 400;
}

.suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  max-width: 800px;
  animation: slideUp 0.6s ease-out 0.2s backwards;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.suggestion-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.9);
  border: 2px solid transparent;
  border-radius: 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  font-size: 14px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  backdrop-filter: blur(10px);
}

.suggestion-pill:hover {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.2);
}

.suggestion-pill:active {
  transform: translateY(0);
}

.suggestion-icon {
  font-size: 18px;
  line-height: 1;
  display: flex;
  align-items: center;
}

.suggestion-text {
  white-space: nowrap;
  line-height: 1.4;
}

/* Dark mode adjustments */
html.dark .icon svg path,
html.dark .icon svg circle {
  stroke: #8b9ef9;
}

html.dark h2 {
  background: linear-gradient(135deg, #8b9ef9 0%, #9d7fc0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

html.dark .suggestion-pill {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

html.dark .suggestion-pill:hover {
  background: linear-gradient(135deg, rgba(139, 158, 249, 0.2) 0%, rgba(157, 127, 192, 0.2) 100%);
  border-color: rgba(139, 158, 249, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
  .empty-state {
    padding: 60px 20px;
  }
  
  .icon {
    width: 90px;
    height: 90px;
    margin-bottom: 24px;
  }
  
  h2 {
    font-size: 32px;
  }
  
  p {
    font-size: 17px;
    margin-bottom: 32px;
  }
  
  .suggestions {
    gap: 10px;
  }
  
  .suggestion-pill {
    padding: 10px 16px;
    font-size: 13px;
  }
  
  .suggestion-icon {
    font-size: 16px;
  }
  
  .suggestion-text {
    white-space: normal;
    text-align: left;
  }
}
</style>
