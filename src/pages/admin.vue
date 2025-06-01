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
              class="w-full flex items-center justify-center gap-2 rounded-lg px-4 py-3 text-sm font-medium transition-all bg-gray-100 text-gray-800 hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="isPdfLibsLoading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-800" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
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
                  ? 'bg-gray-900 text-white shadow-md' 
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
                  ? 'bg-gray-900 text-white shadow-md' 
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
                  ? 'bg-gray-900 text-white shadow-md' 
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
                  ? 'bg-gray-900 text-white shadow-md' 
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
                  ? 'bg-gray-900 text-white shadow-md' 
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


      <main class="p-6 md:p-8 overflow-auto h-screen">
        <!-- Add/Edit Dialog -->
        <div v-if="showAddDialog || editDialog" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-white p-6 rounded-xl shadow-2xl w-full max-w-md transform transition-all duration-300 scale-100 max-h-screen overflow-y-auto">
            <h2 class="text-xl font-semibold mb-6 text-gray-800">
              {{ editDialog ? 'Rediģēt' : 'Pievienot' }} {{ currentEditType === 'orders' ? 'pasūtījumu' : currentEditType === 'materials' ? 'materiālu' : 'darbinieku' }}
            </h2>
            <form @submit.prevent="editDialog ? saveEdit() : (currentTab === 'orders' ? addOrder() : currentTab === 'materials' ? addMaterial() : addEmployee())">
              <!-- Order Form -->
              <div v-if="showOrderForm || (editDialog && currentEditType === 'orders')" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nosaukums</label>
                  <input 
                    :value="editDialog ? editData.nosaukums : newOrder.nosaukums"
                    @input="updateValue($event, 'nosaukums')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    placeholder="Nosaukums"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                  <input 
                    :value="editDialog ? editData.daudzums : newOrder.daudzums"
                    @input="updateValue($event, 'daudzums')"
                    type="number"
                    min="0.01"
                    step="0.01"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    placeholder="Daudzums"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Statuss</label>
                  <select 
                    :value="editDialog ? editData.status : newOrder.status"
                    @input="updateValue($event, 'status')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors bg-white"
                    required
                  >
                    <option value="Nav sākts">Nav sākts</option>
                    <option value="Procesā">Procesā</option>
                    <option value="Pabeigts">Pabeigts</option>
                  </select>
                </div>

                <!-- Material search input -->
                <div class="mt-4">
                  <label class="block text-sm font-medium text-gray-700 mb-1">Meklēt materiālu</label>
                  <div class="relative">
                    <input
                      v-model="materialSearch"
                      type="text"
                      class="w-full p-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 outline-none transition-colors"
                      placeholder="Sāciet rakstīt materiāla nosaukumu..."
                    />
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-3.5 text-gray-400">
                      <circle cx="11" cy="11" r="8"></circle>
                      <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                  </div>

                  <ul v-if="filteredMaterialsForSearch.length && materialSearch" class="bg-white border rounded-lg shadow-lg mt-1 max-h-48 overflow-y-auto z-10">
                    <li
                      v-for="material in filteredMaterialsForSearch"
                      :key="material.id"
                      @click="editDialog ? addMaterialToEdit(material) : addMaterialToOrder(material)"
                      class="px-4 py-2.5 hover:bg-gray-50 cursor-pointer transition-colors border-b border-gray-100 last:border-0"
                    >
                      <div class="flex justify-between items-center">
                        <span class="font-medium">{{ material.nosaukums }}</span>
                        <span class="text-sm text-gray-500">Pieejams: {{ material.daudzums }} {{ material.vieniba }}</span>
                      </div>
                    </li>
                  </ul>
                </div>

                <!-- Show selected materials -->
                <div v-if="editDialog ? editData.materials?.length : orderMaterials.length" class="mt-4 bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <h4 class="text-sm font-semibold mb-3 text-gray-700">Materiāli pasūtījumā:</h4>
                  <div v-for="(mat, index) in editDialog ? editData.materials : orderMaterials" :key="mat.material_id || mat.id" class="flex items-center gap-3 mb-2 p-2 bg-white rounded-lg border border-gray-100 shadow-sm">
                    <span class="flex-1 font-medium text-gray-800">{{ getMaterialName(mat.material_id || mat.id) }}</span>
                    <div class="flex items-center gap-2">
                      <input
                        type="number"
                        v-model.number="mat.quantity"
                        min="0.01"
                        step="0.01"
                        class="w-20 border border-gray-300 p-1.5 rounded-md text-center"
                      />
                      <span class="text-sm text-gray-500">{{ getMaterialUnit(mat.material_id || mat.id) }}</span>
                      <button
                        type="button"
                        @click="editDialog ? editData.materials.splice(index, 1) : orderMaterials.splice(index, 1)"
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
              <div v-if="showMaterialForm || (editDialog && currentEditType === 'materials')" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Nosaukums</label>
                  <input 
                    :value="editDialog ? editData.nosaukums : newMaterial.nosaukums"
                    @input="updateValue($event, 'nosaukums')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    placeholder="Nosaukums"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Noliktava</label>
                  <select 
                    :value="editDialog ? editData.noliktava : newMaterial.noliktava"
                    @input="updateValue($event, 'noliktava')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors bg-white"
                    required
                  >
                    <option value="Balta noliktava">Balta noliktava</option>
                    <option value="Centrālā noliktava">Centrālā noliktava</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vieta</label>
                  <input 
                    :value="editDialog ? editData.vieta : newMaterial.vieta"
                    @input="updateValue($event, 'vieta')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    placeholder="Vieta"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vienība</label>
                  <input 
                    :value="editDialog ? editData.vieniba : newMaterial.vieniba"
                    @input="updateValue($event, 'vieniba')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    placeholder="Vienība"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                  <input 
                    :value="editDialog ? editData.daudzums : newMaterial.daudzums"
                    @input="updateValue($event, 'daudzums')"
                    type="number"
                    min="0.01"
                    step="0.01"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    required
                  />
                </div>
              </div>

              <!-- Worker Form -->
              <div v-if="showWorkerForm || (editDialog && currentEditType === 'workers')" class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Vārds</label>
                  <input 
                    :value="editDialog ? editData.vards : newEmployee.vards"
                    @input="updateValue($event, 'vards')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    placeholder="Vārds"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Uzvārds</label>
                  <input 
                    :value="editDialog ? editData.uzvards : newEmployee.uzvards"
                    @input="updateValue($event, 'uzvards')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    placeholder="Uzvārds"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Amats</label>
                  <select 
                    :value="editDialog ? editData.amats : newEmployee.amats"
                    @input="updateValue($event, 'amats')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors bg-white"
                    required
                  >
                    <option value="Šuvēja">Šuvēja</option>
                    <option value="Galdnieks">Galdnieks</option>
                    <option value="Komplektētājs">Komplektētājs</option>
                    <option value="Kravejs">Kravejs</option>
                    <option value="Tapsētajs">Tapsētajs</option>
                    <option value="Administrators">Administrators</option>
                  </select>
                </div>
                <div v-if="(editDialog ? editData.amats : newEmployee.amats) === 'Administrators'">
                  <div class="flex items-center justify-between mb-2">
                    <label class="block text-sm font-medium text-gray-700">Parole</label>
                    <button 
                      v-if="editDialog"
                      @click="showPasswordChange = !showPasswordChange"
                      type="button"
                      class="text-sm text-gray-600 hover:text-gray-900"
                    >
                      {{ showPasswordChange ? 'Atcelt' : 'Mainīt paroli' }}
                    </button>
                  </div>
                  <input 
                    v-if="!editDialog || showPasswordChange"
                    :value="editDialog ? editData.password : newEmployee.password"
                    @input="updateValue($event, 'password')"
                    type="password"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    placeholder="Parole"
                    :required="!editDialog || showPasswordChange"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Kods</label>
                  <input 
                    :value="editDialog ? editData.kods : newEmployee.kods"
                    @input="updateValue($event, 'kods')"
                    type="number"
                    min="1"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-1">Statuss</label>
                  <select 
                    :value="editDialog ? editData.status : newEmployee.status"
                    @input="updateValue($event, 'status')"
                    class="p-3 w-full border border-gray-300 rounded-lg focus:ring-2 focus:ring-gray-500 focus:border-gray-500 outline-none transition-colors bg-white"
                    required
                  >
                    <option value="Aktīvs">Aktīvs</option>
                    <option value="Neaktīvs">Neaktīvs</option>
                  </select>
                </div>
              </div>

              <div class="flex justify-end gap-4 mt-6">
                <button @click="editDialog ? cancelEdit() : closeAddDialog()" class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors">
                  {{ editDialog ? 'Atcelt' : 'Aizvērt' }}
                </button>
                <button type="submit" class="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors">
                  {{ editDialog ? 'Saglabāt' : 'Pievienot' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Page header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
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
            class="inline-flex items-center justify-center rounded-lg text-sm font-medium transition-all focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 bg-gray-900 text-white hover:bg-gray-800 h-10 px-5 py-2.5 shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" class="mr-2">
              <path d="M5 12h14"></path>
              <path d="M12 5v14"></path>
            </svg>
            Pievienot {{ currentTab === 'orders' ? 'pasūtījumu' : currentTab === 'materials' ? 'materiālu' : 'darbinieku' }}
          </button>
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
                    class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 shadow-sm transition-colors"
                  />
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                  </svg>
                </div>
              </div>
              
              <!-- Sorting and limits -->
              <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6 p-6">
                <div class="flex items-center gap-3">
                  <label class="text-sm font-medium text-gray-700">Kārtot pēc:</label>
                  <div class="relative">
                    <select v-model="sortKey" class="appearance-none border border-gray-300 text-sm rounded-lg px-4 py-2 pr-8 bg-white shadow-sm focus:ring-2 focus:ring-gray-500">
                      <option value="">Nav</option>
                      <option value="nosaukums">Nosaukums</option>
                      <option value="daudzums">Daudzums</option>
                      <option value="status">Statuss</option>
                    </select>
                    <svg class="absolute right-2 top-2.5 w-4 h-4 text-gray-400 pointer-events-none" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>

                  <button @click="sortAsc = !sortAsc" class="flex items-center text-sm text-gray-700 hover:text-gray-900 transition">
                    <svg v-if="sortAsc" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                    {{ sortAsc ? 'Augošā' : 'Dilstošā' }}
                  </button>
                </div>

                <div class="flex items-center gap-3">
                  <label class="text-sm font-medium text-gray-700">Rādīt ierakstus:</label>
                  <select v-model="limitCount" class="border border-gray-300 text-sm rounded-lg px-4 py-2 bg-white shadow-sm focus:ring-2 focus:ring-gray-500 focus:border-gray-500">
                    <option value="10">10</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                    <option value="9999">Visus</option>
                  </select>
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
                      <button @click="openDetailsDialog(order)" class="text-gray-700 hover:text-gray-900 font-medium transition-colors">Skatīt</button>
                      <button @click="openEditDialog('orders', order)" class="text-gray-700 hover:text-gray-900 font-medium transition-colors">Rediģēt</button>
                      <button @click="deleteOrder(order.id)" class="text-red-600 hover:text-red-800 font-medium transition-colors">Dzēst</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="filteredOrders.length === 0">
                  <td colspan="4" class="px-6 py-10 text-center text-sm text-gray-500">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-gray-300 mb-3">
                        <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
                        <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
                      </svg>
                      <p>Nav pasūtījumu</p>
                      <button @click="openAddDialog" class="mt-2 text-gray-700 hover:underline">Pievienot pasūtījumu</button>
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
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 shadow-sm transition-colors"
                 />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>
            
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6 p-6">
              <!-- Date filters and sorting -->
              <div class="flex flex-col md:flex-row gap-4 items-start md:items-center">
                <div class="flex gap-4 items-center">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">No:</label>
                    <input type="date" v-model="periodStart" class="p-2 border rounded-lg border-gray-300 focus:ring-2 focus:ring-gray-500" />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Līdz:</label>
                    <input type="date" v-model="periodEnd" class="p-2 border rounded-lg border-gray-300 focus:ring-2 focus:ring-gray-500" />
                  </div>
                
                </div>
                
                <!-- Sorting -->
                <div class="flex items-center gap-3">
                  <label class="text-sm font-medium text-gray-700">Kārtot pēc:</label>
                  <div class="relative">
                    <select v-model="shiftSortKey" class="appearance-none border border-gray-300 text-sm rounded-lg px-4 py-2 pr-8 bg-white shadow-sm focus:ring-2 focus:ring-gray-500">
                      <option value="">Nav</option>
                      <option value="vards">Vārds</option>
                      <option value="uzvards">Uzvārds</option>
                      <option value="hours">Stundas</option>
                      <option value="date">Datums</option>
                    </select>
                    <svg class="absolute right-2 top-2.5 w-4 h-4 text-gray-400 pointer-events-none" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>

                  <button @click="shiftSortAsc = !shiftSortAsc" class="flex items-center text-sm text-gray-700 hover:text-gray-900 transition">
                    <svg v-if="shiftSortAsc" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                    </svg>
                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                    {{ shiftSortAsc ? 'Augošā' : 'Dilstošā' }}
                  </button>
                </div>
              </div>
              
              <!-- Limit records -->
              <div class="flex items-center gap-3">
                <label class="text-sm font-medium text-gray-700">Rādīt ierakstus:</label>
                <select v-model="limitCount" class="border border-gray-300 text-sm rounded-lg px-4 py-2 bg-white shadow-sm focus:ring-2 focus:ring-gray-500 focus:border-gray-500">
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="50">50</option>
                  <option value="9999">Visus</option>
                </select>
              </div>
            </div>

            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Vārds</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Uzvārds</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Amats</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Stundas</th>
                  <th class="px-6 py-3.5 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">Datums</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(emp, index) in filteredShiftsByDate" :key="emp.id + '-' + (emp.start_time || index)" class="hover:bg-gray-50 transition-colors">
                  <td class="px-6 py-4 text-sm font-medium text-gray-900 whitespace-nowrap">{{ emp.vards }}</td>
                  <td class="px-6 py-4 text-sm text-gray-900 whitespace-nowrap">{{ emp.uzvards }}</td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ emp.amats }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="w-16 bg-gray-200 rounded-full h-2.5 mr-2">
                        <div class="bg-gray-900 h-2.5 rounded-full" :style="{ width: `${Math.min(100, (emp.hours / 8) * 100)}%` }"></div>
                      </div>
                      <span class="text-sm font-semibold text-gray-900">{{ formatDuration(emp.hours) }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">
                    {{ formatDate(emp.start_time) }}
                  </td>
                </tr>
                <tr v-if="filteredShiftsByDate.length === 0">
                  <td colspan="5" class="px-6 py-10 text-center text-sm text-gray-500">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-gray-300 mb-3">
                        <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                        <line x1="16" y1="2" x2="16" y2="6"></line>
                        <line x1="8" y1="2" x2="8" y2="6"></line>
                        <line x1="3" y1="10" x2="21" y2="10"></line>
                      </svg>
                      <p>Nav maiņu datu izvēlētajā periodā</p>
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
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 shadow-sm transition-colors"
                />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>
            
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6 p-6">
              <div class="flex items-center gap-3">
                <label class="text-sm font-medium text-gray-700">Kārtot pēc:</label>
                <div class="relative">
                  <select v-model="sortKey" class="appearance-none border border-gray-300 text-sm rounded-lg px-4 py-2 pr-8 bg-white shadow-sm focus:ring-2 focus:ring-gray-500">
                    <option value="">Nav</option>
                    <option value="nosaukums">Nosaukums</option>
                    <option value="daudzums">Daudzums</option>
                  </select>
                  <svg class="absolute right-2 top-2.5 w-4 h-4 text-gray-400 pointer-events-none" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>

                <button @click="sortAsc = !sortAsc" class="flex items-center text-sm text-gray-700 hover:text-gray-900 transition">
                  <svg v-if="sortAsc" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                  {{ sortAsc ? 'Augošā' : 'Dilstošā' }}
                </button>
              </div>

              <div class="flex items-center gap-3">
                <label class="text-sm font-medium text-gray-700">Rādīt ierakstus:</label>
                <select v-model="limitCount" class="border border-gray-300 text-sm rounded-lg px-4 py-2 bg-white shadow-sm focus:ring-2 focus:ring-gray-500 focus:border-gray-500">
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="50">50</option>
                  <option value="9999">Visus</option>
                </select>
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
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ material.daudzums.toLocaleString('lv-LV', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }}</td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ material.vieniba }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-3 py-1 text-xs font-semibold rounded-full bg-gray-100 text-gray-800">
                      {{ material.noliktava }}
                    </span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">{{ material.vieta }}</td>
                  <td class="px-6 py-4 text-sm text-gray-700 whitespace-nowrap">
                    <div class="flex space-x-3">
                      <button @click="openEditDialog('materials', material)" class="text-gray-700 hover:text-gray-900 font-medium transition-colors">Rediģēt</button>
                      <button @click="openTransferDialog(material)" class="text-blue-600 hover:text-blue-800 font-medium transition-colors">Pārvietot</button>
                      <button @click="deleteMaterial(material.id)" class="text-red-600 hover:text-red-800 font-medium transition-colors">Dzēst</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="materials.length === 0">
                  <td colspan="6" class="px-6 py-10 text-center text-sm text-gray-500">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-gray-300 mb-3">
                        <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                        <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                        <line x1="12" y1="22.08" x2="12" y2="12"></line>
                      </svg>
                      <p>Nav materiālu</p>
                      <button @click="openAddDialog" class="mt-2 text-gray-700 hover:underline">Pievienot materiālu</button>
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
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 shadow-sm transition-colors"
                />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
            </div>
            
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6 p-6">
              <div class="flex items-center gap-3">
                <label class="text-sm font-medium text-gray-700">Kārtot pēc:</label>
                <div class="relative">
                  <select v-model="sortKey" class="appearance-none border border-gray-300 text-sm rounded-lg px-4 py-2 pr-8 bg-white shadow-sm focus:ring-2 focus:ring-gray-500">
                    <option value="">Nav</option>
                    <option value="id">ID</option>
                    <option value="vards">Vārds</option>
                    <option value="uzvards">Uzvārds</option>
                    <option value="amats">Amats</option>
                    <option value="status">Statuss</option>
                  </select>
                  <svg class="absolute right-2 top-2.5 w-4 h-4 text-gray-400 pointer-events-none" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </div>

                <button @click="sortAsc = !sortAsc" class="flex items-center text-sm text-gray-700 hover:text-gray-900 transition">
                  <svg v-if="sortAsc" xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
                  </svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                  {{ sortAsc ? 'Augošā' : 'Dilstošā' }}
                </button>
              </div>

              <div class="flex items-center gap-3">
                <label class="text-sm font-medium text-gray-700">Rādīt ierakstus:</label>
                <select v-model="limitCount" class="border border-gray-300 text-sm rounded-lg px-4 py-2 bg-white shadow-sm focus:ring-2 focus:ring-gray-500 focus:border-gray-500">
                  <option value="10">10</option>
                  <option value="20">20</option>
                  <option value="50">50</option>
                  <option value="9999">Visus</option>
                </select>
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
                      <button @click="openEditDialog('workers', employee)" class="text-gray-700 hover:text-gray-900 font-medium transition-colors">Rediģēt</button>
                      <button @click="deleteEmployee(employee.id)" class="text-red-600 hover:text-red-800 font-medium transition-colors">Dzēst</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="employees.length === 0">
                  <td colspan="6" class="px-6 py-10 text-center text-sm text-gray-500">
                    <div class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="text-gray-300 mb-3">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                      </svg>
                      <p>Nav darbinieku</p>
                      <button @click="openAddDialog" class="mt-2 text-gray-700 hover:underline">Pievienot darbinieku</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Statistics Tab -->
          <div v-if="currentTab === 'stats'" class="p-6">
            <!-- Header with additional export options -->
            <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-6 gap-4">
              <div class="relative max-w-md w-full">
                <input
                  v-model="materialStatsSearchQuery"
                  type="text"
                  placeholder="Meklēt pēc materiāla nosaukuma..."
                  class="w-full px-4 py-2.5 pl-10 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 shadow-sm transition-colors"
                />
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="absolute left-3 top-2.5 text-gray-400">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
              
              <!-- Export Options -->
              <div class="flex flex-wrap gap-2">
                <button 
                  @click="showChart = !showChart" 
                  :class="[
                    'inline-flex items-center px-3 py-2 text-sm font-medium rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors',
                    showChart ? 'bg-gray-900 text-white' : 'text-gray-700 bg-white border border-gray-300 hover:bg-gray-50'
                  ]"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2">
                    <path d="M3 3v18h18"></path>
                    <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"></path>
                  </svg>
                  {{ showChart ? 'Slēpt grafiku' : 'Rādīt grafiku' }}
                </button>
              </div>
            </div>

            <!-- Chart Section -->
            <div v-if="showChart && filteredMaterialStats.length > 0" class="mb-8 bg-white rounded-xl shadow-sm p-6 border border-gray-200">
              <h3 class="text-lg font-semibold text-gray-800 mb-4">Materiālu izmantošanas grafiks</h3>
              <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Pie Chart Representation -->
                <div class="relative">
                  <h4 class="text-sm font-medium text-gray-700 mb-3">Proporcijas</h4>
                  <div class="space-y-2">
                    <div v-for="(stat, index) in topMaterialStats" :key="stat.id" class="flex items-center">
                      <div 
                        class="w-4 h-4 rounded mr-3" 
                        :style="{ backgroundColor: getChartColor(index) }"
                      ></div>
                      <span class="text-sm text-gray-700 flex-1">{{ stat.nosaukums }}</span>
                      <span class="text-sm font-semibold text-gray-900">{{ stat.totalUsed }}</span>
                      <span class="text-xs text-gray-500 ml-2">
                        ({{ Math.round((stat.totalUsed / totalMaterialUsage) * 100) }}%)
                      </span>
                    </div>
                  </div>
                </div>
                
                <!-- Bar Chart Representation -->
                <div>
                  <h4 class="text-sm font-medium text-gray-700 mb-3">Salīdzinājums</h4>
                  <div class="space-y-3">
                    <div v-for="(stat, index) in topMaterialStats" :key="stat.id" class="flex items-center">
                      <div class="w-24 text-xs text-gray-600 truncate">{{ stat.nosaukums }}</div>
                      <div class="flex-1 mx-3">
                        <div class="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            class="h-2 rounded-full transition-all duration-500" 
                            :style="{ 
                              width: `${(stat.totalUsed / maxMaterialUsage) * 100}%`,
                              backgroundColor: getChartColor(index)
                            }"
                          ></div>
                        </div>
                      </div>
                      <span class="text-sm font-semibold text-gray-900 w-8">{{ stat.totalUsed }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              <div class="bg-white rounded-xl shadow-sm p-4 border border-gray-200">
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-700">
                      <path d="M12 20V10"></path>
                      <path d="M18 20V4"></path>
                      <path d="M6 20v-4"></path>
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Kopā izmantojumi</p>
                    <p class="text-xl font-bold text-gray-900">{{ totalMaterialUsage }}</p>
                  </div>
                </div>
              </div>
              
              <div class="bg-white rounded-xl shadow-sm p-4 border border-gray-200">
                <div class="flex items-center">
                  <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center mr-3">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-700">
                      <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                      <circle cx="9" cy="7" r="4"></circle>
                    </svg>
                  </div>
                  <div>
                    <p class="text-sm text-gray-500">Populārākais</p>
                    <p class="text-sm font-bold text-gray-900 truncate">{{ mostUsedMaterial?.nosaukums || 'Nav' }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Stats Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="stat in filteredMaterialStats" :key="stat.id" class="bg-white rounded-xl shadow-sm p-6 border border-gray-200 hover:shadow-md transition-shadow">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="font-medium text-gray-800 text-lg">{{ stat.nosaukums }}</h3>
                  <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-700">
                      <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                      <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                      <line x1="12" y1="22.08" x2="12" y2="12"></line>
                    </svg>
                  </div>
                </div>
                <p class="text-4xl font-bold text-gray-900">{{ stat.totalUsed }}</p>
                <div class="flex items-center mt-2">
                  <p class="text-sm text-gray-500">reizes pasūtījumos</p>
                  <div v-if="totalMaterialUsage > 0" class="ml-auto px-2 py-1 bg-gray-100 text-gray-800 text-xs font-semibold rounded-full">
                    {{ Math.round((stat.totalUsed / totalMaterialUsage) * 100) }}%
                  </div>
                </div>
                <div class="mt-4 w-full bg-gray-200 rounded-full h-1.5">
                  <div class="bg-gray-900 h-1.5 rounded-full" :style="{ width: `${maxMaterialUsage > 0 ? (stat.totalUsed / maxMaterialUsage) * 100 : 0}%` }"></div>
                </div>
                
                <!-- Additional info -->
                <div class="mt-4 pt-4 border-t border-gray-100">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-500">Reitings:</span>
                    <span class="font-medium text-gray-900">#{{ getRanking(stat) }}</span>
                  </div>
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
            <div>
              <h3 class="font-medium text-gray-700 mb-2">Atbildīgais par pasūtījumu:</h3>
              <p v-if="detailsData.employee" class="m-5 text-sm text-gray-800">
                {{ detailsData.employee.vards }} {{ detailsData.employee.uzvards }}
                <span v-if="detailsData.employee.amats">({{ detailsData.employee.amats }})</span>
              </p>
              <p v-else class="text-sm text-gray-500">Nav pievienota darbinieka.</p>
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
                    :class="{ 'text-red-600': !hasEnoughMaterial(mat), 'text-gray-900': hasEnoughMaterial(mat) }"
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
                class="px-4 py-2.5 text-sm font-medium text-white bg-gray-900 border border-transparent rounded-lg shadow-sm hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors"
              >
                Aizvērt
              </button>
            </div>
          </div>
        </div>

        <!-- Transfer Material Dialog -->
        <div v-if="showTransferDialog" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div class="bg-white p-6 rounded-xl shadow-2xl w-full max-w-md">
            <h2 class="text-xl font-semibold mb-6 text-gray-800">Pārvietot materiālu</h2>
            <form @submit.prevent="transferMaterial">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Materiāls</label>
                <div class="font-medium">{{ transferData.nosaukums }}</div>
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">No noliktavas</label>
                <div class="font-medium">{{ transferData.noliktava }}</div>
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Daudzums</label>
                <input v-model.number="transferData.daudzums" type="number" min="0.01" :max="transferData.max" step="0.01"
                  class="p-3 w-full border border-gray-300 rounded-lg" required />
                <div class="text-xs text-gray-500 mt-1">Pieejams: {{ transferData.max }} {{ transferData.vieniba }}</div>
              </div>
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">Uz noliktavu</label>
                <select v-model="transferData.toNoliktava" class="p-3 w-full border border-gray-300 rounded-lg" required>
                  <option v-for="opt in warehouseOptions" :key="opt" :value="opt" :disabled="opt === transferData.noliktava">{{ opt }}</option>
                </select>
              </div>
              <div class="flex justify-end gap-4 mt-6">
                <button @click="showTransferDialog = false" type="button" class="px-6 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50">Atcelt</button>
                <button type="submit" class="px-6 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700">Pārvietot</button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref, computed, onMounted, watch, h } from 'vue';
import { showToast } from '../toast';

// PDF libraries
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
    showToast('Neizdevās ielādēt PDF funkcionalitāti!', 'error');
  } finally {
    isPdfLibsLoading.value = false;
  }
};

