import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router from './router'
import i18n from './i18n'
import './styles/main.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import App from './App.vue'

// Initialize stores
import { useUIStore } from './stores/ui'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

// Setup Pinia with persistence
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.use(i18n) // Add i18n support

// Initialize UI store (apply theme on startup)
const uiStore = useUIStore()
uiStore.initialize()

// Initialize auth store (fetch user profile if token exists)
const authStore = useAuthStore()
authStore.initialize()

app.mount('#app')
