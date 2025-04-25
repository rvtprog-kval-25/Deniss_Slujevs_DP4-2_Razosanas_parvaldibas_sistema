<template>
  <div class="h-full bg-gray-100 flex flex-col justify-center items-center py-12">
    <div class="grid grid-cols-1 md:grid-cols-4 gap-12 px-4">

      <!-- Materiāli -->
      <div class="flex flex-col items-center">
        <a href="/Materials">
          <div
            class="bg-black rounded-lg w-40 h-40 flex items-center justify-center hover:bg-gray-800 hover:scale-105 transition-all duration-200 ease-in-out cursor-pointer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4h18v6H3V4zm3 10h12v6H6v-6z" />
            </svg>
          </div>
        </a>
        <span class="mt-4 text-lg font-light text-black">Materiāli</span>
      </div>

      <!-- Pasūtījumi -->
      <div class="flex flex-col items-center">
        <a href="/Orders">
          <div
            class="bg-black rounded-lg w-40 h-40 flex items-center justify-center hover:bg-gray-800 hover:scale-105 transition-all duration-200 ease-in-out cursor-pointer"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5h14v14H5V5zm3 3v8m4-8v8m4-8v8" />
            </svg>
          </div>
        </a>
        <span class="mt-4 text-lg font-light text-black">Pasūtījumi</span>
      </div>

      <!-- Sākt Maiņu -->
      <div class="flex flex-col items-center">
        <div
          @click="startShift"
          class="bg-black rounded-lg w-40 h-40 flex items-center justify-center hover:bg-gray-800 hover:scale-105 transition-all duration-200 ease-in-out cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </div>
        <span class="mt-4 text-lg font-light text-black">Sākt Maiņu</span>
      </div>

      <!-- Beigt Maiņu -->
      <div class="flex flex-col items-center">
        <div
          @click="endShift"
          class="bg-black rounded-lg w-40 h-40 flex items-center justify-center hover:bg-gray-800 hover:scale-105 transition-all duration-200 ease-in-out cursor-pointer"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <span class="mt-4 text-lg font-light text-black">Beigt Maiņu</span>
      </div>

    </div>

    <!-- Shift Notification -->
    <transition name="fade">
      <div v-if="showShiftNotification" class="fixed top-0 left-1/2 transform -translate-x-1/2 mt-4 p-4 bg-green-600 text-white rounded-lg shadow-lg max-w-xs w-full text-center">
        <p>Maiņa sākta!</p>
      </div>
    </transition>

    <transition name="fade">
      <div v-if="showEndShiftNotification" class="fixed top-0 left-1/2 transform -translate-x-1/2 mt-4 p-4 bg-red-600 text-white rounded-lg shadow-lg max-w-xs w-full text-center">
        <p>Maiņa pabeigta!</p>
      </div>
    </transition>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";

export default defineComponent({
  setup() {
    const userId = localStorage.getItem("userId");
    const shiftId = ref(null);
    const showShiftNotification = ref(false);
    const showEndShiftNotification = ref(false);

    onMounted(() => {
      const savedId = localStorage.getItem(`activeShiftId_${userId}`);
      if (savedId) {
        shiftId.value = savedId;
      }
    });

    const startShift = async () => {
      if (shiftId.value) {
        showEndShiftNotification.value = false;
        showShiftNotification.value = false;
        return;
      }

      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch("http://localhost:5000/api/shifts/start", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
          },
          body: JSON.stringify({ started_at: new Date().toISOString() }),
        });

        if (!response.ok) throw new Error("Neizdevās sākt maiņu.");

        const data = await response.json();
        shiftId.value = data.id;
        localStorage.setItem(`activeShiftId_${userId}`, data.id);

        showShiftNotification.value = true;

        // Hide notification after 3 seconds
        setTimeout(() => {
          showShiftNotification.value = false;
        }, 3000);

      } catch (error) {
        console.error(error);
        alert("Kļūda: nevarēja sākt maiņu.");
      }
    };

    const endShift = async () => {
      if (!shiftId.value) {
        alert("Nav aktīvas maiņas.");
        return;
      }

      try {
        const token = localStorage.getItem("authToken");
        const response = await fetch(`http://localhost:5000/api/shifts/end/${shiftId.value}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
          },
          body: JSON.stringify({ ended_at: new Date().toISOString() }),
        });

        if (!response.ok) throw new Error("Neizdevās beigt maiņu.");

        localStorage.removeItem(`activeShiftId_${userId}`);
        shiftId.value = null;

        showEndShiftNotification.value = true;

        // Hide notification after 3 seconds
        setTimeout(() => {
          showEndShiftNotification.value = false;
        }, 3000);

      } catch (error) {
        console.error(error);
        alert("Kļūda: nevarēja beigt maiņu.");
      }
    };

    return {
      startShift,
      endShift,
      showShiftNotification,
      showEndShiftNotification,
    };
  },
});
</script>

<style scoped>
/* Fade in and out transition for notifications */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
