<template>
  <div class="h-full bg-gray-100 flex flex-col items-center py-12">
    <!-- Поисковая строка -->
    <div class="w-full max-w-4xl px-4 mb-6">
      <div class="sticky top-0 bg-gray-100 z-10">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Meklē materiālus"
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-transparent transition-all"
        />
      </div>
    </div>

    <!-- Состояние загрузки -->
    <div v-if="loading" class="text-gray-600 text-center">Dati tiek ielādēti...</div>

    <!-- Ошибка загрузки -->
    <div v-if="error" class="text-red-500 text-center">Kļūda: {{ error }}</div>

    <!-- Список материалов -->
    <div v-if="!loading && !error" class="w-full max-w-6xl bg-white rounded-lg shadow-md">
      <ul>
        <li
          v-for="material in filteredMaterials"
          :key="material._id"
          class="flex items-center justify-between px-6 py-4 border-b last:border-b-0 hover:bg-gray-100 transition-colors cursor-pointer"
        >
          <!-- Информация о материале -->
          <div>
            <h3 class="text-lg font-semibold text-gray-800">{{ material.nosaukums }}</h3>
            <p class="text-sm text-gray-600">Daudzums: {{ material.daudzums }}</p>
          </div>
          <!-- Кнопка подробнее -->
          <button
            @click="goToDetails(material._id)"
            class="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600 transition-colors"
          >
            Sīkāk
          </button>
        </li>
      </ul>
    </div>

    <!-- Сообщение при отсутствии результатов -->
    <div
      v-if="!loading && !error && filteredMaterials.length === 0"
      class="mt-8 text-gray-600 text-center"
    >
      Nav atbilstošu materiālu
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const materials = ref([]);
const searchQuery = ref("");
const loading = ref(true);
const error = ref(null);

// Функция загрузки данных с Flask API
const fetchMaterials = async () => {
  const token = localStorage.getItem('authToken');  // Чтение токена из localStorage
  if (!token) {
    error.value = "Token not found!";
    loading.value = false;
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/materials", {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,  // Отправка токена в заголовке Authorization
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error("Neizdevās ielādēt materiālus");
    }

    materials.value = await response.json();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

// Загружаем данные при монтировании компонента
onMounted(fetchMaterials);

// Фильтрация материалов по поисковому запросу
const filteredMaterials = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return materials.value.filter(
    (material) =>
      material.nosaukums.toLowerCase().includes(query) ||
      material.daudzums.toString().includes(query)
  );
});

// Функция перехода к деталям материала
const goToDetails = (id) => {
  console.log("Navigating to material with ID:", id); // Лог
  router.push({ name: "MaterialDetails", params: { id: String(id) } });
};
</script>

<style scoped>
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
li:last-child {
  border-bottom: none;
}
</style>
