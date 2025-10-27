<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import type { RouteLocationMatched } from 'vue-router'

const route = useRoute()
const { t } = useI18n()

// Map route names to translation keys
const routeTitleMap: Record<string, string> = {
  'Chat': 'nav.chat',
  'History': 'nav.history',
  'Training': 'nav.training',
  'Settings': 'nav.settings',
  'Login': 'nav.login',
  'Register': 'nav.register',
  'NotFound': 'errors.404'
}

// Generate breadcrumb items from current route
const breadcrumbs = computed(() => {
  const matched = route.matched.filter((item) => item.meta && item.meta.title)

  return matched.map((item: RouteLocationMatched) => ({
    path: item.path,
    title: item.meta.title as string,
    icon: item.meta.icon as string | undefined
  }))
})

// Check if current breadcrumb is active (last item)
const isActive = (index: number) => {
  return index === breadcrumbs.value.length - 1
}

// Get translated title
const getTranslatedTitle = (title: string) => {
  // Find the route name that matches the title
  const routeName = Object.keys(routeTitleMap).find(key => title.includes(key))
  if (routeName && routeTitleMap[routeName]) {
    return t(routeTitleMap[routeName])
  }
  return title
}
</script>

<template>
  <el-breadcrumb separator="/" class="breadcrumb">
    <el-breadcrumb-item
      v-for="(item, index) in breadcrumbs"
      :key="item.path"
      :to="isActive(index) ? undefined : item.path"
    >
      <el-icon v-if="item.icon" class="breadcrumb-icon">
        <component :is="item.icon" />
      </el-icon>
      <span>{{ getTranslatedTitle(item.title) }}</span>
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<style scoped>
.breadcrumb {
  font-size: 14px;
}

.breadcrumb :deep(.el-breadcrumb__separator) {
  color: rgba(255, 255, 255, 0.6);
  font-weight: 300;
}

.breadcrumb :deep(.el-breadcrumb__inner) {
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  font-weight: 500;
}

.breadcrumb :deep(.el-breadcrumb__inner:hover) {
  color: #ffffff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.breadcrumb-icon {
  margin-right: 6px;
  vertical-align: middle;
}

.breadcrumb :deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: #ffffff;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.breadcrumb :deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner:hover) {
  color: #ffffff;
}
</style>
