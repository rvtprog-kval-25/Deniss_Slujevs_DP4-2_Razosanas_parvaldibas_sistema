<template>
  <div class="min-h-screen bg-gray-50">
    <div class="grid md:grid-cols-[280px_1fr]">
      <!-- Sidebar -->
      <aside class="hidden md:flex flex-col h-screen bg-white border-r border-gray-200 shadow-sm">
        <!-- Navigation -->
        <div class="flex-1 overflow-auto py-6 px-4">
          <div class="mb-8">
            <button 
              @click="exportToPDF" 
              :disabled="!isPdfLibsReady || isPdfLibsLoading"
              class="w-full flex items-center justify-center gap-2 rounded-lg px-4 py-3 text-sm font-medium transition-all bg-blue-50 text-blue-700 hover:bg-blue-100 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="isPdfLibsLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
              </svg>
              {{ isPdfLibsLoading ? 'Ielādē PDF...' : 'Eksportēt PDF' }}
            </button>
          </div>
          
          <nav class="space-y-1.5">
            <button 
              @click="currentTab = 'orders'" 
              :class="[ 
                'w-full flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200', 
                currentTab === 'orders' 
                  ? 'bg-blue-600 text-white shadow-md' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
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
                'w-full flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200', 
                currentTab === 'materials' 
                  ? 'bg-blue-600 text-white shadow-md' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
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
                'w-full flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200', 
                currentTab === 'workers' 
                  ? 'bg-blue-600 text-white shadow-md' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
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
            
            <button 
              @click="currentTab = 'shifts'" 
              :class="[ 
                'w-full flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200', 
                currentTab === 'shifts' 
                  ? 'bg-blue-600 text-white shadow-md' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" class="flex-shrink-0">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              Maiņu statistika
            </button>
            
            <button 
              @click="currentTab = 'stats'" 
              :class="[ 
                'w-full flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all duration-200', 
                currentTab === 'stats' 
                  ? 'bg-blue-600 text-white shadow-md' 
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100' 
              ]"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 20V10"></path>
                <path d="M18 20V4"></path>
                <path d="M6 20v-4"></path>
              </svg>
              Statistika
            </button>
          </nav>
        </div>
      </aside>

      <!-- Main content -->
      <main class="p-6 md:p-8 overflow-auto h-screen">
        <!-- Edit Dialog -->
        <div v-if="editDialog" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-white p-6 rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-300 scale-100">
            <h2 class="text-xl font-semibold mb-6 text-gray-800">
              Rediģēt {{ currentEditType === 'orders' ? 'pasūtījumu' : currentEditType === 'materials' ? 'materiālu' : 'darbinieku' }}
            </h2>
            <form @submit.prevent="saveEdit">
              <div v-if="currentEditType === 'orders'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nosaukums</label>
                  <input v-model="editData.nosaukums" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Nosaukums" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                  <input v-model="editData.daudzums" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Daudzums" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Statuss</label>
                  <select v-model="editData.status" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors bg-white" required>
                    <option value="Nav sākts">Nav sākts</option>
                    <option value="Procesā">Procesā</option>
                    <option value="Pabeigts">Pabeigts</option>
                  </select>
                  <!-- Material search input for edit -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Meklēt materiālu</label>
                    <div class="relative">
                      <input
                        v-model="materialSearch"
                        type="text"
                        class="w-full p-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                        placeholder="Sāciet rakstīt materiāla nosaukumu..."
                      />
                      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-3.5 text-gray-400">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                      </svg>
                    </div>

                    <ul v-if="filteredMaterials.length && materialSearch" class="bg-white border rounded-lg shadow-lg mt-1 max-h-48 overflow-y-auto z-10">
                      <li
                        v-for="material in filteredMaterials"
                        :key="material.id"
                        @click="addMaterialToEdit(material)"
                        class="px-4 py-2.5 hover:bg-blue-50 cursor-pointer transition-colors border-b border-gray-100 last:border-0"
                      >
                        <div class="flex justify-between items-center">
                          <span class="font-medium">{{ material.nosaukums }}</span>
                          <span class="text-sm text-gray-500">Pieejams: {{ material.daudzums }} {{ material.vieniba }}</span>
                        </div>
                      </li>
                    </ul>
                  </div>

                  <!-- Show selected materials -->
                  <div v-if="editData.materials?.length" class="mt-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <h4 class="text-sm font-semibold mb-3 text-gray-700">Materiāli pasūtījumā:</h4>
                    <div v-for="(mat, index) in editData.materials" :key="mat.material_id || mat.id" class="flex items-center gap-3 mb-2 p-2 bg-white rounded-lg border border-gray-100 shadow-sm">
                      <span class="flex-1 font-medium text-gray-800">{{ getMaterialName(mat.material_id || mat.id) }}</span>
                      <div class="flex items-center gap-2">
                        <input
                          type="number"
                          v-model.number="mat.quantity"
                          min="1"
                          class="w-20 border border-gray-300 p-1.5 rounded-md text-center"
                        />
                        <span class="text-sm text-gray-500">{{ getMaterialUnit(mat.material_id || mat.id) }}</span>
                        <button
                          type="button"
                          @click="editData.materials.splice(index, 1)"
                          class="text-red-500 hover:text-red-700 transition-colors p-1"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M3 6h18"></path>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                            <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                          </svg>
                        </button>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
              <div v-if="currentEditType === 'materials'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nosaukums</label>
                  <input v-model="editData.nosaukums" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Nosaukums materiāla" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                  <input v-model="editData.daudzums" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Daudzums" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Mērvienība</label>
                  <input v-model="editData.vieniba" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Mērvienība" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Noliktava</label>
                  <select v-model="editData.noliktava" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors bg-white" required>
                    <option value="Galvenā noliktava">Galvenā noliktava</option>
                    <option value="Baltā noliktava">Baltā noliktava</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vieta</label>
                  <input v-model="editData.vieta" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Vieta" required />
                </div>
              </div>
              <div v-if="currentEditType === 'workers'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vārds</label>
                  <input v-model="editData.vards" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Vārds" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Uzvārds</label>
                  <input v-model="editData.uzvards" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Uzvārds" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Amats</label>
                  <input v-model="editData.amats" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Amats" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Kods</label>
                  <input v-model="editData.kods" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors" placeholder="Kods" required />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Statuss</label>
                  <select v-model="editData.status" class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors bg-white" required>
                    <option value="Aktīvs">Aktīvs</option>
                    <option value="Neaktīvs">Neaktīvs</option>
                  </select>
                </div>
              </div>
              <div class="flex justify-end gap-3 mt-6">
                <button @click="cancelEdit" type="button" class="px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
                  Atcelt
                </button>
                <button type="submit" class="px-4 py-2.5 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
                  Saglabāt
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Page header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900 mb-1">
              {{ currentTab === 'orders' ? 'Pasūtījumi' : 
                 currentTab === 'materials' ? 'Materiāli' : 
                 currentTab === 'workers' ? 'Darbinieki' : 
                 currentTab === 'shifts' ? 'Maiņu statistika' : 'Statistika' }}
            </h1>
            <p class="text-gray-500">
              {{ 
                currentTab === 'orders' ? 'Pārvaldiet visus pasūtījumus' : 
                currentTab === 'materials' ? 'Pārvaldiet noliktavas krājumus' : 
                currentTab === 'workers' ? 'Pārvaldiet darbiniekus' : 
                currentTab === 'shifts' ? 'Aplūkojiet maiņu statistiku' : 'Aplūkojiet materiālu izmantošanas statistiku' 
              }}
            </p>
          </div>
          <button 
            v-if="['orders', 'materials', 'workers'].includes(currentTab)"
            @click="openAddDialog" 
            class="inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 bg-blue-600 text-white hover:bg-blue-700 h-10 px-5 py-2.5 shadow-sm"
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
          <div class="bg-white p-6 rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-300 scale-100">
            <h2 class="text-xl font-semibold mb-6 text-gray-800">
              Pievienot {{ currentTab === 'orders' ? 'pasūtījumu' : currentTab === 'materials' ? 'materiālu' : 'darbinieku' }}
            </h2>
            <form @submit.prevent="currentTab === 'orders' ? addOrder() : currentTab === 'materials' ? addMaterial() : addEmployee()">
              <!-- Order Form -->
              <div v-if="currentTab === 'orders'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nosaukums</label>
                  <input v-model="newOrder.nosaukums" 
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Pasūtījuma nosaukums"
                         required>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                  <input v-model="newOrder.daudzums"
                         type="number"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Daudzums"
                         required>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Statuss</label>
                  <select v-model="newOrder.status"
                          class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors bg-white"
                          required>
                    <option value="Nav sākts">Nav sākts</option>
                    <option value="Procesā">Procesā</option>
                    <option value="Pabeigts">Pabeigts</option>
                  </select>
                </div>
                
                <!-- Material search input -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Meklēt materiālu</label>
                  <div class="relative">
                    <input
                      v-model="materialSearch"
                      type="text"
                      class="w-full p-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                      placeholder="Sāciet rakstīt materiāla nosaukumu..."
                    />
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-3.5 text-gray-400">
                      <circle cx="11" cy="11" r="8"></circle>
                      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                  </div>

                  <!-- Dropdown of filtered materials -->
                  <ul v-if="filteredMaterials.length && materialSearch" class="bg-white border rounded-lg shadow-lg mt-1 max-h-48 overflow-y-auto z-10">
                    <li
                      v-for="material in filteredMaterials"
                      :key="material.id"
                      @click="addMaterialToOrder(material)"
                      class="px-4 py-2.5 hover:bg-blue-50 cursor-pointer transition-colors border-b border-gray-100 last:border-0"
                    >
                      <div class="flex justify-between items-center">
                        <span class="font-medium">{{ material.nosaukums }}</span>
                        <span class="text-sm text-gray-500">Pieejams: {{ material.daudzums }} {{ material.vieniba }}</span>
                      </div>
                    </li>
                  </ul>
                </div>

                <!-- Selected materials list -->
                <div v-if="orderMaterials.length" class="mt-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h4 class="text-sm font-semibold mb-3 text-gray-700">Materiāli pasūtījumā:</h4>
                  <div v-for="(mat, index) in orderMaterials" :key="mat.id" class="flex items-center gap-3 mb-2 p-2 bg-white rounded-lg border border-gray-100 shadow-sm">
                    <span class="flex-1 font-medium text-gray-800">{{ mat.nosaukums }}</span>
                    <div class="flex items-center gap-2">
                      <input
                        type="number"
                        v-model.number="mat.quantity"
                        min="1"
                        class="w-20 border border-gray-300 p-1.5 rounded-md text-center"
                      />
                      <span class="text-sm text-gray-500">{{ mat.vieniba }}</span>
                      <button
                        type="button"
                        @click="removeMaterialFromOrder(index)"
                        class="text-red-500 hover:text-red-700 transition-colors p-1"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M3 6h18"></path>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6"></path>
                          <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Material Form -->
              <div v-if="currentTab === 'materials'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nosaukums</label>
                  <input v-model="newMaterial.nosaukums"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Materiāla nosaukums"
                         required>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                  <input v-model="newMaterial.daudzums"
                         type="number"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Daudzums"
                         required>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Mērvienība</label>
                  <input v-model="newMaterial.vieniba"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Mērvienība"
                         required>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Noliktava</label>
                  <select v-model="newMaterial.noliktava"
                          class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors bg-white"
                          required>
                    <option value="Galvenā noliktava">Galvenā noliktava</option>
                    <option value="Baltā noliktava">Baltā noliktava</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vieta</label>
                  <input v-model="newMaterial.vieta"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Vieta"
                         required>
                </div>
              </div>

              <!-- Worker Form -->
              <div v-if="currentTab === 'workers'" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vārds</label>
                  <input v-model="newEmployee.vards"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Darbinieka vārds"
                         required>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Uzvārds</label>
                  <input v-model="newEmployee.uzvards"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Darbinieka uzvārds"
                         required>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Amats</label>
                  <input v-model="newEmployee.amats"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Amats"
                         required>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Kods</label>
                  <input v-model="newEmployee.kods"
                         class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
                         placeholder="Identifikācijas kods"
                         required>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Statuss</label>
                  <select v-model="newEmployee.status"
                          class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none transition-colors bg-white"
                          required>
                    <option value="Aktīvs">Aktīvs</option>
                    <option value="Neaktīvs">Neaktīvs</option>
                  </select>
                </div>
              </div>

              <!-- Common Buttons -->
              <div class="flex justify-end gap-3 mt-6">
                <button @click="showAddDialog = false" 
                        type="button" 
                        class="px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
                  Atcelt
                </button>
                <button type="submit" 
                        class="px-4 py-2.5 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors">
                  Saglabāt
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Data Tables -->
        <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
          <!-- Orders Table -->
          <div v-if="currentTab === 'orders'" class="overflow-x-auto">
            <div class="p-6 border-b border-gray-100">
              <div class="relative max-w-md">
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Meklēt pasūtījumus..."
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-colors"
                />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>

            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Nosaukums</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Daudzums</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Statuss</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Darbības</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="order in filteredOrders" :key="order.id" class="hover:bg-gray-50 transition-colors duration-150">
                  <td class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap">{{ order.nosaukums }}</td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ order.daudzums }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 text-xs font-semibold rounded-full"
                      :class="{
                        'bg-green-100 text-green-800': order.status === 'Pabeigts',
                        'bg-yellow-100 text-yellow-800': order.status === 'Procesā',
                        'bg-gray-100 text-gray-800': order.status === 'Nav sākts'
                      }">
                      {{ order.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">
                    <div class="flex space-x-3">
                      <button @click="openDetailsDialog(order)" class="text-blue-600 hover:text-blue-800 font-medium transition-colors">Skatīt</button>
                      <button @click="openEditDialog('orders', order)" class="text-green-600 hover:text-green-800 font-medium transition-colors">Rediģēt</button>
                      <button @click="deleteOrder(order.id)" class="text-red-600 hover:text-red-800 font-medium transition-colors">Dzēst</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="orders.length === 0">
                  <td colspan="5" class="px-6 py-10 text-center text-sm text-gray-500">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-gray-300 mb-3">
                        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                        <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                      </svg>
                      <p>Nav pasūtījumu</p>
                      <button @click="openAddDialog" class="mt-2 text-blue-600 hover:underline">Pievienot pasūtījumu</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Shifts Table -->
          <div v-if="currentTab === 'shifts'" class="overflow-x-auto">
            <div class="p-6 border-b border-gray-100">
              <div class="relative max-w-md w-full">
                <input
                  v-model="shiftSearchQuery"
                  type="text"
                  placeholder="Meklēt pēc vārda..."
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-colors"
                 />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>

            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Vārds</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Uzvārds</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Amats</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Stundas</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="emp in filteredShiftStats" :key="emp.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap">{{ emp.vards }}</td>
                  <td class="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">{{ emp.uzvards }}</td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ emp.amats }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-16 bg-gray-200 rounded-full h-2.5 mr-2">
                        <div class="bg-blue-600 h-2.5 rounded-full" :style="{ width: `${Math.min(100, (emp.hours / 200) * 100)}%` }"></div>
                      </div>
                      <span class="text-sm font-semibold text-gray-900">{{ formatDuration(emp.hours) }}</span>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredShiftStats.length === 0">
                  <td colspan="4" class="px-6 py-10 text-center text-sm text-gray-500">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-gray-300 mb-3">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                      </svg>
                      <p>Nav datu par maiņām</p>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Materials Table -->
          <div v-if="currentTab === 'materials'" class="overflow-x-auto">
            <div class="p-6 border-b border-gray-100">
              <div class="relative max-w-md">
                <input
                  v-model="searchMaterials"
                  type="text"
                  placeholder="Meklēt materiālus..."
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-colors"
                />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>

            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Nosaukums</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Daudzums</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Vienība</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Noliktava</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Vieta</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Darbības</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="material in filteredMaterials" :key="material.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap">{{ material.nosaukums }}</td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ material.daudzums }}</td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ material.vieniba }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 text-xs font-semibold rounded-full bg-blue-50 text-blue-700">
                      {{ material.noliktava }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ material.vieta }}</td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">
                    <div class="flex space-x-3">
                      <button @click="openEditDialog('materials', material)" class="text-blue-600 hover:text-blue-800 font-medium transition-colors">Rediģēt</button>
                      <button @click="deleteMaterial(material.id)" class="text-red-600 hover:text-red-800 font-medium transition-colors">Dzēst</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="materials.length === 0">
                  <td colspan="7" class="px-6 py-10 text-center text-sm text-gray-500">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-gray-300 mb-3">
                        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                        <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                        <line x1="12" y1="22.08" x2="12" y2="12"></line>
                      </svg>
                      <p>Nav materiālu</p>
                      <button @click="openAddDialog" class="mt-2 text-blue-600 hover:underline">Pievienot materiālu</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Workers Table -->
          <div v-if="currentTab === 'workers'" class="overflow-x-auto">
            <div class="p-6 border-b border-gray-100">
              <div class="relative max-w-md">
                <input
                  v-model="searchWorkers"
                  type="text"
                  placeholder="Meklēt darbiniekus..."
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-colors"
                />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>

            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Vārds</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Uzvārds</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Amats</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Kods</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Statuss</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Darbības</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="employee in filteredEmployees" :key="employee.id" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap">{{ employee.vards }}</td>
                  <td class="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">{{ employee.uzvards }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
                      {{ employee.amats }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ employee.kods }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 text-xs font-semibold rounded-full"
                      :class="{
                        'bg-green-100 text-green-800': employee.status === 'Aktīvs',
                        'bg-red-100 text-red-800': employee.status === 'Neaktīvs'
                      }">
                      {{ employee.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">
                    <div class="flex space-x-3">
                      <button @click="openEditDialog('workers', employee)" class="text-blue-600 hover:text-blue-800 font-medium transition-colors">Rediģēt</button>
                      <button @click="deleteEmployee(employee.id)" class="text-red-600 hover:text-red-800 font-medium transition-colors">Dzēst</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="employees.length === 0">
                  <td colspan="7" class="px-6 py-10 text-center text-sm text-gray-500">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-gray-300 mb-3">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                      </svg>
                      <p>Nav darbinieku</p>
                      <button @click="openAddDialog" class="mt-2 text-blue-600 hover:underline">Pievienot darbinieku</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Statistics Tab -->
          <div v-if="currentTab === 'stats'" class="p-6">
            <div class="mb-6">
              <div class="relative max-w-md">
                <input
                  v-model="materialStatsSearchQuery"
                  type="text"
                  placeholder="Meklēt pēc materiāla nosaukuma..."
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm transition-colors"
                />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>

            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="stat in filteredMaterialStats" :key="stat.id" class="bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="font-medium text-gray-800 text-lg">{{ stat.nosaukums }}</h3>
                  <div class="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-blue-600">
                      <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                      <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                      <line x1="12" y1="22.08" x2="12" y2="12"></line>
                    </svg>
                  </div>
                </div>
                <p class="text-4xl font-bold text-blue-600">{{ stat.totalUsed }}</p>
                <div class="flex items-center mt-2">
                  <p class="text-sm text-gray-500">reizes pasūtījumos</p>
                  <div v-if="totalMaterialUsage > 0" class="ml-auto px-2 py-1 bg-blue-50 text-blue-700 text-xs font-semibold rounded-full">
                    {{ Math.round((stat.totalUsed / totalMaterialUsage) * 100) }}%
                  </div>
                </div>
                <div class="mt-4 w-full bg-gray-200 rounded-full h-1.5">
                  <div class="bg-blue-600 h-1.5 rounded-full" :style="{ width: `${maxMaterialUsage > 0 ? (stat.totalUsed / maxMaterialUsage) * 100 : 0}%` }"></div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredMaterialStats.length === 0" class="text-center py-16 text-gray-500">
              <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="mx-auto text-gray-300 mb-4">
                <path d="M12 20v-6M6 20V10M18 20V4"></path>
              </svg>
              <p class="text-lg">Nav atrasti dati par materiālu izmantošanu</p>
              <p class="text-sm mt-2">Pievienojiet materiālus pasūtījumiem, lai redzētu statistiku</p>
            </div>
          </div>
        </div>

        <!-- Details Dialog -->
        <div v-if="showDetailsDialog" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-white p-6 rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-300 scale-100">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-semibold text-gray-800">Pasūtījuma detaļas</h2>
              <span class="px-3 py-1 text-xs font-semibold rounded-full"
                :class="{
                  'bg-green-100 text-green-800': detailsData.status === 'Pabeigts',
                  'bg-yellow-100 text-yellow-800': detailsData.status === 'Procesā',
                  'bg-gray-100 text-gray-800': detailsData.status === 'Nav sākts'
                }">
                {{ detailsData.status }}
              </span>
            </div>
            
            <div class="space-y-4 mb-6 bg-gray-50 p-4 rounded-lg">
              <div class="flex border-b border-gray-200 pb-3">
                <span class="font-medium text-gray-700 w-1/3">ID:</span>
                <span class="text-gray-900">{{ detailsData.id }}</span>
              </div>
              <div class="flex border-b border-gray-200 pb-3">
                <span class="font-medium text-gray-700 w-1/3">Nosaukums:</span>
                <span class="text-gray-900">{{ detailsData.nosaukums }}</span>
              </div>
              <div class="flex border-b border-gray-200 pb-3">
                <span class="font-medium text-gray-700 w-1/3">Daudzums:</span>
                <span class="text-gray-900">{{ detailsData.daudzums }}</span>
              </div>
            </div>
            
            <div class="mb-6">
              <h3 class="font-medium text-gray-700 mb-3">Materiāli:</h3>
              <div v-if="detailsData.materials && detailsData.materials.length > 0" class="space-y-2">
                <div v-for="mat in detailsData.materials" :key="mat.material_id" class="flex justify-between items-center p-3 bg-white rounded-lg border border-gray-200 shadow-sm">
                  <div>
                    <span class="font-medium text-gray-800">{{ getMaterialName(mat.material_id) }}</span>
                    <span class="text-sm text-gray-500 ml-2">{{ getMaterialUnit(mat.material_id) }}</span>
                  </div>
                  <span
                    class="font-semibold"
                    :class="{ 'text-red-600': !hasEnoughMaterial(mat), 'text-blue-600': hasEnoughMaterial(mat) }"
                  >
                    {{ mat.quantity }} x {{ detailsData.daudzums }} = {{ mat.quantity * detailsData.daudzums }}
                  </span>
                </div>
              </div>
              <div v-else class="bg-gray-50 rounded-lg p-4 text-center">
                <p class="text-sm text-gray-500">Nav pievienotu materiālu</p>
              </div>
            </div>
            
            <div class="flex justify-end">
              <button 
                @click="closeDetailsDialog" 
                class="px-4 py-2.5 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-lg shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
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
import axios from 'axios';
import { ref, computed, onMounted } from 'vue';

// PDF библиотеки
const isPdfLibsLoading = ref(false);
const isPdfLibsReady = ref(false);

const initPdfLibs = async () => {
  try {
    isPdfLibsLoading.value = true;
    const [jspdfModule, autotableModule] = await Promise.all([
      import('jspdf'),
      import('jspdf-autotable')
    ]);
    window.jsPDF = jspdfModule.default;
    window.autoTable = autotableModule.default;
    isPdfLibsReady.value = true;
  } catch (error) {
    console.error('PDF ielādes kļūda:', error);
    alert('Neizdevās ielādēt PDF funkcionalitāti!');
  } finally {
    isPdfLibsLoading.value = false;
  }
};

onMounted(async () => {
  await initPdfLibs();
});

// Табы
const currentTab = ref('orders');
const searchQuery = ref('');
const searchMaterials = ref('');
const searchWorkers = ref('');
const shiftSearchQuery = ref('');
const materialStatsSearchQuery = ref('');
const materialSearch = ref('');

// Диалоговые окна
const showDetailsDialog = ref(false);
const detailsData = ref({});
const orderMaterials = ref([]);
const showAddDialog = ref(false);
const editDialog = ref(false);
const editData = ref({});
const materialStatsRaw = ref([]);
const currentEditType = ref('');

// Данные
const orders = ref([]);
const materials = ref([]);
const employees = ref([]);
const shiftStats = ref([]);
const periodStart = ref('');
const periodEnd = ref('');


// Формы
const newOrder = ref({ nosaukums: '', daudzums: '', status: 'Nav sākts', materials: [] });
const selectedMaterials = ref([{ id: '', quantity: 1 }]);
const newMaterial = ref({ nosaukums: '', daudzums: '', vieniba: '', noliktava: '', vieta: '' });
const newEmployee = ref({ vards: '', uzvards: '', amats: '', kods: '', status: 'Aktīvs' });

// Вычисляемые свойства
const filteredOrders = computed(() => {
  return orders.value.filter(order =>
    order.nosaukums.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const filteredMaterials = computed(() => {
  return materials.value.filter(mat =>
    mat.nosaukums.toLowerCase().includes(materialSearch.value.toLowerCase())
  );
});

const filteredEmployees = computed(() => {
  return employees.value.filter(emp =>
    emp.vards.toLowerCase().includes(searchWorkers.value.toLowerCase()) ||
    emp.uzvards.toLowerCase().includes(searchWorkers.value.toLowerCase())
  );
});

const filteredShiftStats = computed(() => {
  const search = shiftSearchQuery.value.toLowerCase();
  return shiftStats.value.filter(emp => {
    const vards = emp.vards?.toLowerCase() || '';
    const uzvards = emp.uzvards?.toLowerCase() || '';
    return vards.includes(search) || uzvards.includes(search);
  });
});

// Статистика использования материалов
const materialUsageStats = computed(() => materialStatsRaw.value);
const filteredMaterialStats = computed(() => {
  const search = materialStatsSearchQuery.value.toLowerCase();
  if (!search) return materialUsageStats.value;
  return materialUsageStats.value.filter(stat =>
    stat.nosaukums.toLowerCase().includes(search)
  );
});

const totalMaterialUsage = computed(() => {
  return materialUsageStats.value.reduce((sum, stat) => sum + stat.totalUsed, 0);
});

const maxMaterialUsage = computed(() => {
  return materialUsageStats.value.length ? Math.max(...materialUsageStats.value.map(stat => stat.totalUsed)) : 0;
});

// Загрузка данных
const fetchOrders = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('http://127.0.0.1:5000/orders', {
      headers: { Authorization: `Bearer ${token}` }
    });
    orders.value = response.data;
  } catch (error) {
    console.error('Error fetching orders:', error);
  }
};

const fetchMaterials = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const res = await axios.get('http://127.0.0.1:5000/materials', {
      headers: { Authorization: `Bearer ${token}` }
    });
    materials.value = res.data.materials;
  } catch (e) {
    console.error('Kļūda ielādējot materiālus:', e);
  }
};

