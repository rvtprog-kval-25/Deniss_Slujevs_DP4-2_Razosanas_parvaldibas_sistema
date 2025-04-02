<template>
    <div class="h-full bg-gray-100 flex flex-col justify-center items-center py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-12 px-4">
    
        <div class="flex flex-col items-center">
          <a href="/Materials">
            <div
              class="bg-black rounded-lg w-40 h-40 flex items-center justify-center hover:bg-gray-800 hover:scale-105 transition-all duration-200 ease-in-out cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-16 w-16 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 4h18v6H3V4zm3 10h12v6H6v-6z"
                />
              </svg>
            </div>
          </a>
          <span class="mt-4 text-lg font-light text-black">Materiāli</span>
        </div>
  
        <!-- Pasūtījumi -->
        <div class="flex flex-col items-center">
          <a href="Orders">
            <div
              class="bg-black rounded-lg w-40 h-40 flex items-center justify-center hover:bg-gray-800 hover:scale-105 transition-all duration-200 ease-in-out cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-16 w-16 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 5h14v14H5V5zm3 3v8m4-8v8m4-8v8"
                />
              </svg>
            </div>
          </a>
          <span class="mt-4 text-lg font-light text-black">Pasūtījumi</span>
        </div>
  
        <!-- Sākt Maiņu -->
        <div class="flex flex-col items-center">
          <a href="/sakt-mainu">
            <div
              class="bg-black rounded-lg w-40 h-40 flex items-center justify-center hover:bg-gray-800 hover:scale-105 transition-all duration-200 ease-in-out cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-16 w-16 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 5l7 7-7 7"
                />
              </svg>
            </div>
          </a>
          <span class="mt-4 text-lg font-light text-black">Sākt Maiņu</span>
        </div>
  
        <!-- Beigt Mainu -->
        <div class="flex flex-col items-center">
          <a href="/beigt-mainu">
            <div
              class="bg-black rounded-lg w-40 h-40 flex items-center justify-center hover:bg-gray-800 hover:scale-105 transition-all duration-200 ease-in-out cursor-pointer"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-16 w-16 text-white"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>
          </a>
          <span class="mt-4 text-lg font-light text-black">Beigt Mainu</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent } from "vue";
  
  export default defineComponent({});
  </script>
  
