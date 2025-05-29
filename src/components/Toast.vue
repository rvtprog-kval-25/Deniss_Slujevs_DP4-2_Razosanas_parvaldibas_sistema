<template>
  <transition name="toast-fade">
    <div v-if="visible" :class="['toast', type]" @mouseenter="pause" @mouseleave="resume">
      <slot>
        {{ message }}
      </slot>
    </div>
  </transition>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  message: String,
  type: { type: String, default: 'info' }, // info, success, error
  duration: { type: Number, default: 3500 }
});

const visible = ref(true);
let timer = null;

const close = () => (visible.value = false);

const pause = () => clearTimeout(timer);
const resume = () => {
  timer = setTimeout(close, props.duration);
};

onMounted(() => {
  timer = setTimeout(close, props.duration);
});
onUnmounted(() => clearTimeout(timer));
</script>

<style scoped>
.toast {
  position: fixed;
  top: 30px;
  right: 30px;
  min-width: 220px;
  max-width: 350px;
  padding: 16px 24px;
  border-radius: 8px;
  color: #ffffff;
  font-weight: 500;
  box-shadow: 0 2px 16px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  opacity: 0.98;
  font-size: 1rem;
}
.toast.info { background: #558bff; }
.toast.success { background: #41ff87; }
.toast.error { background: #ff5252; }
.toast-fade-enter-active, .toast-fade-leave-active { transition: opacity 0.4s; }
.toast-fade-enter-from, .toast-fade-leave-to { opacity: 0; }
</style> 
