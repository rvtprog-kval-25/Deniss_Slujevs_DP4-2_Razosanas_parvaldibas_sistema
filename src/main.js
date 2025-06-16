import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/axios'  // Добавляем импорт настроенного axios

const app = createApp(App)
app.use(router)
app.mount('#app') 