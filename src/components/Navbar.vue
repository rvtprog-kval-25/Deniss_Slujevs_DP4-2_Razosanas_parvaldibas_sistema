<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-6xl mx-auto px-4">
      <div class="flex justify-between">
        <div class="flex space-x-7">
          <div>
            <a class="flex items-center py-4 px-2">
              <span class="font-semibold text-xl">Sencis</span>
            </a>
          </div>
        </div>
        <div class="md:flex items-center">
          <a href="javascript:void(0);" @click="logout" class="font-semibold py-1 px-6 text-lg outline rounded hover:bg-black hover:text-white duration-500">Iziet</a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const logout = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error("Token not found");
      return;
    }
    const response = await fetch('http://localhost:5000/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.ok) {
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      router.push('/login');
    } else {
      console.error("Logout failed");
    }
  } catch (error) {
    console.error("Error during logout:", error);
  }
};
</script>
