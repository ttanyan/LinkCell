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
            <!-- 显示 tags 标签 -->
            <div class="memory-tags" v-if="memory.tags && memory.tags.length > 0">
              <span v-for="(tag, index) in memory.tags" :key="index" class="tag">
                {{ tag }}{{ index < memory.tags.length - 1 ? ', ' : '' }}
              </span>
            </div>
            <span class="memory-date">{{ formatDate(memory.created_at) }}</span>
          </div>
          
          <!-- 展开的详情和操作按钮 -->
          <div class="memory-actions" v-if="expandedMemoryId === memory.id">
            <button class="action-button edit-button" @click.stop="editMemory(memory)">编辑</button>
            <button class="action-button delete-button" @click.stop="confirmDelete(memory.id)">删除</button>
          </div>
        </div>
        
        <!-- 空状态 -->
        <div class="empty-state" v-if="filteredMemories.length === 0">
          <p>暂无记忆</p>
        </div>
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
    
    <!-- 删除确认对话框 -->
    <el-dialog
      v-model="showDeleteDialog"
      title="删除记忆"
      width="30%"
    >
      <span>确定要删除这条记忆吗？</span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDeleteDialog = false">取消</el-button>
          <el-button type="danger" @click="confirmDeleteMemory">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { Refresh, ZoomIn, ZoomOut } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

