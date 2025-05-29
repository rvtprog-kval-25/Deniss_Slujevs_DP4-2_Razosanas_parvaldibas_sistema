import { createApp, h } from 'vue';
import Toast from './components/Toast.vue';

export function showToast(message, type = 'info', duration = 3500, custom = null) {
  const mountNode = document.createElement('div');
  document.body.appendChild(mountNode);

  const app = createApp({
    render() {
      return h(
        Toast,
        { message, type, duration },
        custom ? { default: custom } : undefined
      );
    }
  });
  app.mount(mountNode);
} 