// Sorting and filtering
const sortKey = ref('');
const sortAsc = ref(true);
const limitCount = ref(50);

// Separate sorting variables for shifts
const shiftSortKey = ref('');
const shiftSortAsc = ref(true);

const sortByKey = (arr, key, ascending = true) => {
  return [...arr].sort((a, b) => {
    let valA = a[key];
    let valB = b[key];
    
    // Handle dates
    if (key === 'date') {
      valA = new Date(valA);
      valB = new Date(valB);
    }
    
    if (valA < valB) return ascending ? -1 : 1;
    if (valA > valB) return ascending ? 1 : -1;
    return 0;
  });
};

// Tabs
const currentTab = ref('orders');
const searchQuery = ref('');
const searchMaterials = ref('');
const searchWorkers = ref('');
const shiftSearchQuery = ref('');
const materialStatsSearchQuery = ref('');
const materialSearch = ref('');

// Dialogs
const showDetailsDialog = ref(false);
const detailsData = ref({});
const orderMaterials = ref([]);
const showAddDialog = ref(false);
const editDialog = ref(false);
const editData = ref({});
const materialStatsRaw = ref([]);
const currentEditType = ref('');

// Data
const orders = ref([]); // Initialize with empty array to prevent undefined errors
const materials = ref([]);
const employees = ref([]);
const shiftStats = ref([]);
const periodStart = ref('');
const periodEnd = ref('');

