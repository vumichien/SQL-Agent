<template>
  <div class="app-container">
    <!-- Routes that don't need the app layout (login, register) -->
    <template v-if="!useLayout">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </template>

    <!-- Routes that use the app layout (chat, history, etc.) -->
    <AppLayout v-else>
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </AppLayout>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import AppLayout from './components/AppLayout.vue'

const route = useRoute()

// Determine if current route should use the app layout
const useLayout = computed(() => {
  const noLayoutRoutes = ['/login', '/register', '/404']
  return !noLayoutRoutes.includes(route.path) && route.name !== 'NotFound'
})
</script>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
}

/* Route transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