const fetchWorkers = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('http://127.0.0.1:5000/employees', {
      headers: { Authorization: `Bearer ${token}` }
    });
    employees.value = response.data.employees;
  } catch (error) {
    console.error('Error fetching employees:', error);
  }
};

const fetchShiftStats = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('http://localhost:5000/api/shifts/stats', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    shiftStats.value = response.data;
  } catch (error) {
    console.error('Ошибка загрузки статистики:', error);
  }
};

// Добавление записей
const addOrder = async () => {
  try {
    const token = localStorage.getItem('authToken');
    if (!newOrder.value.nosaukums || !newOrder.value.daudzums) {
      alert('Aizpildiet visus laukus!');
      return;
    }
    if (orderMaterials.value.length === 0) {
      alert('Pievienojiet vismaz vienu materiālu!');
      return;
    }
    const missing = orderMaterials.value.filter((mat) => {
  const warehouseMaterial = materials.value.find(m => m.id === mat.id);
  if (!warehouseMaterial) return true;
  const totalRequired = Number(mat.quantity) * Number(newOrder.value.daudzums);
  return totalRequired > Number(warehouseMaterial.daudzums);
});

if (missing.length > 0) {
  const missingNames = missing.map(m => m.nosaukums).join(', ');
  alert(`Nav pietiekami materiālu noliktavā: ${missingNames}`);
  return;
}

    const payload = {
      ...newOrder.value,
      materials: orderMaterials.value.map(mat => ({
        material_id: mat.id,
        quantity: mat.quantity
      }))
    };

    await axios.post('http://127.0.0.1:5000/orders', payload, {
      headers: { Authorization: `Bearer ${token}` }
    });

    showAddDialog.value = false;
    newOrder.value = { nosaukums: '', daudzums: '', status: 'Nav sākts' };
    orderMaterials.value = [];
    await fetchOrders();
  } catch (err) {
    alert(err.response?.data?.error || 'Kļūda pievienojot pasūtījumu.');
    console.error(err);
  }
};

