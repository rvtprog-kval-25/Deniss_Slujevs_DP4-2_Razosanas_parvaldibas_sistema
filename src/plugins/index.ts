/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import vuetify from './vuetify'
import pinia from '../stores'
import router from '../router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

// Types
import type { App } from 'vue'

export function registerPlugins (app: App) {
  app
    .use(vuetify)
    .use(router)
    .use(pinia)
    .use(Toast, {
      transition: "Vue-Toastification__bounce",
      maxToasts: 3,
      newestOnTop: true
    })
}
