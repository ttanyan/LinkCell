<template>
  <div class="memory-panel" :class="{ 'dark': isDarkMode }">
    <div class="panel-header">
      <h3>我的记忆</h3>
      <button class="close-button" @click="isVisible = false">×</button>
    </div>
    
    <div class="search-container">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="搜索记忆..." 
        class="search-input"
        @input="searchMemories"
      />
    </div>
    
    <div class="memories-list" v-if="filteredMemories.length > 0">
      <div 
        v-for="memory in filteredMemories" 
        :key="memory.id" 
        class="memory-item"
      >
        <div class="memory-content">
          <p>{{ memory.content }}</p>
          <span class="memory-date">{{ formatDate(memory.created_at) }}</span>
        </div>
        <div class="memory-actions">
          <button class="action-button edit-button" @click="editMemory(memory)">编辑</button>
          <button class="action-button delete-button" @click="deleteMemory(memory.id)">删除</button>
        </div>
      </div>
    </div>
    
    <div class="empty-state" v-else>
      <p>暂无记忆</p>
      <p class="empty-hint">开始添加您的记忆吧</p>
    </div>
    
    <div class="add-memory">
      <input 
        type="text" 
        v-model="newMemoryContent" 
        placeholder="添加新记忆..." 
        class="add-input"
        @keyup.enter="addMemory"
      />
      <button class="add-button" @click="addMemory">+</button>
    </div>
    
    <!-- 编辑记忆对话框 -->
    <div class="modal" v-if="showEditModal">
      <div class="modal-content">
        <h4>编辑记忆</h4>
        <input 
          type="text" 
          v-model="editingMemory.content" 
          class="edit-input"
        />
        <div class="modal-actions">
          <button class="modal-button cancel-button" @click="showEditModal = false">取消</button>
          <button class="modal-button save-button" @click="saveEditMemory">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:isVisible'])

// 状态管理
const memories = ref([])
const searchQuery = ref('')
const newMemoryContent = ref('')
const showEditModal = ref(false)
const editingMemory = ref({ id: '', content: '' })
const isDarkMode = ref(false)

// 计算过滤后的记忆
const filteredMemories = computed(() => {
  if (!searchQuery.value) return memories.value
  return memories.value.filter(memory => 
    memory.content.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 检查深色模式
const checkDarkMode = () => {
  isDarkMode.value = document.documentElement.classList.contains('dark')
}

// 加载记忆
const loadMemories = async () => {
  try {
    const response = await fetch('/api/memos/list')
    if (response.ok) {
      const data = await response.json()
      memories.value = data.memories || []
    }
  } catch (error) {
    console.error('Failed to load memories:', error)
  }
}

// 搜索记忆
const searchMemories = () => {
  // 搜索逻辑由 computed 自动处理
}

// 添加记忆
const addMemory = async () => {
  if (!newMemoryContent.value.trim()) return
  
  try {
    const response = await fetch('/api/memos/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: newMemoryContent.value.trim(),
        metadata: {}
      })
    })
    
    if (response.ok) {
      newMemoryContent.value = ''
      await loadMemories()
    }
  } catch (error) {
    console.error('Failed to add memory:', error)
  }
}

// 编辑记忆
const editMemory = (memory) => {
  editingMemory.value = { ...memory }
  showEditModal.value = true
}

