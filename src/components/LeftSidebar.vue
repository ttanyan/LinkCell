<template>
  <div class="left-sidebar">
    <div class="search-container">
      <el-input
        v-model="searchQuery"
        placeholder="Search..."
        class="search-input"
      />
    </div>
    

    
    <!-- 文档上传区域 -->
    <div 
      class="upload-area"
      @drop="handleDrop"
      @dragover.prevent
      @dragenter.prevent
      @click="triggerFileInput"
    >
      <input 
        type="file" 
        ref="fileInput" 
        style="display: none" 
        @change="handleFileSelect"
        multiple
        accept=".pdf"
      />
      <el-icon class="upload-icon"><Upload /></el-icon>
      <p>拖拽文件到此处或点击上传</p>
      <el-progress v-if="uploadProgress > 0" :percentage="uploadProgress" :format="() => ''" />
    </div>
    
    <!-- 已选文档显示 -->
    <div v-if="selectedDocuments.length > 0" class="selected-docs">
      <div class="selected-header">
        <span>{{ selectedDocuments.length }} 个文档已选择</span>
        <el-button type="text" size="small" @click="clearSelection">清除选择</el-button>
      </div>
    </div>
    
    <div class="cell-list">
      <!-- 文档列表 -->
      <div
        v-for="doc in documents"
        :key="doc.id"
        class="cell-item document-item"
        :class="{ active: selectedDocuments.includes(doc.id) }"
        @click="toggleDocumentSelection(doc.id)"
      >
        <div class="cell-icon">
          <el-icon><Document /></el-icon>
        </div>
        <div class="cell-info">
          <div class="cell-title">{{ doc.name }}</div>
          <div class="cell-meta">
            <span class="cell-date">{{ formatDate(doc.upload_time) }}</span>
            <el-tag :type="getStatusType(doc.status)" size="small">{{ doc.status }}</el-tag>
          </div>
        </div>
        <div class="cell-actions">
          <el-button type="text" size="small" @click.stop="reindexDocument(doc.id)">
            <el-icon><Refresh /></el-icon>
          </el-button>
          <el-button type="text" size="small" @click.stop="deleteDocument(doc.id)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
      
      <!-- 静态文件列表 -->
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Folder, Document, Upload, Refresh, Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const searchQuery = ref('')
const activeIndex = ref(1)
const fileInput = ref(null)
const documents = ref([])
const selectedDocuments = ref([])
const uploadProgress = ref(0)

const cellItems = [
  {
    title: 'Project Alpha Docs.pdf',
    date: 'May 30, 2023',
    cells: 12,
    type: 'folder'
  },
  {
    title: 'Tech Stack Notes.pdf',
    date: 'May 30, 2023',
    cells: 12,
    type: 'document'
  },
  {
    title: 'Project Alpha Docs.pdf',
    date: 'May 30, 2023',
    cells: 12,
    type: 'folder'
  },
  {
    title: 'Worstants.pdf',
    date: 'May 11, 2023',
    cells: 12,
    type: 'document'
  },
  {
    title: 'Tech Stack Notes.pdf',
    date: '2023-03-23',
    cells: 12,
    type: 'document'
  },
  {
    title: 'Vimroservices.pdf',
    date: '2022-05-23',
    cells: 12,
    type: 'folder'
  },
  {
    title: 'Asianh Notes.pdf',
    date: '2022-03-25',
    cells: 12,
    type: 'document'
  },
  {
    title: 'Project Beta Docs.pdf',
    date: '2023-06-15',
    cells: 8,
    type: 'folder'
  },
  {
    title: 'Design System.pdf',
    date: '2023-07-20',
    cells: 15,
    type: 'document'
  },
  {
    title: 'API Documentation.pdf',
    date: '2023-08-10',
    cells: 20,
    type: 'document'
  },
  {
    title: 'User Stories.pdf',
    date: '2023-09-05',
    cells: 12,
    type: 'folder'
  },
  {
    title: 'Test Cases.pdf',
    date: '2023-10-12',
    cells: 18,
    type: 'document'
  }
]

