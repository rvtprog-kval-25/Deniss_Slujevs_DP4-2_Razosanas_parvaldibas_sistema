<template>
  <div class="h-full bg-gray-100 flex flex-col items-center py-12">
    <div class="w-full max-w-6xl">
      <!-- Поисковая строка -->
      <div class="sticky top-0 bg-gray-100 z-10 px-4 py-2 flex items-center justify-between">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Meklēšana"
          class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
        />
      </div>

      <!-- Список заказов -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 px-4 w-full mt-6">
        <div v-for="order in filteredOrders" :key="order.id" class="flex flex-col items-center">
          <div
            class="bg-black rounded-lg w-64 h-64 flex flex-col items-center justify-center cursor-pointer p-4"
            @click="goToDetails(order.id)"
          >
            <h3 class="text-lg font-semibold text-white">{{ order.nosaukums || "Pasūtījums" }}</h3>
            <p class="text-sm font-light text-gray-300 mt-2">{{ order.status || "Nav statusa" }}</p>
            

            <!-- Ответственный -->
            <p v-if="order.employee" class="text-sm text-white mt-2">
              Atbildīgais: {{ order.employee.vards }} {{ order.employee.uzvards }}
            </p>
            <p v-else class="text-sm text-gray-400 italic mt-2">
              Nav piešķirts Atbildīgais
            </p>

            <button class="mt-4 px-4 py-2 bg-gray-700 text-white rounded">Sīkāk</button>
          </div>
        </div>
      </div>

      <!-- Пусто -->
      <div v-if="filteredOrders.length === 0" class="mt-8 text-gray-600 text-center">
        Nav tādu pasūtījumu
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const orders = ref([]);
const searchQuery = ref("");

// Фильтр заказов
const filteredOrders = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return orders.value.filter(order =>
    (order.nosaukums || "").toLowerCase().includes(query) ||
    (order.status || "").toLowerCase().includes(query)
  );
});

// Получение токена
const getToken = () => {
  return localStorage.getItem("authToken");
};

// Получение заказов с бэка
onMounted(async () => {
  try {
    const token = getToken();
    if (!token) {
      console.error("Нет токена. Пожалуйста, авторизуйтесь.");
      return;
    }

    const response = await axios.get("http://127.0.0.1:5000/orders", {
      headers: { Authorization: `Bearer ${token}` },
    });

    orders.value = response.data;
  } catch (error) {
    console.error("Kļūda saņemot pasūtījumus:", error.response ? error.response.data : error.message);
  }
});

// Переход к деталям
const goToDetails = (id) => {
  router.push({ name: "OrderDetails", params: { id } });
};
</script>

<style scoped>
/* Простая анимация загрузки и плавность */
</style>
