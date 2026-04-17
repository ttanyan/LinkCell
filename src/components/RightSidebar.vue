<template>
  <div class="right-sidebar">
    <MemosPanel />
    <MemoryGraphPanel />
  </div>
</template>

<script setup>
import MemosPanel from './MemosPanel.vue'
import MemoryGraphPanel from './MemoryGraphPanel.vue'
</script>

<style scoped>
.right-sidebar {
  width: 25%;
  height: 100%;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  overflow: hidden;
  transition: background-color 0.3s ease;
}

.memory-logs {
  height: 40%;
  border-bottom: 1px solid #e5e7eb;
  padding: 20px;
  overflow-y: auto;
  box-sizing: border-box;
  padding-right: 12px;
  transition: border-color 0.3s ease;
}

.memory-logs::-webkit-scrollbar {
  width: 6px;
}

.memory-logs::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.memory-logs::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.memory-logs::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.knowledge-graph {
  height: 60%;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 16px;
  font-weight: bold;
  margin: 0;
  color: #1f2937;
  transition: color 0.3s ease;
}

.graph-actions {
  display: flex;
  gap: 8px;
}

.logs-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.log-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
  background-color: #ffffff;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.log-time {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  transition: color 0.3s ease;
}

.log-content {
  font-size: 13px;
  color: #1f2937;
  flex: 1;
  transition: color 0.3s ease;
}

.link-button {
  align-self: flex-start;
  padding: 0;
  margin-top: 4px;
  color: #409EFF;
  transition: color 0.3s ease;
}

.graph-container {
  flex: 1;
  background-color: #ffffff;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

/* 深色主题样式 */
:deep(.dark .right-sidebar) {
  background-color: #0f172a;
}

:deep(.dark .right-sidebar .memory-logs) {
  border-bottom: 1px solid #333a47;
}

:deep(.dark .right-sidebar .memory-logs::-webkit-scrollbar-track) {
  background: #1e293b;
}

:deep(.dark .right-sidebar .memory-logs::-webkit-scrollbar-thumb) {
  background: #333a47;
}

:deep(.dark .right-sidebar .memory-logs::-webkit-scrollbar-thumb:hover) {
  background: #475569;
}

:deep(.dark .right-sidebar .section-header h3) {
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .log-item) {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

:deep(.dark .right-sidebar .log-time) {
  color: #94a3b8;
}

:deep(.dark .right-sidebar .log-content) {
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .link-button) {
  color: #409EFF;
}

:deep(.dark .right-sidebar .link-button:hover) {
  color: #66b1ff;
}

:deep(.dark .right-sidebar .graph-container) {
  background-color: #1e293b;
  border: 1px solid #333a47;
}
</style>