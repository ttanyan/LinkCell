<template>
  <div class="memory-graph-panel" :class="{ 'dark': isDarkMode }">
    <div class="panel-header">
      <h3>记忆图谱</h3>
      <button class="close-button" @click="isVisible = false">×</button>
    </div>
    
    <div class="graph-controls">
      <button class="control-button" @click="resetGraph">重置</button>
      <button class="control-button" @click="zoomIn">放大</button>
      <button class="control-button" @click="zoomOut">缩小</button>
    </div>
    
    <div class="graph-container">
      <div 
        ref="graphCanvas" 
        class="graph-canvas"
        @mousedown="startDrag"
        @mousemove="drag"
        @mouseup="stopDrag"
        @mouseleave="stopDrag"
      >
        <!-- 连接线 -->
        <svg class="graph-svg" :width="canvasWidth" :height="canvasHeight">
          <line 
            v-for="(edge, index) in graphData.edges" 
            :key="index"
            :x1="getNodePosition(edge.source).x"
            :y1="getNodePosition(edge.source).y"
            :x2="getNodePosition(edge.target).x"
            :y2="getNodePosition(edge.target).y"
            stroke="#409EFF"
            stroke-width="2"
            opacity="0.6"
          />
        </svg>
        
        <!-- 节点 -->
        <div 
          v-for="node in graphData.nodes" 
          :key="node.id"
          class="graph-node"
          :style="{
            left: getNodePosition(node.id).x + 'px',
            top: getNodePosition(node.id).y + 'px',
            backgroundColor: getNodeColor(node)
          }"
          @click="selectNode(node)"
          @mousedown.stop="startNodeDrag(node.id, $event)"
        >
          <div class="node-content">{{ node.label }}</div>
        </div>
      </div>
    </div>
    
    <div class="node-details" v-if="selectedNode">
      <h4>记忆详情</h4>
      <p>{{ selectedNode.content }}</p>
      <span class="node-date">{{ formatDate(selectedNode.created_at) }}</span>
    </div>
    
    <div class="empty-state" v-if="graphData.nodes.length === 0">
      <p>暂无记忆数据</p>
      <p class="empty-hint">添加一些记忆后将显示图谱</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:isVisible'])

// 状态管理
const graphData = ref({ nodes: [], edges: [] })
const selectedNode = ref(null)
const isDarkMode = ref(false)
const graphCanvas = ref(null)
const canvasWidth = ref(600)
const canvasHeight = ref(400)
const nodePositions = ref({})
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const dragOffset = ref({ x: 0, y: 0 })
const nodeDragging = ref(null)
const nodeDragStart = ref({ x: 0, y: 0 })
const zoom = ref(1)

// 检查深色模式
const checkDarkMode = () => {
  isDarkMode.value = document.documentElement.classList.contains('dark')
}

// 加载记忆图谱数据
const loadGraphData = async () => {
  try {
    const response = await fetch('/api/memos/graph')
    if (response.ok) {
      const data = await response.json()
      graphData.value = {
        nodes: data.nodes || [],
        edges: data.edges || []
      }
      initializeNodePositions()
    }
  } catch (error) {
    console.error('Failed to load graph data:', error)
  }
}

// 初始化节点位置
const initializeNodePositions = () => {
  const positions = {}
  const centerX = canvasWidth.value / 2
  const centerY = canvasHeight.value / 2
  const radius = Math.min(centerX, centerY) * 0.8
  
  graphData.value.nodes.forEach((node, index) => {
    const angle = (index / graphData.value.nodes.length) * Math.PI * 2
    positions[node.id] = {
      x: centerX + Math.cos(angle) * radius,
      y: centerY + Math.sin(angle) * radius
    }
  })
  
  nodePositions.value = positions
}

// 获取节点位置
const getNodePosition = (nodeId) => {
  return nodePositions.value[nodeId] || { x: 0, y: 0 }
}

// 获取节点颜色
const getNodeColor = (node) => {
  if (selectedNode.value && selectedNode.value.id === node.id) {
    return '#409EFF'
  }
  return isDarkMode.value ? '#333a47' : '#f0f0f0'
}

// 选择节点
const selectNode = (node) => {
  selectedNode.value = node
}

// 开始拖拽画布
const startDrag = (event) => {
  isDragging.value = true
  dragStart.value = {
    x: event.clientX - dragOffset.value.x,
    y: event.clientY - dragOffset.value.y
  }
}

// 拖拽画布
const drag = (event) => {
  if (isDragging.value) {
    dragOffset.value = {
      x: event.clientX - dragStart.value.x,
      y: event.clientY - dragStart.value.y
    }
  }
}

