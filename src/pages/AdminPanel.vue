
<template>
  <div class="min-h-screen bg-gray-50">
    <div class="grid md:grid-cols-[240px_1fr]">
      <aside class="hidden md:block border-r bg-white h-screen shadow-sm">
        <div class="flex flex-col gap-1 p-6">
          <div class="mb-6">
            
          </div>
          <button 
            @click="currentTab = 'orders'" 
            :class="[ 
              'flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors', 
              currentTab === 'orders' 
                ? 'bg-gray-100 text-gray-900' 
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50' 
            ]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" class="flex-shrink-0">
              <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
              <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
            </svg>
            Pasūtījumi
          </button>
          <button 
            @click="currentTab = 'materials'" 
            :class="[ 
              'flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors', 
              currentTab === 'materials' 
                ? 'bg-gray-100 text-gray-900' 
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50' 
            ]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" class="flex-shrink-0">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
            Materiāli
          </button>
          <button 
            @click="currentTab = 'workers'" 
            :class="[ 
              'flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors', 
              currentTab === 'workers' 
                ? 'bg-gray-100 text-gray-900' 
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50' 
            ]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" class="flex-shrink-0">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            Darbinieki
          </button>
        </div>
      </aside>

      <!-- Main content -->
      <main class="p-6 md:p-8 overflow-auto h-screen">
        <!-- Edit Dialog -->
        <div v-if="editDialog" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
            <h2 class="text-xl font-semibold mb-6 text-gray-800">
              Редактировать {{ currentEditType === 'orders' ? 'заказ' : currentEditType === 'materials' ? 'материал' : 'работника' }}
            </h2>
            <form @submit.prevent="saveEdit">
              <div v-if="currentEditType === 'orders'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Название</label>
                  <input v-model="editData.nosaukums" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Название" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Количество</label>
                  <input v-model="editData.daudzums" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Количество" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Статус</label>
                  <input v-model="editData.status" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Статус" required />
                </div>
              </div>
              <div v-if="currentEditType === 'materials'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Название материала</label>
                  <input v-model="editData.nosaukums" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Название материала" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Количество</label>
                  <input v-model="editData.daudzums" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Количество" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Единица измерения</label>
                  <input v-model="editData.vieniba" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Единица измерения" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Склад</label>
                  <input v-model="editData.noliktava" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Склад" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Местоположение</label>
                  <input v-model="editData.vieta" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Местоположение" required />
                </div>
              </div>
              <div v-if="currentEditType === 'workers'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Имя</label>
                  <input v-model="editData.vards" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Имя" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Фамилия</label>
                  <input v-model="editData.uzvards" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Фамилия" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Должность</label>
                  <input v-model="editData.amats" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Должность" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Код</label>
                  <input v-model="editData.kods" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Код" required />
                </div>
              </div>
              <div class="flex justify-end gap-3 mt-6">
                <button @click="cancelEdit" type="button" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  Отменить
                </button>
                <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  Сохранить
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Page header -->
        <div class="flex justify-between items-center mb-6">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              {{ currentTab === 'orders' ? 'Pasūtījumi' : currentTab === 'materials' ? 'Materiāli' : 'Darbinieki' }}
            </h1>
            <p class="text-gray-500 mt-1">
              {{ currentTab === 'orders' ? 'Pārvaldiet visus pasūtījumus' : currentTab === 'materials' ? 'Pārvaldiet materiālu krājumus' : 'Pārvaldiet darbinieku sarakstu' }}
            </p>
          </div>
          <button 
            @click="openAddDialog" 
            class="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 bg-blue-600 text-white hover:bg-blue-700 h-10 px-4 py-2 shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" class="mr-2">
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
            Pievienot {{ currentTab === 'orders' ? 'pasūtījumu' : currentTab === 'materials' ? 'materiālu' : 'darbinieku' }}
          </button>
        </div>

        <!-- Add Dialog -->
        <div v-if="showAddDialog" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
            <h2 class="text-xl font-semibold mb-6 text-gray-800">
              Pievienot {{ currentTab === 'orders' ? 'pasūtījumu' : currentTab === 'materials' ? 'materiālu' : 'darbinieku' }}
            </h2>
            <form @submit.prevent="currentTab === 'orders' ? addOrder() : currentTab === 'materials' ? addMaterial() : addEmployee()">
              <div v-if="currentTab === 'orders'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nosaukums</label>
                  <input v-model="newOrder.nosaukums" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Nosaukums" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                  <input v-model="newOrder.daudzums" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Daudzums" required />
                </div>
                <input type="hidden" v-model="newOrder.status" value="Nav sākts" />
              </div>
              <div v-if="currentTab === 'materials'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Materiāla nosaukums</label>
                  <input v-model="newMaterial.nosaukums" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Materiāla nosaukums" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                  <input v-model="newMaterial.daudzums" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Daudzums" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Mērvienība</label>
                  <input v-model="newMaterial.vieniba" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Mērvienība" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Izvēlieties noliktavu</label>
                  <select v-model="newMaterial.noliktava" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white" required>
                    <option value="Galvenā noliktava">Galvenā noliktava</option>
                    <option value="Baltā noliktava">Baltā noliktava</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vieta</label>
                  <input v-model="newMaterial.vieta" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Vieta" required />
                </div>
              </div>
              <div v-if="currentTab === 'workers'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vārds</label>
                  <input v-model="newEmployee.vards" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Vārds" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Uzvārds</label>
                  <input v-model="newEmployee.uzvards" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Uzvārds" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Amats</label>
                  <input v-model="newEmployee.amats" class="p-2.5 w-full border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="Amats" required />
                </div>
              </div>
              <div class="flex justify-end gap-3 mt-6">
                <button @click="showAddDialog = false" type="button" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  Atcelt
                </button>
                <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
                  Saglabāt
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Data tables -->
        <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
          <!-- Orders table -->
          <div v-if="currentTab === 'orders'" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nosaukums</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Daudzums</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Statuss</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Darbības</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ order.id }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ order.nosaukums }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ order.daudzums }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                      :class="{
                        'bg-green-100 text-green-800': order.status === 'Pabeigts',
                        'bg-yellow-100 text-yellow-800': order.status === 'Procesā',
                        'bg-gray-100 text-gray-800': order.status === 'Nav sākts'
                      }">
                      {{ order.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <div class="flex space-x-3">
                      <button 
                        @click="openDetailsDialog(order)" 
                        class="text-blue-600 hover:text-blue-900 font-medium"
                      >
                        Skatīt
                      </button>
                      <button 
                        @click="openEditDialog('orders', order)" 
                        class="text-green-600 hover:text-green-900 font-medium"
                      >
                        Rediģēt
                      </button>

                      <button 
                        @click="deleteOrder(order.id)" 
                        class="text-red-600 hover:text-red-900 font-medium"
                      >
                        Dzēst
                      </button>
                    </div>
                  </td>
                </tr>
                <tr v-if="orders.length === 0">
                  <td colspan="5" class="px-6 py-4 text-center text-sm text-gray-500">Nav pasūtījumu</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Materials table -->
          <div v-if="currentTab === 'materials'" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Materiāla nosaukums</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Daudzums</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vienība</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Noliktava</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vieta</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Darbības</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="material in materials" :key="material.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ material.id }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ material.nosaukums }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ material.daudzums }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ material.vieniba }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ material.noliktava }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ material.vieta }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button 
                      @click="openEditDialog('materials', material)" 
                      class="font-medium m-2 text-black"
                    >
                      Rediģēt
                    </button>
                    <button 
                      @click="deleteMaterial(material.id)" 
                      class="text-red-600 hover:text-red-900 font-bold"
                    >
                      Dzēst
                    </button>
                    
                  </td>
                </tr>
                <tr v-if="materials.length === 0">
                  <td colspan="7" class="px-6 py-4 text-center text-sm text-gray-500">Nav materiālu</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Workers table -->
          <div v-if="currentTab === 'workers'" class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Vārds</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uzvārds</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Amats</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kods</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Darbības</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="employee in employees" :key="employee.id" class="hover:bg-gray-50">
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ employee.id }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ employee.vards }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{{ employee.uzvards }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ employee.amats }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ employee.kods }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <button 
                      @click="openEditDialog('workers', employee)" 
                      class="text-black font-medium m-2"
                    >
                      Rediģēt 
                    </button>
                    <button 
                      @click="deleteEmployee(employee.id)" 
                      class="text-red-600 hover:text-red-900 font-bold"
                    >
                      Dzēst
                    </button>
                    
                  </td>
                </tr>
                <tr v-if="employees.length === 0">
                  <td colspan="6" class="px-6 py-4 text-center text-sm text-gray-500">Nav darbinieku</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Details Dialog -->
        <div v-if="showDetailsDialog" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
            <h2 class="text-xl font-semibold mb-4 text-gray-800">Pasūtījuma detaļas</h2>
            
            <div class="space-y-3 mb-6">
              <div class="flex border-b border-gray-100 pb-2">
                <span class="font-medium text-gray-700 w-1/3">ID:</span>
                <span class="text-gray-900">{{ detailsData.id }}</span>
              </div>
              <div class="flex border-b border-gray-100 pb-2">
                <span class="font-medium text-gray-700 w-1/3">Nosaukums:</span>
                <span class="text-gray-900">{{ detailsData.nosaukums }}</span>
              </div>
              <div class="flex border-b border-gray-100 pb-2">
                <span class="font-medium text-gray-700 w-1/3">Daudzums:</span>
                <span class="text-gray-900">{{ detailsData.daudzums }}</span>
              </div>
              <div class="flex border-b border-gray-100 pb-2">
                <span class="font-medium text-gray-700 w-1/3">Statuss:</span>
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" 
                  :class="{
                    'bg-green-100 text-green-800': detailsData.status === 'Pabeigts',
                    'bg-yellow-100 text-yellow-800': detailsData.status === 'Procesā',
                    'bg-gray-100 text-gray-800': detailsData.status === 'Nav sākts'
                  }">
                  {{ detailsData.status }}
                </span>
              </div>
            </div>
            
            <div class="mb-4">
              <h3 class="font-medium text-gray-700 mb-2">Materiāli:</h3>
              <div class="bg-gray-50 rounded-md p-3">
                <ul class="space-y-1">
                  <li v-for="material in orderMaterials" :key="material.id" class="text-sm">
                    {{ material.nosaukums }} - {{ material.daudzums }} {{ material.vieniba }}
                  </li>
                  <li v-if="!orderMaterials || orderMaterials.length === 0" class="text-sm text-gray-500">
                    Nav pievienotu materiālu
                  </li>
                </ul>
              </div>
            </div>
            
            <div class="flex justify-end">
              <button 
                @click="closeDetailsDialog" 
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                Aizvērt
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// States for UI
const currentTab = ref('orders');
const showDetailsDialog = ref(false);
const detailsData = ref({});
const orderMaterials = ref([]);
const showAddDialog = ref(false);
const editDialog = ref(false);
const editData = ref({});
const currentEditType = ref('');

