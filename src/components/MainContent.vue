<template>
  <div class="main-content">
    <div class="conversation-container">
      <div class="conversation-header">
        <h2 class="conversation-title">与模型对话</h2>
        <div class="conversation-actions">
          <el-select v-model="selectedModel" placeholder="选择模型" size="small">
            <el-option
              v-for="model in models"
              :key="model.id"
              :label="model.name"
              :value="model.id"
            />
          </el-select>
          <el-button type="text" icon="Edit" />
          <el-button type="text" icon="More" />
        </div>
      </div>
      <div class="conversation-body">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="message.role === 'user' ? 'user-message' : 'ai-message'"
        >
          <div class="message-card" :class="message.role === 'user' ? 'user-card' : 'ai-card'">
            <div v-if="message.role === 'assistant'" class="ai-avatar">
              <el-avatar size="small" :src="aiAvatar" />
            </div>
            <div v-if="message.role === 'assistant'" class="ai-content-wrapper">
              <div v-if="message.status === 'loading'" class="ai-thinking">
                <span>Thinking...</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: '60%' }"></div>
                </div>
              </div>
              <div v-else class="ai-content">
                <p v-for="(line, lineIndex) in message.content.split('\n')" :key="lineIndex" v-if="line && line.trim()">
                  {{ line }}
                </p>
              </div>
              <div class="ai-footer">
                <el-button type="text" size="small" class="thinking-button">
                  <el-icon><Star /></el-icon> Helpful
                </el-button>
                <el-button type="text" size="small">
                  <el-icon><Refresh /></el-icon>
                </el-button>
              </div>
            </div>
            <div v-else class="message-content">
              {{ message.content }}
            </div>
            <div v-if="message.role === 'assistant'" class="ai-graph">
              <div class="graph-placeholder">
                <div class="graph-node main-node"></div>
                <div class="graph-node secondary-node"></div>
                <div class="graph-node secondary-node"></div>
                <div class="graph-node secondary-node"></div>
                <div class="graph-node secondary-node"></div>
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
import { Message, ArrowRight, Edit, More, Paperclip, Star, Refresh, ArrowUp, Plus, ChatLineRound, Microphone } from '@element-plus/icons-vue'

const messageInput = ref('')
const aiAvatar = 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=AI%20assistant%20icon%20blue%20simple&image_size=square'
const messages = ref([])
const models = ref([])
const selectedModel = ref('')
const isLoading = ref(false)
const chatId = ref('00000000-0000-0000-0000-000000000000')

const isSendButtonDisabled = computed(() => {
  const result = !messageInput.value || !messageInput.value.trim() || !selectedModel.value || isLoading.value
  console.log('isSendButtonDisabled:', result)
  console.log('messageInput.value:', messageInput.value)
  console.log('messageInput.value.trim():', messageInput.value ? messageInput.value.trim() : 'undefined')
  console.log('selectedModel.value:', selectedModel.value)
  console.log('isLoading.value:', isLoading.value)
  return result
})