// Forms
const newOrder = ref({ nosaukums: '', daudzums: '', status: 'Nav sākts', materials: [] });
const newMaterial = ref({ nosaukums: '', daudzums: '', vieniba: '', noliktava: '', vieta: '' });
const newEmployee = ref({ vards: '', uzvards: '', amats: '', kods: '', status: 'Aktīvs' });

// Computed properties for filtering materials in search
const filteredMaterialsForSearch = computed(() => {
  try {
    if (!materialSearch.value) return [];
    if (!materials.value || !Array.isArray(materials.value)) return [];
    
    return materials.value.filter(mat =>
      mat?.nosaukums?.toLowerCase()?.includes(materialSearch.value.toLowerCase()) || false
    );
  } catch (error) {
    console.error('Error filtering materials:', error);
    return [];
  }
});

const filteredOrders = computed(() => {
  try {
    if (!orders.value || !Array.isArray(orders.value)) return [];
    
    const search = searchQuery.value.toLowerCase();
    if (!search) return orders.value.slice(0, limitCount.value);
    
    let result = orders.value.filter(order =>
      order?.nosaukums?.toLowerCase()?.includes(search) || false
    );
    
    if (sortKey.value) {
      result = sortByKey(result, sortKey.value, sortAsc.value);
    }
    
    return result.slice(0, limitCount.value);
  } catch (error) {
    console.error('Error filtering orders:', error);
    return [];
  }
});

