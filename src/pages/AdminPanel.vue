<template>
  <div class="min-h-screen bg-gray-50">
    <div class="grid md:grid-cols-[220px_1fr]">
      <!-- Sānu navigācijas josla -->
      <aside class="hidden md:block border-r bg-white h-[calc(100vh-4rem)]">
        <div class="flex flex-col gap-1 p-4">
          <button 
            @click="currentTab = 'orders'" 
            :class="[ 
              'flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors', 
              currentTab === 'orders' 
                ? 'bg-gray-100 text-gray-900 font-medium' 
                : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50' 
            ]"
          >
            Pasūtījumi
          </button>
          <button 
            @click="currentTab = 'materials'" 
            :class="[ 
              'flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors', 
              currentTab === 'materials' 
                ? 'bg-gray-100 text-gray-900 font-medium' 
                : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50' 
            ]"
          >
            Materiāli
          </button>
          <button 
            @click="currentTab = 'workers'" 
            :class="[ 
              'flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors', 
              currentTab === 'workers' 
                ? 'bg-gray-100 text-gray-900 font-medium' 
                : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50' 
            ]"
          >
            Darbinieki
          </button>
        </div>
      </aside>

      <!-- Galvenais saturs -->
      <main class="p-4 md:p-6">
        <!-- Mobilā navigācija (redzama tikai mobilajās ierīcēs) -->
        <div class="md:hidden mb-4">
          <div class="inline-flex h-10 items-center justify-center rounded-md bg-white p-1 text-gray-600 shadow-sm border">
            <button 
              @click="currentTab = 'orders'" 
              :class="[ 
                'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50', 
                currentTab === 'orders' ? 'bg-gray-100 text-gray-900' : 'text-gray-500' 
              ]"
            >
              Pasūtījumi
            </button>
            <button 
              @click="currentTab = 'materials'" 
              :class="[ 
                'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50', 
                currentTab === 'materials' ? 'bg-gray-100 text-gray-900' : 'text-gray-500' 
              ]"
            >
              Materiāli
            </button>
            <button 
              @click="currentTab = 'workers'" 
              :class="[ 
                'inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50', 
                currentTab === 'workers' ? 'bg-gray-100 text-gray-900' : 'text-gray-500' 
              ]"
            >
              Darbinieki
            </button>
          </div>
        </div>

        <!-- Pievienošanas poga -->
        <div class="flex justify-between items-center mb-4">
          <h1 class="text-xl font-semibold">
            {{ currentTab === 'orders' ? 'Pasūtījumi' : currentTab === 'materials' ? 'Materiāli' : 'Darbinieki' }}
          </h1>
          <button 
            @click="openAddDialog" 
            class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 bg-blue-600 text-white"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 h-4 w-4">
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
            Pievienot {{ currentTab === 'orders' ? 'pasūtījumu' : currentTab === 'materials' ? 'materiālu' : 'darbinieku' }}
          </button>
        </div>

        <!-- Tabulas katram datu tipam -->
        <div v-if="currentTab === 'orders'">
          <table class="min-w-full table-auto border-collapse">
            <thead>
              <tr class="border-b">
                <th class="px-4 py-2 text-left">ID</th>
                <th class="px-4 py-2 text-left">Nosaukums</th>
                <th class="px-4 py-2 text-left">Daudzums</th>
                <th class="px-4 py-2 text-left">Statuss</th>
                <th class="px-4 py-2 text-left">Darbības</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id" class="border-b">
                <td class="px-4 py-2">{{ order.id }}</td>
                <td class="px-4 py-2">{{ order.nosaukums }}</td>
                <td class="px-4 py-2">{{ order.daudzums }}</td>
                <td class="px-4 py-2">{{ order.status }}</td>
                <td class="px-4 py-2">
                  <button 
                    @click="viewOrderDetails(order)" 
                    class="text-blue-500 hover:underline"
                  >
                    Skatīt
                  </button>
                  <button 
                    @click="deleteOrder(order.id)" 
                    class="text-red-500 hover:underline ml-2"
                  >
                    Dzēst
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'materials'">
          <table class="min-w-full table-auto border-collapse">
            <thead>
              <tr class="border-b">
                <th class="px-4 py-2 text-left">ID</th>
                <th class="px-4 py-2 text-left">Materiāla nosaukums</th>
                <th class="px-4 py-2 text-left">Daudzums</th>
                <th class="px-4 py-2 text-left">Vienība</th>
                <th class="px-4 py-2 text-left">Noliktava</th>
                <th class="px-4 py-2 text-left">Vieta</th>
                <th class="px-4 py-2 text-left">Darbības</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="material in materials" :key="material.id" class="border-b">
                <td class="px-4 py-2">{{ material.id }}</td>
                <td class="px-4 py-2">{{ material.nosaukums }}</td>
                <td class="px-4 py-2">{{ material.daudzums }}</td>
                <td class="px-4 py-2">{{ material.vieniba }}</td>
                <td class="px-4 py-2">{{ material.noliktava }}</td>
                <td class="px-4 py-2">{{ material.vieta }}</td>
                <td class="px-4 py-2">
                  <button 
                    @click="deleteMaterial(material.id)" 
                    class="text-red-500 hover:underline"
                  >
                    Dzēst
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="currentTab === 'workers'">
          <table class="min-w-full table-auto border-collapse">
            <thead>
              <tr class="border-b">
                <th class="px-4 py-2 text-left">ID</th>
                <th class="px-4 py-2 text-left">Vārds</th>
                <th class="px-4 py-2 text-left">Uzārds</th>
                <th class="px-4 py-2 text-left">Amats</th>
                <th class="px-4 py-2 text-left">Darbības</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="employee in employees" :key="employee.id" class="border-b">
                <td class="px-4 py-2">{{ employee.id }}</td>
                <td class="px-4 py-2">{{ employee.vards }}</td>
                <td class="px-4 py-2">{{ employee.uzvards }}</td>
                <td class="px-4 py-2">{{ employee.amats }}</td>
                <td class="px-4 py-2">
                  <button 
                    @click="deleteEmployee(employee.id)" 
                    class="text-red-500 hover:underline"
                  >
                    Dzēst
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Состояния для данных
const currentTab = ref('orders');
const orders = ref([]);
const materials = ref([]);
const employees = ref([]);

