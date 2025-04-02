<template>
  <div class="grid md:grid-cols-[220px_1fr]">
    <!-- Боковая панель навигации -->
    <aside class="hidden md:block border-r bg-white h-[calc(100vh-4rem)]">
      <div class="flex flex-col gap-1 p-4">
        <button 
          @click="currentTab = 'workers'" 
          :class="[
            'flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors',
            currentTab === 'workers' 
              ? 'bg-gray-100 text-gray-900 font-medium' 
              : 'text-gray-500 hover:text-gray-900 hover:bg-gray-50'
          ]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
            <circle cx="9" cy="7" r="4"></circle>
            <path d="M22 21v-2a4 4 0 0 0-3-3.87"></path>
            <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
          </svg>
          Darbinieki
        </button>
      </div>
    </aside>

    <!-- Основной контент -->
    <main class="p-4 md:p-6">
      <!-- Кнопка добавления -->
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-xl font-semibold">Darbinieki</h1>
        <button 
          @click="openAddDialog()" 
          class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 bg-blue-600 text-white"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 h-4 w-4">
            <path d="M5 12h14"></path>
            <path d="M12 5v14"></path>
          </svg>
          Pievienot darbinieku
        </button>
      </div>

      <!-- Таблица работников -->
      <div class="bg-white rounded-md border shadow-sm">
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b bg-gray-50">
                <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">#</th>
                <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">Vārds</th>
                <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">Amats</th>
                <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">Kods</th>
                <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">Status</th>
                <th class="h-12 px-4 text-right align-middle font-medium text-gray-500">Darbības</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(worker, index) in workers" :key="worker._id" class="border-b">
                <td class="p-4 align-middle font-medium">{{ index + 1 }}</td>
                <td class="p-4 align-middle">{{ `${worker.vards} ${worker.uzvards}` }}</td>
                <td class="p-4 align-middle">{{ worker.amats }}</td>
                <td class="p-4 align-middle">{{ worker.kods }}</td>
                <td class="p-4 align-middle">
                  <span 
                    :class="[
                      'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold',
                      worker.status === 'Strādā' ? 'bg-green-100 text-green-800' :
                      worker.status === 'Atvaļinājumā' ? 'bg-blue-100 text-blue-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ worker.status }}
                  </span>
                </td>
                <td class="p-4 align-middle text-right relative">
                  <button 
                    @click="toggleDropdown(worker._id, $event)" 
                    class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 w-10 p-0"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                      <circle cx="12" cy="12" r="1"></circle>
                      <circle cx="12" cy="5" r="1"></circle>
                      <circle cx="12" cy="19" r="1"></circle>
                    </svg>
                  </button>
                  <div 
                    v-if="activeDropdown === worker._id" 
                    class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                    :data-dropdown="worker._id"
                  >
                    <div class="py-1">
                      <button @click="openEditDialog(worker)" class="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 h-4 w-4">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                        Rediģēt
                      </button>
                      <button @click="openDeleteDialog(worker)" class="flex w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 h-4 w-4">
                          <path d="M3 6h18"></path>
                          <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                          <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                        </svg>
                        Izdzēst
                      </button>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Модальное окно добавления -->
      <div v-if="showAddDialog" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
          <div class="p-6">
            <h3 class="text-lg font-semibold mb-4">Pievienot darbinieku</h3>
            <div class="space-y-4">
              <div>
                <label class="text-sm font-medium block mb-2">Vārds</label>
                <input 
                  v-model="formData.vards" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Vārds"
                />
              </div>
              <div>
                <label class="text-sm font-medium block mb-2">Uzvārds</label>
                <input 
                  v-model="formData.uzvards" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Uzvārds"
                />
              </div>
              <div>
                <label class="text-sm font-medium block mb-2">Amats</label>
                <select 
                  v-model="formData.amats" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="">Izvelies amatu</option>
                  <option value="Galdnieks">Galdnieks</option>
                  <option value="Tapsētājs">Tapsētājs</option>
                  <option value="Šuvejs/a">Šuvejs/a</option>
                  <option value="Komplektetājs">Komplektetājs</option>
                  <option value="Menedzeris">Menedzeris</option>
                  <option value="Administrators">Administrators</option>
                </select>
              </div>
              <div>
                <label class="text-sm font-medium block mb-2">Кods</label>
                <input 
                  v-model="formData.kods" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Ievadiet kodu"
                />
              </div>
              <div>
                <label class="text-sm font-medium block mb-2">Status</label>
                <select 
                  v-model="formData.status" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="Strādā">Strādā</option>
                  <option value="Atvaļinājumā">Atvaļinājumā</option>
                  <option value="Atlaists">Atlaists</option>
                </select>
              </div>
            </div>
            <div class="flex justify-end gap-2 mt-6">
              <button 
                @click="closeDialog()" 
                class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
              >
                Atcelt
              </button>
              <button 
                @click="addItem()" 
                class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 bg-blue-600 text-white"
              >
                Saglabāt
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Модальное окно редактирования -->
      <div v-if="showEditDialog" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
          <div class="p-6">
            <h3 class="text-lg font-semibold mb-4">Rediģēt darbinieku</h3>
            <div class="space-y-4">
              <div>
                <label class="text-sm font-medium block mb-2">Vārds</label>
                <input 
                  v-model="formData.vards" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Vārds"
                />
              </div>
              <div>
                <label class="text-sm font-medium block mb-2">Uzvārds</label>
                <input 
                  v-model="formData.uzvards" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Uzvārds"
                />
              </div>
              <div>
                <label class="text-sm font-medium block mb-2">Amats</label>
                <select 
                  v-model="formData.amats" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                <option value="">Izvelies amatu</option>
                  <option value="Galdnieks">Galdnieks</option>
                  <option value="Tapsētājs">Tapsētājs</option>
                  <option value="Šuvejs/a">Šuvejs/a</option>
                  <option value="Komplektetājs">Komplektetājs</option>
                  <option value="Menedzeris">Menedzeris</option>
                  <option value="Administrators">Administrators</option>
                </select>
              </div>
              <div>
                <label class="text-sm font-medium block mb-2">Kods</label>
                <input 
                  v-model="formData.kods" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Введите код"
                />
              </div>
              <div>
                <label class="text-sm font-medium block mb-2">Status</label>
                <select 
                  v-model="formData.status" 
                  class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  <option value="Strādā">Strādā</option>
                  <option value="Atvaļinājumā">Atvaļinājumā</option>
                  <option value="Atlaists">Atlaists</option>
                </select>
              </div>
            </div>
            <div class="flex justify-end gap-2 mt-6">
              <button 
                @click="closeDialog()" 
                class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
              >
                Atcelt
              </button>
              <button 
                @click="updateItem()" 
                class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 bg-blue-600 text-white"
              >
                Saglabāt
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Модальное окно удаления -->
      <div v-if="showDeleteDialog" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
        <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
          <div class="p-6">
            <h3 class="text-lg font-semibold mb-2">Izdzēšana</h3>
            <p class="text-gray-500 mb-6">
              Vai tiešām gribat izdzēst?
            </p>
            <div class="flex justify-end gap-2">
              <button 
                @click="closeDialog()" 
                class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
              >
                Atcelt
              </button>
              <button 
                @click="deleteItem()" 
                class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-destructive text-destructive-foreground hover:bg-destructive/90 h-10 px-4 py-2 bg-red-600 text-white"
              >
                Izdzēst
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';