const filteredMaterials = computed(() => {
  try {
    if (!materials.value || !Array.isArray(materials.value)) return [];
    
    let result = materials.value.filter(mat =>
      mat?.nosaukums?.toLowerCase()?.includes(searchMaterials.value.toLowerCase()) || false
    );
    
    if (sortKey.value) {
      result = sortByKey(result, sortKey.value, sortAsc.value);
    }
    
    return result.slice(0, limitCount.value);
  } catch (error) {
    console.error('Error filtering materials:', error);
    return [];
  }
});

const filteredEmployees = computed(() => {
  try {
    if (!employees.value || !Array.isArray(employees.value)) return [];
    
    let result = employees.value.filter(emp =>
      (emp?.vards?.toLowerCase()?.includes(searchWorkers.value.toLowerCase()) || false) ||
      (emp?.uzvards?.toLowerCase()?.includes(searchWorkers.value.toLowerCase()) || false)
    );
    
    if (sortKey.value) {
      result = sortByKey(result, sortKey.value, sortAsc.value);
    }
    
    return result.slice(0, limitCount.value);
  } catch (error) {
    console.error('Error filtering employees:', error);
    return [];
  }
});

const filteredMaterialStats = computed(() => {
  try {
    if (!materialStatsRaw.value || !Array.isArray(materialStatsRaw.value)) return [];
    
    let result = materialStatsRaw.value.filter(stat =>
      stat?.nosaukums?.toLowerCase()?.includes(materialStatsSearchQuery.value.toLowerCase()) || false
    );
    
    if (sortKey.value) {
      result = sortByKey(result, sortKey.value, sortAsc.value);
    }
    
    return result.slice(0, limitCount.value);
  } catch (error) {
    console.error('Error filtering material stats:', error);
    return [];
  }
});