// 保存编辑
const saveEditMemory = async () => {
  try {
    const response = await fetch(`/api/memos/update/${editingMemory.value.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: editingMemory.value.content,
        metadata: {}
      })
    })
    
    if (response.ok) {
      showEditModal.value = false
      await loadMemories()
    }
  } catch (error) {
    console.error('Failed to update memory:', error)
  }
}

// 删除记忆
const deleteMemory = async (memoryId) => {
  if (confirm('确定要删除这条记忆吗？')) {
    try {
      const response = await fetch(`/api/memos/delete/${memoryId}`, {
        method: 'DELETE'
      })
      
      if (response.ok) {
        await loadMemories()
      }
    } catch (error) {
      console.error('Failed to delete memory:', error)
    }
  }
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleString()
}

// 监听可见性变化
watch(() => props.isVisible, (newValue) => {
  if (newValue) {
    loadMemories()
  }
})

// 监听深色模式变化
watch(isDarkMode, (newValue) => {
  // 深色模式变化时的处理
})

// 组件挂载时
onMounted(() => {
  checkDarkMode()
  if (props.isVisible) {
    loadMemories()
  }
  
  // 监听主题变化
  const observer = new MutationObserver(() => {
    checkDarkMode()
  })
  
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
})
</script>

<style scoped>
.memory-panel {
  position: fixed;
  top: 60px;
  right: 20px;
  width: 320px;
  max-height: 80vh;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dark.memory-panel {
  background-color: #1e293b;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.dark .panel-header {
  border-bottom: 1px solid #333a47;
}

.panel-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.dark .panel-header h3 {
  color: #f1f5f9;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
}

.dark .close-button {
  color: #94a3b8;
}

.close-button:hover {
  background-color: #f0f0f0;
}

.dark .close-button:hover {
  background-color: #333a47;
}

.search-container {
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
}

.dark .search-container {
  border-bottom: 1px solid #333a47;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
}

.dark .search-input {
  background-color: #333a47;
  border: 1px solid #475569;
  color: #f1f5f9;
}

.search-input:focus {
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.memories-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.memory-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px;
  margin-bottom: 8px;
  background-color: #f9f9f9;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.dark .memory-item {
  background-color: #333a47;
}

.memory-item:hover {
  background-color: #f0f0f0;
}

.dark .memory-item:hover {
  background-color: #475569;
}

.memory-content {
  flex: 1;
  margin-right: 12px;
}

.memory-content p {
  margin: 0 0 4px 0;
  font-size: 14px;
  color: #333;
  line-height: 1.4;
}

.dark .memory-content p {
  color: #f1f5f9;
}

.memory-date {
  font-size: 12px;
  color: #999;
}

.dark .memory-date {
  color: #94a3b8;
}

.memory-actions {
  display: flex;
  gap: 4px;
}

.action-button {
  padding: 4px 8px;
  font-size: 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.edit-button {
  background-color: #f0f0f0;
  color: #333;
}

.dark .edit-button {
  background-color: #475569;
  color: #f1f5f9;
}

.edit-button:hover {
  background-color: #e0e0e0;
}

.dark .edit-button:hover {
  background-color: #576574;
}

.delete-button {
  background-color: #fff1f0;
  color: #ff4d4f;
}

.dark .delete-button {
  background-color: #7f1d1d;
  color: #fca5a5;
}

.delete-button:hover {
  background-color: #ffccc7;
}

.dark .delete-button:hover {
  background-color: #991b1b;
}

.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: #999;
}

.dark .empty-state {
  color: #94a3b8;
}

.empty-hint {
  font-size: 12px;
  margin-top: 8px;
}

.add-memory {
  display: flex;
  padding: 12px 16px;
  border-top: 1px solid #e0e0e0;
  gap: 8px;
}

.dark .add-memory {
  border-top: 1px solid #333a47;
}

.add-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
}

.dark .add-input {
  background-color: #333a47;
  border: 1px solid #475569;
  color: #f1f5f9;
}

.add-input:focus {
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.add-button {
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 4px;
  background-color: #409EFF;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.add-button:hover {
  background-color: #66b1ff;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.dark .modal-content {
  background-color: #1e293b;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.modal-content h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.dark .modal-content h4 {
  color: #f1f5f9;
}

.edit-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  margin-bottom: 16px;
}

.dark .edit-input {
  background-color: #333a47;
  border: 1px solid #475569;
  color: #f1f5f9;
}

.edit-input:focus {
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.modal-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-button {
  background-color: #f0f0f0;
  color: #333;
}

.dark .cancel-button {
  background-color: #475569;
  color: #f1f5f9;
}

.cancel-button:hover {
  background-color: #e0e0e0;
}

.dark .cancel-button:hover {
  background-color: #576574;
}

.save-button {
  background-color: #409EFF;
  color: white;
}

.save-button:hover {
  background-color: #66b1ff;
}

/* 滚动条样式 */
.memories-list::-webkit-scrollbar {
  width: 6px;
}

.memories-list::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.dark .memories-list::-webkit-scrollbar-track {
  background: #333a47;
}

.memories-list::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.dark .memories-list::-webkit-scrollbar-thumb {
  background: #475569;
}

.memories-list::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

.dark .memories-list::-webkit-scrollbar-thumb:hover {
  background: #576574;
}
</style>