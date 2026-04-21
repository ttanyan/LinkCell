<template>
  <div class="main-content">
    <div class="conversation-container">
      <div class="conversation-header">
        <div class="conversation-title">
          <div class="model-select-container">
            <span class="model-label">模型</span>
            <el-select 
              v-model="selectedModel" 
              placeholder="选择模型" 
              size="small"
              class="model-select"
              popper-class="model-select-dropdown"
            >
              <el-option
                v-for="model in models"
                :key="model.id"
                :label="model.name"
                :value="model.id"
              />
            </el-select>
          </div>
        </div>
        <div class="conversation-actions">
          <el-tooltip content="导出对话" placement="bottom">
            <el-button type="text" class="icon-button" @click="exportConversation">
              <el-icon><Download /></el-icon>
            </el-button>
          </el-tooltip>
          <el-tooltip content="清空对话" placement="bottom">
            <el-button type="text" class="icon-button" @click="clearConversation">
              <el-icon><Delete /></el-icon>
            </el-button>
          </el-tooltip>
        </div>
      </div>
      
      <!-- 已选文档显示 -->
      <div v-if="selectedDocuments.length > 0" class="selected-documents">
        <div class="selected-documents-header">
          <span>已选择的文档:</span>
        </div>
        <div class="selected-documents-list">
          <el-tag
            v-for="doc in selectedDocuments"
            :key="doc"
            closable
            @close="removeDocument(doc)"
          >
            {{ getDocumentName(doc) }}
          </el-tag>
        </div>
      </div>
      
      <div class="conversation-body">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="message.role === 'user' ? 'user-message' : 'ai-message'"
        >
          <!-- 用户消息 -->
          <div v-if="message.role === 'user'" class="user-message-wrapper">
            <div class="user-message-card">
              <div class="user-message-content">{{ message.content }}</div>
            </div>
          </div>
          
          <!-- AI消息 -->
          <div v-else class="ai-message-wrapper">
            <div class="ai-message-content-wrapper">
              <div v-if="message.status === 'loading'" class="ai-thinking">
                <span>Thinking...</span>
                <div class="progress-bar">
                  <div class="progress-fill"></div>
                </div>
              </div>
              <div v-else class="ai-message-content" v-html="renderMarkdown(message.content)">
              </div>
              <div class="ai-footer">
                <el-tooltip content="复制内容" placement="top">
                  <el-button type="text" size="small" class="ai-footer-button" @click="copyMessage(message.content)">
                    <el-icon><DocumentCopy /></el-icon>
                  </el-button>
                </el-tooltip>
                <el-tooltip content="重新生成" placement="top">
                  <el-button type="text" size="small" class="ai-footer-button">
                    <el-icon><Refresh /></el-icon>
                  </el-button>
                </el-tooltip>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="message-input-container">
      <div class="input-wrapper">
        <el-button type="text" class="add-button">
          <el-icon><Plus /></el-icon>
        </el-button>
        <el-input
          v-model="messageInput"
          placeholder="请输入您的问题....."
          class="message-input"
          type="textarea"
          :rows="1"
          :autosize="{ minRows: 1, maxRows: 2 }"
          maxlength="500"
          @keyup.enter.exact="sendMessage"
        />
        <el-button 
          type="primary" 
          class="send-button"
          :disabled="isSendButtonDisabled"
          :class="{ disabled: isSendButtonDisabled }"
          @click="sendMessage"
        >
          <el-icon><ArrowUp /></el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Message, ArrowRight, Edit, More, Paperclip, Star, Refresh, ArrowUp, Plus, ChatLineRound, Microphone, CircleCheck, Download, Delete, DocumentCopy } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { marked } from 'marked'

// 右侧边栏引用
const rightSidebarRef = ref(null)