const addMaterial = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const { nosaukums, noliktava, daudzums, vieniba, vieta } = newMaterial.value;

    if (!nosaukums || !daudzums || !vieniba || !noliktava || !vieta) {
      alert('Lūdzu, aizpildiet visus materiāla laukus!');
      return;
    }

    if (!materials.value.length) {
      await fetchMaterials();
    }

    const existingMaterial = materials.value.find(
      mat => mat.nosaukums === nosaukums && mat.noliktava === noliktava
    );

    if (existingMaterial) {
      const updatedMaterial = {
        ...existingMaterial,
        daudzums: Number(existingMaterial.daudzums) + Number(daudzums)
      };
      await axios.put(`http://127.0.0.1:5000/materials/${existingMaterial.id}`, updatedMaterial, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
    } else {
      await axios.post('http://127.0.0.1:5000/materials', newMaterial.value, {
        headers: { Authorization: `Bearer ${token}` }
      });
    }

    await fetchMaterials();
    showAddDialog.value = false;
    newMaterial.value = { nosaukums: '', daudzums: '', vieniba: '', noliktava: '', vieta: '' };
  } catch (error) {
    console.error('Kļūda pievienojot materiālu:', error);
    alert('Neizdevās pievienot vai atjaunināt materiālu!');
  }
};

