<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-xl shadow-2xl transform transition-all duration-300 hover:scale-[1.02]">
      <div>
        <h2 class="mt-6 text-center text-4xl font-extrabold text-gray-900 tracking-tight">
          Sveiks
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Ievadiet savu kodu, lai turpinātu
        </p>
      </div>

      <!-- Code Input Form -->
      <form @submit.prevent="handleLogin" v-if="!isPasswordInput" class="mt-8 space-y-6">
        <div class="rounded-md shadow-sm -space-y-px">
          <div class="relative">
            <label for="kods" class="sr-only">Kods</label>
            <input
              id="kods"
              v-model="kods"
              name="kods"
              type="text"
              autocomplete="off"
              required
              :class="[ 
                'appearance-none relative block w-full px-4 py-3 border text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 sm:text-sm transition-all duration-200',
                errorMessage ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : 'border-gray-300'
              ]"
              placeholder="Ievadiet kodu"
            />
            <div v-if="errorMessage" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200 transform hover:scale-[1.02]"
            :disabled="isSubmitting"
            :class="{ 'opacity-50 cursor-not-allowed': isSubmitting }"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg v-if="!isSubmitting" class="h-5 w-5 text-gray-300 group-hover:text-gray-200" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isSubmitting ? 'Ielogošanās...' : 'Ieiet' }}
          </button>
        </div>

        <transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <div v-if="errorMessage" class="rounded-md bg-red-50 p-4 mt-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-red-800">{{ errorMessage }}</p>
              </div>
            </div>
          </div>
        </transition>
      </form>

      <!-- Password Input Form -->
      <form v-if="isPasswordInput" @submit.prevent="handlePasswordSubmit" class="mt-8 space-y-6">
        <div class="rounded-md shadow-sm -space-y-px">
          <div class="relative">
            <label for="password" class="sr-only">Parole</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              required
              :class="[ 
                'appearance-none relative block w-full px-4 py-3 border text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 sm:text-sm transition-all duration-200',
                passwordErrorMessage ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : 'border-gray-300'
              ]"
              placeholder="Ievadiet paroli"
            />
            <div v-if="passwordErrorMessage" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-red-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gray-800 hover:bg-gray-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-all duration-200 transform hover:scale-[1.02]"
            :disabled="isSubmitting"
            :class="{ 'opacity-50 cursor-not-allowed': isSubmitting }"
          >
            <span class="absolute left-0 inset-y-0 flex items-center pl-3">
              <svg v-if="!isSubmitting" class="h-5 w-5 text-gray-300 group-hover:text-gray-200" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
            {{ isSubmitting ? 'Ielogošanās...' : 'Ielogoties kā administrators' }}
          </button>
        </div>

        <transition
          enter-active-class="transition ease-out duration-300"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-200"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <div v-if="passwordErrorMessage" class="rounded-md bg-red-50 p-4 mt-4">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm font-medium text-red-800">{{ passwordErrorMessage }}</p>
              </div>
            </div>
          </div>
        </transition>
      </form>

      <!-- Success Message -->
      <transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div
          v-if="showSuccess"
          class="fixed bottom-0 left-1/2 transform -translate-x-1/2 mb-4 p-4 w-96 bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5"
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
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
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
import { useRouter } from "vue-router";

const router = useRouter();
const kods = ref("");
const password = ref("");
const isPasswordInput = ref(false);
const errorMessage = ref("");
const passwordErrorMessage = ref("");
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
    const response = await fetch("http://localhost:5000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ kods: kods.value }),
    });

    const data = await response.json();

    if (response.ok) {
      if (data.user.amats === "Administrators") {
        isPasswordInput.value = true;
      } else {
        localStorage.setItem("token", data.token);
        localStorage.setItem("userRole", data.user.amats);
        localStorage.setItem("userId", data.user.id);
        showSuccess.value = true;
        successMessage.value = "Veiksmīga ielogošanās!";
        setTimeout(() => {
          router.push(data.redirect || "/");
        }, 1000);
      }
    } else {
      throw new Error(data.error || "Login failed");
    }
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isSubmitting.value = false;
  }
};

const handlePasswordSubmit = async () => {
  passwordErrorMessage.value = "";
  showSuccess.value = false;
  isSubmitting.value = true;

  if (!password.value.trim()) {
    passwordErrorMessage.value = "Lūdzu, ievadiet paroli";
    isSubmitting.value = false;
    return;
  }

  try {
    const response = await fetch("http://localhost:5000/login/password", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ kods: kods.value, password: password.value }),
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("userRole", data.user.amats);
      localStorage.setItem("userId", data.user.id);
      showSuccess.value = true;
      successMessage.value = "Veiksmīga ielogošanās!";
      setTimeout(() => {
        router.push(data.redirect || "/admin");
      }, 1000);
    } else {
      throw new Error(data.error || "Login with password failed");
    }
  } catch (error) {
    passwordErrorMessage.value = error.message;
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
.error-pulse-enter-active,
.error-pulse-leave-active {
  transition: all 0.3s ease-in-out;
}
.error-pulse-enter-from,
.error-pulse-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

.success-slide-enter-active,
.success-slide-leave-active {
  transition: all 0.3s ease-out;
}
.success-slide-enter-from,
.success-slide-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>
