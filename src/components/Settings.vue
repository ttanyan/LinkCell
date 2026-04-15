<template>
  <div class="settings-container">
    <div class="settings-body">
      <!-- 模型管理卡片 -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">模型管理</h3>
          <el-button class="close-button" @click="$emit('close-settings')">关闭</el-button>
        </div>
        <div class="card-body">
          <!-- 添加模型按钮 -->
          <div class="action-section">
            <el-button type="primary" class="add-model-button" @click="openAddModelDialog">添加模型</el-button>
          </div>
          
          <!-- 模型表格 -->
          <div class="table-section">
            <el-table :data="models" class="model-table">
              <el-table-column prop="name" label="模型名称" />
              <el-table-column prop="model_type" label="模型类型" />
              <el-table-column prop="model_name" label="具体模型" />
              <el-table-column prop="provider" label="提供商" />
              <el-table-column prop="status" label="状态">
                <template #default="scope">
                  <el-tag class="status-tag" :type="scope.row.status === 'VALID' ? 'success' : 'danger'">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" class="action-column">
                <template #default="scope">
                  <el-button size="small" class="edit-button" @click="editModel(scope.row)">编辑</el-button>
                  <el-button size="small" type="danger" class="delete-button" @click="deleteModel(scope.row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加/编辑模型对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      class="model-dialog"
    >
      <el-form :model="modelForm" label-width="100px" class="model-form">
        <el-form-item label="模型名称">
          <el-input v-model="modelForm.name" placeholder="请输入模型名称" class="form-input" />
        </el-form-item>
        
        <el-form-item label="模型提供商">
          <el-select v-model="modelForm.provider" @change="handleProviderChange" class="form-select">
            <el-option label="OpenAI" value="model_openai_provider" />
            <el-option label="阿里云百炼" value="aliyun_bai_lian_model_provider" />
            <el-option label="Anthropic" value="model_anthropic_provider" />
            <el-option label="Amazon Bedrock" value="model_aws_bedrock_provider" />
            <el-option label="Azure OpenAI" value="model_azure_provider" />
            <el-option label="DeepSeek" value="model_deepseek_provider" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="模型类型">
          <el-select v-model="modelForm.model_type" class="form-select">
            <el-option label="大语言模型 (LLM)" value="LLM" />
            <el-option label="向量嵌入模型 (EMBEDDING)" value="EMBEDDING" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="具体模型">
          <el-input v-model="modelForm.model_name" placeholder="请输入模型名称" class="form-input" />
        </el-form-item>
        
        <el-form-item label="API Key">
          <el-input v-model="modelForm.credential.api_key" type="password" placeholder="请输入API Key" class="form-input" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'aliyun_bai_lian_model_provider'" label="API URL">
          <el-input v-model="modelForm.credential.api_url" placeholder="请输入API URL" class="form-input" />
        </el-form-item>
        
        <el-form-item v-else label="API Base URL">
          <el-input v-model="modelForm.credential.api_base" placeholder="请输入API Base URL (可选)" class="form-input" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_aws_bedrock_provider'" label="Access Key">
          <el-input v-model="modelForm.credential.access_key" placeholder="请输入Access Key" class="form-input" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_aws_bedrock_provider'" label="Secret Key">
          <el-input v-model="modelForm.credential.secret_key" type="password" placeholder="请输入Secret Key" class="form-input" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_aws_bedrock_provider'" label="Region">
          <el-input v-model="modelForm.credential.region" placeholder="请输入Region" class="form-input" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_azure_provider'" label="Deployment Name">
          <el-input v-model="modelForm.credential.deployment_name" placeholder="请输入Deployment Name" class="form-input" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_azure_provider'" label="API Version">
          <el-input v-model="modelForm.credential.api_version" placeholder="请输入API Version" class="form-input" />
        </el-form-item>
        
        <el-form-item class="form-actions">
          <el-button type="primary" @click="validateModel">验证模型</el-button>
          <el-button @click="dialogVisible = false">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script setup>
defineEmits(['close-settings'])
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const dialogVisible = ref(false)
const dialogTitle = ref('添加模型')
const providers = ref([])
const models = ref([])
const availableModels = ref([])

const modelForm = ref({
  name: '',
  provider: '',
  model_type: 'LLM',
  model_name: '',
  credential: {
    api_key: '',
    api_base: ''
  }
})

onMounted(() => {
  loadProviders()
  loadModels()
})

const loadProviders = async () => {
  try {
    console.log('开始加载模型提供商...')
    const response = await fetch('/api/model/provider/list')
    console.log('响应状态:', response.status)
    const data = await response.json()
    console.log('获取到的模型提供商:', data)
    providers.value = data
  } catch (error) {
    console.error('加载提供商失败:', error)
  }
}

