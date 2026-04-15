<template>
  <div class="right-sidebar">
    <div class="memory-logs">
      <div class="section-header">
        <h3>记忆Logs</h3>
      </div>
      <div class="logs-list">
        <div v-for="(log, index) in memoryLogs" :key="index" class="log-item">
          <div class="log-time">{{ log.time }}</div>
          <div class="log-content">{{ log.content }}</div>
          <el-button type="text" size="small" class="link-button">Link</el-button>
        </div>
      </div>
    </div>
    <div class="knowledge-graph">
      <div class="section-header">
        <h3>记忆图谱</h3>
        <div class="graph-actions">
          <el-button type="text" icon="ZoomIn" size="small" />
          <el-button type="text" icon="ZoomOut" size="small" />
        </div>
      </div>
      <div ref="graphContainer" class="graph-container"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ZoomIn, ZoomOut } from '@element-plus/icons-vue'
import * as echarts from 'echarts'

const graphContainer = ref(null)
let chart = null

const memoryLogs = [
  {
    time: '10:15',
    content: 'Summarized Cell: Tech Stack Notes'
  },
  {
    time: '10:45',
    content: 'Added Node: Microservices Architecture'
  },
  {
    time: '09:45',
    content: 'Added Node: Microservices Architecture'
  },
  {
    time: '09:45',
    content: 'Added Node: Microservices Architecture'
  },
  {
    time: '09:35',
    content: 'Added Node: Project Alpha Summary'
  },
  {
    time: '09:00',
    content: 'Added Node Cell: Microservices Architecture'
  }
]

onMounted(() => {
  if (graphContainer.value) {
    chart = echarts.init(graphContainer.value)
    updateChart()
    window.addEventListener('resize', handleResize)
  }
})

onUnmounted(() => {
  if (chart) {
    chart.dispose()
  }
  window.removeEventListener('resize', handleResize)
})

const handleResize = () => {
  if (chart) {
    chart.resize()
  }
}

const updateChart = () => {
  if (!chart) return

  // 检查是否为暗黑模式
  const isDarkMode = document.documentElement.classList.contains('dark')

  const option = {
    tooltip: {
      backgroundColor: isDarkMode ? '#1e293b' : '#ffffff',
      borderColor: isDarkMode ? '#333a47' : '#e5e7eb',
      textStyle: {
        color: isDarkMode ? '#ffffff' : '#1f2937'
      }
    },
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: [
          { 
            name: 'Project Alpha Docs', 
            symbolSize: 30,
            itemStyle: {
              color: isDarkMode ? '#409EFF' : '#3b82f6'
            },
            label: {
              color: isDarkMode ? '#ffffff' : '#000000'
            }
          },
          { 
            name: 'API Gateway', 
            symbolSize: 25,
            itemStyle: {
              color: isDarkMode ? '#10b981' : '#10b981'
            },
            label: {
              color: isDarkMode ? '#ffffff' : '#000000'
            }
          },
          { 
            name: 'Microservices Architecture', 
            symbolSize: 35,
            itemStyle: {
              color: isDarkMode ? '#f59e0b' : '#f59e0b'
            },
            label: {
              color: isDarkMode ? '#ffffff' : '#000000'
            }
          },
          { 
            name: 'Biotechnology', 
            symbolSize: 20,
            itemStyle: {
              color: isDarkMode ? '#8b5cf6' : '#8b5cf6'
            },
            label: {
              color: isDarkMode ? '#ffffff' : '#000000'
            }
          },
          { 
            name: 'Microservices', 
            symbolSize: 20,
            itemStyle: {
              color: isDarkMode ? '#ef4444' : '#ef4444'
            },
            label: {
              color: isDarkMode ? '#ffffff' : '#000000'
            }
          }
        ],
        links: [
          { source: 'Project Alpha Docs', target: 'API Gateway' },
          { source: 'Project Alpha Docs', target: 'Microservices Architecture' },
          { source: 'API Gateway', target: 'Microservices' },
          { source: 'Microservices Architecture', target: 'Microservices' },
          { source: 'Microservices Architecture', target: 'Biotechnology' },
          { source: 'Project Alpha Docs', target: 'Biotechnology' }
        ],
        roam: true,
        label: {
          show: true,
          fontSize: 12
        },
        lineStyle: {
          opacity: 0.9,
          width: 2,
          curveness: 0.1,
          color: isDarkMode ? '#64748b' : '#6b7280'
        },
        force: {
          repulsion: 1000,
          edgeLength: [80, 120]
        }
      }
    ]
  }

  chart.setOption(option)
}
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