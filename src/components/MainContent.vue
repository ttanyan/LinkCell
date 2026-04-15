<template>
  <div class="main-content">
    <div class="conversation-container">
      <div class="conversation-header">
        <h2 class="conversation-title">Microservices Architecture:</h2>
        <div class="conversation-actions">
          <el-button type="text" icon="Edit" />
          <el-button type="text" icon="More" />
        </div>
      </div>
      <div class="conversation-body">
        <div class="user-message">
          <div class="message-card user-card">
            <div class="message-content">
              What is the main concept of microservices architecture?
            </div>
          </div>
        </div>
        <div class="ai-message">
          <div class="message-card ai-card">
            <div class="ai-avatar">
              <el-avatar size="32" :src="aiAvatar" />
            </div>
            <div class="ai-content-wrapper">
              <div class="ai-thinking">
                <span>Thinking...</span>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 100%;"></div>
                </div>
              </div>
              <div class="ai-content">
                <p>Microservices architecture is an approach to software development where an application is composed of small, independent services that communicate with each other using well-defined APIs. Each service is self-contained and can be developed, deployed, and scaled independently.</p>
                
                <h3>Key Characteristics:</h3>
                
                <ul>
                  <li><strong>Service Independence:</strong> Each service can be developed, deployed, and scaled independently.</li>
                  <li><strong>Decentralized Data Management:</strong> Each service typically has its own database.</li>
                  <li><strong>Resilience:</strong> Failure of one service doesn't affect the entire system.</li>
                  <li><strong>Scalability:</strong> Services can be scaled individually based on demand.</li>
                  <li><strong>Technology Diversity:</strong> Different services can use different technologies.</li>
                </ul>
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
            <div class="ai-graph">
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
        
        <div class="user-message">
          <div class="message-card user-card">
            <div class="message-content">
              Summary of the "Tech Stack" cell, please.
            </div>
          </div>
        </div>
        <div class="ai-message">
          <div class="message-card ai-card">
            <div class="ai-avatar">
              <el-avatar size="32" :src="aiAvatar" />
            </div>
            <div class="ai-content-wrapper">
              <div class="ai-thinking">
                <span>Thinking...</span>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 60%;"></div>
                </div>
              </div>
              <div class="ai-content">
                <p>There are comparsent of chroroc of stack cell summary of the "Tech Stack" cell thevase and mow formats.</p>
                
                <h3>AI Responses.</h3>
                
                <h4>Preparations:</h4>
                <ul>
                  <li>API Gateway: anridlesan api onolidew, microservices, Microservices architecture</li>
                  <li>Microservices Architecture : aride nignatirze accessories gateway, openaris, and api-reiconterdoptions</li>
                  <li>Microservices Architecture : concerteetrices, microservices, and alterscassing toneds on microservices.</li>
                </ul>
                
                <h4>Relationships:</h4>
                <ul>
                  <li>API Gateway: compons ioies with shared concepts</li>
                  <li>Microservices Architecture: ieign computen fines and casuallation communications.</li>
                </ul>
                
                <p>Here is what onnovrectozs soon in aiy <a href="#" class="link">knowledge graph</a>.</p>
              </div>
              <div class="ai-footer">
                <el-button type="text" size="small" class="thinking-button">
                  <el-icon><Star /></el-icon> Thinking
                </el-button>
                <el-button type="text" size="small">
                  <el-icon><Refresh /></el-icon>
                </el-button>
              </div>
            </div>
            <div class="ai-graph">
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
        
        <div class="user-message">
          <div class="message-card user-card">
            <div class="message-content">
              How does API Gateway work in microservices architecture?
            </div>
          </div>
        </div>
        <div class="ai-message">
          <div class="message-card ai-card">
            <div class="ai-avatar">
              <el-avatar size="32" :src="aiAvatar" />
            </div>
            <div class="ai-content-wrapper">
              <div class="ai-thinking">
                <span>Thinking...</span>
                <div class="progress-bar">
                  <div class="progress-fill" style="width: 100%;"></div>
                </div>
              </div>
              <div class="ai-content">
                <p>An API Gateway acts as a single entry point for all client requests to the microservices architecture. It routes requests to the appropriate service, handles cross-cutting concerns, and provides a unified interface to clients.</p>
                
                <h3>Key Functions:</h3>
                
                <ul>
                  <li><strong>Request Routing:</strong> Directs client requests to the appropriate microservice.</li>
                  <li><strong>Load Balancing:</strong> Distributes requests across multiple instances of a service.</li>
                  <li><strong>Authentication and Authorization:</strong> Verifies user identity and permissions.</li>
                  <li><strong>Rate Limiting:</strong> Controls the number of requests a client can make.</li>
                  <li><strong>Cache Management:</strong> Stores frequently accessed data to improve performance.</li>
                  <li><strong>Protocol Translation:</strong> Converts between different protocols (e.g., HTTP to gRPC).</li>
                </ul>
                
                <p>Popular API Gateway solutions include Amazon API Gateway, Kong, and Netflix Zuul.</p>
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
            <div class="ai-graph">
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
          placeholder="拖动细胞进行提问....."
          class="message-input"
          type="textarea"
          :rows="1"
          :autosize="{ minRows: 1, maxRows: 2 }"
          maxlength="500"
        />
        <el-button 
          type="primary" 
          class="send-button"
          :disabled="!messageInput.trim()"
          :class="{ disabled: !messageInput.trim() }"
        >
          <el-icon><ArrowUp /></el-icon>
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Message, ArrowRight, Edit, More, Paperclip, Star, Refresh, ArrowUp, Plus, ChatLineRound, Microphone } from '@element-plus/icons-vue'

const messageInput = ref('')
const aiAvatar = 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=AI%20assistant%20icon%20blue%20simple&image_size=square'
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