const totalMaterialUsage = computed(() => {
  return materialStatsRaw.value.reduce((sum, stat) => sum + stat.totalUsed, 0);
});

const maxMaterialUsage = computed(() => {
  return materialStatsRaw.value.length ? Math.max(...materialStatsRaw.value.map(stat => stat.totalUsed)) : 0;
});

const showChart = ref(false);

const topMaterialStats = computed(() => {
  return [...filteredMaterialStats.value]
    .sort((a, b) => b.totalUsed - a.totalUsed)
    .slice(0, 10);
});

const mostUsedMaterial = computed(() => {
  return filteredMaterialStats.value.length > 0 
    ? filteredMaterialStats.value.reduce((max, stat) => 
        stat.totalUsed > max.totalUsed ? stat : max
      )
    : null;
});

const getChartColor = (index) => {
  const colors = [
    '#374151', '#6B7280', '#9CA3AF', '#D1D5DB', '#F3F4F6',
    '#1F2937', '#4B5563', '#111827', '#030712', '#F9FAFB'
  ];
  return colors[index % colors.length];
};

const getRanking = (stat) => {
  const sorted = [...materialStatsRaw.value].sort((a, b) => b.totalUsed - a.totalUsed);
  return sorted.findIndex(s => s.id === stat.id) + 1;
};