const props = defineProps({
  selectedDocuments: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:selectedDocuments'])

const messageInput = ref('')
const messages = ref([])
const models = ref([])
const selectedModel = ref('')
const isLoading = ref(false)
const chatId = ref('00000000-0000-0000-0000-000000000000')
const documents = ref([])

const isSendButtonDisabled = computed(() => {
  const result = !messageInput.value || !messageInput.value.trim() || !selectedModel.value || isLoading.value
  return result
})

const currentModelName = computed(() => {
  const model = models.value.find(m => m.id === selectedModel.value)
  return model ? model.name : '请选择模型'
})

onMounted(() => {
  loadModels()
  loadDocuments()
})

const loadModels = async () => {
  try {
    console.log('加载模型列表...')
    const response = await fetch('/api/model')
    console.log('响应状态:', response.status)
    const data = await response.json()
    console.log('模型列表:', data)
    models.value = data
    if (data.length > 0) {
      selectedModel.value = data[0].id
      console.log('选择的模型:', selectedModel.value)
    }
  } catch (error) {
    console.error('加载模型失败:', error)
  }
}

const loadDocuments = async () => {
  try {
    const response = await fetch('/api/documents')
    const data = await response.json()
    documents.value = data
  } catch (error) {
    console.error('加载文档失败:', error)
  }
}

const getDocumentName = (docId) => {
  const doc = documents.value.find(d => d.id === docId)
  return doc ? doc.name : docId
}

const removeDocument = (docId) => {
  const newSelection = props.selectedDocuments.filter(id => id !== docId)
  emit('update:selectedDocuments', newSelection)
}

const sendMessage = async () => {
  console.log('sendMessage 函数被调用')
  console.log('messageInput.value:', messageInput.value)
  console.log('selectedModel.value:', selectedModel.value)
  if (!messageInput.value.trim() || !selectedModel.value) return
  
  const userMessage = messageInput.value.trim()
  messages.value.push({
    role: 'user',
    content: userMessage
  })
  
  messages.value.push({
    role: 'assistant',
    content: '',
    status: 'loading'
  })
  const aiMessageIndex = messages.value.length - 1
  
  messageInput.value = ''
  isLoading.value = true
  
  let aiFullContent = ''
  
  try {
    // 并行发起两个独立请求
    console.log('发起并行请求')
    
    // 请求1：记忆检索
    const memorySearchPromise = fetch('/api/memos/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        query: userMessage,
        user_id: 'test_user_123',
        conversation_id: chatId.value
      })
    }).then(async (response) => {
      if (response.ok) {
        const data = await response.json()
        console.log('记忆检索响应:', data)
        // 提取正确的记忆数据层级
        const memoriesData = data.memories?.data || data.memories
        console.log('提取的记忆数据:', memoriesData)
        if (memoriesData && rightSidebarRef.value && rightSidebarRef.value.updateMemories) {
          console.log('更新记忆到右侧面板')
          rightSidebarRef.value.updateMemories(memoriesData)
        }
      } else {
        console.error('记忆检索失败:', response.status)
      }
    }).catch((error) => {
      console.error('记忆检索请求失败:', error)
    })
    
    // 请求2：AI对话
    const chatPromise = fetch(`/api/chat/${chatId.value}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userMessage,
        model_id: selectedModel.value,
        workspace_id: '00000000-0000-0000-0000-000000000000',
        selected_documents: props.selectedDocuments
      })
    }).then(async (response) => {
      if (response.ok) {
        const contentType = response.headers.get('Content-Type')
        
        // 检查是否为流式响应 (SSE)
        if (contentType && contentType.includes('text/event-stream')) {
          // 流式响应处理
          const reader = response.body.getReader()
          const decoder = new TextDecoder()
          let fullContent = ''
          
          while (true) {
            const { done, value } = await reader.read()
            if (done) break
            
            const chunk = decoder.decode(value)
            const lines = chunk.split('\n')
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                const data = line.substring(6)
                if (data) {
                  try {
                    const json = JSON.parse(data)
                    
                    if (json.content && json.content.trim()) {
                      fullContent += json.content
                      // 实时更新消息内容
                      messages.value[aiMessageIndex] = {
                        ...messages.value[aiMessageIndex],
                        content: fullContent,
                        status: 'loading'
                      }
                      // 滚动到底部
                      scrollToBottom()
                    }
                    if (json.is_end) {
                      messages.value[aiMessageIndex] = {
                        ...messages.value[aiMessageIndex],
                        content: fullContent,
                        status: 'completed'
                      }
                      // 滚动到底部
                      scrollToBottom()
                      aiFullContent = fullContent
                    }
                  } catch (e) {
                    console.error('解析SSE数据失败:', e)
                  }
                }
              }
            }
          }
        } else {
          // 非流式响应处理
          try {
            const data = await response.json()
            console.log('非流式响应数据:', data)
            if (data.content) {
              // 直接渲染完整回答
              messages.value[aiMessageIndex] = {
                ...messages.value[aiMessageIndex],
                content: data.content,
                status: 'completed'
              }
              // 滚动到底部
              scrollToBottom()
              aiFullContent = data.content
            } else {
              throw new Error('响应数据格式错误')
            }
          } catch (e) {
            console.error('解析非流式响应失败:', e)
            messages.value[aiMessageIndex] = {
              ...messages.value[aiMessageIndex],
              content: `错误: ${e.message || '解析响应失败'}`,
              status: 'error'
            }
          }
        }
      } else {
        const error = await response.json()
        messages.value[aiMessageIndex] = {
          ...messages.value[aiMessageIndex],
          content: `错误: ${error.error || '发送消息失败'}`,
          status: 'error'
        }
      }
    }).catch((error) => {
      console.error('AI对话请求失败:', error)
      messages.value[aiMessageIndex] = {
        ...messages.value[aiMessageIndex],
        content: `错误: ${error.message || '网络错误'}`,
        status: 'error'
      }
    })
    
    // 等待两个请求完成
    await Promise.all([memorySearchPromise, chatPromise])
    
    // AI回答完全结束后，保存对话
    if (aiFullContent) {
      console.log('保存对话到MemOS')
      try {
        const saveResponse = await fetch('/api/memos/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            messages: [
              { "role": "user", "content": userMessage },
              { "role": "assistant", "content": aiFullContent }
            ],
            user_id: 'test_user_123',
            conversation_id: chatId.value
          })
        })
        const saveData = await saveResponse.json()
        console.log('保存对话响应:', saveData)
      } catch (error) {
        console.error('保存对话失败:', error)
      }
    }
  } catch (error) {
    console.error('发送消息失败:', error)
    messages.value[aiMessageIndex] = {
      ...messages.value[aiMessageIndex],
      content: `错误: ${error.message || '网络错误'}`,
      status: 'error'
    }
  } finally {
    isLoading.value = false
    console.log('sendMessage finished')
  }
}

// 导出对话功能
const exportConversation = () => {
  const conversationText = messages.value.map(msg => {
    const role = msg.role === 'user' ? '用户' : 'AI'
    return `${role}: ${msg.content}`
  }).join('\n\n')
  
  const blob = new Blob([conversationText], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `conversation_${new Date().toISOString().slice(0, 10)}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

// 清空对话功能
const clearConversation = () => {
  ElMessageBox.confirm('确定要清空对话吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    messages.value = []
  }).catch(() => {
    // 取消操作，不做任何处理
  })
}

// 复制消息功能
const copyMessage = (content) => {
  // 直接使用传统方法，确保在用户点击事件的直接回调中执行
  const textArea = document.createElement('textarea')
  textArea.value = content
  
  // 确保textarea不在可视区域
  textArea.style.position = 'fixed'
  textArea.style.left = '-999999px'
  textArea.style.top = '-999999px'
  document.body.appendChild(textArea)
  
  // 选择并复制内容
  textArea.focus()
  textArea.select()
  
  try {
    const successful = document.execCommand('copy')
    if (successful) {
      ElMessage({
        message: '复制成功',
        type: 'success',
        position: 'top-right',
        duration: 2500,
        showIcon: true
      })
    } else {
      // 如果传统方法失败，尝试使用Clipboard API
      if (navigator.clipboard) {
        navigator.clipboard.writeText(content).then(() => {
          ElMessage({
            message: '复制成功',
            type: 'success',
            position: 'top-right',
            duration: 2500,
            showIcon: true
          })
        }).catch(err => {
          console.error('复制失败:', err)
          ElMessage({
            message: '复制失败，请手动复制',
            type: 'error',
            position: 'top-right',
            duration: 2500,
            showIcon: true
          })
        })
      } else {
        throw new Error('复制命令执行失败')
      }
    }
  } catch (err) {
    console.error('复制失败:', err)
    ElMessage({
      message: '复制失败，请手动复制',
      type: 'error',
      position: 'top-right',
      duration: 2500,
      showIcon: true
    })
  } finally {
    // 延迟移除textarea，确保复制操作完成
    setTimeout(() => {
      document.body.removeChild(textArea)
    }, 100)
  }
}

// 渲染Markdown内容
const renderMarkdown = (content) => {
  if (!content) return ''
  return marked(content)
}

// 滚动到底部
const scrollToBottom = () => {
  setTimeout(() => {
    const conversationBody = document.querySelector('.conversation-body')
    if (conversationBody) {
      conversationBody.scrollTop = conversationBody.scrollHeight
    }
  }, 100)
}

// 接收右侧边栏引用
defineExpose({
  setRightSidebarRef: (ref) => {
    console.log('setRightSidebarRef called with:', ref)
    rightSidebarRef.value = ref
    console.log('rightSidebarRef set to:', rightSidebarRef.value)
    if (rightSidebarRef.value) {
      console.log('rightSidebarRef has updateMemories:', typeof rightSidebarRef.value.updateMemories === 'function')
    }
  }
})
</script>

<style scoped>
.main-content {
  width: 52%;
  flex: 1;
  min-width: 600px;
  height: 100%;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e5e7eb;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.conversation-container {
  flex: 1;
  overflow: hidden;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.conversation-body {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-right: 8px;
  margin-bottom: 16px;
}

.conversation-body::-webkit-scrollbar {
  width: 6px;
}

.conversation-body::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.conversation-body::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.conversation-body::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 深色主题滚动条 */
:deep(.dark .main-content .conversation-body::-webkit-scrollbar-track) {
  background: #1f2937;
}

:deep(.dark .main-content .conversation-body::-webkit-scrollbar-thumb) {
  background: #4b5563;
}

:deep(.dark .main-content .conversation-body::-webkit-scrollbar-thumb:hover) {
  background: #6b7280;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.conversation-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
  transition: color 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.model-select-container {
  display: flex;
  align-items: center;
  gap: 6px;
}

.model-label {
  font-size: 14px;
  color: #6b7280;
  white-space: nowrap;
}

.model-select {
  border-radius: 8px !important;
  background-color: #ffffff !important;
  border: 1px solid #e5e7eb !important;
  min-width: 120px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
}

:deep(.model-select .el-select__wrapper) {
  box-shadow: none !important;
  border: 1px solid #e5e7eb !important;
  background-color: #ffffff !important;
  border-radius: 8px !important;
  padding: 2px 8px !important;
}

:deep(.model-select .el-select__input) {
  font-size: 14px !important;
  color: #1f2937 !important;
}

:deep(.model-select .el-select__caret) {
  color: #6b7280 !important;
  font-size: 12px !important;
  transition: all 0.3s ease;
}

:deep(.model-select:hover .el-select__caret) {
  color: #409EFF !important;
}

:deep(.model-select-dropdown) {
  border-radius: 8px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  border: 1px solid #e5e7eb !important;
}

:deep(.model-select-dropdown .el-option) {
  font-size: 14px !important;
  padding: 8px 12px !important;
}

:deep(.model-select-dropdown .el-option:hover) {
  background-color: #f3f4f6 !important;
}

:deep(.model-select-dropdown .el-option.is-selected) {
  background-color: #e6f7ff !important;
  color: #409EFF !important;
}

.conversation-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.selected-documents {
  margin-bottom: 20px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.selected-documents-header {
  font-size: 14px;
  font-weight: 500;
  color: #6b7280;
  margin-bottom: 8px;
}

.selected-documents-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.selected-documents-list .el-tag {
  margin-bottom: 4px;
}

.icon-button {
  width: 32px;
  height: 32px;
  min-width: 32px;
  border-radius: 50%;
  background-color: #f3f4f6;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  padding: 0;
}

.icon-button:hover {
  background-color: #e5e7eb;
  color: #111827;
}

.icon-button .el-icon {
  font-size: 16px;
}

/* 用户消息样式 */
.user-message-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.user-message-card {
  max-width: 70%;
  background-color: #409EFF;
  color: white;
  border-radius: 16px 8px 16px 16px;
  padding: 12px 16px;
  position: relative;
}

.user-message-content {
  font-size: 14px;
  line-height: 1.6;
}

/* AI消息样式 */
.ai-message-wrapper {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  max-width: 85%;
}

.ai-message-content-wrapper {
  flex: 1;
  background-color: #f3f4f6;
  border-radius: 8px 16px 16px 16px;
  padding: 16px 20px;
  position: relative;
}

.ai-thinking {
  display: flex;
  align-items: center;
  gap: 12px;
}

.ai-thinking span {
  color: #6b7280;
  font-size: 14px;
}

.progress-bar {
  width: 60px;
  height: 4px;
  background-color: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #409EFF;
  border-radius: 2px;
  animation: loading 1.5s ease-in-out infinite;
}

@keyframes loading {
  0% {
    width: 0%;
  }
  50% {
    width: 100%;
  }
  100% {
    width: 0%;
  }
}

.ai-message-content {
  font-size: 14px;
  line-height: 1.7;
  color: #1f2937;
  margin-bottom: 12px;
}

/* Markdown样式 */
.ai-message-content h1,
.ai-message-content h2,
.ai-message-content h3,
.ai-message-content h4,
.ai-message-content h5,
.ai-message-content h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.ai-message-content h1 {
  font-size: 2em;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.3em;
}

.ai-message-content h2 {
  font-size: 1.5em;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.3em;
}

.ai-message-content h3 {
  font-size: 1.25em;
}

.ai-message-content h4 {
  font-size: 1em;
}

.ai-message-content h5 {
  font-size: 0.875em;
}

.ai-message-content h6 {
  font-size: 0.85em;
  color: #6b7280;
}

.ai-message-content p {
  margin-top: 0;
  margin-bottom: 16px;
}

.ai-message-content ul,
.ai-message-content ol {
  margin-top: 0;
  margin-bottom: 16px;
  padding-left: 2em;
}

.ai-message-content ul li,
.ai-message-content ol li {
  margin-bottom: 8px;
}

.ai-message-content ul ul,
.ai-message-content ul ol,
.ai-message-content ol ul,
.ai-message-content ol ol {
  margin-top: 8px;
  margin-bottom: 8px;
}

.ai-message-content strong {
  font-weight: 600;
}

.ai-message-content em {
  font-style: italic;
}

.ai-message-content code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.875em;
  padding: 0.2em 0.4em;
  margin: 0;
  background-color: rgba(175, 184, 193, 0.2);
  border-radius: 3px;
}

.ai-message-content pre {
  margin-top: 0;
  margin-bottom: 16px;
  padding: 16px;
  overflow: auto;
  font-size: 0.875em;
  line-height: 1.45;
  background-color: #f3f4f6;
  border-radius: 6px;
}

.ai-message-content pre code {
  padding: 0;
  margin: 0;
  font-size: 100%;
  word-break: normal;
  white-space: pre;
  background: transparent;
  border: 0;
}

.ai-message-content a {
  color: #409EFF;
  text-decoration: none;
  transition: color 0.2s ease;
}

.ai-message-content a:hover {
  color: #66b1ff;
  text-decoration: underline;
}

.ai-message-content blockquote {
  margin-top: 0;
  margin-bottom: 16px;
  padding: 16px;
  background-color: #f8f9fa;
  border-left: 4px solid #409EFF;
  border-radius: 0 6px 6px 0;
}

.ai-message-content blockquote p {
  margin-bottom: 0;
}

.ai-message-content table {
  margin-top: 0;
  margin-bottom: 16px;
  width: 100%;
  border-collapse: collapse;
}

.ai-message-content table th,
.ai-message-content table td {
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
}

.ai-message-content table th {
  font-weight: 600;
  background-color: #f3f4f6;
  text-align: left;
}

.ai-message-content hr {
  margin-top: 24px;
  margin-bottom: 24px;
  border: 0;
  border-top: 1px solid #e5e7eb;
}

.ai-footer {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}

.ai-footer-button {
  font-size: 14px;
  color: #409EFF !important;
  padding: 8px !important;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.ai-footer-button:hover {
  background-color: rgba(64, 158, 255, 0.1);
}

.ai-footer-button .el-icon {
  font-size: 16px;
  margin-right: 0;
}

/* 消息输入容器 */
.message-input-container {
  padding: 20px 16px;
  border-top: 1px solid #e5e7eb;
  background-color: #ffffff;
  display: flex;
  justify-content: center;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.input-wrapper {
  display: flex;
  align-items: flex-start;
  width: 100%;
  max-width: 900px;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  padding: 12px 16px;
  background-color: #ffffff;
  transition: all 0.3s ease;
  min-height: 48px;
}

.input-wrapper:focus-within {
  border-color: #409EFF;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.12);
}

.add-button {
  width: 32px;
  height: 32px;
  min-width: 32px;
  border-radius: 50%;
  background-color: #f3f4f6;
  color: #1f2937;
  margin-right: 12px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.add-button:hover {
  background-color: #e5e7eb;
  color: #111827;
}

.add-button .el-icon {
  font-size: 18px;
}

.message-input {
  flex: 1;
  border: none !important;
  box-shadow: none !important;
  padding: 0;
  font-size: 16px;
  min-height: 20px;
  max-height: 100px;
  resize: none;
  line-height: 1.5;
  background: transparent;
  outline: none !important;
}

.message-input::placeholder {
  color: #9ca3af;
  transition: color 0.3s ease;
}

.message-input:focus {
  box-shadow: none !important;
  outline: none !important;
  border: none !important;
}

/* 确保Element Plus输入框组件没有边框 */
:deep(.el-input__wrapper) {
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
}

:deep(.el-input__inner) {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  outline: none !important;
}

:deep(.el-textarea__inner) {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  outline: none !important;
  resize: none !important;
}

.send-button {
  width: auto;
  height: auto;
  min-width: auto;
  border-radius: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 12px;
  flex-shrink: 0;
  background: transparent;
  border: none;
  color: #409EFF;
  padding: 4px;
  transition: color 0.3s ease;
}

.send-button:hover:not(:disabled) {
  background: transparent;
  color: #66b1ff;
}

.send-button:disabled {
  background: transparent !important;
  color: #c0c4cc !important;
  cursor: not-allowed;
}

.send-button .el-icon {
  font-size: 18px;
}

.send-button:disabled .el-icon {
  color: #c0c4cc;
}

/* 自定义ElMessage样式 */
:deep(.el-message) {
  background-color: #FFFFFF !important;
  color: #1f2937 !important;
  font-size: 14px !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  border: none !important;
  padding: 12px 16px !important;
}

:deep(.el-message__icon) {
  color: #10b981 !important;
  font-size: 18px !important;
}

:deep(.el-message--success .el-message__icon) {
  color: #10b981 !important;
}

/* 深色主题样式 */
:deep(.dark .main-content) {
  background-color: #0f172a;
  border-right: 1px solid #374151;
}

:deep(.dark .main-content .conversation-title) {
  color: #f3f4f6;
}

:deep(.dark .main-content .model-label) {
  color: #9ca3af;
}

:deep(.dark .main-content .model-select) {
  background-color: #1e293b !important;
  border: 1px solid #333a47 !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
}

:deep(.dark .main-content .model-select .el-select__wrapper) {
  background-color: #1e293b !important;
  border: 1px solid #333a47 !important;
}

:deep(.dark .main-content .model-select .el-select__input) {
  color: #409EFF !important;
}

:deep(.dark .main-content .model-select .el-select__caret) {
  color: #409EFF !important;
}

:deep(.dark .main-content .model-select:hover .el-select__caret) {
  color: #66b1ff !important;
}

:deep(.dark .main-content .model-select-dropdown) {
  background-color: #1e293b !important;
  border: 1px solid #333a47 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}

:deep(.dark .main-content .model-select-dropdown .el-option) {
  color: #f1f5f9 !important;
}

:deep(.dark .main-content .model-select-dropdown .el-option:hover) {
  background-color: #333a47 !important;
}

:deep(.dark .main-content .model-select-dropdown .el-option.is-selected) {
  background-color: #1e40af !important;
  color: #f1f5f9 !important;
}

:deep(.dark .main-content .selected-documents) {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

:deep(.dark .main-content .selected-documents-header) {
  color: #9ca3af;
}

:deep(.dark .main-content .selected-documents-list .el-tag) {
  background-color: #333a47;
  border-color: #475569;
  color: #f1f5f9;
}

:deep(.dark .main-content .selected-documents-list .el-tag .el-tag__close) {
  color: #9ca3af;
}

:deep(.dark .main-content .selected-documents-list .el-tag .el-tag__close:hover) {
  color: #f1f5f9;
}

:deep(.dark .main-content .icon-button) {
  background-color: #1e293b;
  color: #409EFF;
  border: 1px solid #333a47;
}

:deep(.dark .main-content .icon-button:hover) {
  background-color: #333a47;
  color: #66b1ff;
}

:deep(.dark .main-content .user-message-card) {
  background-color: #409EFF;
}

:deep(.dark .main-content .ai-message-content-wrapper) {
  background-color: #1e293b;
  border-radius: 8px 16px 16px 16px;
  padding: 16px 20px;
}

:deep(.dark .main-content .ai-thinking span) {
  color: #94a3b8;
}

:deep(.dark .main-content .progress-bar) {
  background-color: #333a47;
}

:deep(.dark .main-content .progress-fill) {
  background-color: #409EFF;
}

:deep(.dark .main-content .ai-message-content) {
  color: #f1f5f9;
  font-size: 14px;
  line-height: 1.7;
  margin-bottom: 12px;
}

/* 深色主题下的Markdown样式 */
:deep(.dark .main-content .ai-message-content h1),
:deep(.dark .main-content .ai-message-content h2),
:deep(.dark .main-content .ai-message-content h3),
:deep(.dark .main-content .ai-message-content h4),
:deep(.dark .main-content .ai-message-content h5),
:deep(.dark .main-content .ai-message-content h6) {
  color: #f1f5f9;
}

:deep(.dark .main-content .ai-message-content h1),
:deep(.dark .main-content .ai-message-content h2) {
  border-bottom-color: #374151;
}

:deep(.dark .main-content .ai-message-content h6) {
  color: #9ca3af;
}

:deep(.dark .main-content .ai-message-content code) {
  background-color: rgba(175, 184, 193, 0.1);
  color: #f1f5f9;
}

:deep(.dark .main-content .ai-message-content pre) {
  background-color: #1e293b;
  color: #f1f5f9;
}

:deep(.dark .main-content .ai-message-content blockquote) {
  background-color: #1e293b;
  border-left-color: #409EFF;
}

:deep(.dark .main-content .ai-message-content table th) {
  background-color: #333a47;
  border-color: #475569;
  color: #f1f5f9;
}

:deep(.dark .main-content .ai-message-content table td) {
  border-color: #475569;
  color: #f1f5f9;
}

:deep(.dark .main-content .ai-message-content hr) {
  border-top-color: #374151;
}

:deep(.dark .main-content .ai-message-content a) {
  color: #66b1ff;
}

:deep(.dark .main-content .ai-message-content a:hover) {
  color: #93c5fd;
}

:deep(.dark .main-content .ai-footer) {
  background-color: #333a47;
  padding: 8px 12px;
  border-radius: 6px;
  margin-top: 12px;
  display: flex;
  gap: 16px;
}

:deep(.dark .main-content .ai-footer-button) {
  color: #409EFF !important;
  font-size: 14px;
  padding: 8px !important;
  border-radius: 4px;
  transition: all 0.2s ease;
}

:deep(.dark .main-content .ai-footer-button:hover) {
  color: #66b1ff !important;
  background-color: rgba(64, 158, 255, 0.2);
}

:deep(.dark .main-content .message-input-container) {
  border-top: 1px solid #333a47;
  background-color: #0f172a;
}

:deep(.dark .main-content .input-wrapper) {
  border: 1px solid #333a47;
  background-color: #1e293b;
}

:deep(.dark .main-content .input-wrapper:focus-within) {
  border-color: #409EFF;
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.12);
}

:deep(.dark .main-content .add-button) {
  background-color: #333a47;
  color: #f1f5f9;
}

:deep(.dark .main-content .add-button:hover) {
  background-color: #475569;
  color: #ffffff;
}

:deep(.dark .main-content .message-input::placeholder) {
  color: #94a3b8;
}

:deep(.dark .main-content .send-button) {
  color: #409EFF;
}

:deep(.dark .main-content .send-button:hover:not(:disabled)) {
  color: #66b1ff;
}

:deep(.dark .main-content .send-button:disabled) {
  color: #64748b !important;
}

/* 深色主题下的ElMessage样式 */
:deep(.dark .el-message) {
  background-color: #1e293b !important;
  color: #f3f4f6 !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
}

:deep(.dark .el-message__icon) {
  color: #34d399 !important;
}
</style>