<template>
  <div class="right-sidebar">
    <div class="memory-logs">
      <div class="section-header">
        <h3>我的记忆</h3>
      </div>
      
      <!-- 搜索框 -->
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索记忆..." 
          class="search-input"
          @input="searchMemories"
        />
      </div>
      
      <!-- 记忆列表 -->
      <div class="memories-list">
        <div 
          v-for="memory in filteredMemories" 
          :key="memory.id" 
          class="memory-item"
          :class="{ 'expanded': expandedMemoryId === memory.id }"
        >
          <div class="memory-content" @click="toggleMemoryExpand(memory.id)">
            <p>{{ memory.content }}</p>
            <span class="memory-date">{{ formatDate(memory.created_at) }}</span>
          </div>
          
          <!-- 展开的详情和操作按钮 -->
          <div class="memory-actions" v-if="expandedMemoryId === memory.id">
            <button class="action-button edit-button" @click.stop="editMemory(memory)">编辑</button>
            <button class="action-button delete-button" @click.stop="deleteMemory(memory.id)">删除</button>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div class="empty-state" v-if="filteredMemories.length === 0">
          <p>暂无记忆</p>
          <p class="empty-hint">开始添加您的记忆吧</p>
        </div>
      </div>
      
      <!-- 添加记忆输入框 -->
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
    </div>
    
    <div class="knowledge-graph">
      <div class="section-header">
        <h3>记忆图谱</h3>
        <div class="graph-actions">
          <el-button type="text" icon="Refresh" size="small" @click="resetGraph" />
          <el-button type="text" icon="ZoomIn" size="small" @click="zoomIn" />
          <el-button type="text" icon="ZoomOut" size="small" @click="zoomOut" />
        </div>
      </div>
      <div ref="graphContainer" class="graph-container"></div>
    </div>
    
    <!-- 编辑记忆对话框 -->
    <div class="edit-modal" v-if="showEditModal">
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
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { Refresh, ZoomIn, ZoomOut } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 记忆管理状态
const memories = ref([])
const searchQuery = ref('')
const newMemoryContent = ref('')
const expandedMemoryId = ref(null)
const showEditModal = ref(false)
const editingMemory = ref({ id: '', content: '' })

// 图谱状态
const graphContainer = ref(null)
let chart = null