// Details dialog
const openDetailsDialog = async (order) => {
  try {
    const token = localStorage.getItem('authToken');

    const res = await axios.get(`https://kvdarbsbackend.vercel.app/orders/${order.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!materials.value.length) {
      await fetchMaterials();
    }

    detailsData.value = res.data;
    showDetailsDialog.value = true;
  } catch (err) {
    console.error("Kļūda saņemot detaļas:", err);
    showToast("Neizdevās ielādēt pasūtījuma detaļas!", 'error');
  }
};

const closeDetailsDialog = () => {
  showDetailsDialog.value = false;
};

// Add dialog
const closeAddDialog = () => {
  showAddDialog.value = false;
  materialSearch.value = '';
  
  // Reset form data
  if (currentTab.value === 'orders') {
    newOrder.value = { nosaukums: '', daudzums: '', status: 'Nav sākts' };
    orderMaterials.value = [];
  } else if (currentTab.value === 'materials') {
    newMaterial.value = { nosaukums: '', daudzums: '', vieniba: '', noliktava: 'Balta noliktava', vieta: '' };
  } else if (currentTab.value === 'workers') {
    newEmployee.value = { vards: '', uzvards: '', amats: 'Šuvēja', kods: '', status: 'Aktīvs' };
  }
};

const openAddDialog = () => {
  showAddDialog.value = true;
  materialSearch.value = '';
  currentEditType.value = currentTab.value;

  // Initialize form data based on current tab
  if (currentTab.value === 'orders') {
    orderMaterials.value = [];
    newOrder.value = { nosaukums: '', daudzums: '', status: 'Nav sākts' };
  } else if (currentTab.value === 'materials') {
    newMaterial.value = { nosaukums: '', daudzums: '', vieniba: '', noliktava: 'Balta noliktava', vieta: '' };
  } else if (currentTab.value === 'workers') {
    newEmployee.value = { vards: '', uzvards: '', amats: 'Šuvēja', kods: '', status: 'Aktīvs' };
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

// Material order functions
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

// Helper functions
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

const formatDate = (dateString) => {
  if (!dateString) return '';
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return '';
    return date.toLocaleDateString('lv-LV', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  } catch (error) {
    console.error('Error formatting date:', error);
    return '';
  }
};

// Load on mount
onMounted(async () => {
  await initPdfLibs();
  await fetchOrders();
  await fetchMaterials();
  await fetchShiftStats();
  await fetchWorkers();
  await fetchMaterialStats();
});

// Watch for period changes and automatically update data
watch([periodStart, periodEnd], () => {
  if (currentTab.value === 'shifts') {
    fetchShiftStats();
  }
});

// API calls
const fetchOrders = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('https://kvdarbsbackend.vercel.app/orders', {
      headers: { Authorization: `Bearer ${token}` }
    });
    // Ensure we always have an array
    orders.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    handleError(error, 'Neizdevās ielādēt pasūtījumus. Lūdzu, mēģiniet vēlreiz.');
    // Set to empty array on error
    orders.value = [];
  }
};

const fetchMaterials = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('https://kvdarbsbackend.vercel.app/materials', {
      headers: { Authorization: `Bearer ${token}` }
    });
    materials.value = response.data.materials;
  } catch (error) {
    handleError(error, 'Neizdevās ielādēt materiālus. Lūdzu, mēģiniet vēlreiz.');
  }
};

const fetchWorkers = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('https://kvdarbsbackend.vercel.app/employees', {
      headers: { Authorization: `Bearer ${token}` }
    });
    employees.value = response.data.employees;
  } catch (error) {
    handleError(error, 'Neizdevās ielādēt darbiniekus. Lūdzu, mēģiniet vēlreiz.');
  }
};

const fetchShiftStats = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const params = {};
    if (periodStart.value) {
      params.start = `${periodStart.value}T00:00:00`;
    }
    if (periodEnd.value) {
      params.end = `${periodEnd.value}T23:59:59`;
    }

    const response = await axios.get('https://kvdarbsbackend.vercel.app/api/shifts/stats', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      params: params,
    });
    shiftStats.value = response.data;
  } catch (error) {
    handleError(error, 'Neizdevās ielādēt maiņu statistiku. Lūdzu, mēģiniet vēlreiz.');
  }
};

const fetchMaterialStats = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('https://kvdarbsbackend.vercel.app/api/stats/materials', {
      headers: { Authorization: `Bearer ${token}` }
    });
    materialStatsRaw.value = response.data;
  } catch (error) {
    handleError(error, 'Neizdevās ielādēt materiālu statistiku. Lūdzu, mēģiniet vēlreiz.');
  }
};

// Add this function before addOrder
const checkMaterialAvailability = (materials) => {
  const insufficientMaterials = [];
  
  for (const mat of materials) {
    const material = materials.value.find(m => m.id === mat.id);
    if (!material) {
      insufficientMaterials.push({ id: mat.id, reason: 'Materiāls nav atrasts' });
      continue;
    }
    
    const requiredAmount = mat.daudzums * newOrder.value.daudzums;
    if (material.daudzums < requiredAmount) {
      insufficientMaterials.push({
        id: mat.id,
        name: material.nosaukums,
        available: material.daudzums,
        required: requiredAmount
      });
    }
  }
  
  return insufficientMaterials;
};

const addOrder = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const materialsToSend = orderMaterials.value.map(mat => ({
      id: mat.id,
      daudzums: mat.quantity
    }));

    // Vispirms iegūstam jaunākos materiālu datus
    await fetchMaterials();

    // Pārbaudam materiālu pieejamību ar jaunākajiem datiem
    const insufficientMaterials = checkMaterialAvailability(materialsToSend);
    if (insufficientMaterials.length > 0) {
      const errorMessage = insufficientMaterials.map(mat => 
        mat.reason ? mat.reason : 
        `Materiālam "${mat.name}" nepietiek daudzuma. Pieejams: ${mat.available}, Nepieciešams: ${mat.required}`
      ).join('\n');
      showToast(errorMessage, 'error');
      return;
    }

    // Izveidojam pasūtījumu ar materiālu versijām
    const orderResponse = await axios.post('https://kvdarbsbackend.vercel.app/orders', {
      ...newOrder.value,
      materials: materialsToSend.map(mat => ({
        ...mat,
        version: materials.value.find(m => m.id === mat.id).version // Pievienojam materiāla versiju
      }))
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Atjauninām materiālu daudzumus
    for (const mat of materialsToSend) {
      const material = materials.value.find(m => m.id === mat.id);
      if (material) {
        const newQuantity = material.daudzums - (mat.daudzums * newOrder.value.daudzums);
        await axios.put(`https://kvdarbsbackend.vercel.app/materials/${mat.id}`, {
          ...material,
          daudzums: newQuantity,
          version: material.version // Nosūtam versiju
        }, {
          headers: { Authorization: `Bearer ${token}` }
        });
      }
    }

    showAddDialog.value = false;
    await fetchOrders();
    await fetchMaterials();
    newOrder.value = { nosaukums: '', daudzums: '', status: 'Nav sākts' };
    orderMaterials.value = [];
    showToast('Pasūtījums ir veiksmīgi pievienots sistēmā!', 'success');
  } catch (error) {
    if (error.response?.status === 409) {
      // Konflikta gadījumā atjauninām datus un parādam kļūdu
      await fetchMaterials();
      showToast('Materiālu daudzums ir mainījies. Lūdzu, pārbaudiet pieejamību un mēģiniet vēlreiz.', 'error');
    } else {
      handleError(error, 'Neizdevās pievienot pasūtījumu. Lūdzu, pārbaudiet ievadītos datus un pārliecinieties, ka visi materiāli ir pieejami.');
    }
  }
};

const addMaterial = async () => {
  try {
    const token = localStorage.getItem('authToken');
    await axios.post('https://kvdarbsbackend.vercel.app/materials', newMaterial.value, {
      headers: { Authorization: `Bearer ${token}` }
    });
    showAddDialog.value = false;
    await fetchMaterials();
    newMaterial.value = { nosaukums: '', daudzums: '', vieniba: '', noliktava: '', vieta: '' };
    showToast('Materiāls ir veiksmīgi pievienots sistēmā!', 'success');
  } catch (error) {
    handleError(error, 'Neizdevās pievienot materiālu. Lūdzu, pārbaudiet ievadītos datus un pārliecinieties, ka materiāls ar šādu nosaukumu vēl neeksistē.');
  }
};

