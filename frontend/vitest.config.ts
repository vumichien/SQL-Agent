import { defineConfig, mergeConfig } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      globals: true,
      environment: 'happy-dom',
      setupFiles: ['./tests/setup.ts'],
      css: {
        modules: {
          classNameStrategy: 'non-scoped'
        }
      },
      server: {
        deps: {
          inline: ['element-plus']
        }
      },
      coverage: {
        provider: 'v8',
        reporter: ['text', 'json', 'html', 'lcov'],
        exclude: [
          'node_modules/',
          'tests/',
          'dist/',
          '*.config.ts',
          '*.d.ts',
          'src/main.ts',
          'src/vite-env.d.ts',
          'src/plotly.d.ts'
        ],
        include: ['src/**/*.{ts,vue}'],
        all: true,
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      },
      include: ['tests/**/*.{test,spec}.{js,ts}'],
      exclude: ['node_modules', 'dist', '.idea', '.git', '.cache'],
      testTimeout: 10000
    }
  })
)
