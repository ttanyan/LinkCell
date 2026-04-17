<template>
  <div class="memory-graph-panel">
    <div class="panel-header" @click="toggleCollapse">
      <h3>记忆图谱</h3>
      <span class="collapse-icon">{{ isCollapsed ? '▼' : '▲' }}</span>
    </div>
    
    <div v-if="!isCollapsed" class="panel-content">
      <!-- 图谱容器 -->
      <div class="graph-container" ref="graphContainer">
        <svg 
          ref="graphSvg"
          class="graph-svg"
          :width="graphWidth"
          :height="graphHeight"
          @mousedown="startDrag"
          @mousemove="drag"
          @mouseup="endDrag"
          @mouseleave="endDrag"
          @wheel="zoom"
        >
          <!-- 连接线 -->
          <g v-if="graphData.edges && graphData.edges.length > 0">
            <line
              v-for="(edge, index) in graphData.edges"
              :key="index"
              :x1="edge.source.x"
              :y1="edge.source.y"
              :x2="edge.target.x"
              :y2="edge.target.y"
              class="edge"
            />
          </g>
          
          <!-- 节点 -->
          <g v-if="graphData.nodes && graphData.nodes.length > 0">
            <g
              v-for="node in graphData.nodes"
              :key="node.id"
              :transform="`translate(${node.x}, ${node.y})`"
              @click="selectNode(node)"
              class="node"
              :class="{ 'selected': selectedNode && selectedNode.id === node.id }"
            >
              <circle r="20" class="node-circle" />
              <text 
                text-anchor="middle" 
                dy=".3em" 
                class="node-text"
                :style="{ fontSize: `${Math.max(10, 16 - node.content.length / 10)}px` }"
              >
                {{ node.content.substring(0, 10) }}{{ node.content.length > 10 ? '...' : '' }}
              </text>
            </g>
          </g>
        </svg>
        
        <!-- 控制按钮 -->
        <div class="graph-controls">
          <button class="control-button" @click="resetView">重置视图</button>
          <button class="control-button" @click="zoomIn">放大</button>
          <button class="control-button" @click="zoomOut">缩小</button>
        </div>
      </div>
      
      <!-- 节点详情 -->
      <div v-if="selectedNode" class="node-details">
        <h4>记忆详情</h4>
        <p>{{ selectedNode.content }}</p>
        <div class="node-meta">
          <span v-if="selectedNode.created_at">
            创建时间: {{ formatDate(selectedNode.created_at) }}
          </span>
          <span v-else-if="selectedNode.updated_at">
            更新时间: {{ formatDate(selectedNode.updated_at) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'

// 状态管理
const isCollapsed = ref(false)
const graphData = ref({ nodes: [], edges: [] })
const selectedNode = ref(null)
const graphContainer = ref(null)
const graphSvg = ref(null)
const graphWidth = ref(400)
const graphHeight = ref(300)
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const transform = ref({ x: 0, y: 0, scale: 1 })

// 方法：切换折叠状态
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
  if (!isCollapsed.value) {
    setTimeout(() => {
      resizeGraph()
    }, 100)
  }
}

// 方法：调整图谱大小
const resizeGraph = () => {
  if (graphContainer.value) {
    graphWidth.value = graphContainer.value.clientWidth
    graphHeight.value = graphContainer.value.clientHeight - 50 // 减去控制按钮高度
  }
}

// 方法：加载图谱数据
const loadGraphData = async () => {
  try {
    const response = await fetch('/api/memos/graph')
    const data = await response.json()
    
    if (data.nodes && data.edges) {
      // 如果没有坐标，生成随机坐标
      const nodes = data.nodes.map((node, index) => {
        if (!node.x || !node.y) {
          return {
            ...node,
            x: 50 + (index * 100) % (graphWidth.value - 100),
            y: 50 + Math.floor(index / 4) * 100
          }
        }
        return node
      })
      
      graphData.value = {
        nodes,
        edges: data.edges
      }
    } else {
      // 生成示例数据
      generateSampleData()
    }
  } catch (error) {
    console.error('加载图谱数据失败:', error)
    // 生成示例数据
    generateSampleData()
  }
}

// 方法：生成示例数据
const generateSampleData = () => {
  const sampleNodes = [
    { id: '1', content: '喜欢打球', x: 100, y: 100 },
    { id: '2', content: '爱吃蔬菜', x: 300, y: 100 },
    { id: '3', content: '最近肠胃不舒服', x: 200, y: 200 },
    { id: '4', content: '喜欢游泳', x: 100, y: 300 },
    { id: '5', content: '经常健身', x: 300, y: 300 }
  ]
  
  const sampleEdges = [
    { source: { x: 100, y: 100 }, target: { x: 200, y: 200 } },
    { source: { x: 300, y: 100 }, target: { x: 200, y: 200 } },
    { source: { x: 100, y: 300 }, target: { x: 100, y: 100 } },
    { source: { x: 300, y: 300 }, target: { x: 300, y: 100 } },
    { source: { x: 100, y: 300 }, target: { x: 300, y: 300 } }
  ]
  
  graphData.value = {
    nodes: sampleNodes,
    edges: sampleEdges
  }
}

// 方法：选择节点
const selectNode = (node) => {
  selectedNode.value = node
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

// 方法：开始拖拽
const startDrag = (event) => {
  isDragging.value = true
  dragStart.value = {
    x: event.clientX - transform.value.x,
    y: event.clientY - transform.value.y
  }
}

// 方法：拖拽
const drag = (event) => {
  if (isDragging.value) {
    transform.value = {
      ...transform.value,
      x: event.clientX - dragStart.value.x,
      y: event.clientY - dragStart.value.y
    }
    updateTransform()
  }
}

// 方法：结束拖拽
const endDrag = () => {
  isDragging.value = false
}

// 方法：缩放
const zoom = (event) => {
  event.preventDefault()
  const scaleFactor = event.deltaY > 0 ? 0.9 : 1.1
  transform.value = {
    ...transform.value,
    scale: Math.max(0.5, Math.min(2, transform.value.scale * scaleFactor))
  }
  updateTransform()
}

// 方法：更新变换
const updateTransform = () => {
  if (graphSvg.value) {
    graphSvg.value.style.transform = `translate(${transform.value.x}px, ${transform.value.y}px) scale(${transform.value.scale})`
  }
}

// 方法：重置视图
const resetView = () => {
  transform.value = { x: 0, y: 0, scale: 1 }
  updateTransform()
}

// 方法：放大
const zoomIn = () => {
  transform.value = {
    ...transform.value,
    scale: Math.min(2, transform.value.scale * 1.2)
  }
  updateTransform()
}

// 方法：缩小
const zoomOut = () => {
  transform.value = {
    ...transform.value,
    scale: Math.max(0.5, transform.value.scale * 0.8)
  }
  updateTransform()
}

// 生命周期：组件挂载时加载数据
onMounted(() => {
  loadGraphData()
  resizeGraph()
  window.addEventListener('resize', resizeGraph)
})

// 生命周期：组件卸载时清理
onMounted(() => {
  return () => {
    window.removeEventListener('resize', resizeGraph)
  }
})
</script>

<style scoped>
.memory-graph-panel {
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

.graph-container {
  position: relative;
  width: 100%;
  height: 400px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
  background-color: #f9f9f9;
  margin-bottom: 16px;
}

.graph-svg {
  position: absolute;
  top: 0;
  left: 0;
  transition: transform 0.1s ease;
}

.edge {
  stroke: #909399;
  stroke-width: 2;
  stroke-dasharray: 5,5;
}

.node {
  cursor: pointer;
  transition: all 0.3s ease;
}

.node-circle {
  fill: #409EFF;
  stroke: #ffffff;
  stroke-width: 2;
  transition: all 0.3s ease;
}

.node:hover .node-circle {
  fill: #66b1ff;
  r: 22;
}

.node.selected .node-circle {
  fill: #67c23a;
  r: 22;
}

.node-text {
  fill: #ffffff;
  font-size: 12px;
  font-weight: 500;
  pointer-events: none;
}

.graph-controls {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
  z-index: 10;
}

.control-button {
  padding: 6px 12px;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.control-button:hover {
  background-color: #ffffff;
  border-color: #409EFF;
  color: #409EFF;
}

.node-details {
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.node-details h4 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.node-details p {
  margin: 0 0 8px 0;
  font-size: 14px;
  line-height: 1.5;
  color: #606266;
}

.node-meta {
  font-size: 12px;
  color: #909399;
}

/* 深色主题适配 */
.dark .memory-graph-panel {
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

.dark .graph-container {
  border-color: #475569;
  background-color: #1e293b;
}

.dark .edge {
  stroke: #64748b;
}

.dark .node-circle {
  fill: #1e40af;
  stroke: #f1f5f9;
}

.dark .node:hover .node-circle {
  fill: #3b82f6;
}

.dark .node.selected .node-circle {
  fill: #15803d;
}

.dark .control-button {
  background-color: rgba(51, 65, 85, 0.9);
  border-color: #475569;
  color: #f1f5f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.dark .control-button:hover {
  background-color: #334155;
  border-color: #60a5fa;
  color: #60a5fa;
}

.dark .node-details {
  border-color: #475569;
  background-color: #1e293b;
}

.dark .node-details h4 {
  color: #f1f5f9;
}

.dark .node-details p {
  color: #e2e8f0;
}

.dark .node-meta {
  color: #94a3b8;
}
</style>