// 计算过滤后的记忆
const filteredMemories = computed(() => {
  if (!searchQuery.value) return memories.value
  return memories.value.filter(memory => 
    memory.content.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

// 加载记忆
const loadMemories = async () => {
  try {
    const response = await fetch('/api/memos/list')
    if (response.ok) {
      const data = await response.json()
      memories.value = data.memories || []
    } else {
      console.error('Failed to load memories:', response.status)
      // 模拟数据，用于测试
      memories.value = [
        { id: 1, content: '我喜欢打球', created_at: new Date().toISOString() },
        { id: 2, content: '我爱吃蔬菜', created_at: new Date().toISOString() },
        { id: 3, content: '最近肠胃不舒服', created_at: new Date().toISOString() }
      ]
    }
  } catch (error) {
    console.error('Failed to load memories:', error)
    // 模拟数据，用于测试
    memories.value = [
      { id: 1, content: '我喜欢打球', created_at: new Date().toISOString() },
      { id: 2, content: '我爱吃蔬菜', created_at: new Date().toISOString() },
      { id: 3, content: '最近肠胃不舒服', created_at: new Date().toISOString() }
    ]
  }
}

// 搜索记忆
const searchMemories = () => {
  // 搜索逻辑由 computed 自动处理
}

// 切换记忆展开状态
const toggleMemoryExpand = (memoryId) => {
  expandedMemoryId.value = expandedMemoryId.value === memoryId ? null : memoryId
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
        if (expandedMemoryId.value === memoryId) {
          expandedMemoryId.value = null
        }
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

// 图谱相关函数
const loadGraphData = async () => {
  try {
    const response = await fetch('/api/memos/graph')
    if (response.ok) {
      const data = await response.json()
      updateChart(data.nodes || [], data.edges || [])
    } else {
      console.error('Failed to load graph data:', response.status)
      // 模拟数据，用于测试
      const mockNodes = [
        { id: 1, label: '我喜欢打球', size: 30, color: '#409EFF' },
        { id: 2, label: '我爱吃蔬菜', size: 25, color: '#10b981' },
        { id: 3, label: '最近肠胃不舒服', size: 20, color: '#f59e0b' }
      ]
      const mockEdges = [
        { source: 1, target: 2 },
        { source: 2, target: 3 }
      ]
      updateChart(mockNodes, mockEdges)
    }
  } catch (error) {
    console.error('Failed to load graph data:', error)
    // 模拟数据，用于测试
    const mockNodes = [
      { id: 1, label: '我喜欢打球', size: 30, color: '#409EFF' },
      { id: 2, label: '我爱吃蔬菜', size: 25, color: '#10b981' },
      { id: 3, label: '最近肠胃不舒服', size: 20, color: '#f59e0b' }
    ]
    const mockEdges = [
      { source: 1, target: 2 },
      { source: 2, target: 3 }
    ]
    updateChart(mockNodes, mockEdges)
  }
}

const resetGraph = () => {
  loadGraphData()
}

const zoomIn = () => {
  if (chart) {
    chart.dispatchAction({
      type: 'dataZoom',
      start: 0,
      end: 50
    })
  }
}

const zoomOut = () => {
  if (chart) {
    chart.dispatchAction({
      type: 'dataZoom',
      start: 0,
      end: 100
    })
  }
}

const updateChart = (nodes, edges) => {
  if (!chart) return

  // 检查是否为暗黑模式
  const isDarkMode = document.documentElement.classList.contains('dark')

  // 转换节点数据
  const chartNodes = nodes.map(node => ({
    id: node.id,
    name: node.label || node.content.substring(0, 20) + '...',
    symbolSize: node.size || 30,
    itemStyle: {
      color: node.color || (isDarkMode ? '#409EFF' : '#3b82f6')
    },
    label: {
      color: isDarkMode ? '#ffffff' : '#000000'
    },
    data: node
  }))

  // 转换边数据
  const chartEdges = edges.map(edge => ({
    source: edge.source,
    target: edge.target,
    lineStyle: {
      opacity: 0.6,
      width: 2,
      curveness: 0.1
    }
  }))

  const option = {
    tooltip: {
      backgroundColor: isDarkMode ? '#1e293b' : '#ffffff',
      borderColor: isDarkMode ? '#333a47' : '#e5e7eb',
      textStyle: {
        color: isDarkMode ? '#ffffff' : '#1f2937'
      },
      formatter: function(params) {
        if (params.dataType === 'node') {
          return params.data.data.content || params.name
        }
        return ''
      }
    },
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: chartNodes,
        links: chartEdges,
        roam: true,
        label: {
          show: true,
          fontSize: 12,
          overflow: 'truncate'
        },
        lineStyle: {
          opacity: 0.6,
          width: 2,
          curveness: 0.1,
          color: isDarkMode ? '#64748b' : '#6b7280'
        },
        force: {
          repulsion: 1000,
          edgeLength: [80, 120]
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 4
          }
        }
      }
    ]
  }

  chart.setOption(option)
}

const handleResize = () => {
  if (chart) {
    chart.resize()
  }
}

// 检查深色模式
const checkDarkMode = () => {
  return document.documentElement.classList.contains('dark')
}

// 监听深色模式变化
const observer = new MutationObserver(() => {
  if (chart) {
    loadGraphData()
  }
})

onMounted(() => {
  // 加载记忆
  loadMemories()
  
  // 初始化图谱
  if (graphContainer.value) {
    chart = echarts.init(graphContainer.value)
    loadGraphData()
    window.addEventListener('resize', handleResize)
  }
  
  // 监听主题变化
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
})

onUnmounted(() => {
  if (chart) {
    chart.dispose()
  }
  window.removeEventListener('resize', handleResize)
  observer.disconnect()
})

// 定时刷新记忆列表
setInterval(loadMemories, 30000) // 每30秒刷新一次
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
  display: flex;
  flex-direction: column;
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

/* 搜索框样式 */
.search-container {
  margin-bottom: 16px;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
}

.search-input:focus {
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

/* 记忆列表样式 */
.memories-list {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.memory-item {
  padding: 12px;
  background-color: #ffffff;
  border-radius: 6px;
  border: 1px solid #e5e7eb;
  transition: all 0.2s ease;
  cursor: pointer;
}

.memory-item:hover {
  background-color: #f0f0f0;
}

.memory-item.expanded {
  border-color: #409EFF;
}

.memory-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.memory-content p {
  margin: 0;
  font-size: 14px;
  color: #333;
  line-height: 1.4;
}

.memory-date {
  font-size: 12px;
  color: #999;
}

.memory-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #e0e0e0;
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

.edit-button:hover {
  background-color: #e0e0e0;
}

.delete-button {
  background-color: #fff1f0;
  color: #ff4d4f;
}

.delete-button:hover {
  background-color: #ffccc7;
}

/* 添加记忆样式 */
.add-memory {
  display: flex;
  gap: 8px;
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #e0e0e0;
}

.add-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s ease;
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

/* 空状态样式 */
.empty-state {
  padding: 40px 20px;
  text-align: center;
  color: #999;
}

.empty-hint {
  font-size: 12px;
  margin-top: 8px;
}

/* 图谱样式 */
.graph-container {
  flex: 1;
  background-color: #ffffff;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

/* 编辑模态框样式 */
.edit-modal {
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

.modal-content h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.edit-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  margin-bottom: 16px;
  transition: all 0.2s ease;
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

.cancel-button:hover {
  background-color: #e0e0e0;
}

.save-button {
  background-color: #409EFF;
  color: white;
}

.save-button:hover {
  background-color: #66b1ff;
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

:deep(.dark .right-sidebar .memory-item) {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

:deep(.dark .right-sidebar .memory-item:hover) {
  background-color: #333a47;
}

:deep(.dark .right-sidebar .memory-content p) {
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .memory-date) {
  color: #94a3b8;
}

:deep(.dark .right-sidebar .action-button.edit-button) {
  background-color: #333a47;
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .action-button.edit-button:hover) {
  background-color: #475569;
}

:deep(.dark .right-sidebar .action-button.delete-button) {
  background-color: #7f1d1d;
  color: #fca5a5;
}

:deep(.dark .right-sidebar .action-button.delete-button:hover) {
  background-color: #991b1b;
}

:deep(.dark .right-sidebar .search-input) {
  background-color: #333a47;
  border: 1px solid #475569;
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .search-input::placeholder) {
  color: #64748b;
}

:deep(.dark .right-sidebar .add-input) {
  background-color: #333a47;
  border: 1px solid #475569;
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .add-input::placeholder) {
  color: #64748b;
}

:deep(.dark .right-sidebar .empty-state) {
  color: #94a3b8;
}

:deep(.dark .right-sidebar .graph-container) {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

:deep(.dark .right-sidebar .modal-content) {
  background-color: #1e293b;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

:deep(.dark .right-sidebar .modal-content h4) {
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .edit-input) {
  background-color: #333a47;
  border: 1px solid #475569;
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .edit-input::placeholder) {
  color: #64748b;
}

:deep(.dark .right-sidebar .modal-button.cancel-button) {
  background-color: #475569;
  color: #f1f5f9;
}

:deep(.dark .right-sidebar .modal-button.cancel-button:hover) {
  background-color: #576574;
}
</style>