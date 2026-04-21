<template>
  <div class="app-container">
    <AppHeader 
      @open-settings="showSettings = true" 
    />
    <div class="main-container" v-if="!showSettings">
      <LeftSidebar :selectedDocuments="selectedDocuments" @update:selectedDocuments="selectedDocuments = $event" />
      <MainContent :selectedDocuments="selectedDocuments" @update:selectedDocuments="selectedDocuments = $event" ref="mainContentRef" />
      <RightSidebar ref="rightSidebarRef" />
    </div>
    <Settings v-else @close-settings="showSettings = false" />
  </div>
</template>

<script setup>
import { ref, provide, onMounted } from 'vue'
import AppHeader from './components/AppHeader.vue'
import LeftSidebar from './components/LeftSidebar.vue'
import MainContent from './components/MainContent.vue'
import RightSidebar from './components/RightSidebar.vue'
import Settings from './components/Settings.vue'

const showSettings = ref(false)
const selectedDocuments = ref([])
const rightSidebarRef = ref(null)
const mainContentRef = ref(null)

// 提供共享状态
provide('selectedDocuments', selectedDocuments)

// 组件挂载后，将 rightSidebarRef 传递给 mainContentRef
onMounted(() => {
  console.log('App mounted')
  // 添加延迟，确保组件完全挂载
  setTimeout(() => {
    console.log('mainContentRef.value:', mainContentRef.value)
    console.log('rightSidebarRef.value:', rightSidebarRef.value)
    if (mainContentRef.value && rightSidebarRef.value) {
      console.log('Setting rightSidebarRef')
      mainContentRef.value.setRightSidebarRef(rightSidebarRef.value)
    } else {
      console.log('Failed to set rightSidebarRef:', {
        mainContentRef: !!mainContentRef.value,
        rightSidebarRef: !!rightSidebarRef.value
      })
    }
  }, 1000)
})
</script>

<style scoped>
.app-container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background-color: #ffffff;
  transition: background-color 0.3s ease;
}

.main-container {
  display: flex;
  height: calc(100vh - 56px);
  margin-top: 56px;
  width: 100%;
  overflow: hidden;
}
</style>

<style>
/* 全局样式重置 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, fill 0.3s ease, stroke 0.3s ease;
}

html, body {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

/* 确保页面最小宽度 */
.app-container {
  min-width: 1200px;
}

/* 全局深色主题样式 */
.dark .app-container {
  background-color: #0f172a;
}

/* 左侧侧边栏深色主题 */
.dark .left-sidebar {
  background-color: #111827;
  border-right: 1px solid #374151;
}

.dark .left-sidebar .cell-item {
  color: #f3f4f6;
}

.dark .left-sidebar .cell-item:hover {
  background-color: #1f2937;
}

.dark .left-sidebar .cell-item.active {
  background-color: #1e40af;
  border-left: 3px solid #60a5fa;
}

.dark .left-sidebar .cell-icon {
  color: #9ca3af;
}

.dark .left-sidebar .cell-title {
  color: #f3f4f6;
}

.dark .left-sidebar .cell-meta {
  color: #9ca3af;
}

.dark .left-sidebar .cell-list::-webkit-scrollbar-track {
  background: #1f2937;
}

.dark .left-sidebar .cell-list::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.dark .left-sidebar .cell-list::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

/* 搜索框深色主题 */
.dark .left-sidebar .el-input__wrapper {
  background-color: #1f2937 !important;
  border-color: #374151 !important;
  box-shadow: none !important;
}

.dark .left-sidebar .el-input__inner {
  color: #f3f4f6 !important;
  background-color: #1f2937 !important;
}

.dark .left-sidebar .el-input__inner::placeholder {
  color: #6b7280 !important;
}

.dark .left-sidebar .el-input__prefix-inner {
  color: #9ca3af !important;
}

/* 中间主内容区深色主题 */
.dark .main-content {
  background-color: #0f172a;
  border-right: 1px solid #333a47;
}

.dark .main-content .conversation-title {
  color: #f1f5f9;
}

