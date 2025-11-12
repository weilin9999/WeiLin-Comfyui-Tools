import { fileURLToPath, URL } from 'node:url'
import { resolve } from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

/** @type {import('vite').UserConfig} */
// https://vitejs.dev/config/
export default defineConfig({
  define: {
    'process.env.NODE_ENV': '"production"',
  },
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    // outDir: '../javascript',
    // assetsDir: '../',
    minify: true,
    sourcemap: true,
    // watch: {
      // https://rollupjs.org/configuration-options/#watch
    // },
    lib: {
      entry: resolve(__dirname, 'main.js'),
      name: 'weilin-prompt-ui',
      formats: ['umd'],
    },
    rollupOptions: {
      plugins: [
      ],
      output: {
        globals: {
        },
        name: "WeiLinPromptUI",
        dir: '../', // 对于多文件构建，指定文件夹输出路径
        format: 'umd',
        chunkFileNames: 'dist/javascript/[name].chunk.js', // 指定 chunk 文件名称
        entryFileNames: 'dist/javascript/[name].entry.js', // 指定入口文件名称
        assetFileNames: 'dist/style.[ext]'
      },
    },
  }
})