const addEmployee = async () => {
  try {
    const token = localStorage.getItem('authToken');
    const response = await axios.get('https://kvdarbsbackend.vercel.app/employees', {
      headers: { Authorization: `Bearer ${token}` }
    });

    const duplicateCode = response.data.employees.find(e => Number(e.kods) === Number(newEmployee.value.kods));
    if (duplicateCode) {
      showToast('Darbinieks ar šādu kodu jau eksistē sistēmā. Lūdzu, izmantojiet citu kodu.', 'error');
      return;
    }

    const duplicateName = response.data.employees.find(e => 
      e.vards.toLowerCase() === newEmployee.value.vards.toLowerCase() && 
      e.uzvards.toLowerCase() === newEmployee.value.uzvards.toLowerCase()
    );
    if (duplicateName) {
      showToast('Darbinieks ar šādu vārdu un uzvārdu jau eksistē sistēmā. Lūdzu, pārbaudiet ievadītos datus.', 'error');
      return;
    }

    await axios.post('https://kvdarbsbackend.vercel.app/employees', newEmployee.value, {
      headers: { Authorization: `Bearer ${token}` }
    });
    showAddDialog.value = false;
    await fetchWorkers();
    newEmployee.value = { vards: '', uzvards: '', amats: '', kods: '', status: 'Aktīvs' };
    showToast('Darbinieks ir veiksmīgi pievienots sistēmā!', 'success');
  } catch (error) {
    handleError(error, 'Neizdevās pievienot darbinieku. Lūdzu, pārbaudiet ievadītos datus un pārliecinieties, ka visi obligātie lauki ir aizpildīti.');
  }
};

