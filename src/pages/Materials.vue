<template>
  <div class="min-h-screen bg-gray-100 py-10 px-4 flex flex-col items-center">
    <!-- Кнопка + Поиск в одной строке -->
    <div class="w-full max-w-4xl mb-6 flex items-center gap-4">
      <!-- Кнопка домой -->
      <button
        @click="goHome"
        class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-gray-700 text-white hover:bg-gray-600"
      >
        Uz sākumu
      </button>

      <!-- Поле поиска -->
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Meklē materiālus..."
        class="flex-1 px-4 py-2 rounded-lg border border-gray-300 shadow-sm focus:ring-2 focus:ring-gray-500 focus:outline-none"
      />
    </div>

    <!-- Состояния -->
    <div v-if="loading" class="text-gray-600 text-center">Dati tiek ielādēti...</div>
    <div v-else-if="error" class="text-red-500 text-center">Kļūda: {{ error }}</div>
    <div v-else-if="filteredMaterials.length === 0" class="text-gray-500 text-center">
      Nav atbilstošu materiālu
    </div>

    <!-- Список материалов -->
    <div v-else class="w-full max-w-6xl bg-white rounded-lg shadow divide-y divide-gray-200">
      <div
        v-for="material in filteredMaterials"
        :key="material.id"
        class="flex justify-between items-center px-6 py-4 hover:bg-gray-50 transition"
      >
        <div>
          <h3 class="text-lg font-semibold text-gray-800">{{ material.nosaukums }}</h3>
        </div>
        <button
          @click="goToDetails(material.id)"
          class="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600"
        >
          Sīkāk
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const materials = ref([]);
const searchQuery = ref('');
const loading = ref(true);
const error = ref(null);

const fetchMaterials = async () => {
  const token = localStorage.getItem('authToken');
  if (!token) {
    error.value = 'Autorizācijas tokens nav atrasts.';
    loading.value = false;
    return;
  }

  try {
    const res = await fetch('https://kvdarbsbackend.vercel.app/materials', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    const data = await res.json();
    if (!res.ok || !data.success) {
      throw new Error(data.error || 'Neizdevās ielādēt materiālus');
    }

    materials.value = data.materials;
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

onMounted(fetchMaterials);

const filteredMaterials = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return materials.value.filter((m) =>
    [m.nosaukums, m.noliktava, m.vieta, m.vienibas].some((field) =>
      field.toLowerCase().includes(query)
    )
  );
});

const goToDetails = (id) => {
  router.push({ name: 'MaterialDetails', params: { id: String(id) } });
};
const goHome = () => {
  router.push('/home');

};
</script>


