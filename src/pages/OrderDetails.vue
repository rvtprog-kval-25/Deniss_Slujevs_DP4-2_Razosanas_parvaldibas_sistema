<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4">
    <div class="max-w-lg w-full space-y-6 bg-white rounded-lg shadow-lg p-6">
      <!-- Back Button -->
      <div class="flex items-center mb-6">
        <button
          @click="router.push('/orders')"
          class="inline-flex items-center text-indigo-600 hover:text-indigo-800 transition-colors"
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
        </div>

        <!-- Worker Information -->
        <div v-if="order.darbinieks" class="p-4 bg-blue-50 border border-blue-100 rounded-md">
          <h3 class="text-lg font-medium text-gray-800">Darbinieks:</h3>
          <p class="mt-2 text-gray-600">
            {{ order.darbinieks.vards }} {{ order.darbinieks.uzvards }}
          </p>
        </div>

        <!-- Materials Information -->
        <div v-if="order.materials && order.materials.length" class="p-4 bg-blue-50 border border-blue-100 rounded-md">
          <h3 class="text-lg font-medium text-gray-800">Materiāli:</h3>
          <ul class="mt-2 space-y-2">
            <li
              v-for="(material, index) in order.materials"
              :key="index"
              class="flex items-center"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6 text-blue-600 mr-2"
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
              <span class="text-blue-800 font-medium">
                Materiāls: {{ material.material_name || "Nav norādīts" }} ({{ material.quantity || "Nav norādīts" }} vienības)
              </span>
            </li>
          </ul>
        </div>

        <!-- Error Message -->
        <div
          v-if="error"
          class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded"
        >
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();

// States for loading, error, and order data
const isLoading = ref(true);
const error = ref(null);
const order = ref({});

// Function to get the token from localStorage
const getToken = () => {
  return localStorage.getItem("authToken"); // Get token from localStorage
};

// Fetch order by ID with token in the header
const fetchOrder = async () => {
  try {
    const orderId = route.params.id; // Get order ID from URL
    const token = getToken(); // Get the token

    if (!token) {
      throw new Error("Nav pieejams autorizācijas tokens. Lūdzu, piesakieties.");
    }

    // Fetch order with authorization token in header
    const response = await fetch(`http://127.0.0.1:5000/orders/${orderId}`, {
      headers: {
        Authorization: `Bearer ${token}`, // Add token to the headers
      },
    });
    
    if (!response.ok) {
      throw new Error("Pasūtījums nav atrasts");
    }

    const data = await response.json();
    order.value = data;
  } catch (err) {
    error.value = err.message || "Error fetching order";
    order.value = { nosaukums: "Nav atrasts" };
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchOrder();
});
</script>
