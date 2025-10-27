<template>
  <el-container class="app-layout" direction="vertical">
    <AppHeader />
    <el-container class="main-container" direction="horizontal">
      <AppSidebar />
      <AppMain>
        <slot></slot>
      </AppMain>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
import AppMain from './AppMain.vue'
</script>

<style scoped>
.app-layout {
  height: 100vh;
  width: 100%;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.main-container {
  flex: 1;
  height: calc(100vh - 60px);
  display: flex;
  flex-direction: row;
  overflow: hidden;
}
</style>
