<template>
  <div class="left-sidebar">
    <div class="search-container">
      <el-input
        v-model="searchQuery"
        placeholder="Search..."
        class="search-input"
      />
    </div>
    <div class="cell-list">
      <div
        v-for="(item, index) in cellItems"
        :key="index"
        class="cell-item"
        :class="{ active: activeIndex === index }"
        @click="activeIndex = index"
      >
        <div class="cell-icon">
          <el-icon v-if="item.type === 'folder'"><Folder /></el-icon>
          <el-icon v-else><Document /></el-icon>
        </div>
        <div class="cell-info">
          <div class="cell-title">{{ item.title }}</div>
          <div class="cell-meta">
            <span class="cell-date">{{ item.date }}</span>
            <span class="cell-count">{{ item.cells }} cells</span>
          </div>
        </div>
      </div>
    </div>
    <div class="add-cell-btn">
      <el-button type="primary" class="full-width">Add Cell</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Folder, Document } from '@element-plus/icons-vue'

const searchQuery = ref('')
const activeIndex = ref(1)

const cellItems = [
  {
    title: 'Project Alpha Docs',
    date: 'May 30, 2023',
    cells: 12,
    type: 'folder'
  },
  {
    title: 'Tech Stack Notes',
    date: 'May 30, 2023',
    cells: 12,
    type: 'document'
  },
  {
    title: 'Project Alpha Docs',
    date: 'May 30, 2023',
    cells: 12,
    type: 'folder'
  },
  {
    title: 'Worstants',
    date: 'May 11, 2023',
    cells: 12,
    type: 'document'
  },
  {
    title: 'Tech Stack Notes',
    date: '2023-03-23',
    cells: 12,
    type: 'document'
  },
  {
    title: 'Vimroservices',
    date: '2022-05-23',
    cells: 12,
    type: 'folder'
  },
  {
    title: 'Asianh Notes',
    date: '2022-03-25',
    cells: 12,
    type: 'document'
  },
  {
    title: 'Project Beta Docs',
    date: '2023-06-15',
    cells: 8,
    type: 'folder'
  },
  {
    title: 'Design System',
    date: '2023-07-20',
    cells: 15,
    type: 'document'
  },
  {
    title: 'API Documentation',
    date: '2023-08-10',
    cells: 20,
    type: 'document'
  },
  {
    title: 'User Stories',
    date: '2023-09-05',
    cells: 12,
    type: 'folder'
  },
  {
    title: 'Test Cases',
    date: '2023-10-12',
    cells: 18,
    type: 'document'
  }
]
</script>

<style scoped>
.left-sidebar {
  width: 25%;
  height: 100%;
  background-color: #f8f9fa;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.search-container {
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
}

.cell-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 16px;
  padding-right: 8px;
}

.cell-list::-webkit-scrollbar {
  width: 6px;
}

.cell-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.cell-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.cell-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.cell-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 8px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cell-item:hover {
  background-color: #e9ecef;
}

.cell-item.active {
  background-color: #e3f2fd;
  border-left: 3px solid #409EFF;
}

.cell-icon {
  margin-right: 12px;
  color: #6b7280;
  transition: color 0.3s ease;
}

.cell-info {
  flex: 1;
}

.cell-title {
  font-size: 14px;
  font-weight: 500;
  color: #1f2937;
  margin-bottom: 4px;
  transition: color 0.3s ease;
}

.cell-meta {
  font-size: 12px;
  color: #6b7280;
  display: flex;
  justify-content: space-between;
  transition: color 0.3s ease;
}

.add-cell-btn {
  margin-top: auto;
  flex-shrink: 0;
}

.full-width {
  width: 100%;
}

/* 深色主题样式 */
:deep(.dark .left-sidebar) {
  background-color: #111827;
  border-right: 1px solid #374151;
}

:deep(.dark .left-sidebar .cell-list::-webkit-scrollbar-track) {
  background: #1f2937;
}

:deep(.dark .left-sidebar .cell-list::-webkit-scrollbar-thumb) {
  background: #4b5563;
}

:deep(.dark .left-sidebar .cell-list::-webkit-scrollbar-thumb:hover) {
  background: #6b7280;
}

:deep(.dark .left-sidebar .cell-item) {
  color: #f3f4f6;
}

:deep(.dark .left-sidebar .cell-item:hover) {
  background-color: #1f2937;
}

:deep(.dark .left-sidebar .cell-item.active) {
  background-color: #1e40af;
  border-left: 3px solid #60a5fa;
}

:deep(.dark .left-sidebar .cell-icon) {
  color: #9ca3af;
}

:deep(.dark .left-sidebar .cell-title) {
  color: #f3f4f6;
}

:deep(.dark .left-sidebar .cell-meta) {
  color: #9ca3af;
}
</style>