// Edit functions
const openEditDialog = async (type, item) => {
  currentEditType.value = type;
  editData.value = { ...item };
  editDialog.value = true;
  materialSearch.value = '';

  if (type === 'orders') {
    try {
      const token = localStorage.getItem('authToken');
      const res = await axios.get(`https://kvdarbsbackend.vercel.app/orders/${item.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      editData.value = res.data;
    } catch (err) {
      console.error("Kļūda saņemot detaļas:", err);
      showToast("Neizdevās ielādēt pasūtījuma detaļas!", 'error');
    }
  }
};

const saveEdit = async () => {
  try {
    const token = localStorage.getItem('authToken');
    let url;
    if (currentEditType.value === 'orders') {
      url = `https://kvdarbsbackend.vercel.app/orders/${editData.value.id}`;
    } else if (currentEditType.value === 'materials') {
      url = `https://kvdarbsbackend.vercel.app/materials/${editData.value.id}`;
    } else if (currentEditType.value === 'workers') {
      url = `https://kvdarbsbackend.vercel.app/employees/${editData.value.id}`;
    }

    let data = { ...editData.value };

    if (currentEditType.value === 'workers' && !showPasswordChange.value) {
      delete data.password;
    }

    if (currentEditType.value === 'orders') {
      const materialsToSend = editData.value.materials.map(m => ({
        material_id: m.material_id || m.id,
        daudzums: m.quantity || 1
      }));
      data.materials = materialsToSend;
    }

    await axios.put(url, data, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Tikai ja nav kļūdas:
    editDialog.value = false;
    showPasswordChange.value = false;
    if (currentEditType.value === 'orders') {
      await fetchOrders();
    } else if (currentEditType.value === 'materials') {
      await fetchMaterials();
    } else if (currentEditType.value === 'workers') {
      await fetchWorkers();
    }
    showActionToast('Izmaiņas ir veiksmīgi saglabātas sistēmā!', 'success');
  } catch (error) {
    // NEaizver editDialog, NErādi success toast
    handleError(error, 'Neizdevās saglabāt izmaiņas. Lūdzu, pārbaudiet ievadītos datus un pārliecinieties, ka visi obligātie lauki ir aizpildīti.');
  }
};

const cancelEdit = () => {
  editDialog.value = false;
  showPasswordChange.value = false;
};

// Delete functions
const deleteOrder = async (id) => {
  showDeleteToast('Vai tiešām vēlaties dzēst šo pasūtījumu? Šo darbību nevarēs atsaukt.', async () => {
    try {
      const token = localStorage.getItem('authToken');
      await axios.delete(`https://kvdarbsbackend.vercel.app/orders/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchOrders();
      showActionToast('Pasūtījums ir veiksmīgi dzēsts no sistēmas!', 'success');
    } catch (error) {
      handleError(error, 'Neizdevās dzēst pasūtījumu. Lūdzu, pārbaudiet, vai pasūtījums nav jau pabeigts vai procesā.');
    }
  });
};

const deleteMaterial = async (id) => {
  showDeleteToast('Vai tiešām vēlaties dzēst šo materiālu? Šo darbību nevarēs atsaukt.', async () => {
    try {
      const token = localStorage.getItem('authToken');
      await axios.delete(`https://kvdarbsbackend.vercel.app/materials/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchMaterials();
      showActionToast('Materiāls ir veiksmīgi dzēsts no sistēmas!', 'success');
    } catch (error) {
      handleError(error, 'Neizdevās dzēst materiālu. Lūdzu, pārbaudiet, vai materiāls nav izmantots kādā aktīvā pasūtījumā.');
    }
  });
};

const deleteEmployee = async (id) => {
  showDeleteToast('Vai tiešām vēlaties dzēst šo darbinieku? Šo darbību nevarēs atsaukt.', async () => {
    try {
      const token = localStorage.getItem('authToken');
      await axios.delete(`https://kvdarbsbackend.vercel.app/employees/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await fetchWorkers();
      showActionToast('Darbinieks ir veiksmīgi dzēsts no sistēmas!', 'success');
    } catch (error) {
      handleError(error, 'Neizdevās dzēst darbinieku. Lūdzu, pārbaudiet, vai darbinieks nav piešķirts kādam aktīvam pasūtījumam.');
    }
  });
};

const applyDateFilter = () => {
  fetchShiftStats();
};

const filteredShiftsByDate = computed(() => {
  let result = shiftStats.value;

  if (shiftSearchQuery.value) {
    result = result.filter(emp =>
      emp.vards.toLowerCase().includes(shiftSearchQuery.value.toLowerCase()) ||
      emp.uzvards.toLowerCase().includes(shiftSearchQuery.value.toLowerCase())
    );
  }

  if (shiftSortKey.value) {
    result = sortByKey(result, shiftSortKey.value, shiftSortAsc.value);
  }

  return result.map(emp => ({
    ...emp,
    formattedDate: new Date(emp.start_time).toLocaleDateString('lv-LV', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  })).slice(0, limitCount.value);
});

async function exportToPDF() {
  try {
    if (!isPdfLibsReady.value) {
      showToast('PDF bibliotēkas vēl nav ielādētas. Lūdzu, uzgaidiet, kamēr tās tiks ielādētas.', 'error');
      return;
    }

    const token = localStorage.getItem('authToken');
    if (!token) {
      showToast('Jūsu sesija ir beigusies. Lūdzu, ielogojieties sistēmā vēlreiz.', 'error');
      return;
    }

    // Get current tab and data
    const reportType = currentTab.value;
    
    // Get current filters based on tab
    let searchField;
    let statusField;
    let startDateField;
    let endDateField;

    switch (reportType) {
      case 'orders':
        searchField = searchQuery.value;
        statusField = selectedStatus.value;
        break;
      case 'materials':
        searchField = searchMaterials.value;
        break;
      case 'workers':
        searchField = searchWorkers.value;
        break;
      case 'shifts':
        searchField = shiftSearchQuery.value;
        startDateField = periodStart.value;
        endDateField = periodEnd.value;
        break;
      default:
        searchField = '';
    }

    // Send request to backend
    const response = await axios.get('https://kvdarbsbackend.vercel.app/api/export_pdf', {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        report_type: reportType,
        search_query: searchField,
        status: statusField,
        start_date: startDateField,
        end_date: endDateField
      },
      responseType: 'blob'
    }).catch(error => {
      console.error('PDF export error:', error.response?.data?.error || error.message);
      showToast(error.response?.data?.error || 'Neizdevās eksportēt PDF. Lūdzu, mēģiniet vēlreiz.', 'error');
      throw error;
    });

    // Create blob and download
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${reportType}_atskaite.pdf`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

    showActionToast('PDF eksportēts veiksmīgi!', 'success');
  } catch (error) {
    handleError(error, 'Neizdevās eksportēt PDF');
  } finally {
    isPdfLibsLoading.value = false;
  }
}

const showOrderForm = computed(() => showAddDialog.value && currentTab.value === 'orders');
const showMaterialForm = computed(() => showAddDialog.value && currentTab.value === 'materials');
const showWorkerForm = computed(() => showAddDialog.value && currentTab.value === 'workers');

const showPasswordChange = ref(false);

// Add this function at the beginning of the script section
const handleError = (error, defaultMessage) => {
  let msg = defaultMessage;
  if (error.response?.data?.error) {
    msg = error.response.data.error;
  } else if (error.response?.data?.message) {
    msg = error.response.data.message;
  } else if (typeof error.response?.data === 'string') {
    msg = error.response.data;
  }

  // Ja kļūda ir par materiāla trūkumu, piedāvā iestatīt maksimālo daudzumu ar smuku toast
  const match = msg.match(/Nepietiek materiāla: (.*), nepieciešams ([0-9.]+), ir tikai ([0-9.]+)/i);
  if (match) {
    const materialName = match[1];
    const required = parseFloat(match[2]);
    const available = parseFloat(match[3]);
    const mat = orderMaterials.value.find(m => getMaterialName(m.id) === materialName);
    if (mat && mat.quantity > 0) {
      const maxQty = Math.floor(available / mat.quantity);
      if (maxQty > 0) {
        showToast(
          '',
          'error',
          10000,
          () => h('div', [
            h('div', `Materiāla "${materialName}" pietiek tikai pasūtījuma daudzumam ${maxQty}.`),
            h('div', { style: 'margin-top: 10px; display: flex; gap: 10px;' }, [
              h('button', {
                style: 'background:#fff;color:#1f2937;padding:6px 16px;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;transition:background 0.2s;',
                onMouseover: e => e.target.style.background = '#f3f4f6',
                onMouseout: e => e.target.style.background = '#fff',
                onClick: () => {
                  newOrder.value.daudzums = maxQty;
                  document.body.querySelectorAll('.toast').forEach(el => el.remove());
                }
              }, 'Iestatīt uz ' + maxQty),
              h('button', {
                style: 'background:#fff;color:#1f2937;padding:6px 16px;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;transition:background 0.2s;',
                onMouseover: e => e.target.style.background = '#f3f4f6',
                onMouseout: e => e.target.style.background = '#fff',
                onClick: () => {
                  document.body.querySelectorAll('.toast').forEach(el => el.remove());
                }
              }, 'Atcelt')
            ])
          ])
        );
      } else {
        showToast(`Materiāla "${materialName}" nepietiek nevienam pasūtījumam.`, 'error');
      }
      return;
    }
  }
  showToast(msg, 'error');
};

function showActionToast(message, type = 'info', buttonText = null, onButton = null) {
  // Ja nav buttonText, rāda tikai tekstu, bez pogas
  if (!buttonText) {
    showToast(message, type);
    return;
  }
  showToast(
    '',
    type,
    7000,
    () => h('div', [
      h('div', message),
      h('div', { style: 'margin-top: 10px; display: flex; gap: 10px;' }, [
        h('button', {
          style: 'background:#fff;color:#1f2937;padding:6px 16px;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;transition:background 0.2s;',
          onMouseover: e => e.target.style.background = '#f3f4f6',
          onMouseout: e => e.target.style.background = '#fff',
          onClick: () => {
            if (onButton) onButton();
            document.body.querySelectorAll('.toast').forEach(el => el.remove());
          }
        }, buttonText)
      ])
    ])
  );
}

function showDeleteToast(message, onConfirm) {
  showToast(
    '',
    'error',
    10000,
    () => h('div', [
      h('div', message),
      h('div', { style: 'margin-top: 10px; display: flex; gap: 10px;' }, [
        h('button', {
          style: 'background:#fff;color:#1f2937;padding:6px 16px;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;transition:background 0.2s;',
          onMouseover: e => e.target.style.background = '#f3f4f6',
          onMouseout: e => e.target.style.background = '#fff',
          onClick: () => {
            onConfirm();
            document.body.querySelectorAll('.toast').forEach(el => el.remove());
          }
        }, 'Jā, dzēst'),
        h('button', {
          style: 'background:#1f2937;color:#fff;padding:6px 16px;border:none;border-radius:6px;cursor:pointer;transition:background 0.2s;',
          onMouseover: e => e.target.style.background = '#111827',
          onMouseout: e => e.target.style.background = '#1f2937',
          onClick: () => {
            document.body.querySelectorAll('.toast').forEach(el => el.remove());
          }
        }, 'Atcelt')
      ])
    ])
  );
}

const showTransferDialog = ref(false);
const transferData = ref({
  id: null,
  nosaukums: '',
  noliktava: '',
  vieniba: '',
  daudzums: 0,
  max: 0,
  toNoliktava: ''
});
const warehouseOptions = ['Balta noliktava', 'Centrālā noliktava'];

function openTransferDialog(material) {
  transferData.value = {
    id: material.id,
    nosaukums: material.nosaukums,
    noliktava: material.noliktava,
    vieniba: material.vieniba,
    daudzums: 0,
    max: material.daudzums,
    toNoliktava: warehouseOptions.find(opt => opt !== material.noliktava)
  };
  showTransferDialog.value = true;
}

async function transferMaterial() {
  try {
    const token = localStorage.getItem('authToken');
    await axios.post('https://kvdarbsbackend.vercel.app/materials/transfer', {
      material_id: transferData.value.id,
      daudzums: transferData.value.daudzums,
      from_noliktava: transferData.value.noliktava,
      to_noliktava: transferData.value.toNoliktava
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    showTransferDialog.value = false;
    await fetchMaterials();
    showToast('Materiāls veiksmīgi pārvietots!', 'success');
  } catch (error) {
    handleError(error, 'Neizdevās pārvietot materiālu. Lūdzu, pārbaudiet datus.');
  }
}

</script>