const API_URL = 'http://localhost:5000'; // Адрес Flask API

// Текущая вкладка
const currentTab = ref('workers');

// Данные для таблицы
const workers = ref([]);

// Состояние диалоговых окон
const showAddDialog = ref(false);
const showEditDialog = ref(false);
const showDeleteDialog = ref(false);

const activeDropdown = ref(null);
const editingItem = ref(null);

// Сообщение об успешной операции или ошибке
const message = ref('');
const showMessage = ref(false);

// Данные формы
const formData = reactive({
  id: null,
  vards: '',
  uzvards: '',
  amats: '',
  kods: '', // Поле "Код"
  status: ''
});

// Проверка токена
const checkToken = () => {
  const token = localStorage.getItem('authToken');
  if (!token) {
    alert('Jāieeiet sistēmā');
    return false;
  }
  return true;
};

// Методы
const toggleDropdown = (id, event) => {
  if (activeDropdown.value === id) {
    activeDropdown.value = null;
  } else {
    activeDropdown.value = id;

    // Проверяем положение меню
    const dropdownMenu = document.querySelector(`[data-dropdown="${id}"]`);
    if (dropdownMenu) {
      const rect = event.target.getBoundingClientRect();
      const windowHeight = window.innerHeight;

      // Если меню выходит за пределы экрана, показываем его сверху
      if (rect.bottom + dropdownMenu.offsetHeight > windowHeight) {
        dropdownMenu.style.top = `-${dropdownMenu.offsetHeight + 10}px`;
      } else {
        dropdownMenu.style.top = `${event.target.offsetHeight + 5}px`;
      }

      // Устанавливаем позицию по горизонтали
      dropdownMenu.style.left = `0px`;
    }
  }
};