onMounted(() => {
  loadModels()
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
  
  const aiMessageIndex = messages.value.length
  messages.value.push({
    role: 'assistant',
    content: '',
    status: 'loading'
  })
  
  messageInput.value = ''
  isLoading.value = true
  
  try {
    console.log('发送消息请求到:', `/api/chat/${chatId.value}/chat`)
    console.log('请求参数:', {
      message: userMessage,
      model_id: selectedModel.value,
      workspace_id: '00000000-0000-0000-0000-000000000000'
    })
    const response = await fetch(`/api/chat/${chatId.value}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: userMessage,
        model_id: selectedModel.value,
        workspace_id: '00000000-0000-0000-0000-000000000000'
      })
    })
    console.log('响应状态:', response.status)
    
    if (response.ok) {
      console.log('响应类型:', response.headers.get('Content-Type'))
      console.log('响应体:', response.body)
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullContent = ''
      
      while (true) {
        const { done, value } = await reader.read()
        console.log('读取数据块:', { done, value: value ? value.length : 0 })
        if (done) break
        
        const chunk = decoder.decode(value)
        console.log('解码后的数据:', chunk)
        const lines = chunk.split('\n')
        console.log('分割后的行:', lines)
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.substring(6)
            console.log('提取的数据:', data)
            if (data) {
              try {
                const json = JSON.parse(data)
                console.log('解析后的JSON:', json)
                if (json.content) {
                  fullContent += json.content
                  console.log('当前完整内容:', fullContent)
                  messages.value[aiMessageIndex] = {
                    ...messages.value[aiMessageIndex],
                    content: fullContent,
                    status: json.is_end ? 'completed' : 'loading'
                  }
                }
                if (json.is_end) {
                  messages.value[aiMessageIndex] = {
                    ...messages.value[aiMessageIndex],
                    status: 'completed'
                  }
                }
              } catch (e) {
                console.error('解析SSE数据失败:', e)
              }
            }
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
  } catch (error) {
    console.error('发送消息失败:', error)
    messages.value[aiMessageIndex] = {
      ...messages.value[aiMessageIndex],
      content: `错误: ${error.message || '网络错误'}`,
      status: 'error'
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.main-content {
  width: 50%;
  height: 100%;
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e5e7eb;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.conversation-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.conversation-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.conversation-title {
  font-size: 16px;
  font-weight: 500;
  margin: 0;
  color: #1f2937;
  transition: color 0.3s ease;
}

.conversation-actions {
  display: flex;
  gap: 8px;
}

.user-message {
  margin-bottom: 20px;
}

.ai-message {
  margin-bottom: 20px;
}

.message-card {
  border-radius: 4px;
  padding: 16px;
  position: relative;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.user-card {
  background-color: #f3f4f6;
  border: none;
  transition: background-color 0.3s ease;
}

.ai-card {
  display: flex;
  gap: 16px;
}

.ai-avatar {
  flex-shrink: 0;
  margin-top: 4px;
}

.ai-content-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.ai-thinking {
  margin-bottom: 16px;
}

.ai-thinking span {
  display: block;
  margin-bottom: 8px;
  color: #6b7280;
  transition: color 0.3s ease;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background-color: #e5e7eb;
  border-radius: 2px;
  overflow: hidden;
  transition: background-color 0.3s ease;
}

.progress-fill {
  height: 100%;
  background-color: #409EFF;
  border-radius: 2px;
}

.ai-content {
  margin-bottom: 16px;
  flex: 1;
}

.ai-content h3 {
  font-size: 14px;
  font-weight: 500;
  margin: 16px 0 8px 0;
  color: #1f2937;
  transition: color 0.3s ease;
}

.ai-content h4 {
  font-size: 13px;
  font-weight: 500;
  margin: 12px 0 6px 0;
  color: #1f2937;
  transition: color 0.3s ease;
}

.ai-content p {
  margin: 8px 0;
  line-height: 1.5;
  color: #1f2937;
  transition: color 0.3s ease;
}

.ai-content ul {
  margin: 8px 0;
  padding-left: 20px;
}

.ai-content li {
  margin: 4px 0;
  color: #1f2937;
  line-height: 1.4;
  transition: color 0.3s ease;
}

.ai-content .link {
  color: #409EFF;
  text-decoration: none;
  transition: color 0.3s ease;
}

.ai-content .link:hover {
  text-decoration: underline;
}

.ai-footer {
  margin-top: 16px;
  display: flex;
  gap: 12px;
}

.thinking-button {
  display: flex;
  align-items: center;
  gap: 4px;
}

.ai-graph {
  flex-shrink: 0;
  width: 120px;
  height: 120px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.graph-placeholder {
  position: relative;
  width: 100px;
  height: 100px;
}

.graph-node {
  position: absolute;
  border-radius: 50%;
  border: 2px solid #409EFF;
}

.main-node {
  width: 24px;
  height: 24px;
  background-color: #409EFF;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.secondary-node {
  width: 16px;
  height: 16px;
  background-color: #ffffff;
  transition: background-color 0.3s ease;
}

.secondary-node:nth-child(2) {
  top: 20%;
  left: 50%;
  transform: translateX(-50%);
}

.secondary-node:nth-child(3) {
  top: 50%;
  left: 20%;
  transform: translateY(-50%);
}

.secondary-node:nth-child(4) {
  top: 50%;
  right: 20%;
  transform: translateY(-50%);
}

.secondary-node:nth-child(5) {
  bottom: 20%;
  left: 50%;
  transform: translateX(-50%);
}

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

/* 深色主题样式 */
:deep(.dark .main-content) {
  background-color: #0f172a;
  border-right: 1px solid #374151;
}

:deep(.dark .main-content .conversation-title) {
  color: #f3f4f6;
}

:deep(.dark .main-content .message-card) {
  background-color: #1e293b;
  border: 1px solid #334155;
}

:deep(.dark .main-content .user-card) {
  background-color: #334155;
  border: none;
}

:deep(.dark .main-content .ai-thinking span) {
  color: #9ca3af;
}

:deep(.dark .main-content .progress-bar) {
  background-color: #374151;
}

:deep(.dark .main-content .ai-content h3) {
  color: #f3f4f6;
}

:deep(.dark .main-content .ai-content h4) {
  color: #f3f4f6;
}

:deep(.dark .main-content .ai-content p) {
  color: #f3f4f6;
}

:deep(.dark .main-content .ai-content li) {
  color: #f3f4f6;
}

:deep(.dark .main-content .ai-graph) {
  background-color: #1e293b;
  border: 1px solid #334155;
}

:deep(.dark .main-content .secondary-node) {
  background-color: #1e293b;
}

:deep(.dark .main-content .message-input-container) {
  border-top: 1px solid #374151;
  background-color: #0f172a;
}

:deep(.dark .main-content .input-wrapper) {
  border: 1px solid #334155;
  background-color: #1e293b;
}

:deep(.dark .main-content .input-wrapper:focus-within) {
  border-color: #60a5fa;
  box-shadow: 0 2px 12px rgba(96, 165, 250, 0.12);
}

:deep(.dark .main-content .add-button) {
  background-color: #334155;
  color: #f3f4f6;
}

:deep(.dark .main-content .add-button:hover) {
  background-color: #475569;
  color: #ffffff;
}

:deep(.dark .main-content .message-input::placeholder) {
  color: #6b7280;
}

:deep(.dark .main-content .send-button) {
  color: #60a5fa;
}

:deep(.dark .main-content .send-button:hover:not(:disabled)) {
  color: #93c5fd;
}

:deep(.dark .main-content .send-button:disabled) {
  color: #64748b !important;
}
</style>