const loadModels = async () => {
  try {
    const response = await fetch('/api/model')
    const data = await response.json()
    models.value = data
  } catch (error) {
    console.error('加载模型失败:', error)
  }
}

const handleProviderChange = async () => {
  if (modelForm.value.provider) {
    try {
      const response = await fetch(`/api/model/provider/${modelForm.value.provider}/model/list?model_type=${modelForm.value.model_type}`)
      const data = await response.json()
      availableModels.value = data
      modelForm.value.model_name = ''
    } catch (error) {
      console.error('加载模型列表失败:', error)
    }
  } else {
    availableModels.value = []
  }
}

const openAddModelDialog = () => {
  dialogTitle.value = '添加模型'
  modelForm.value = {
    name: '',
    provider: '',
    model_type: 'LLM',
    model_name: '',
    credential: {
      api_key: '',
      api_base: '',
      api_url: ''
    }
  }
  availableModels.value = []
  console.log('打开模型添加对话框时的模型提供商列表:', providers.value)
  dialogVisible.value = true
}

const editModel = (model) => {
  dialogTitle.value = '编辑模型'
  modelForm.value = {
    ...model,
    credential: {
      api_key: '',
      api_base: ''
    }
  }
  availableModels.value = []
  dialogVisible.value = true
}

const validateModel = async () => {
  try {
    const response = await fetch(`/api/model/provider/${modelForm.value.provider}/valid`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model_type: modelForm.value.model_type,
        model_name: modelForm.value.model_name,
        model_credential: modelForm.value.credential
      })
    })
    
    const data = await response.json()
    if (data.valid) {
      await saveModel()
    } else {
      ElMessage.error('模型验证失败')
    }
  } catch (error) {
    console.error('验证模型失败:', error)
    ElMessage.error('验证模型失败')
  }
}

const saveModel = async () => {
  try {
    const response = await fetch('/api/model/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        ...modelForm.value,
        workspace_id: '00000000-0000-0000-0000-000000000000'
      })
    })
    
    if (response.ok) {
      ElMessage.success('模型保存成功')
      dialogVisible.value = false
      loadModels()
    } else {
      const data = await response.json()
      ElMessage.error(data.error || '保存模型失败')
    }
  } catch (error) {
    console.error('保存模型失败:', error)
    ElMessage.error('保存模型失败')
  }
}

