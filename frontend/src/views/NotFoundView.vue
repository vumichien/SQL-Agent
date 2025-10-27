<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/chat')
}
</script>

<template>
  <div class="not-found-view">
    <el-result
      icon="warning"
      title="404"
      sub-title="Page not found"
    >
      <template #extra>
        <el-button type="primary" @click="goHome">Back to Chat</el-button>
      </template>
    </el-result>
  </div>
</template>

<style scoped>
.not-found-view {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--el-bg-color);
}
</style>