// 记忆管理状态
const memories = ref([])
const searchQuery = ref('')
const expandedMemoryId = ref(null)
const showEditModal = ref(false)
const editingMemory = ref({ id: '', content: '' })
const showDeleteDialog = ref(false)
const memoryIdToDelete = ref(null)

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
const loadMemories = async (query = "") => {
  try {
    const response = await fetch(`/api/memos/list?query=${encodeURIComponent(query)}`)
    if (response.ok) {
      const data = await response.json()
      // 处理 search_memory 返回的结果结构
      const memoryData = data.memories || data
      const newMemories = []
      
      // 只处理 preference_detail_list，只展示 preference 字段
      if (memoryData.preference_detail_list && Array.isArray(memoryData.preference_detail_list)) {
        memoryData.preference_detail_list.forEach((item, index) => {
          if (item.preference) {
            newMemories.push({
              id: `preference_${index}`,
              content: item.preference, // 只显示 preference 字段，不显示 reasoning
              created_at: new Date().toISOString()
            })
          }
        })
      }
      
      memories.value = newMemories
    } else {
      console.error('Failed to load memories:', response.status)
      memories.value = []
    }
  } catch (error) {
    console.error('Failed to load memories:', error)
    memories.value = []
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

// 确认删除记忆
const confirmDelete = (memoryId) => {
  memoryIdToDelete.value = memoryId
  showDeleteDialog.value = true
}

// 执行删除记忆
const confirmDeleteMemory = async () => {
  if (!memoryIdToDelete.value) return
  
  try {
    // 直接从前端删除记忆
    const index = memories.value.findIndex(memory => memory.id === memoryIdToDelete.value)
    if (index !== -1) {
      memories.value.splice(index, 1)
      if (expandedMemoryId.value === memoryIdToDelete.value) {
        expandedMemoryId.value = null
      }
    }
    
    // 同时调用后端 API
    try {
      const response = await fetch(`/api/memos/delete/${memoryIdToDelete.value}`, {
        method: 'DELETE'
      })
      console.log('Delete memory response:', response.status)
    } catch (error) {
      console.error('Failed to delete memory from backend:', error)
    }
  } catch (error) {
    console.error('Failed to delete memory:', error)
  } finally {
    showDeleteDialog.value = false
    memoryIdToDelete.value = null
  }
}

// 删除记忆（保留原方法名，确保兼容性）
const deleteMemory = async (memoryId) => {
  confirmDelete(memoryId)
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
      updateChart([], [])
    }
  } catch (error) {
    console.error('Failed to load graph data:', error)
    updateChart([], [])
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
  // 初始化图谱
  if (graphContainer.value) {
    chart = echarts.init(graphContainer.value)
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

// 从对话数据中更新记忆
defineExpose({
  updateMemories: (memoryData) => {
    console.log('updateMemories called with:', memoryData)
    try {
      // 处理 search_memory 返回的结果
      const newMemories = []
      
      // 优先从根节点提取数据，兜底兼容data层级
      const memoryDetailList = memoryData.memory_detail_list || memoryData?.data?.memory_detail_list || []
      const preferenceDetailList = memoryData.preference_detail_list || memoryData?.data?.preference_detail_list || []
      
      console.log('Extracted memory_detail_list:', memoryDetailList)
      console.log('Extracted preference_detail_list:', preferenceDetailList)
      
      // 处理 memory_detail_list
      if (Array.isArray(memoryDetailList)) {
        console.log('Processing memory_detail_list:', memoryDetailList)
        memoryDetailList.forEach((item, index) => {
          if (item.memory_value || item.memory_key) {
            newMemories.push({
              id: item.id || `memory_${index}`,
              content: item.memory_value || item.memory_key, // 优先使用memory_value，兜底使用memory_key
              tags: item.tags || [],
              created_at: item.create_time ? new Date(item.create_time).toISOString() : new Date().toISOString(),
              relativity: item.relativity || 0.5
            })
          }
        })
      }
      
      // 处理 preference_detail_list
      if (Array.isArray(preferenceDetailList)) {
        console.log('Processing preference_detail_list:', preferenceDetailList)
        preferenceDetailList.forEach((item, index) => {
          if (item.preference) {
            newMemories.push({
              id: item.id || `preference_${index}`,
              content: item.preference,
              created_at: item.create_time ? new Date(item.create_time).toISOString() : new Date().toISOString(),
              relativity: item.relativity || 0.5
            })
          }
        })
      }
      
      console.log('New memories:', newMemories)
      if (newMemories.length > 0) {
        memories.value = newMemories
        console.log('Memories updated:', memories.value)
      } else {
        console.log('No memories found to update')
      }
      
      // 构建图谱数据（即使没有graph字段）
      const graphData = {
        nodes: [],
        edges: []
      }
      
      // 从记忆数据中构建图谱
      if (newMemories.length > 0) {
        newMemories.forEach((memory, index) => {
          // 计算节点大小：20 + (relativity || 0.5) * 60
          const nodeSize = 20 + (memory.relativity || 0.5) * 60
          graphData.nodes.push({
            id: memory.id,
            label: memory.content.substring(0, 20) + '...',
            content: memory.content,
            size: nodeSize,
            color: `#${(index * 50 % 255).toString(16).padStart(2, '0')}${(index * 100 % 255).toString(16).padStart(2, '0')}${(index * 150 % 255).toString(16).padStart(2, '0')}`
          })
          if (index > 0) {
            graphData.edges.push({
              source: newMemories[index - 1].id,
              target: memory.id
            })
          }
        })
      }
      
      console.log('Graph data:', graphData)
      updateChart(graphData.nodes, graphData.edges)
    } catch (error) {
      console.error('Failed to update memories:', error)
    }
  }
})

// 移除定时刷新，只在对话结束后更新
</script>

<style scoped>
.right-sidebar {
  width: 30%;
  min-width: 360px;
  max-width: 480px;
  height: 100%;
  background-color: #f8f9fa;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  overflow: hidden;
  flex-shrink: 0;
  transition: background-color 0.3s ease;
}

.memory-logs {
  height: 55%;
  border-bottom: 1px solid #e5e7eb;
  padding: 16px;
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
  height: 45%;
  padding: 16px;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
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

/* 标签样式 */
.memory-tags {
  margin: 4px 0;
  font-size: 12px;
}

.tag {
  color: #64748b;
  background-color: #f1f5f9;
  padding: 2px 6px;
  border-radius: 10px;
  margin-right: 4px;
  display: inline-block;
}

:deep(.dark .right-sidebar .tag) {
  color: #94a3b8;
  background-color: #333a47;
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