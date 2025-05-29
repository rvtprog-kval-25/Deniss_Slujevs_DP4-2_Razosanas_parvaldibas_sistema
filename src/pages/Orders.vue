<template>
  <div class="min-h-screen bg-gray-100 py-10 px-4 flex flex-col items-center">
    <!-- Кнопка + Поиск в одной строке -->
    <div class="w-full max-w-4xl mb-6 flex items-center gap-4">
      <!-- Кнопка домой -->
      <button
        @click="goHome"
        class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-700 text-white hover:bg-gray-600"
      >
        Uz sākumu
      </button>

      <!-- Поле поиска -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Meklē pasūtījumu..."
        class="flex-1 px-4 py-2 rounded-lg border border-gray-300 shadow-sm focus:ring-2 focus:ring-gray-500 focus:outline-none"
      />

      <select v-model="statusFilter" class="px-4 py-2 rounded-lg border border-gray-300 bg-white shadow-sm focus:ring-2 focus:ring-gray-500 focus:outline-none">
        <option value="">Visi statusi</option>
        <option value="Nav sākts">Nav sākts</option>
        <option value="Pieņemts">Pieņemts</option>
        <option value="Pabeigts">Pabeigts</option>
      </select>
    </div>

    <!-- Список заказов -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 px-4 w-full mt-6">
      <div v-for="order in filteredOrders" :key="order.id" class="flex flex-col items-center">
        <div
          class="bg-white rounded-xl w-72 h-64 flex flex-col items-start justify-between cursor-pointer p-5 shadow hover:shadow-lg transition"
          @click="goToDetails(order.id)"
        >
          <div class="flex items-center justify-between w-full">
            <h3 class="text-lg font-semibold text-gray-900 truncate">{{ order.nosaukums || "Pasūtījums" }}</h3>
            <span
              class="ml-2 px-3 py-1 text-xs font-semibold rounded-full"
              :class="{
                'bg-green-100 text-green-800': order.status === 'Pabeigts',
                'bg-gray-100 text-gray-800': order.status === 'Nav sākts',
                'bg-blue-100 text-blue-800': order.status === 'Pieņemts'
              }"
            >
              {{ order.status || "Nav statusa" }}
            </span>
          </div>
  
          <div class="mt-1 text-sm text-gray-600">Daudzums: {{ Number(order.daudzums).toLocaleString('lv-LV', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</div>
          <div class="mt-1 text-sm text-gray-600" v-if="order.employee">
            Atbildīgais: {{ order.employee.vards }} {{ order.employee.uzvards }}
          </div>
          <div class="mt-1 text-sm text-gray-400 italic" v-else>
            Nav piešķirts atbildīgais
          </div>
          <button class="mt-auto px-4 py-2 bg-gray-800 text-white rounded-lg w-full hover:bg-gray-900 transition">Sīkāk</button>
        </div>
      </div>
    </div>

    <!-- Пусто -->
    <div v-if="filteredOrders.length === 0" class="mt-8 text-gray-600 text-center">
      Nav tādu pasūtījumu
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
const statusFilter = ref("");

const statusOrder = {
  "Pieņemts": 2,
  "Nav sākts": 3,
  "Pabeigts": 4
};

const filteredOrders = computed(() => {
  const query = searchQuery.value.toLowerCase();
  let result = orders.value.filter(order =>
    (order.nosaukums || "").toLowerCase().includes(query) ||
    (order.status || "").toLowerCase().includes(query)
  );
  if (statusFilter.value) {
    result = result.filter(order => order.status === statusFilter.value);
  }
  return result.sort((a, b) => {
    const aOrder = statusOrder[a.status] || 99;
    const bOrder = statusOrder[b.status] || 99;
    if (aOrder !== bOrder) return aOrder - bOrder;
    return (a.nosaukums || '').localeCompare(b.nosaukums || '');
  });
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

    const response = await axios.get("https://kvdarbsbackend.vercel.app/orders", {
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
const goHome = () => {
  router.push('/home');
};
</script>

