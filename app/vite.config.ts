
/// <reference types="vitest" />
import { getViteConfig } from 'astro/config';

export default getViteConfig({
  test: {
    environment: 'node',
    globals: true,
    include: [
      '**/*.{test,spec}.{js,ts,jsx,tsx}',
    ],
    css: true,
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      reportsDirectory: 'coverage',
      all: true,
      include: ['src/**/*.{js,jsx,ts,tsx,astro}']
    }
  },
});
