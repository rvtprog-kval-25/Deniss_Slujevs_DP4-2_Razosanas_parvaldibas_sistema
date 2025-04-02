<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4">
    <div class="max-w-lg w-full space-y-6 bg-white rounded-lg shadow-lg p-6">
      <!-- Кнопка "Назад" -->
      <div class="flex items-center mb-6">
        <button
          @click="router.push('/materials')"
          class="inline-flex items-center text-indigo-600 hover:text-indigo-800 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          Atpakaļ
        </button>
      </div>

      <!-- Загрузка данных -->
      <div v-if="isLoading" class="animate-pulse space-y-4">
        <div class="h-6 bg-gray-200 rounded w-3/4"></div>
        <div class="h-4 bg-gray-200 rounded w-2/3"></div>
        <div class="h-4 bg-gray-200 rounded w-full"></div>
        <div class="h-12 bg-gray-200 rounded w-1/2"></div>
      </div>

      <!-- Отображение данных материала -->
      <div v-else class="space-y-6">
        <div class="space-y-2">
          <h1 class="text-2xl font-bold text-gray-900">{{ material.nosaukums || "Nav atrasts" }}</h1>
          <p class="text-black text-sm">Daudzums: {{ material.daudzums || "Nav norādīts" }}</p>
        </div>

        <!-- Информация о складе -->
        <div class="p-4 bg-blue-50 border border-blue-100 rounded-md">
          <h3 class="text-lg font-medium text-gray-800">Noliktavas informācija:</h3>
          <div class="flex items-center mt-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600 mr-2" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M3 10h11l5-5M3 14h8l5 5"/>
            </svg>
            <span class="text-blue-800 font-medium">
              Noliktava: {{ material.warehouse?.warehouse_name || "Nezināms noliktava" }}
            </span>
          </div>
        </div>

        <!-- Ошибка -->
        <div v-if="material.nosaukums === 'Nav atrasts' || error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          Materiāls ar šādu ID nav atrasts.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

// Инициализация роутера и маршрута
const router = useRouter();
const route = useRoute();

// Состояния
const isLoading = ref(true); // Флаг загрузки
const error = ref(null); // Ошибка
const material = ref({}); // Данные материала

// Функция для получения данных материала
const fetchMaterial = async () => {
  try {
    const materialId = route.params.id; // Получаем ID материала из URL
    console.log("Fetching material with ID:", materialId);

    // Извлекаем токен из localStorage
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      throw new Error("Нет токена. Пожалуйста, авторизуйтесь.");
    }

    // Запрос к API с токеном в заголовке
    const response = await fetch(`http://127.0.0.1:5000/materials/${materialId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`, // Передаем токен в заголовке
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error("Materiāls nav atrasts");
    }

    const data = await response.json(); // Парсим данные
    console.log("Fetched material data:", data);

    // Проверяем, что данные содержат необходимые поля
    if (!data.nosaukums || !data.warehouse) {
      throw new Error("Nepilnīgi dati par materiālu");
    }

    material.value = data; // Сохраняем данные
  } catch (err) {
    console.error("Error fetching material:", err.message);
    error.value = err.message;
    material.value = { nosaukums: "Nav atrasts", description: "Materiāls ar šādu ID nav atrasts." };
  } finally {
    isLoading.value = false; // Завершаем загрузку
  }
};

// Вызываем функцию при монтировании компонента
onMounted(fetchMaterial);
</script>

<style scoped>
/* Дополнительные стили */
.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