// Data states
const orders = ref([]);
const materials = ref([]);
const employees = ref([]);

// Form states
const newOrder = ref({ nosaukums: '', daudzums: '', status: 'Nav sākts' });
const newMaterial = ref({ nosaukums: '', daudzums: '', vieniba: '', noliktava: '', vieta: '' });
const newEmployee = ref({ vards: '', uzvards: '', amats: '' });

// Data fetching
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

// Add functions
const addOrder = async () => {
  try {
    const token = localStorage.getItem('authToken');

    // Проверка заполнения полей
    if (!newOrder.value.nosaukums || !newOrder.value.daudzums) {
      alert('Заполните все обязательные поля!');
      return;
    }

    // Отправка запроса
    await axios.post('http://127.0.0.1:5000/orders',
      {
        nosaukums: newOrder.value.nosaukums,
        daudzums: newOrder.value.daudzums,
        status: newOrder.value.status
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );

    await fetchOrders(); // обновление списка заказов
    showAddDialog.value = false; // закрытие диалога
    newOrder.value = { nosaukums: '', daudzums: '', status: '' }; // сброс формы
  } catch (error) {
    console.error('Error adding order:', error);
  }
};


const addEmployee = async () => {
  try {
    const token = localStorage.getItem('authToken');
    await axios.post('http://127.0.0.1:5000/employees', newEmployee.value, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchWorkers();
    showAddDialog.value = false;
    newEmployee.value = { vards: '', uzvards: '', amats: '' };
  } catch (error) {
    console.error('Error adding employee:', error);
  }
};

// Delete functions
const deleteOrder = async (id) => {
  try {
    const token = localStorage.getItem('authToken');
    await axios.delete(`http://127.0.0.1:5000/orders/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchOrders();
  } catch (error) {
    console.error('Error deleting order:', error);
  }
};

const deleteMaterial = async (id) => {
  try {
    const token = localStorage.getItem('authToken');
    await axios.delete(`http://127.0.0.1:5000/materials/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchMaterials();
  } catch (error) {
    console.error('Error deleting material:', error);
  }
};

const deleteEmployee = async (id) => {
  try {
    const token = localStorage.getItem('authToken');
    await axios.delete(`http://127.0.0.1:5000/employees/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchWorkers();
  } catch (error) {
    console.error('Error deleting employee:', error);
  }
};

// Edit functions
const editOrder = async (id, updatedOrder) => {
  try {
    const token = localStorage.getItem('authToken');
    await axios.put(`http://127.0.0.1:5000/orders/${id}`, updatedOrder, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchOrders();
  } catch (error) {
    console.error('Error editing order:', error);
  }
};

const editMaterial = async (id, updatedMaterial) => {
  try {
    const token = localStorage.getItem('authToken');
    await axios.put(`http://127.0.0.1:5000/materials/${id}`, updatedMaterial, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchMaterials();
  } catch (error) {
    console.error('Error editing material:', error);
  }
};

const editEmployee = async (id, updatedEmployee) => {
  try {
    const token = localStorage.getItem('authToken');
    await axios.put(`http://127.0.0.1:5000/employees/${id}`, updatedEmployee, {
      headers: { Authorization: `Bearer ${token}` },
    });
    await fetchWorkers();
  } catch (error) {
    console.error('Error editing employee:', error);
  }
};

// Dialog handlers
const openEditDialog = (type, data) => {
  currentEditType.value = type;
  editData.value = { ...data };
  editDialog.value = true;
};

const saveEdit = async () => {
  if (currentEditType.value === 'orders') {
    await editOrder(editData.value.id, editData.value);
  } else if (currentEditType.value === 'materials') {
    await editMaterial(editData.value.id, editData.value);
  } else if (currentEditType.value === 'workers') {
    await editEmployee(editData.value.id, editData.value);
  }
  editDialog.value = false;
};

const cancelEdit = () => {
  editDialog.value = false;
};

const openDetailsDialog = (data) => {
  detailsData.value = { ...data };
  orderMaterials.value = [];
  showDetailsDialog.value = true;
};

const closeDetailsDialog = () => {
  showDetailsDialog.value = false;
};

const openAddDialog = () => {
  showAddDialog.value = true;
};

// Initial data load
onMounted(async () => {
  await fetchOrders();
  await fetchMaterials();
  await fetchWorkers();
});
</script>