// 停止拖拽画布
const stopDrag = () => {
  isDragging.value = false
}

// 开始拖拽节点
const startNodeDrag = (nodeId, event) => {
  nodeDragging.value = nodeId
  const rect = graphCanvas.value.getBoundingClientRect()
  nodeDragStart.value = {
    x: event.clientX - rect.left - getNodePosition(nodeId).x,
    y: event.clientY - rect.top - getNodePosition(nodeId).y
  }
}

// 拖拽节点
const dragNode = (event) => {
  if (nodeDragging.value) {
    const rect = graphCanvas.value.getBoundingClientRect()
    nodePositions.value[nodeDragging.value] = {
      x: event.clientX - rect.left - nodeDragStart.value.x,
      y: event.clientY - rect.top - nodeDragStart.value.y
    }
  }
}

// 停止拖拽节点
const stopNodeDrag = () => {
  nodeDragging.value = null
}

// 重置图谱
const resetGraph = () => {
  zoom.value = 1
  dragOffset.value = { x: 0, y: 0 }
  initializeNodePositions()
}

// 放大
const zoomIn = () => {
  if (zoom.value < 2) {
    zoom.value += 0.1
  }
}

// 缩小
const zoomOut = () => {
  if (zoom.value > 0.5) {
    zoom.value -= 0.1
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
    loadGraphData()
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
    loadGraphData()
  }
  
  // 监听主题变化
  const observer = new MutationObserver(() => {
    checkDarkMode()
  })
  
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ['class']
  })
  
  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    if (graphCanvas.value) {
      canvasWidth.value = graphCanvas.value.offsetWidth
      canvasHeight.value = graphCanvas.value.offsetHeight
      initializeNodePositions()
    }
  })
  
  // 初始化画布大小
  if (graphCanvas.value) {
    canvasWidth.value = graphCanvas.value.offsetWidth
    canvasHeight.value = graphCanvas.value.offsetHeight
  }
})
</script>

<style scoped>
.memory-graph-panel {
  position: fixed;
  bottom: 20px;
  left: 20px;
  width: 400px;
  height: 400px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.dark.memory-graph-panel {
  background-color: #1e293b;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #e0e0e0;
}

.dark .panel-header {
  border-bottom: 1px solid #333a47;
}

.panel-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.dark .panel-header h3 {
  color: #f1f5f9;
}

.close-button {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 20px;
  height: 20px;
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

.graph-controls {
  display: flex;
  gap: 8px;
  padding: 8px 16px;
  border-bottom: 1px solid #e0e0e0;
  background-color: #f9f9f9;
}

.dark .graph-controls {
  border-bottom: 1px solid #333a47;
  background-color: #333a47;
}

.control-button {
  padding: 4px 8px;
  font-size: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background-color: #ffffff;
  cursor: pointer;
  transition: all 0.2s ease;
}

.dark .control-button {
  border: 1px solid #475569;
  background-color: #1e293b;
  color: #f1f5f9;
}

.control-button:hover {
  background-color: #f0f0f0;
}

.dark .control-button:hover {
  background-color: #475569;
}

.graph-container {
  flex: 1;
  overflow: hidden;
  position: relative;
  background-color: #f9f9f9;
}

.dark .graph-container {
  background-color: #0f172a;
}

.graph-canvas {
  width: 100%;
  height: 100%;
  position: relative;
  cursor: grab;
  transform-origin: center center;
}

.graph-canvas:active {
  cursor: grabbing;
}

.graph-svg {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
  pointer-events: none;
}

.graph-node {
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 2;
  border: 2px solid #409EFF;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.dark .graph-node {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.graph-node:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.node-content {
  font-size: 12px;
  text-align: center;
  padding: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  color: #333;
}

.dark .node-content {
  color: #f1f5f9;
}

.node-details {
  padding: 12px 16px;
  border-top: 1px solid #e0e0e0;
  background-color: #f9f9f9;
}

.dark .node-details {
  border-top: 1px solid #333a47;
  background-color: #333a47;
}

.node-details h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.dark .node-details h4 {
  color: #f1f5f9;
}

.node-details p {
  margin: 0 0 4px 0;
  font-size: 13px;
  color: #666;
  line-height: 1.4;
}

.dark .node-details p {
  color: #94a3b8;
}

.node-date {
  font-size: 11px;
  color: #999;
}

.dark .node-date {
  color: #64748b;
}

.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: #999;
  padding: 40px 20px;
}

.dark .empty-state {
  color: #94a3b8;
}

.empty-hint {
  font-size: 12px;
  margin-top: 8px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .memory-graph-panel {
    width: calc(100vw - 40px);
    height: 300px;
  }
}
</style>