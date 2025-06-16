import { ref } from 'vue'

export function useToast() {
  const showToast = ref(false)
  const toastMessage = ref('')
  const toastType = ref('success') // 'success' или 'error'

  const showSuccessToast = (message) => {
    toastMessage.value = message
    toastType.value = 'success'
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)
  }

  const showErrorToast = (message) => {
    toastMessage.value = message
    toastType.value = 'error'
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)
  }

  return {
    showToast,
    toastMessage,
    toastType,
    showSuccessToast,
    showErrorToast
  }
} 