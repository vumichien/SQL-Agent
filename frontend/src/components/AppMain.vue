<template>
  <el-main class="app-main">
    <slot></slot>
  </el-main>
</template>

<script setup lang="ts">
// Main content area - just a wrapper for now
</script>

<style scoped>
.app-main {
  background: linear-gradient(135deg, #f5f7fa 0%, #f8f9fb 50%, #fafbfc 100%);
  padding: 0;
  overflow-y: auto;
  height: calc(100vh - 60px);
  position: relative;
}

.app-main::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.03) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.03) 0%, transparent 50%);
  pointer-events: none;
}

/* Scrollbar styling */
.app-main::-webkit-scrollbar {
  width: 8px;
}

.app-main::-webkit-scrollbar-track {
  background: transparent;
}

.app-main::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
}

.app-main::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #5568d3 0%, #653a8b 100%);
}

/* Dark mode adjustments */
html.dark .app-main {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1f1f1f 100%);
}

html.dark .app-main::before {
  background-image: 
    radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.05) 0%, transparent 50%);
}
</style>
