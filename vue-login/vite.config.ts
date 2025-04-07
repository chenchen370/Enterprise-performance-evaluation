import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
import { resolve } from 'path'
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src')
    },
    //extensions: [".ts", ".js", ".vue", ".json", ".mjs"],
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"]
  },

    // 配置服务器的代理设置
    server: {
      // 代理配置，用于重定向请求到其他服务器
      proxy: {
        // 定义一个代理规则，将/hello-world路径下的请求代理到指定的目标服务器
        '/api': {
          // 目标服务器的地址
          target: 'http://127.0.0.1:5000',
          // 更改请求的origin为代理服务器的origin，以便与目标服务器交互
          changeOrigin: true,
          // 重写请求路径，移除/hello-world前缀
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      }
    },
})
