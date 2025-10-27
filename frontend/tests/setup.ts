import { vi } from 'vitest'
import { config } from '@vue/test-utils'

// Mock CSS imports
vi.mock('*.css', () => ({}))
vi.mock('element-plus/dist/index.css', () => ({}))
vi.mock('element-plus/theme-chalk/index.css', () => ({}))

// Mock Element Plus auto-import
config.global.stubs = {
  ElButton: true,
  ElInput: true,
  ElForm: true,
  ElFormItem: true,
  ElCard: true,
  ElTable: true,
  ElTableColumn: true,
  ElPagination: true,
  ElDialog: true,
  ElDrawer: true,
  ElDropdown: true,
  ElDropdownMenu: true,
  ElDropdownItem: true,
  ElMenu: true,
  ElMenuItem: true,
  ElSwitch: true,
  ElBadge: true,
  ElAvatar: true,
  ElIcon: true,
  ElTooltip: true,
  ElTag: true,
  ElEmpty: true,
  ElSkeleton: true,
  ElSkeletonItem: true,
  ElTabs: true,
  ElTabPane: true,
  ElSelect: true,
  ElOption: true,
  ElMessage: true,
  ElMessageBox: true,
  ElNotification: true,
  ElLoading: true,
  // Stub Element Plus icons
  User: true,
  Position: true,
  Search: true,
  Edit: true,
  Delete: true,
  View: true,
  Plus: true,
  Close: true,
  Check: true,
  InfoFilled: true,
  WarningFilled: true,
  CircleCloseFilled: true,
  SuccessFilled: true,
  Moon: true,
  Sunny: true,
  Message: true,
  ChatDotRound: true,
  Clock: true,
  Document: true,
  RefreshRight: true,
  Download: true,
  Upload: true,
  Setting: true,
  ArrowLeft: true,
  ArrowRight: true
}

// Mock window.matchMedia for theme detection
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn()
  }))
})

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return []
  }
  unobserve() {}
} as any

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
} as any

// Mock MutationObserver
global.MutationObserver = class MutationObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() {
    return []
  }
} as any