const fetchMaterialStats = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('http://127.0.0.1:5000/api/stats/materials', {
      headers: { Authorization: `Bearer ${token}` }
    });
    materialStatsRaw.value = response.data;
  } catch (error) {
    console.error('Kļūda ielādējot statistiku:', error);
  }
};

const addEmployee = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const { vards, uzvards, amats, kods } = newEmployee.value;

    if (!vards || !uzvards || !amats || !kods) {
      alert('Lūdzu, aizpildiet visus laukus!');
      return;
    }

    if (!employees.value.length) {
      await fetchWorkers();
    }

    const enteredCode = String(kods).trim().toLowerCase();
    const duplicateByCode = employees.value.find(emp =>
      String(emp.kods).trim().toLowerCase() === enteredCode
    );

    if (duplicateByCode) {
      alert(`Darbinieks ar šo kodu (${kods}) jau eksistē!`);
      return;
    }

    const duplicateByName = employees.value.find(emp =>
      emp.vards.trim().toLowerCase() === vards.trim().toLowerCase() &&
      emp.uzvards.trim().toLowerCase() === uzvards.trim().toLowerCase()
    );

    if (duplicateByName) {
      alert(`Darbinieks ar šo vārdu un uzvārdu (${vards} ${uzvards}) jau eksistē!`);
      return;
    }

    await axios.post('http://127.0.0.1:5000/employees', newEmployee.value, {
      headers: { Authorization: `Bearer ${token}` }
    });

    await fetchWorkers();
    showAddDialog.value = false;
    newEmployee.value = { vards: '', uzvards: '', amats: '', kods: '', status: 'Aktīvs' };
  } catch (error) {
    console.error('Error adding employee:', error);
    alert('Neizdevās pievienot darbinieku!');
  }
};

