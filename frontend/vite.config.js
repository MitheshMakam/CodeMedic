import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const apiRoutes = ['/analyze', '/summary', '/bugs', '/security', '/tests', '/readme', '/commit', '/explain', '/improve', '/health']

export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    proxy: Object.fromEntries(apiRoutes.map(route => [route, {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    }])),
  },
})
