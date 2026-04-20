# LinkCell

LinkCell 是一个集成了 MemOS SDK 的智能对话系统，提供记忆管理、智能语义检索、会话管理等功能。

## 功能特性

- **记忆管理**：查看、编辑、删除用户记忆
- **记忆图谱**：可视化展示记忆之间的关联
- **智能语义检索**：基于记忆的语义搜索
- **会话管理**：创建和管理对话
- **文档管理**：上传和管理文档
- **大模型增强**：基于记忆的模型增强

## 技术栈

- **后端**：Django 6.0
- **前端**：Vue 3 + Vite
- **SDK**：MemoryOS
- **可视化**：ECharts

## 安装说明

### 1. 环境要求

- Python 3.13+
- Node.js 18+
- npm 9+

### 2. 安装依赖

#### 后端依赖

```bash
pip install -r requirements.txt
```

#### 前端依赖

```bash
npm install
```

### 3. 配置

#### MemOS API Key

在 `settings.py` 文件中设置 MemOS API Key：

```python
# MemOS API Configuration
MEMOS_API_KEY = 'your_api_key_here'
```

#### 数据库迁移

```bash
python manage.py migrate
```

## 启动方式

### 1. 启动后端服务器

```bash
python manage.py runserver 8001
```

### 2. 启动前端服务器

```bash
npm run dev
```

### 3. 访问应用

打开浏览器，访问：http://localhost:3001/

## 目录结构

```
LinkCell/
├── apps/                  # 后端应用
│   ├── models_provider/    # 模型管理
│   ├── application/        # 应用核心
│   └── memos_integration/  # MemOS 集成
├── src/                   # 前端代码
│   ├── components/         # 前端组件
│   ├── assets/             # 静态资源
│   └── main.js            # 前端入口
├── requirements.txt        # 后端依赖
├── package.json            # 前端依赖
├── vite.config.js         # Vite 配置
└── README.md              # 项目说明
```

## API 接口

### 记忆管理

- `GET /api/memos/list` - 获取记忆列表
- `GET /api/memos/graph` - 获取记忆图谱
- `PUT /api/memos/update/{memory_id}` - 更新记忆
- `DELETE /api/memos/delete/{memory_id}` - 删除记忆

### 会话管理

- `POST /api/conversations/create` - 创建对话

### 文档管理

- `POST /api/documents/upload` - 上传文档

### 智能语义检索

- `POST /api/rag/retrieve` - 检索相关记忆

## 注意事项

1. 确保设置了正确的 MemOS API Key
2. 后端服务器默认运行在端口 8001
3. 前端服务器默认运行在端口 3001
4. 首次运行需要执行数据库迁移

## 开发说明

### 前端开发

```bash
npm run dev
```

### 后端开发

```bash
python manage.py runserver 8001
```

### 构建生产版本

```bash
npm run build
```

## MemOS SDK 功能

MemOS SDK 提供了以下功能：

### 获取 API Key

从 MemOS 平台获取自动生成的 API Key，将其添加到 `settings.py` 文件中：

```python
# MemOS API Configuration
MEMOS_API_KEY = 'your_api_key_here'
```

### 安装 SDK

通过 pip 安装 MemOS 的 Python 包：

```bash
pip install MemoryOS -U
```

### 初始化客户端

用 API Key 初始化 MemOS 客户端，即可开始发送请求：

```python
from memos.api.client import MemOSClient  

client = MemOSClient(api_key="YOUR_API_KEY")
```

### 存储原始对话

将用户的原始对话记录存入 MemOS，MemOS 会自动抽象、加工，并保存为记忆：

```python
messages = [
  {"role": "user", "content": "我暑假定好去广州旅游，住宿的话有哪些连锁酒店可选？"},
  {"role": "assistant", "content": "您可以考虑【七天、全季、希尔顿】等等"},
  {"role": "user", "content": "我选七天"},
  {"role": "assistant", "content": "好的，有其他问题再问我。"}
]
user_id = "memos_user_123"
conversation_id = "0610"

res = client.add_message(messages=messages, user_id=user_id, conversation_id=conversation_id)

print(f"result: {res}")
```

### 检索相关记忆

用户在一个新的会话中，提出让 AI 推荐国庆旅游计划，MemOS 会自动召回相关记忆供 AI 参考，从而推荐更加个性化的旅游计划：

```python
query = "我国庆想出去玩，帮我推荐个没去过的城市，以及没住过的酒店品牌"
user_id = "memos_user_123"
conversation_id ="0928"

res = client.search_memory(query=query, user_id=user_id, conversation_id=conversation_id)

print(f"result: {res}")
```

### 其他功能

- **记忆管理**：创建、更新、删除、获取记忆列表
- **智能语义检索**：RAG 功能，自动召回相关记忆
- **会话/对话管理**：创建对话、保存历史、自动关联记忆
- **文档/知识管理**：上传文档、自动向量化、索引
- **大模型增强**：自动给模型补充记忆，不让模型失忆
- **记忆图谱**：可视化展示记忆之间的关联