// Редактирование
const openEditDialog = (type, item) => {
  currentEditType.value = type;

  // Копируем основные данные
  editData.value = { ...item };

  // Если редактируем заказ — обработаем материалы
  if (type === 'orders' && item.materials) {
    editData.value.materials = item.materials.map(m => ({
      ...m,
      quantity: m.daudzums, // 👈 добавляем поле quantity
    }));
  }

  editDialog.value = true;
};

const saveEdit = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const id = editData.value.id;

    if (currentEditType.value === 'orders') {
  // Проверка остатков...
  const missing = editData.value.materials.filter((mat) => {
    const warehouseMaterial = materials.value.find(m => m.id === mat.material_id || m.id === mat.id);
    if (!warehouseMaterial) return true;
    const totalRequired = Number(mat.quantity) * Number(editData.value.daudzums);
    return totalRequired > Number(warehouseMaterial.daudzums);
  });

  if (missing.length > 0) {
    const missingNames = missing.map(m => getMaterialName(m.material_id || m.id)).join(', ');
    alert(`Nav pietiekami materiālu noliktavā: ${missingNames}`);
    return;
  }

  const payload = {
    nosaukums: editData.value.nosaukums,
    daudzums: editData.value.daudzums,
    status: editData.value.status,
    materials: editData.value.materials.map(m => ({
      material_id: m.material_id || m.id,
      daudzums: m.quantity
    }))
  };

  await axios.put(`http://127.0.0.1:5000/orders/${id}`, payload, {
    headers: { Authorization: `Bearer ${token}` }
  });

      await fetchOrders();
    } else if (currentEditType.value === 'materials') {
      await axios.put(`http://127.0.0.1:5000/materials/${id}`, editData.value, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchMaterials();
    } else if (currentEditType.value === 'workers') {
      await axios.put(`http://127.0.0.1:5000/employees/${id}`, editData.value, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchWorkers();
    }

     editDialog.value = false;
  } catch (error) {
    console.error('Error saving edit:', error);
    alert('Neizdevās saglabāt izmaiņas!');
  }
};