onMounted(() => {
  loadDocuments()
})

const loadDocuments = async () => {
  try {
    const response = await fetch('/api/documents')
    const data = await response.json()
    documents.value = data
  } catch (error) {
    console.error('加载文档失败:', error)
    ElMessage.error('加载文档失败')
  }
}

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = async (event) => {
  const files = event.target.files
  await uploadFiles(files)
}

const handleDrop = async (event) => {
  event.preventDefault()
  const files = event.dataTransfer.files
  await uploadFiles(files)
}

const uploadFiles = async (files) => {
  for (const file of files) {
    // 验证文件类型
    if (!file.name.endsWith('.pdf')) {
      ElMessage.error('仅支持PDF文件')
      continue
    }
    
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      uploadProgress.value = 0
      const response = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData
      })
      
      if (response.ok) {
        ElMessage.success('文件上传成功')
        loadDocuments()
      } else {
        const error = await response.json()
        ElMessage.error(`上传失败: ${error.error}`)
      }
    } catch (error) {
      console.error('上传失败:', error)
      ElMessage.error('上传失败')
    } finally {
      uploadProgress.value = 0
    }
  }
}

const toggleDocumentSelection = (docId) => {
  const index = selectedDocuments.value.indexOf(docId)
  if (index > -1) {
    selectedDocuments.value.splice(index, 1)
  } else {
    selectedDocuments.value.push(docId)
  }
}

const clearSelection = () => {
  selectedDocuments.value = []
}

const deleteDocument = async (docId) => {
  try {
    const response = await fetch(`/api/documents/${docId}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      ElMessage.success('文档删除成功')
      loadDocuments()
      // 从选择中移除
      const index = selectedDocuments.value.indexOf(docId)
      if (index > -1) {
        selectedDocuments.value.splice(index, 1)
      }
    } else {
      ElMessage.error('删除失败')
    }
  } catch (error) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败')
  }
}

const reindexDocument = async (docId) => {
  try {
    const response = await fetch(`/api/documents/${docId}/reindex`, {
      method: 'POST'
    })
    
    if (response.ok) {
      ElMessage.success('重新索引成功')
      loadDocuments()
    } else {
      ElMessage.error('重新索引失败')
    }
  } catch (error) {
    console.error('重新索引失败:', error)
    ElMessage.error('重新索引失败')
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

const getStatusType = (status) => {
  switch (status) {
    case 'COMPLETED':
      return 'success'
    case 'INDEXING':
      return 'warning'
    case 'FAILED':
      return 'danger'
    default:
      return 'info'
  }
}
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

.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.upload-area:hover {
  border-color: #409EFF;
  background-color: #ecf5ff;
}

.upload-icon {
  font-size: 32px;
  color: #409EFF;
  margin-bottom: 10px;
}

.upload-area p {
  margin: 0;
  color: #6b7280;
  font-size: 14px;
}

.selected-docs {
  margin-bottom: 16px;
  padding: 12px;
  background-color: #ecf5ff;
  border-radius: 4px;
  border: 1px solid #d9ecff;
}

.selected-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  color: #1f2937;
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

.document-item {
  position: relative;
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
  align-items: center;
  transition: color 0.3s ease;
}

.cell-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}

.cell-item:hover .cell-actions {
  opacity: 1;
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

:deep(.dark .upload-area) {
  border-color: #374151;
  background-color: #1f2937;
}

:deep(.dark .upload-area:hover) {
  border-color: #60a5fa;
  background-color: #1e3a8a;
}

:deep(.dark .upload-area p) {
  color: #9ca3af;
}

:deep(.dark .selected-docs) {
  background-color: #1e3a8a;
  border-color: #3b82f6;
}

:deep(.dark .selected-header) {
  color: #f3f4f6;
}
</style>