.dark .main-content .message-card {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

.dark .main-content .user-card {
  background-color: #409EFF;
  border: none;
}

.dark .main-content .ai-thinking span {
  color: #94a3b8;
}

.dark .main-content .progress-bar {
  background-color: #333a47;
}

.dark .main-content .progress-fill {
  background-color: #409EFF;
}

.dark .main-content .ai-content h3 {
  color: #f1f5f9;
}

.dark .main-content .ai-content h4 {
  color: #f1f5f9;
}

.dark .main-content .ai-content p {
  color: #f1f5f9;
}

.dark .main-content .ai-content li {
  color: #f1f5f9;
}

.dark .main-content .ai-graph {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

.dark .main-content .secondary-node {
  background-color: #1e293b;
}

/* 模型选择和操作按钮 */
.dark .main-content .model-select {
  background-color: #1e293b !important;
  border: 1px solid #333a47 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

.dark .main-content .model-select .el-select__wrapper {
  background-color: #1e293b !important;
  border: 1px solid #333a47 !important;
}

.dark .main-content .model-select .el-select__input {
  color: #409EFF !important;
}

.dark .main-content .model-select .el-select__caret {
  color: #409EFF !important;
}

.dark .main-content .icon-button {
  background-color: #1e293b;
  color: #409EFF;
  border: 1px solid #333a47;
}

.dark .main-content .icon-button:hover {
  background-color: #333a47;
  color: #66b1ff;
}

/* AI消息样式 */
.dark .main-content .ai-message-content-wrapper {
  background-color: #1e293b;
  border-radius: 8px 16px 16px 16px;
  padding: 16px 20px;
}

.dark .main-content .ai-message-content {
  color: #f1f5f9;
  font-size: 14px;
  line-height: 1.7;
  margin-bottom: 12px;
}

.dark .main-content .ai-footer {
  background-color: #333a47;
  padding: 8px 12px;
  border-radius: 6px;
  margin-top: 12px;
  display: flex;
  gap: 16px;
}

.dark .main-content .ai-footer-button {
  color: #409EFF !important;
  font-size: 12px;
  padding: 0 !important;
}

.dark .main-content .ai-footer-button:hover {
  color: #66b1ff !important;
}

.dark .main-content .message-input-container {
  border-top: 1px solid #333a47;
  background-color: #0f172a;
}

.dark .main-content .input-wrapper {
  border: 1px solid #333a47;
  background-color: #1e293b;
}

.dark .main-content .input-wrapper:focus-within {
  border-color: #409EFF;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.12);
}

.dark .main-content .add-button {
  background-color: #333a47;
  color: #f1f5f9;
}

.dark .main-content .add-button:hover {
  background-color: #475569;
  color: #ffffff;
}

.dark .main-content .message-input::placeholder {
  color: #94a3b8;
}

.dark .main-content .send-button {
  color: #409EFF;
}

.dark .main-content .send-button:hover:not(:disabled) {
  color: #66b1ff;
}

.dark .main-content .send-button:disabled {
  color: #64748b !important;
}

/* 右侧侧边栏深色主题 */
.dark .right-sidebar {
  background-color: #0f172a;
}

.dark .right-sidebar .memory-logs {
  border-bottom: 1px solid #333a47;
}

.dark .right-sidebar .memory-logs::-webkit-scrollbar-track {
  background: #1e293b;
}

.dark .right-sidebar .memory-logs::-webkit-scrollbar-thumb {
  background: #333a47;
}

.dark .right-sidebar .memory-logs::-webkit-scrollbar-thumb:hover {
  background: #475569;
}

.dark .right-sidebar .section-header h3 {
  color: #f1f5f9;
}

.dark .right-sidebar .log-item {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

.dark .right-sidebar .log-time {
  color: #94a3b8;
}

.dark .right-sidebar .log-content {
  color: #f1f5f9;
}

.dark .right-sidebar .link-button {
  color: #409EFF;
}

.dark .right-sidebar .link-button:hover {
  color: #66b1ff;
}

.dark .right-sidebar .graph-container {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

/* Element Plus 组件深色主题 */
.dark {
  --el-color-primary: #409EFF;
  --el-color-success: #10b981;
  --el-color-warning: #f59e0b;
  --el-color-danger: #ef4444;
  --el-color-info: #409EFF;
  --el-bg-color: #0f172a;
  --el-bg-color-page: #0f172a;
  --el-bg-color-overlay: #1e293b;
  --el-text-color-primary: #f1f5f9;
  --el-text-color-regular: #e2e8f0;
  --el-text-color-secondary: #94a3b8;
  --el-text-color-placeholder: #64748b;
  --el-border-color: #333a47;
  --el-border-color-light: #333a47;
  --el-border-color-lighter: #333a47;
  --el-border-color-extra-light: #333a47;
  --el-fill-color: #1e293b;
  --el-fill-color-light: #333a47;
  --el-fill-color-lighter: #333a47;
  --el-fill-color-extra-light: #333a47;
  --el-box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  --el-box-shadow-light: 0 2px 4px rgba(0, 0, 0, 0.1);
  --el-box-shadow-lighter: 0 2px 4px rgba(0, 0, 0, 0.05);
  --el-box-shadow-dark: 0 4px 12px rgba(0, 0, 0, 0.25);
}
</style>