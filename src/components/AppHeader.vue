<template>
  <header class="app-header" :class="{ 'dark': isDarkTheme }">
    <div class="header-left">
      <h1 class="logo">LinkCell</h1>
    </div>
    <div class="header-right">
      <button 
        class="theme-toggle-button" 
        @click="toggleTheme"
        title="Toggle theme"
      >
        <svg v-if="isDarkTheme" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="5"></circle>
          <line x1="12" y1="1" x2="12" y2="3"></line>
          <line x1="12" y1="21" x2="12" y2="23"></line>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
          <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
          <line x1="1" y1="12" x2="3" y2="12"></line>
          <line x1="21" y1="12" x2="23" y2="12"></line>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
          <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
        <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      </button>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isDarkTheme = ref(false)

const toggleTheme = () => {
  isDarkTheme.value = !isDarkTheme.value
  updateTheme()
}

const updateTheme = () => {
  if (isDarkTheme.value) {
    document.documentElement.classList.add('dark')
    document.body.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    document.body.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDarkTheme.value = true
    updateTheme()
  }
})
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  background-color: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  z-index: 9999;
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 10000;
}

.theme-toggle-button {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #374151;
  transition: all 0.2s ease;
  padding: 0;
}

.theme-toggle-button:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.app-header.dark {
  background-color: #111827;
  border-bottom: 1px solid #374151;
}

.app-header.dark .theme-toggle-button {
  color: #d1d5db;
}

.app-header.dark .theme-toggle-button:hover {
  background: #1f2937;
  color: #f3f4f6;
}

.logo {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
  transition: color 0.3s ease;
}

.app-header.dark .logo {
  color: #f3f4f6;
}
</style>