<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4">
    <div class="max-w-lg w-full space-y-6 bg-white rounded-lg shadow-lg p-6">
      <!-- Back Button -->
      <div class="flex items-center mb-6">
        <button
          @click="router.push('/orders')"
          class="inline-flex items-center text-black"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"/>
          </svg>
          Atpakaļ
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="animate-pulse space-y-4">
        <div class="h-6 bg-gray-200 rounded w-3/4"></div>
        <div class="h-4 bg-gray-200 rounded w-2/3"></div>
        <div class="h-4 bg-gray-200 rounded w-full"></div>
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">
        <!-- Order Name and Status -->
        <div class="space-y-2">
          <h1 class="text-2xl font-bold text-gray-900">{{ order.nosaukums || "Nav atrasts" }}</h1>
          <p class="text-gray-600">Statuss: {{ order.status || "Nav norādīts" }}</p>
          <p class="text-gray-600">Daudzums: {{ order.daudzums }}</p>
        </div>

        <!-- Worker Information -->
        <div v-if="order.employee" class="p-4 bg-gray-50 border border-gray-200 rounded-md">
          <h3 class="text-lg font-medium text-gray-800">Darbinieks:</h3>
          <p class="mt-2 text-gray-600">
            {{ order.employee.vards }} {{ order.employee.uzvards }}
          </p>
        </div>

        <!-- Materials Information -->
        <div v-if="order.materials && order.materials.length" class="p-4 bg-gray-50 border border-gray-200 rounded-md">
          <h3 class="text-lg font-medium text-gray-800">Materiāli:</h3>
          <ul class="mt-2 space-y-2">
            <li
              v-for="(material, index) in order.materials"
              :key="index"
              class="flex items-center"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6 text-gray-600 mr-2"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4-4a8 8 0 1111.314 0z"
                />
              </svg>
              <span class="text-gray-800 font-medium">
                Materiāls: {{ material.nosaukums || "Nav norādīts" }}
                (
                  {{
                    material.daudzums !== undefined && material.daudzums !== 'Nav norādīts' && order.daudzums !== undefined
                      ? `${Number(material.daudzums).toLocaleString('lv-LV', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} x ${Number(order.daudzums).toLocaleString('lv-LV', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
                      : "Nav norādīts"
                  }}
                  = {{ Number(material.daudzums * order.daudzums).toLocaleString('lv-LV', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }} {{ material.vieniba || 'vienības' }}
                )
              </span>
            </li>
          </ul>
        </div>

        <!-- Buttons: Only if not finished -->
        <div v-if="order.status !== 'Pabeigts'" class="flex flex-col items-center gap-4">
          <!-- Accept Order Button -->
          <button
            v-if="order.status === 'Nav sākts'"
            @click="acceptOrder"
            class="px-4 py-2 rounded-md bg-gray-700 text-white hover:bg-gray-600"
          >
            Pieņemt pasūtījumu
          </button>

          <!-- Finish Order Button -->
          <button
            v-if="order.status === 'Pieņemts'"
            @click="finishOrder"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Pabeigt pasūtījumu
          </button>
        </div>

        <!-- Error Message -->
        <div
          v-if="error"
          class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded whitespace-pre-line"
          v-html="error"
        >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

// Router setup
const router = useRouter();
const route = useRoute();

// States
const isLoading = ref(true);
const error = ref(null);
const order = ref({});
const isAccepted = ref(false);


const currentUser = {
  id: parseInt(localStorage.getItem("userId")) || null,
};

// Function to get token
const getToken = () => {
  return localStorage.getItem("authToken");
};

// Fetch order details
const fetchOrder = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      error.value = "Token not found";
      isLoading.value = false;
      return;
    }
    const response = await fetch(`http://localhost:5000/orders/${route.params.id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    order.value = data;

    console.log('Order data after fetch:', order.value);
    console.log('Materials in order after fetch:', order.value.materials);

    isAccepted.value = !!data.employee;
  } catch (err) {
    console.error("Error fetching order:", err.message);
    error.value = err.message || "Error fetching order";
  } finally {
    isLoading.value = false;
  }
};

// Accept order
const acceptOrder = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      error.value = "Token not found";
      return;
    }

    const response = await fetch(`http://localhost:5000/api/orders/${route.params.id}/accept`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      error.value = data.error || "Error accepting order";
      return;
    }

    // Обновляем детали заказа сразу после принятия
    await fetchOrder();
    // Принудительно обновляем currentUser.id из localStorage (на случай, если он изменился)
    currentUser.id = parseInt(localStorage.getItem("userId")) || null;
  } catch (err) {
    console.error("Error accepting order:", err);
    error.value = "Error accepting order. Please try again.";
  }
};

// Finish order
const finishOrder = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      error.value = "Token not found";
      return;
    }
    const response = await fetch(`http://localhost:5000/orders/${route.params.id}/finish`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    await fetchOrder();
  } catch (err) {
    console.error("Error finishing order:", err.message);
    error.value = err.message || "Error finishing order";
  }
};

onMounted(() => {
  fetchOrder();
});
</script>
