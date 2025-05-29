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
  const token = localStorage.getItem('authToken');  // Извлекаем токен из localStorage

  if (!token) {
    console.error("Ошибка: Токен отсутствует в localStorage");
    router.push('/login');
    return;
  }

  try {
    const response = await fetch('https://kvdarbsbackend.vercel.app/logout', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,  // Отправляем токен на сервер
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (response.status === 403) {
      console.error("Ошибка 403: Токен недействителен", data);
      localStorage.removeItem('authToken');  // Удаляем токен из localStorage
      router.push('/login');
      return;
    }

    if (response.ok && data.success) {
      console.log("Выход выполнен успешно!");
      localStorage.removeItem('authToken');  // Удаляем токен из localStorage
      router.push('/login');  // Перенаправляем на страницу входа
    } else {
      console.error("Ошибка выхода:", data.error);
    }
  } catch (error) {
    console.error("Ошибка запроса logout:", error);
  }
};
</script>
