<template>
  <div class="w-full h-full flex items-center justify-center bg-gray-100">
    <div class="max-w-md w-full space-y-8 p-6 bg-white rounded-lg shadow-md">
      <h2 class="text-center text-3xl font-extrabold text-gray-900">Sveiks</h2>
      <form @submit.prevent="handleLogin" class="mt-8 space-y-6">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="kods" class="sr-only">Kods</label>
            <input
              id="kods"
              v-model="kods"
              name="kods"
              type="text"
              autocomplete="off"
              required
              :class="[
                'appearance-none rounded-none relative block w-full px-3 py-2 border text-gray-900 rounded-t-md focus:outline-none focus:ring-gray-500 focus:border-gray-500 focus:z-10 sm:text-sm',
                errorMessage ? 'border-red-500 focus:border-red-500' : ''
              ]"
              placeholder="Ievadiet kodu"
            />
          </div>
        </div>
        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-gray-600 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all"
            :disabled="isSubmitting"
            :class="{ 'bg-gray-500 cursor-not-allowed': isSubmitting }"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3"></span>
            Ieiet
          </button>
        </div>
        <!-- Error Message with Animation -->
        <transition name="error-pulse">
          <div v-if="errorMessage" class="text-red-500 text-center mt-4">{{ errorMessage }}</div>
        </transition>
      </form>
      <!-- Success Message with Animation -->
      <transition name="success-slide">
        <div
          v-if="showSuccess"
          class="fixed bottom-0 left-1/2 transform -translate-x-1/2 mb-4 p-4 w-96 bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 transition-all"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <svg
                class="h-6 w-6 text-green-500"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l7.146 4.949a2 2 0 002.827 0l7.146-4.949M5 19l7.146-4.949a2 2 0 012.827 0l7.146 4.949m-14.292 0L12 8.95l12.292 8.55"
                />
              </svg>
              <h3 class="ml-2 text-lg font-semibold text-green-600">{{ successMessage }}</h3>
            </div>
            <button @click="showSuccess = false" class="text-gray-400 hover:text-gray-600 transition">
              <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </div>
          <p class="mt-2 text-gray-600">Jūs esat veiksmīgi ielogots!</p>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const kods = ref("");
const errorMessage = ref("");
const showSuccess = ref(false);
const successMessage = ref("");
const isSubmitting = ref(false);

const handleLogin = async () => {
  errorMessage.value = "";
  showSuccess.value = false;
  isSubmitting.value = true;

  if (!kods.value.trim()) {
    errorMessage.value = "Lūdzu, ievadiet derīgu kodu";
    isSubmitting.value = false;
    return;
  }

  try {
    const response = await axios.post("http://127.0.0.1:5000/login", { kods: kods.value });

    if (response.data.success) {
      localStorage.setItem("authToken", response.data.token);
      localStorage.setItem("userId", response.data.user.id); // ✅ Сохраняем userId

      successMessage.value = `${response.data.user.vards} ${response.data.user.uzvards}`;
      showSuccess.value = true;

      setTimeout(() => {
        showSuccess.value = false;
        const redirectPath = response.data.redirect;
        if (redirectPath) {
          router.push(redirectPath);
        }
      }, 2000);
    } else {
      errorMessage.value = "Nepareizs kods";
    }
  } catch (error) {
    if (error.response?.data?.error) {
      errorMessage.value = error.response.data.error;
    } else if (error.code === "ERR_NETWORK") {
      errorMessage.value = "Nav savienojuma ar serveri";
    } else {
      errorMessage.value = "Servera kļūda";
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style>
/* Error animation (pulse) */
.error-pulse-enter-active,
.error-pulse-leave-active {
  animation: pulse 1.2s;
  transition: opacity 0.3s;
}
.error-pulse-enter-from,
.error-pulse-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

/* Success animation (slide up) */
.success-slide-enter-active {
  animation: slide-up 0.5s;
}
.success-slide-leave-active {
  animation: slide-up 0.5s reverse;
}
@keyframes slide-up {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>