const cancelEdit = () => {
  editDialog.value = false;
};

// Удаление
const deleteOrder = async (id) => {
  try {
    if (confirm('Vai tiešām vēlaties dzēst šo pasūtījumu?')) {
      const token = localStorage.getItem('authToken');
      await axios.delete(`http://127.0.0.1:5000/orders/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchOrders();
    }
  } catch (error) {
    console.error('Error deleting order:', error);
    alert('Neizdevās dzēst pasūtījumu!');
  }
};

const deleteMaterial = async (id) => {
  try {
    if (confirm('Vai tiešām vēlaties dzēst šo materiālu?')) {
      const token = localStorage.getItem('authToken');
      await axios.delete(`http://127.0.0.1:5000/materials/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchMaterials();
    }
  } catch (error) {
    console.error('Error deleting material:', error);
    alert('Neizdevās dzēst materiālu!');
  }
};

const deleteEmployee = async (id) => {
  try {
    if (confirm('Vai tiešām vēlaties dzēst šo darbinieku?')) {
      const token = localStorage.getItem('authToken');
      await axios.delete(`http://127.0.0.1:5000/employees/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchWorkers();
    }
  } catch (error) {
    console.error('Error deleting employee:', error);
    alert('Neizdevās dzēst darbinieku!');
  }
};

// Экспорт в PDF
const filteredOrdersByDate = computed(() => {
  if (!periodStart.value || !periodEnd.value) return orders.value;
  const start = new Date(periodStart.value);
  const end = new Date(periodEnd.value);
  return orders.value.filter(o => {
    const date = new Date(o.created_at);
    return date >= start && date <= end;
  });
});

const filteredShiftsByDate = computed(() => {
  if (!periodStart.value || !periodEnd.value) return shiftStats.value;
  const start = new Date(periodStart.value);
  const end = new Date(periodEnd.value);
  return shiftStats.value.filter(s => {
    const date = new Date(s.date); // замените на фактическое поле даты
    return date >= start && date <= end;
  });
});

const filteredStatsByDate = computed(() => {
  if (!periodStart.value || !periodEnd.value) return materialStatsRaw.value;
  const start = new Date(periodStart.value);
  const end = new Date(periodEnd.value);
  return materialStatsRaw.value.filter(s => {
    const date = new Date(s.date); // замените на фактическое поле
    return date >= start && date <= end;
  });
});

const exportToPDF = async () => {
  if (!isPdfLibsReady.value) {
    alert('Lūdzu, gaidiet, kamēr tiks ielādētas PDF bibliotēkas!');
    return;
  }

  try {
    const doc = new window.jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4'
    });

    // Шрифты
    doc.addFont('https://cdn.jsdelivr.net/npm/roboto-font@0.1.0/fonts/Roboto/roboto-regular-webfont.ttf', 'Roboto', 'normal');
    doc.addFont('https://cdn.jsdelivr.net/npm/roboto-font@0.1.0/fonts/Roboto/roboto-bold-webfont.ttf', 'Roboto', 'bold');

    const currentDate = new Date().toLocaleDateString('lv-LV');

    const normalizeText = (str) => str.replace(/\+/g, 'ī').replace(/\s+/g, ' ').trim();

    let columns = [];
    let tableData = [];

    switch (currentTab.value) {
      case 'workers':
        columns = ['ID', 'Vārds', 'Uzvārds', 'Amats', 'Kods', 'Statuss'];
        tableData = employees.value.map(e => [
          e.id,
          normalizeText(e.vards),
          normalizeText(e.uzvards),
          normalizeText(e.amats),
          e.kods,
          e.status
        ]);
        break;

      case 'shifts':
      columns = ['ID', 'Vārds', 'Uzvārds', 'Stundas'];
      tableData = filteredShiftsByDate.value.map(s => [
        s.id,
        normalizeText(s.vards),
        normalizeText(s.uzvards),
        s.hours
      ]);
      break;

      case 'orders':
        columns = ['ID', 'Nosaukums', 'Daudzums', 'Statuss', 'Datums'];
        tableData = filteredOrdersByDate.value
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
          .map(o => [
            o.id,
            normalizeText(o.nosaukums),
            o.daudzums,
            normalizeText(o.status),
            new Date(o.created_at).toLocaleDateString('lv-LV')
          ]);
        break;



      case 'materials':
        columns = ['ID', 'Materiāla nosaukums', 'Daudzums', 'Vienība', 'Noliktava', 'Vieta'];
        tableData = materials.value.map(m => [
          m.id,
          normalizeText(m.nosaukums),
          m.daudzums,
          m.vieniba,
          normalizeText(m.noliktava),
          normalizeText(m.vieta)
        ]);
        break;
        
      case 'stats':
        columns = ['Materiāla nosaukums', 'Izmantots pasūtījumos'];
        tableData = materialUsageStats.value.map(s => [
          normalizeText(s.nosaukums),
          s.totalUsed
        ]);
        break;
    }

    doc.setFont('Roboto', 'normal');
    doc.setFontSize(16);
    doc.setTextColor(40, 62, 104);
    
    let title = '';
    switch (currentTab.value) {
      case 'orders': title = 'PASŪTĪJUMI'; break;
      case 'materials': title = 'MATERIĀLI'; break;
      case 'workers': title = 'DARBINIEKI'; break;
      case 'shifts': title = 'MAIŅU STATISTIKA'; break;
      case 'stats': title = 'MATERIĀLU STATISTIKA'; break;
      default: title = currentTab.value.toUpperCase();
    }
    
    doc.text(`${title} (${currentDate})`, 15, 20);

    window.autoTable(doc, {
      head: [columns],
      body: tableData,
      startY: 30,
      theme: 'grid',
      styles: {
        font: 'Roboto',
        fontSize: 10,
        cellPadding: 2,
        overflow: 'linebreak',
        textColor: [51, 51, 51],
        lineColor: [221, 221, 221]
      },
      headStyles: {
        fontStyle: 'bold',
        fillColor: [40, 62, 104],
        textColor: 255
      },
      columnStyles: {
        0: { cellWidth: 20 },
        1: { cellWidth: 40 },
        2: { cellWidth: 30 },
        3: { cellWidth: 30 }
      },
      didParseCell: data => {
        data.cell.styles.font = 'Roboto';
      }
    });

    doc.save(`${currentTab.value}_${currentDate}.pdf`);
  } catch (error) {
    console.error('PDF kļūda:', error);
    alert('Radās kļūda eksportējot PDF!');
  }
};

// Открытие деталей
const openDetailsDialog = async (order) => {
  try {
    const token = localStorage.getItem('authToken');

    // загружаем детали заказа
    const res = await axios.get(`http://127.0.0.1:5000/orders/${order.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // загружаем материалы (если ещё не были загружены)
    if (!materials.value.length) {
      await fetchMaterials();
    }

    detailsData.value = res.data;
    showDetailsDialog.value = true;
  } catch (err) {
    console.error("Kļūda saņemot detaļas:", err);
    alert("Neizdevās ielādēt pasūtījuma detaļas!");
  }
};



const closeDetailsDialog = () => {
  showDetailsDialog.value = false;
};

// Открытие добавления
const openAddDialog = () => {
  showAddDialog.value = true;
  
  if (currentTab.value === 'orders') {
    orderMaterials.value = [];
    newOrder.value = { nosaukums: '', daudzums: '', status: 'Nav sākts' };
  } else if (currentTab.value === 'materials') {
    newMaterial.value = { nosaukums: '', daudzums: '', vieniba: '', noliktava: 'Galvenā noliktava', vieta: '' };
  } else if (currentTab.value === 'workers') {
    newEmployee.value = { vards: '', uzvards: '', amats: '', kods: '', status: 'Aktīvs' };
  }
};
const addMaterialToEdit = (material) => {
  if (!editData.value.materials) {
    editData.value.materials = [];
  }

  const exists = editData.value.materials.find(m => m.material_id === material.id || m.id === material.id);
  if (exists) {
    exists.quantity++;
  } else {
    editData.value.materials.push({
      material_id: material.id,
      quantity: 1,
      nosaukums: material.nosaukums,
      vieniba: material.vieniba
    });
  }

  materialSearch.value = '';
};

// Работа с материалами в заказе
const addMaterialToOrder = (material) => {
  const existingIndex = orderMaterials.value.findIndex(m => m.id === material.id);
  
  if (existingIndex !== -1) {
    orderMaterials.value[existingIndex].quantity++;
  } else {
    orderMaterials.value.push({
      id: material.id,
      nosaukums: material.nosaukums,
      quantity: 1,
      vieniba: material.vieniba
    });
  }
  
  materialSearch.value = '';
};

const removeMaterialFromOrder = (index) => {
  orderMaterials.value.splice(index, 1);
};

// Вспомогательные функции
const getMaterialName = (materialId) => {
  const material = materials.value.find(m => m.id === materialId);
  return material ? material.nosaukums : 'Nezināms materiāls';
};

const getMaterialUnit = (materialId) => {
  const material = materials.value.find(m => m.id === materialId);
  return material ? material.vieniba : '';
};


const hasEnoughMaterial = (mat) => {
  const material = materials.value.find(m => m.id === mat.material_id);
  if (!material) return false;
  const required = (mat.quantity || 0) * (detailsData.value.daudzums || 0);
  return material.daudzums >= required;
};

const formatDuration = (hours) => {
  const totalMinutes = Math.round(hours * 60);
  const h = Math.floor(totalMinutes / 60);
  const m = totalMinutes % 60;
  return `${h}h ${m}min`;
};

// Загрузка при монтировании
onMounted(async () => {
  await fetchOrders();
  await fetchMaterials();
  await fetchShiftStats();
  await fetchWorkers();
  await fetchMaterialStats();
});
</script>
