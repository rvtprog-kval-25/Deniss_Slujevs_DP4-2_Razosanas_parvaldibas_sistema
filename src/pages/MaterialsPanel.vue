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
            Работники
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
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
              <path d="M4 3h6l8 7v8l-8 7h-6v-16z"></path>
              <polyline points="12 9 12 4 20 12"></polyline>
            </svg>
            Материалы
          </button>
        </div>
      </aside>
  
      <!-- Основной контент -->
      <main class="p-4 md:p-6">
        <!-- Кнопка добавления -->
        <div class="flex justify-between items-center mb-4">
          <h1 class="text-xl font-semibold">Материалы</h1>
          <button 
            @click="openAddDialog()" 
            class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 bg-blue-600 text-white"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 h-4 w-4">
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
            Добавить материал
          </button>
        </div>
  
        <!-- Таблица материалов -->
        <div class="bg-white rounded-md border shadow-sm">
          <div class="overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b bg-gray-50">
                  <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">#</th>
                  <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">Название</th>
                  <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">Склад</th>
                  <th class="h-12 px-4 text-left align-middle font-medium text-gray-500">Количество</th>
                  <th class="h-12 px-4 text-right align-middle font-medium text-gray-500">Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(material, index) in materials" :key="material._id" class="border-b">
                  <td class="p-4 align-middle font-medium">{{ index + 1 }}</td>
                  <td class="p-4 align-middle">{{ material.nosaukums }}</td>
                  <td class="p-4 align-middle">{{ material.warehouse_name }}</td>
                  <td class="p-4 align-middle">{{ material.daudzums }}</td>
                  <td class="p-4 align-middle text-right relative">
                    <button 
                      @click="toggleDropdown(material._id, $event)" 
                      class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 w-10 p-0"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4">
                        <circle cx="12" cy="12" r="1"></circle>
                        <circle cx="12" cy="5" r="1"></circle>
                        <circle cx="12" cy="19" r="1"></circle>
                      </svg>
                    </button>
                    <div 
                      v-if="activeDropdown === material._id" 
                      class="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                      :data-dropdown="material._id"
                    >
                      <div class="py-1">
                        <button @click="openEditDialog(material)" class="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 h-4 w-4">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                          </svg>
                          Редактировать
                        </button>
                        <button @click="openDeleteDialog(material)" class="flex w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-gray-100">
                          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2 h-4 w-4">
                            <path d="M3 6h18"></path>
                            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                          </svg>
                          Удалить
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
              <h3 class="text-lg font-semibold mb-4">Добавить материал</h3>
              <div class="space-y-4">
                <div>
                  <label class="text-sm font-medium block mb-2">Название</label>
                  <input 
                    v-model="formData.nosaukums" 
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="Введите название материала"
                  />
                </div>
                <div>
                  <label class="text-sm font-medium block mb-2">Склад</label>
                  <select 
                    v-model="formData.warehouse_id" 
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    <option value="">Выберите склад</option>
                    <option v-for="warehouse in warehouses" :key="warehouse._id" :value="warehouse._id">
                      {{ warehouse.nosaukums }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="text-sm font-medium block mb-2">Количество</label>
                  <input 
                    v-model="formData.daudzums" 
                    type="number" 
                    min="0" 
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="Введите количество"
                  />
                </div>
              </div>
              <div class="flex justify-end gap-2 mt-6">
                <button 
                  @click="closeDialog()" 
                  class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
                >
                  Отмена
                </button>
                <button 
                  @click="addMaterial()" 
                  class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 bg-blue-600 text-white"
                >
                  Сохранить
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Модальное окно редактирования -->
        <div v-if="showEditDialog" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
            <div class="p-6">
              <h3 class="text-lg font-semibold mb-4">Редактировать материал</h3>
              <div class="space-y-4">
                <div>
                  <label class="text-sm font-medium block mb-2">Название</label>
                  <input 
                    v-model="formData.nosaukums" 
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="Введите название материала"
                  />
                </div>
                <div>
                  <label class="text-sm font-medium block mb-2">Склад</label>
                  <select 
                    v-model="formData.warehouse_id" 
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    <option value="">Выберите склад</option>
                    <option v-for="warehouse in warehouses" :key="warehouse._id" :value="warehouse._id">
                      {{ warehouse.nosaukums }}
                    </option>
                  </select>
                </div>
                <div>
                  <label class="text-sm font-medium block mb-2">Количество</label>
                  <input 
                    v-model="formData.daudzums" 
                    type="number" 
                    min="0" 
                    class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="Введите количество"
                  />
                </div>
              </div>
              <div class="flex justify-end gap-2 mt-6">
                <button 
                  @click="closeDialog()" 
                  class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
                >
                  Отмена
                </button>
                <button 
                  @click="updateMaterial()" 
                  class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2 bg-blue-600 text-white"
                >
                  Сохранить
                </button>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Модальное окно удаления -->
        <div v-if="showDeleteDialog" class="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
          <div class="bg-white rounded-lg shadow-lg w-full max-w-md">
            <div class="p-6">
              <h3 class="text-lg font-semibold mb-2">Подтверждение удаления</h3>
              <p class="text-gray-500 mb-6">
                Вы уверены, что хотите удалить этот материал? Это действие невозможно отменить.
              </p>
              <div class="flex justify-end gap-2">
                <button 
                  @click="closeDialog()" 
                  class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-10 px-4 py-2"
                >
                  Отмена
                </button>
                <button 
                  @click="deleteMaterial()" 
                  class="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-destructive text-destructive-foreground hover:bg-destructive/90 h-10 px-4 py-2 bg-red-600 text-white"
                >
                  Удалить
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
  const currentTab = ref('materials');
  
  // Данные для таблицы материалов
  const materials = ref([]);
  const warehouses = ref([]);
  
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
    nosaukums: '',
    warehouse_id: '',
    daudzums: ''
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
  
      const dropdownMenu = document.querySelector(`[data-dropdown="${id}"]`);
      if (dropdownMenu) {
        const rect = event.target.getBoundingClientRect();
        const windowHeight = window.innerHeight;
  
        if (rect.bottom + dropdownMenu.offsetHeight > windowHeight) {
          dropdownMenu.style.top = `-${dropdownMenu.offsetHeight + 10}px`;
        } else {
          dropdownMenu.style.top = `${event.target.offsetHeight + 5}px`;
        }
  
        dropdownMenu.style.left = `0px`;
      }
    }
  };
  
  const openAddDialog = () => {
    if (!checkToken()) return; // Проверка токена
    Object.keys(formData).forEach(key => {
      formData[key] = '';
    });
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
  
  // Загрузка данных материалов


const fetchMaterials = async () => {
  if (!checkToken()) return; // Проверка токена
  try {
    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/materials`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error(`Ошибка при загрузке материалов: ${response.statusText}`);
    }

    const data = await response.json();
    materials.value = data.map((material, index) => {
      const warehouse = warehouses.value.find(w => w._id === material.warehouse_id); // Находим склад по ID
      return {
        ...material,
        id: index + 1,
        warehouse_name: warehouse ? warehouse.nosaukums : 'Не указано' // Имя склада или "Не указано"
      };
    });
    console.log("Загружены материалы:", materials.value);
  } catch (error) {
    console.error('Ошибка при загрузке материалов:', error);
    showMessage.value = true;
    message.value = 'Не удалось загрузить список материалов.';
    setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
  }
};
  // Загрузка данных складов

const fetchWarehouses = async () => {
  if (!checkToken()) return; // Проверка токена
  try {
    const token = localStorage.getItem('authToken');
    const response = await fetch(`${API_URL}/warehouses`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    if (!response.ok) {
      throw new Error(`Ошибка при загрузке складов: ${response.statusText}`);
    }

    const data = await response.json();
    warehouses.value = data.map(warehouse => ({ ...warehouse, _id: warehouse._id }));
    console.log("Загружены склады:", warehouses.value);
  } catch (error) {
    console.error('Ошибка при загрузке складов:', error);
    showMessage.value = true;
    message.value = 'Не удалось загрузить список складов.';
    setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
  }
};
  // Добавление материала
  const addMaterial = async () => {
    if (!checkToken()) return; // Проверка токена
    try {
      if (!formData.nosaukums || !formData.warehouse_id || !formData.daudzums) {
        showMessage.value = true;
        message.value = 'Пожалуйста, заполните все обязательные поля.';
        setTimeout(() => (showMessage.value = false), 3000);
        return;
      }
  
      const token = localStorage.getItem('authToken');
      const response = await fetch(`${API_URL}/materials`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          nosaukums: formData.nosaukums,
          warehouse_id: formData.warehouse_id,
          daudzums: formData.daudzums
        })
      });
  
      if (!response.ok) {
        throw new Error(`Ошибка при добавлении материала: ${response.statusText}`);
      }
  
      await fetchMaterials();
      closeDialog();
      showMessage.value = true;
      message.value = 'Материал успешно добавлен.';
      setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
    } catch (error) {
      console.error('Ошибка при добавлении материала:', error);
      showMessage.value = true;
      message.value = 'Не удалось добавить материал.';
      setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
    }
  };
  
  // Обновление материала
  const updateMaterial = async () => {
    if (!checkToken()) return; // Проверка токена
    try {
      if (!editingItem.value) return;
      if (!formData.nosaukums || !formData.warehouse_id || !formData.daudzums) {
        showMessage.value = true;
        message.value = 'Пожалуйста, заполните все обязательные поля.';
        setTimeout(() => (showMessage.value = false), 3000);
        return;
      }
  
      const token = localStorage.getItem('authToken');
      const response = await fetch(`${API_URL}/materials/${editingItem.value._id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          nosaukums: formData.nosaukums,
          warehouse_id: formData.warehouse_id,
          daudzums: formData.daudzums
        })
      });
  
      if (!response.ok) {
        throw new Error(`Ошибка при обновлении материала: ${response.statusText}`);
      }
  
      await fetchMaterials();
      closeDialog();
      showMessage.value = true;
      message.value = 'Материал успешно обновлен.';
      setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
    } catch (error) {
      console.error('Ошибка при обновлении материала:', error);
      showMessage.value = true;
      message.value = 'Не удалось обновить материал.';
      setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
    }
  };
  
  // Удаление материала
  const deleteMaterial = async () => {
    if (!checkToken()) return; // Проверка токена
    try {
      if (!editingItem.value) return;
  
      const token = localStorage.getItem('authToken');
      const response = await fetch(`${API_URL}/materials/${editingItem.value._id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
  
      if (!response.ok) {
        throw new Error(`Ошибка при удалении материала: ${response.statusText}`);
      }
  
      await fetchMaterials();
      closeDialog();
      showMessage.value = true;
      message.value = 'Материал успешно удален.';
      setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
    } catch (error) {
      console.error('Ошибка при удалении материала:', error);
      showMessage.value = true;
      message.value = 'Не удалось удалить материал.';
      setTimeout(() => (showMessage.value = false), 3000); // Скрыть сообщение через 3 секунды
    }
  };
  
  onMounted(async () => {
  await fetchMaterials(); // Загрузка материалов
  await fetchWarehouses(); // Загрузка складов
});
  </script>