<template>
  <Teleport to="body">
    <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-semibold">Pasūtījuma detaļas</h3>
          <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div v-if="order" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500">Nosaukums</p>
              <p class="font-medium">{{ order.nosaukums }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Daudzums</p>
              <p class="font-medium">{{ order.daudzums }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Statuss</p>
              <p class="font-medium">{{ order.status }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500">Atbildīgais darbinieks</p>
              <p class="font-medium">{{ order.employee ? `${order.employee.vards} ${order.employee.uzvards}` : 'Nav piešķirts' }}</p>
            </div>
          </div>

          <div class="mt-6">
            <h4 class="font-semibold mb-2">Materiāli</h4>
            <div class="border rounded-lg overflow-hidden">
              <table class="min-w-full">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Nosaukums</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Daudzums</th>
                    <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Vienība</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr v-for="material in order.materials" :key="material.id">
                    <td class="px-4 py-2">{{ material.nosaukums }}</td>
                    <td class="px-4 py-2">{{ material.daudzums }}</td>
                    <td class="px-4 py-2">{{ material.vieniba }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    required: true
  },
  order: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])
</script> 