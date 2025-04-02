<template>
  <div class="h-full bg-gray-100 flex flex-col items-center py-12">
    <div class="w-full max-w-6xl">
      <!-- Поисковая строка -->
      <div class="sticky top-0 bg-gray-100 z-10 px-4 py-2 flex items-center justify-between">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Mēklēšana"
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
        />
        <button @click="showAddForm = true" class="px-4 py-2 bg-black text-white rounded">
          Pievienot
        </button>
      </div>

      <!-- Список заказов -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 px-4 w-full mt-6">
        <div v-for="order in filteredOrders" :key="order._id" class="flex flex-col items-center">
          <div
            class="bg-black rounded-lg w-64 h-64 flex flex-col items-center justify-center cursor-pointer"
            @click="goToDetails(order._id)"
          >
            <h3 class="text-lg font-semibold text-white">{{ order.nosaukums }}</h3>
            <p class="text-sm font-light text-gray-300 mt-2">{{ order.status }}</p>
            <button class="mt-4 px-4 py-2 bg-gray-700 text-white rounded">Sīkāk</button>
          </div>
        </div>
      </div>

      <!-- Форма добавления -->
      <div v-if="showAddForm" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h2 class="text-lg font-semibold mb-4">Добавить заказ</h2>
          <input v-model="newOrder.nosaukums" type="text" placeholder="Название" class="w-full px-4 py-2 border rounded mb-2" />
          <input v-model="newOrder.status" type="text" placeholder="Статус" class="w-full px-4 py-2 border rounded mb-2" />
          <input v-model.number="newOrder.daudzums" type="number" placeholder="Количество" class="w-full px-4 py-2 border rounded mb-2" />
          <button @click="addOrder" class="px-4 py-2 bg-black text-white rounded">Добавить</button>
          <button @click="showAddForm = false" class="px-4 py-2 bg-gray-400 text-white rounded ml-2">Отмена</button>
        </div>
      </div>

      <!-- Сообщение при отсутствии заказов -->
      <div v-if="filteredOrders.length === 0" class="mt-8 text-gray-600 text-center">Nav tādu pasūtījumu</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

// Инициализация роутера
const router = useRouter();

// Состояния
const orders = ref([]);
const searchQuery = ref("");
const showAddForm = ref(false);
const newOrder = ref({ nosaukums: "", status: "", daudzums: 1 });

// Функция для получения токена из localStorage
const getToken = () => {
  return localStorage.getItem("authToken"); // Получаем токен из localStorage
};

// Функция для загрузки заказов с авторизацией
onMounted(async () => {
  try {
    const token = getToken(); // Получаем токен
    if (!token) {
      console.error("Нет токена. Пожалуйста, авторизуйтесь.");
      return;
    }

    // Загружаем заказы с API с передачей токена в заголовке
    const response = await axios.get("http://127.0.0.1:5000/orders", {
      headers: {
        Authorization: `Bearer ${token}`, // Указываем токен в заголовке
      },
    });

    // Преобразуем _id в строку для корректного отображения
    orders.value = response.data.map(order => ({
      ...order,
      _id: String(order._id), // Преобразуем _id в строку
    }));
  } catch (error) {
    console.error("Ошибка загрузки заказов:", error.response ? error.response.data : error.message);
  }
});

// Фильтрация заказов по поисковому запросу
const filteredOrders = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return orders.value.filter(order => 
    order.nosaukums.toLowerCase().includes(query) ||
    order.status.toLowerCase().includes(query)
  );
});

// Переход на страницу деталей заказа
const goToDetails = (id) => {
  router.push({ name: "OrderDetails", params: { id } });
};

// Функция добавления нового заказа
const addOrder = async () => {
  try {
    const token = getToken(); // Получаем токен
    if (!token) {
      console.error("Нет токена. Пожалуйста, авторизуйтесь.");
      return;
    }

    const response = await axios.post("http://127.0.0.1:5000/orders", newOrder.value, {
      headers: {
        Authorization: `Bearer ${token}`, // Указываем токен в заголовке
      },
    });

    // Добавляем новый заказ в список
    orders.value.push({ ...newOrder.value, _id: String(response.data._id) });
    showAddForm.value = false;
    newOrder.value = { nosaukums: "", status: "", daudzums: 1 };
  } catch (error) {
    console.error("Ошибка добавления заказа:", error.response ? error.response.data : error.message);
  }
};
</script>

<style scoped>
/* Можете добавить стили по вашему усмотрению */
</style>
