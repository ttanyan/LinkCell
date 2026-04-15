<template>
  <div class="app-container">
    <AppHeader @open-settings="showSettings = true" />
    <div class="main-container" v-if="!showSettings">
      <LeftSidebar />
      <MainContent />
      <RightSidebar />
    </div>
    <Settings v-else @close-settings="showSettings = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import LeftSidebar from './components/LeftSidebar.vue'
import MainContent from './components/MainContent.vue'
import RightSidebar from './components/RightSidebar.vue'
import Settings from './components/Settings.vue'

const showSettings = ref(false)
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
}
</style>

<style>
/* 确保所有元素都有平滑过渡 */
* {
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease, fill 0.3s ease, stroke 0.3s ease;
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
  border-right: 1px solid #374151;
}

.dark .main-content .conversation-title {
  color: #f3f4f6;
}

.dark .main-content .message-card {
  background-color: #1e293b;
  border: 1px solid #334155;
}

.dark .main-content .user-card {
  background-color: #334155;
  border: none;
}

.dark .main-content .ai-thinking span {
  color: #9ca3af;
}

.dark .main-content .progress-bar {
  background-color: #374151;
}

.dark .main-content .ai-content h3 {
  color: #f3f4f6;
}

.dark .main-content .ai-content h4 {
  color: #f3f4f6;
}

.dark .main-content .ai-content p {
  color: #f3f4f6;
}

.dark .main-content .ai-content li {
  color: #f3f4f6;
}

.dark .main-content .ai-graph {
  background-color: #1e293b;
  border: 1px solid #334155;
}

.dark .main-content .secondary-node {
  background-color: #1e293b;
}

.dark .main-content .message-input-container {
  border-top: 1px solid #374151;
  background-color: #0f172a;
}

.dark .main-content .input-wrapper {
  border: 1px solid #334155;
  background-color: #1e293b;
}

.dark .main-content .input-wrapper:focus-within {
  border-color: #60a5fa;
  box-shadow: 0 2px 12px rgba(96, 165, 250, 0.12);
}

.dark .main-content .add-button {
  background-color: #334155;
  color: #f3f4f6;
}

.dark .main-content .add-button:hover {
  background-color: #475569;
  color: #ffffff;
}

.dark .main-content .message-input::placeholder {
  color: #6b7280;
}

.dark .main-content .send-button {
  color: #60a5fa;
}

.dark .main-content .send-button:hover:not(:disabled) {
  color: #93c5fd;
}

.dark .main-content .send-button:disabled {
  color: #64748b !important;
}

/* 右侧侧边栏深色主题 */
.dark .right-sidebar {
  background-color: #111827;
}

.dark .right-sidebar .memory-logs {
  border-bottom: 1px solid #374151;
}

.dark .right-sidebar .memory-logs::-webkit-scrollbar-track {
  background: #1f2937;
}

.dark .right-sidebar .memory-logs::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.dark .right-sidebar .memory-logs::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

.dark .right-sidebar .section-header h3 {
  color: #f3f4f6;
}

.dark .right-sidebar .log-item {
  background-color: #1e293b;
  border: 1px solid #334155;
}

.dark .right-sidebar .log-time {
  color: #9ca3af;
}

.dark .right-sidebar .log-content {
  color: #f3f4f6;
}

.dark .right-sidebar .link-button {
  color: #60a5fa;
}

.dark .right-sidebar .graph-container {
  background-color: #1e293b;
  border: 1px solid #334155;
}

/* Element Plus 组件深色主题 */
.dark {
  --el-color-primary: #60a5fa;
  --el-color-success: #34d399;
  --el-color-warning: #fbbf24;
  --el-color-danger: #f87171;
  --el-color-info: #60a5fa;
  --el-bg-color: #111827;
  --el-bg-color-page: #111827;
  --el-bg-color-overlay: #1f2937;
  --el-text-color-primary: #f3f4f6;
  --el-text-color-regular: #d1d5db;
  --el-text-color-secondary: #9ca3af;
  --el-text-color-placeholder: #6b7280;
  --el-border-color: #374151;
  --el-border-color-light: #374151;
  --el-border-color-lighter: #374151;
  --el-border-color-extra-light: #374151;
  --el-fill-color: #1f2937;
  --el-fill-color-light: #374151;
  --el-fill-color-lighter: #374151;
  --el-fill-color-extra-light: #374151;
  --el-box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
  --el-box-shadow-light: 0 1px 4px rgba(0, 0, 0, 0.3);
  --el-box-shadow-lighter: 0 1px 4px rgba(0, 0, 0, 0.3);
  --el-box-shadow-dark: 0 1px 4px rgba(0, 0, 0, 0.5);
}
</style>