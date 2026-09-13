import { defineConfig, mergeConfig } from 'vitest/config'

import configuracionVite from './vite.config.ts'

export default mergeConfig(
  configuracionVite,
  defineConfig({
    test: {
      environment: 'jsdom',
      setupFiles: ['./src/test/setup.ts'],
    },
  }),
)
