<template>
  <div class="memos-panel">
    <div class="panel-header" @click="toggleCollapse">
      <h3>我的记忆</h3>
      <span class="collapse-icon">{{ isCollapsed ? '▼' : '▲' }}</span>
    </div>
    
    <div v-if="!isCollapsed" class="panel-content">
      <!-- 搜索框 -->
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索记忆..."
          class="search-input"
          @input="handleSearch"
        />
      </div>
      
      <!-- 记忆列表 -->
      <div class="memories-list">
        <div 
          v-for="memory in filteredMemories" 
          :key="memory.id"
          class="memory-item"
        >
          <div class="memory-content">
            <p>{{ memory.content }}</p>
            <div class="memory-meta">
              <span class="memory-date">{{ formatDate(memory.created_at || memory.updated_at) }}</span>
              <div class="memory-actions">
                <button class="action-button edit" @click="editMemory(memory)">编辑</button>
                <button class="action-button delete" @click="deleteMemory(memory.id)">删除</button>
              </div>
            </div>
          </div>
        </div>
        <div v-if="filteredMemories.length === 0" class="empty-state">
          <p>暂无记忆</p>
        </div>
      </div>
      
      <!-- 添加记忆按钮 -->
      <div class="add-memory-container">
        <button class="add-memory-button" @click="showAddMemory = true">
          + 添加记忆
        </button>
      </div>
    </div>
    
    <!-- 添加/编辑记忆对话框 -->
    <div v-if="showAddMemory || editingMemory" class="memory-dialog-overlay" @click="closeDialog">
      <div class="memory-dialog" @click.stop>
        <h4>{{ editingMemory ? '编辑记忆' : '添加记忆' }}</h4>
        <textarea 
          v-model="memoryContent" 
          placeholder="输入记忆内容..."
          class="memory-textarea"
          rows="4"
        ></textarea>
        <div class="dialog-actions">
          <button class="cancel-button" @click="closeDialog">取消</button>
          <button class="save-button" @click="saveMemory">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

// 状态管理
const isCollapsed = ref(false)
const searchQuery = ref('')
const memories = ref([])
const showAddMemory = ref(false)
const editingMemory = ref(null)
const memoryContent = ref('')

// 计算属性：过滤后的记忆列表
const filteredMemories = computed(() => {
  if (!searchQuery.value) return memories.value
  return memories.value.filter(memory => 
    memory.content.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 方法：切换折叠状态
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

// 方法：格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 方法：加载记忆列表
const loadMemories = async () => {
  try {
    const response = await fetch('/api/memos/list')
    const data = await response.json()
    if (data.status === 'success') {
      memories.value = data.memories
    }
  } catch (error) {
    console.error('加载记忆失败:', error)
  }
}

// 方法：搜索记忆
const handleSearch = () => {
  // 实时搜索已通过计算属性实现
}

// 方法：添加记忆
const saveMemory = async () => {
  try {
    const url = editingMemory.value ? `/api/memos/update/${editingMemory.value.id}` : '/api/memos/create'
    const method = editingMemory.value ? 'PUT' : 'POST'
    
    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: memoryContent.value
      })
    })
    
    const data = await response.json()
    if (data.status === 'success') {
      await loadMemories()
      closeDialog()
    }
  } catch (error) {
    console.error('保存记忆失败:', error)
  }
}

// 方法：编辑记忆
const editMemory = (memory) => {
  editingMemory.value = memory
  memoryContent.value = memory.content
  showAddMemory.value = true
}

// 方法：删除记忆
const deleteMemory = async (memoryId) => {
  if (confirm('确定要删除这条记忆吗？')) {
    try {
      const response = await fetch(`/api/memos/delete/${memoryId}`, {
        method: 'DELETE'
      })
      
      const data = await response.json()
      if (data.status === 'success') {
        await loadMemories()
      }
    } catch (error) {
      console.error('删除记忆失败:', error)
    }
  }
}

// 方法：关闭对话框
const closeDialog = () => {
  showAddMemory.value = false
  editingMemory.value = null
  memoryContent.value = ''
}

// 生命周期：组件挂载时加载记忆
onMounted(() => {
  loadMemories()
})
</script>

