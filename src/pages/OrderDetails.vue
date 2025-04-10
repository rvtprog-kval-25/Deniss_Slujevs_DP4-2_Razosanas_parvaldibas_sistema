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
                  Materiāls: {{ material.material_name || "Nav norādīts" }}
                  (
                    {{
                      material.quantity !== undefined && material.quantity !== 'Nav norādīts' && order.daudzums !== undefined
                        ? `${material.quantity} x ${order.daudzums}`
                        : "Nav norādīts"
                    }}
                    = {{ (parseInt(material.quantity) || 0) * (parseInt(order.daudzums) || 0) }} vienības
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
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Pieņemt pasūtījumu
          </button>

          <!-- Finish Order Button -->
          <button
            v-if="order.status === 'Pieņemts' && order.employee && order.employee.id === currentUser.id"
            @click="finishOrder"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
          >
            Pabeigt pasūtījumu
          </button>
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
    const orderId = route.params.id;
    const token = getToken();

    if (!token) throw new Error("Nav pieejams autorizācijas tokens. Lūdzu, piesakieties.");

    const response = await fetch(`http://127.0.0.1:5000/orders/${orderId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) throw new Error("Pasūtījums nav atrasts");

    const data = await response.json();
    order.value = data;

    isAccepted.value = !!data.employee;
  } catch (err) {
    error.value = err.message || "Error fetching order";
    order.value = { nosaukums: "Nav atrasts" };
  } finally {
    isLoading.value = false;
  }
};

// Accept order
const acceptOrder = async () => {
  const token = getToken();
  const orderId = route.params.id;

  try {
    const response = await fetch(`http://127.0.0.1:5000/orders/${orderId}/accept`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ employee_id: currentUser.id }),
    });

    if (!response.ok) throw new Error("Kļūda pieņemot pasūtījumu");

    const data = await response.json();
    order.value = data;
    isAccepted.value = true;
  } catch (err) {
    error.value = err.message || "Error accepting order";
  }
};

// Finish order
const finishOrder = async () => {
  const token = getToken();
  const orderId = route.params.id;

  try {
    const response = await fetch(`http://127.0.0.1:5000/orders/${orderId}/finish`, {
      method: "PATCH",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ status: "Pabeigts" }),
    });

    if (!response.ok) throw new Error("Kļūda pabeidzot pasūtījumu");

    const data = await response.json();
    order.value = data;
  } catch (err) {
    error.value = err.message || "Error finishing order";
  }
};

onMounted(() => {
  fetchOrder();
});
</script>