const deleteModel = async (modelId) => {
  try {
    const response = await fetch(`/api/model/${modelId}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      ElMessage.success('模型删除成功')
      loadModels()
    } else {
      ElMessage.error('删除模型失败')
    }
  } catch (error) {
    console.error('删除模型失败:', error)
    ElMessage.error('删除模型失败')
  }
}
</script>

<style scoped>
/* 全局设置 */
.settings-container {
  height: 100%;
  overflow-y: auto;
  background-color: #f8f9fa;
  transition: background-color 0.3s ease;
}

/* 主体内容 */
.settings-body {
  padding: 32px;
}

/* 卡片样式 */
.card {
  background-color: #ffffff;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  overflow: hidden;
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  border-bottom: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
  transition: color 0.3s ease;
}

.close-button {
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  transition: all 0.3s ease;
}

.close-button:hover {
  background-color: #f3f4f6;
}

/* 卡片主体 */
.card-body {
  padding: 32px;
}

/* 操作区域 */
.action-section {
  margin-bottom: 24px;
}

.add-model-button {
  border-radius: 8px;
  height: 44px;
  padding: 0 20px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

/* 表格区域 */
.table-section {
  background-color: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

/* 表格样式 */
.model-table {
  border-radius: 12px;
  overflow: hidden;
  border: none;
  transition: all 0.3s ease;
}

.model-table th {
  height: 60px;
  font-size: 14px;
  font-weight: 500;
  background-color: #f8f9fa;
  color: #6b7280;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 20px;
  transition: all 0.3s ease;
}

.model-table td {
  height: 60px;
  font-size: 14px;
  color: #1f2937;
  border-bottom: 1px solid #f1f5f9;
  padding: 0 20px;
  transition: all 0.3s ease;
}

.model-table tr:hover td {
  background-color: #f1f5f9;
}

/* 状态标签 */
.status-tag {
  border-radius: 12px;
  padding: 6px 16px;
  font-size: 12px;
  font-weight: 500;
}

/* 操作列 */
.action-column {
  text-align: right;
}

.edit-button {
  border-radius: 6px;
  padding: 6px 16px;
  margin-right: 12px;
  background-color: #f3f4f6;
  color: #409EFF;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.edit-button:hover {
  background-color: #e5e7eb;
  color: #409EFF;
}

.delete-button {
  border-radius: 6px;
  padding: 6px 16px;
  transition: all 0.3s ease;
}

/* 对话框样式 */
.model-dialog {
  border-radius: 16px;
  overflow: hidden;
}

.model-form {
  padding: 32px 0;
}

.form-input,
.form-select {
  border-radius: 8px;
  width: 100%;
  transition: all 0.3s ease;
  border: 1px solid #e5e7eb;
  background-color: #ffffff;
  color: #1f2937;
  height: 44px;
  font-size: 14px;
}

.form-input:focus,
.form-select:focus {
  border-color: #409EFF;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
}

.form-actions .el-button {
  padding: 0 20px;
  height: 44px;
  font-size: 14px;
  font-weight: 500;
}
</style>

<style>
/* 暗黑主题 */
.dark .settings-container {
  background-color: #121826;
}

.dark .card {
  background-color: #1e293b;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.dark .card-header {
  border-bottom: 1px solid #333a47;
}

.dark .card-title {
  color: #f1f5f9;
}

.dark .close-button {
  color: #94a3b8;
}

.dark .close-button:hover {
  background-color: #333a47;
  color: #f1f5f9;
}

.dark .table-section {
  background-color: #1e293b;
  border: 1px solid #333a47;
}

.dark .model-table th {
  background-color: #1e293b;
  color: #94a3b8;
  border-bottom: 1px solid #333a47;
}

.dark .model-table td {
  color: #f1f5f9;
  border-bottom: 1px solid #333a47;
}

.dark .model-table tr:hover td {
  background-color: #273449;
}

.dark .status-tag {
  background-color: rgba(16, 185, 129, 0.8);
  color: #ffffff;
}

.dark .edit-button {
  background-color: #333a47;
  color: #60a5fa;
  border: 1px solid #333a47;
}

.dark .edit-button:hover {
  background-color: #475569;
  color: #60a5fa;
}

/* 对话框样式 - 暗黑主题 */
.dark .model-dialog {
  background-color: #1e293b;
}

.dark .model-dialog .el-dialog__title {
  color: #f1f5f9;
}

.dark .model-form label {
  color: #94a3b8;
}

.dark .form-input,
.dark .form-select {
  background-color: #1e293b;
  border: 1px solid #333a47;
  color: #f1f5f9;
}

.dark .form-input::placeholder,
.dark .form-select::placeholder {
  color: #64748b;
}

.dark .form-input:focus,
.dark .form-select:focus {
  border-color: #60a5fa;
  box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
}

.dark .el-dialog__header {
  border-bottom: 1px solid #333a47;
}

.dark .el-dialog__footer {
  border-top: 1px solid #333a47;
}

/* 确保Element Plus组件在暗黑主题下正确显示 */
.dark .el-table {
  --el-table-bg-color: #273449;
  --el-table-text-color: #f1f5f9;
  --el-table-border-color: #333a47;
  --el-table-header-bg-color: #273449;
  --el-table-header-text-color: #94a3b8;
  --el-table-row-hover-bg-color: #273449;
}

/* 确保表格单元格背景色与行背景色一致 */
.dark .el-table__row {
  background-color: #273449 !important;
}

.dark .el-table__row:hover {
  background-color: #273449 !important;
}

.dark .el-table__cell {
  background-color: #273449 !important;
  border-bottom: 1px solid #333a47 !important;
}

.dark .el-tag--success {
  --el-tag-bg-color: rgba(16, 185, 129, 0.8);
  --el-tag-border-color: rgba(16, 185, 129, 0.8);
  --el-tag-text-color: #ffffff;
}

.dark .el-button--primary {
  --el-button-bg-color: #409EFF;
  --el-button-border-color: #409EFF;
  --el-button-hover-bg-color: #66b1ff;
  --el-button-hover-border-color: #66b1ff;
}

.dark .el-button--danger {
  --el-button-bg-color: #ef4444;
  --el-button-border-color: #ef4444;
  --el-button-hover-bg-color: #f87171;
  --el-button-hover-border-color: #f87171;
}

.dark .el-input__wrapper {
  --el-input-bg-color: #1e293b;
  --el-input-border-color: #333a47;
  --el-input-text-color: #f1f5f9;
  --el-input-placeholder-color: #64748b;
}

.dark .el-select {
  --el-select-bg-color: #1e293b;
  --el-select-border-color: #333a47;
  --el-select-text-color: #f1f5f9;
  --el-select-placeholder-color: #64748b;
}

.dark .el-dialog {
  --el-dialog-bg-color: #1e293b;
  --el-dialog-border-color: #333a47;
  --el-dialog-title-text-color: #f1f5f9;
}

/* 确保表单在暗黑主题下正确显示 */
.dark .el-form-item__label {
  color: #94a3b8 !important;
}

.dark .el-input__inner {
  color: #f1f5f9 !important;
}

.dark .el-select__input {
  color: #f1f5f9 !important;
}

.dark .el-select__placeholder {
  color: #64748b !important;
}
</style>