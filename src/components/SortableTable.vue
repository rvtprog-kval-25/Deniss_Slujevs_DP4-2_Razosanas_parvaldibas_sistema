<template>
  <div class="overflow-x-auto">
    <table class="min-w-full bg-white border border-gray-200">
      <thead>
        <tr>
          <th
            v-for="column in columns"
            :key="column.key"
            @click="sortBy(column.key)"
            class="px-6 py-3 border-b border-gray-200 bg-gray-50 text-left text-xs leading-4 font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
          >
            <div class="flex items-center space-x-1">
              <span>{{ column.label }}</span>
              <span v-if="currentSort.key === column.key" class="text-gray-400">
                {{ currentSort.direction === 'asc' ? '↑' : '↓' }}
              </span>
            </div>
          </th>
        </tr>
      </thead>
      <tbody class="bg-white">
        <tr v-for="(item, index) in sortedItems" :key="index" class="hover:bg-gray-50">
          <td
            v-for="column in columns"
            :key="column.key"
            class="px-6 py-4 whitespace-no-wrap border-b border-gray-200"
          >
            <template v-if="column.key === 'actions' && column.action">
              <button 
                @click="column.action(item)"
                class="text-blue-600 hover:text-blue-800"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </template>
            <template v-else>
              {{ item[column.key] }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  },
  columns: {
    type: Array,
    required: true
  },
  isShiftsTable: {
    type: Boolean,
    default: false
  }
})

const currentSort = ref({
  key: '',
  direction: 'asc'
})

const sortBy = (key) => {
  if (currentSort.value.key === key) {
    currentSort.value.direction = currentSort.value.direction === 'asc' ? 'desc' : 'asc'
  } else {
    currentSort.value.key = key
    currentSort.value.direction = 'asc'
  }
}

const sortedItems = computed(() => {
  if (!currentSort.value.key) return props.items

  return [...props.items].sort((a, b) => {
    const aValue = a[currentSort.value.key]
    const bValue = b[currentSort.value.key]

    // Специальная обработка для дат в таблице смен
    if (props.isShiftsTable && (currentSort.value.key === 'sakums' || currentSort.value.key === 'beigas')) {
      const dateA = new Date(aValue)
      const dateB = new Date(bValue)
      return currentSort.value.direction === 'asc' ? dateA - dateB : dateB - dateA
    }

    // Обычная сортировка для остальных случаев
    if (typeof aValue === 'string') {
      return currentSort.value.direction === 'asc'
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }

    return currentSort.value.direction === 'asc'
      ? aValue - bValue
      : bValue - aValue
  })
})
</script> 