<style scoped>
.memos-panel {
  background-color: #f5f7fa;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  cursor: pointer;
  background-color: #ffffff;
  border-radius: 8px 8px 0 0;
  border-bottom: 1px solid #e4e7ed;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.collapse-icon {
  font-size: 12px;
  color: #909399;
  transition: transform 0.3s ease;
}

.panel-content {
  padding: 16px;
  background-color: #ffffff;
  border-radius: 0 0 8px 8px;
}

.search-container {
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.memories-list {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 16px;
}

.memory-item {
  padding: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  margin-bottom: 12px;
  background-color: #f9f9f9;
  transition: all 0.3s ease;
}

.memory-item:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
}

.memory-content p {
  margin: 0 0 8px 0;
  font-size: 14px;
  line-height: 1.5;
  color: #303133;
}

.memory-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #909399;
}

.memory-actions {
  display: flex;
  gap: 8px;
}

.action-button {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-button.edit {
  background-color: #ecf5ff;
  color: #409EFF;
}

.action-button.edit:hover {
  background-color: #d9ecff;
}

.action-button.delete {
  background-color: #fef0f0;
  color: #f56c6c;
}

.action-button.delete:hover {
  background-color: #fde2e2;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #909399;
  font-size: 14px;
}

.add-memory-container {
  text-align: center;
}

.add-memory-button {
  width: 100%;
  padding: 10px;
  background-color: #409EFF;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.add-memory-button:hover {
  background-color: #66b1ff;
}

.memory-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.memory-dialog {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.memory-dialog h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.memory-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
  margin-bottom: 16px;
  transition: border-color 0.3s ease;
}

.memory-textarea:focus {
  outline: none;
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.cancel-button, .save-button {
  padding: 8px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-button {
  background-color: #ffffff;
  color: #606266;
}

.cancel-button:hover {
  border-color: #c0c4cc;
  color: #303133;
}

.save-button {
  background-color: #409EFF;
  color: #ffffff;
  border-color: #409EFF;
}

.save-button:hover {
  background-color: #66b1ff;
  border-color: #66b1ff;
}

/* 深色主题适配 */
.dark .memos-panel {
  background-color: #1e293b;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.3);
}

.dark .panel-header {
  background-color: #334155;
  border-bottom: 1px solid #475569;
}

.dark .panel-header h3 {
  color: #f1f5f9;
}

.dark .collapse-icon {
  color: #94a3b8;
}

.dark .panel-content {
  background-color: #334155;
}

.dark .search-input {
  background-color: #1e293b;
  border-color: #475569;
  color: #f1f5f9;
}

.dark .search-input::placeholder {
  color: #64748b;
}

.dark .search-input:focus {
  border-color: #60a5fa;
  box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
}

.dark .memory-item {
  background-color: #1e293b;
  border-color: #475569;
}

.dark .memory-item:hover {
  border-color: #60a5fa;
}

.dark .memory-content p {
  color: #f1f5f9;
}

.dark .memory-meta {
  color: #94a3b8;
}

.dark .action-button.edit {
  background-color: #1e3a8a;
  color: #60a5fa;
}

.dark .action-button.edit:hover {
  background-color: #334155;
}

.dark .action-button.delete {
  background-color: #7f1d1d;
  color: #fca5a5;
}

.dark .action-button.delete:hover {
  background-color: #991b1b;
}

.dark .empty-state {
  color: #94a3b8;
}

.dark .add-memory-button {
  background-color: #1e40af;
}

.dark .add-memory-button:hover {
  background-color: #3b82f6;
}

.dark .memory-dialog {
  background-color: #334155;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.dark .memory-dialog h4 {
  color: #f1f5f9;
}

.dark .memory-textarea {
  background-color: #1e293b;
  border-color: #475569;
  color: #f1f5f9;
}

.dark .memory-textarea::placeholder {
  color: #64748b;
}

.dark .memory-textarea:focus {
  border-color: #60a5fa;
  box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
}

.dark .cancel-button {
  background-color: #334155;
  color: #94a3b8;
  border-color: #475569;
}

.dark .cancel-button:hover {
  border-color: #64748b;
  color: #f1f5f9;
}

.dark .save-button {
  background-color: #1e40af;
  border-color: #1e40af;
}

.dark .save-button:hover {
  background-color: #3b82f6;
  border-color: #3b82f6;
}
</style>