const openAddDialog = () => {
  if (!checkToken()) return; // Проверка токена
  Object.keys(formData).forEach(key => {
    formData[key] = '';
  });
  formData.status = 'Srādā';
  showAddDialog.value = true;
  activeDropdown.value = null;
};

const openEditDialog = (item) => {
  if (!checkToken()) return; // Проверка токена
  editingItem.value = item;
  Object.keys(item).forEach(key => {
    if (key in formData) {
      formData[key] = item[key];
    }
  });
  showEditDialog.value = true;
  activeDropdown.value = null;
};

const openDeleteDialog = (item) => {
  if (!checkToken()) return; // Проверка токена
  editingItem.value = item;
  showDeleteDialog.value = true;
  activeDropdown.value = null;
};

const closeDialog = () => {
  showAddDialog.value = false;
  showEditDialog.value = false;
  showDeleteDialog.value = false;
  editingItem.value = null;
};

// Загрузка данных работников
const fetchWorkers = async () => {
  if (!checkToken()) return; // Проверка токена
  try {
    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/employees`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error(`Kļūda ${response.statusText}`);
    }

    const data = await response.json();
    workers.value = data.map((worker, index) => ({ ...worker, id: index + 1 }));
  } catch (error) {
    console.error('Kļūda', error);
    showMessage.value = true;
    message.value = 'Kļūda';
    setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
  }
};

// Добавление работника
const addItem = async () => {
  if (!checkToken()) return; // Проверка токена
  try {
    // Проверяем обязательные поля
    if (!formData.vards || !formData.uzvards || !formData.amats) {
      showMessage.value = true;
      message.value = 'Aizpildiet visus laukus';
      setTimeout(() => (showMessage.value = false), 3000);
      return;
    }

    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/employees`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        vards: formData.vards,
        uzvards: formData.uzvards,
        amats: formData.amats,
        kods: formData.kods, 
        status: formData.status
      })
    });

    if (!response.ok) {
      throw new Error(`Kļūda ${response.statusText}`);
    }

    await fetchWorkers();
    closeDialog();
    showMessage.value = true;
    message.value = 'Veiksmīgi pievienots';
    setTimeout(() => (showMessage.value = false), 3000); 
  } catch (error) {
    console.error('Kļūda', error);
    showMessage.value = true;
    message.value = 'Neizdeevas pievienot';
    setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
  }
};

// Обновление работника
const updateItem = async () => {
  if (!checkToken()) return; // Проверка токена
  try {
    if (!editingItem.value) return;

    // Проверяем обязательные поля
    if (!formData.vards || !formData.uzvards || !formData.amats) {
      showMessage.value = true;
      message.value = 'Aizpildiet visus laukus';
      setTimeout(() => (showMessage.value = false), 3000);
      return;
    }

    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/employees/${editingItem.value._id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        vards: formData.vards,
        uzvards: formData.uzvards,
        amats: formData.amats,
        kods: formData.kods, 
        status: formData.status
      })
    });

    if (!response.ok) {
      throw new Error(`Kļūda ${response.statusText}`);
    }

    await fetchWorkers();
    closeDialog();
    showMessage.value = true;
    message.value = 'Veiksmīgi';
    setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
  } catch (error) {
    console.error('Kļūda', error);
    showMessage.value = true;
    message.value = 'Neizdevās';
    setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
  }
};

// Удаление работника
const deleteItem = async () => {
  if (!checkToken()) return; // Проверка токена
  try {
    if (!editingItem.value) return;

    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/employees/${editingItem.value._id}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error(`Kļūda ${response.statusText}`);
    }

    await fetchWorkers();
    closeDialog();
    showMessage.value = true;
    message.value = 'Veiksmīgi  izdzēsts';
    setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
  } catch (error) {
    console.error('Kļūda', error);
    showMessage.value = true;
    message.value = 'Neidzevās';
    setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
  }
};

onMounted(async () => {
  await fetchWorkers();
});
</script>