// Состояния для формы добавления
const newOrder = ref({ nosaukums: '', daudzums: '', status: '' });
const newMaterial = ref({ nosaukums: '', daudzums: '', vieniba: '', noliktava: '', vieta: '' });
const newEmployee = ref({ vards: '', uzvards: '', amats: '' });
const showAddDialog = ref(false);

// Функции для получения данных
const fetchOrders = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('http://127.0.0.1:5000/orders', {
      headers: { Authorization: `Bearer ${token}` },
    });
    orders.value = response.data;
  } catch (error) {
    console.error('Error fetching orders:', error);
  }
};

const fetchMaterials = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('http://127.0.0.1:5000/materials', {
      headers: { Authorization: `Bearer ${token}` },
    });
    materials.value = response.data.materials;
  } catch (error) {
    console.error('Error fetching materials:', error);
  }
};

const fetchWorkers = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('http://127.0.0.1:5000/employees', {
      headers: { Authorization: `Bearer ${token}` },
    });
    employees.value = response.data.employees;
  } catch (error) {
    console.error('Error fetching employees:', error);
  }
};

// Функции для добавления данных
const addOrder = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.post('http://127.0.0.1:5000/orders', newOrder.value, {
      headers: { Authorization: `Bearer ${token}` },
    });
    orders.value.push(response.data);
    newOrder.value = { nosaukums: '', daudzums: '', status: '' };  // очистить форму
    showAddDialog.value = false;  // закрыть диалог
  } catch (error) {
    console.error('Error adding order:', error);
  }
};

const addMaterial = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.post('http://127.0.0.1:5000/materials', newMaterial.value, {
      headers: { Authorization: `Bearer ${token}` },
    });
    materials.value.push(response.data);
    newMaterial.value = { nosaukums: '', daudzums: '', vieniba: '', noliktava: '', vieta: '' };
    showAddDialog.value = false;
  } catch (error) {
    console.error('Error adding material:', error);
  }
};

const addEmployee = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.post('http://127.0.0.1:5000/employees', newEmployee.value, {
      headers: { Authorization: `Bearer ${token}` },
    });
    employees.value.push(response.data);
    newEmployee.value = { vards: '', uzvards: '', amats: '' };
    showAddDialog.value = false;
  } catch (error) {
    console.error('Error adding employee:', error);
  }
};

// Функция для открытия диалога
const openAddDialog = () => {
  showAddDialog.value = true;
};

// Функции для удаления
const deleteOrder = async (id) => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.delete(`http://127.0.0.1:5000/orders/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === 200) {
      orders.value = orders.value.filter(order => order.id !== id);
    }
  } catch (error) {
    console.error('Error deleting order:', error);
  }
};

const deleteMaterial = async (id) => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.delete(`http://127.0.0.1:5000/materials/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === 200) {
      materials.value = materials.value.filter(material => material.id !== id);
    }
  } catch (error) {
    console.error('Error deleting material:', error);
  }
};

const deleteEmployee = async (id) => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.delete(`http://127.0.0.1:5000/employees/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === 200) {
      employees.value = employees.value.filter(employee => employee.id !== id);
    }
  } catch (error) {
    console.error('Error deleting employee:', error);
  }
};

// Получение данных при монтировании
onMounted(() => {
  fetchOrders();
  fetchMaterials();
  fetchWorkers();
});
</script>
