<template>
  <div class="settings-container">
    <div class="settings-header">
      <h2>设置</h2>
      <el-button @click="$emit('close-settings')">关闭</el-button>
    </div>
    
    <div class="settings-section">
      <h3>模型管理</h3>
      <div class="model-actions">
        <el-button type="primary" @click="openAddModelDialog">添加模型</el-button>
      </div>
      
      <el-table :data="models" style="width: 100%">
        <el-table-column prop="name" label="模型名称" width="180" />
        <el-table-column prop="model_type" label="模型类型" width="120" />
        <el-table-column prop="model_name" label="具体模型" width="180" />
        <el-table-column prop="provider" label="提供商" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'VALID' ? 'success' : 'danger'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button size="small" @click="editModel(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteModel(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <!-- 添加/编辑模型对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="modelForm" label-width="100px">
        <el-form-item label="模型名称">
          <el-input v-model="modelForm.name" placeholder="请输入模型名称" />
        </el-form-item>
        
        <el-form-item label="模型提供商">
          <el-select v-model="modelForm.provider" @change="handleProviderChange" style="width: 100%">
            <el-option label="OpenAI" value="model_openai_provider" />
            <el-option label="阿里云百炼" value="aliyun_bai_lian_model_provider" />
            <el-option label="Anthropic" value="model_anthropic_provider" />
            <el-option label="Amazon Bedrock" value="model_aws_bedrock_provider" />
            <el-option label="Azure OpenAI" value="model_azure_provider" />
            <el-option label="DeepSeek" value="model_deepseek_provider" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="模型类型">
          <el-select v-model="modelForm.model_type">
            <el-option label="大语言模型 (LLM)" value="LLM" />
            <el-option label="向量嵌入模型 (EMBEDDING)" value="EMBEDDING" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="具体模型">
          <el-input v-model="modelForm.model_name" placeholder="请输入模型名称" style="width: 100%" />
        </el-form-item>
        
        <el-form-item label="API Key">
          <el-input v-model="modelForm.credential.api_key" type="password" placeholder="请输入API Key" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'aliyun_bai_lian_model_provider'" label="API URL">
          <el-input v-model="modelForm.credential.api_url" placeholder="请输入API URL" />
        </el-form-item>
        
        <el-form-item v-else label="API Base URL">
          <el-input v-model="modelForm.credential.api_base" placeholder="请输入API Base URL (可选)" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_aws_bedrock_provider'" label="Access Key">
          <el-input v-model="modelForm.credential.access_key" placeholder="请输入Access Key" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_aws_bedrock_provider'" label="Secret Key">
          <el-input v-model="modelForm.credential.secret_key" type="password" placeholder="请输入Secret Key" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_aws_bedrock_provider'" label="Region">
          <el-input v-model="modelForm.credential.region" placeholder="请输入Region" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_azure_provider'" label="Deployment Name">
          <el-input v-model="modelForm.credential.deployment_name" placeholder="请输入Deployment Name" />
        </el-form-item>
        
        <el-form-item v-if="modelForm.provider === 'model_azure_provider'" label="API Version">
          <el-input v-model="modelForm.credential.api_version" placeholder="请输入API Version" />
        </el-form-item>
        
        <el-form-item>
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
      api_base: ''
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
.settings-container {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

.settings-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.settings-section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 8px;
}

.dark .settings-section {
  background-color: #1e293b;
}

.model-actions {
  margin-bottom: 20px;
}

.settings-section h3 {
  margin-bottom: 20px;
  font-size: 16px;
  font-weight: 600;
}

.el-table {
  margin-top: 10px;
}
</style>