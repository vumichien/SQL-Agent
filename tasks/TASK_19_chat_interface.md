# TASK 19: Chat Interface Components

**Status**: Not Started
**Estimated Time**: 8-10 hours
**Dependencies**: TASK 16, 17, 18 (Element Plus, Stores, Router)

## OVERVIEW
Build complete chat interface with message components and real-time interaction.

## COMPONENTS

### ChatView.vue (Page)
- Layout with messages container + input
- Uses El-Container, El-Header, El-Main

### MessageList.vue
- Scrollable message container
- Auto-scroll to bottom
- Empty state with suggested questions

### UserMessage.vue
```vue
<template>
  <div class="user-message">
    <el-avatar :icon="UserFilled" />
    <div class="message-content">
      {{ message.question }}
    </div>
  </div>
</template>
```

### AssistantMessage.vue
```vue
<template>
  <div class="assistant-message">
    <el-avatar src="/logo.svg" />
    <div class="message-content">
      <SQLDisplay v-if="message.sql" :sql="message.sql" />
      <ResultsTable v-if="message.results" :results="message.results" />
      <PlotlyChart v-if="message.visualization" :figure="message.visualization" />
      <FollowupQuestions v-if="message.followup" :questions="message.followup" />
    </div>
  </div>
</template>
```

### ChatInput.vue
- El-Input with send button
- Loading state
- Enter key support

### LoadingIndicator.vue
- Typing animation
- Uses El-Loading or custom

### EmptyState.vue
- Welcome message
- Suggested questions chips
- Click to ask

## API INTEGRATION
```typescript
// src/api/query.ts
import axios from 'axios'

export const queryAPI = {
  async sendQuery(question: string) {
    const { data } = await axios.post('/api/v0/query', { question })
    return data
  }
}
```

## SUCCESS CRITERIA
- ✅ Chat interface renders
- ✅ Can send messages
- ✅ Receives responses
- ✅ Loading states working
- ✅ Auto-scroll working

**Created**: 2025-10-27
