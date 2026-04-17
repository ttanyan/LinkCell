"""MemOS Client Implementation"""

import os
import sys
from typing import List, Dict, Optional, Any

# 添加系统路径，确保能正确导入MemoryOS SDK
sys.path.insert(0, '/home/tlw/miniconda3/lib/python3.13/site-packages')
from memos.api.client import MemOSClient as SDKMemOSClient


class MemOSClient:
    """MemOS Client for interacting with MemOS API using SDK"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemOSClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize MemOS Client"""
        if not hasattr(self, '_initialized'):
            self.api_key = os.environ.get('MEMOS_API_KEY', '')
            self.client = SDKMemOSClient(api_key=self.api_key)
            self._initialized = True

    # 记忆管理
    def create_memory(self, user_id: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """Create memory"""
        try:
            # 使用SDK创建记忆
            result = self.client.memories.create(
                user_id=user_id,
                content=content,
                metadata=metadata or {}
            )
            return result
        except Exception as e:
            raise Exception(f"Create memory failed: {str(e)}")

    def search_memory(self, user_id: str, query: str) -> List[Dict]:
        """Search memory semantically"""
        try:
            # 使用SDK搜索记忆
            result = self.client.memories.search(
                user_id=user_id,
                query=query
            )
            return result.get('memories', [])
        except Exception as e:
            raise Exception(f"Search memory failed: {str(e)}")

    def update_memory(self, memory_id: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """Update memory"""
        try:
            # 使用SDK更新记忆
            result = self.client.memories.update(
                memory_id=memory_id,
                content=content,
                metadata=metadata or {}
            )
            return result
        except Exception as e:
            raise Exception(f"Update memory failed: {str(e)}")

    def delete_memory(self, memory_id: str) -> Dict:
        """Delete memory"""
        try:
            # 使用SDK删除记忆
            result = self.client.memories.delete(memory_id=memory_id)
            return result
        except Exception as e:
            raise Exception(f"Delete memory failed: {str(e)}")

    def get_memories(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get memory list"""
        try:
            # 使用SDK获取记忆列表
            result = self.client.memories.list(
                user_id=user_id,
                limit=limit,
                offset=offset
            )
            return result.get('memories', [])
        except Exception as e:
            raise Exception(f"Get memories failed: {str(e)}")

    # 智能语义检索 (RAG)
    def rag_retrieve(self, user_id: str, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant memories for RAG"""
        try:
            # 使用SDK进行RAG检索
            result = self.client.rag.retrieve(
                user_id=user_id,
                query=query,
                top_k=top_k
            )
            return result.get('memories', [])
        except Exception as e:
            raise Exception(f"RAG retrieve failed: {str(e)}")

    # 会话/对话管理
    def create_conversation(self, user_id: str, title: str) -> Dict:
        """Create conversation"""
        try:
            # 使用SDK创建对话
            result = self.client.conversations.create(
                user_id=user_id,
                title=title
            )
            return result
        except Exception as e:
            raise Exception(f"Create conversation failed: {str(e)}")

    def save_message(self, conversation_id: str, role: str, content: str) -> Dict:
        """Save message to conversation"""
        try:
            # 使用SDK保存消息
            result = self.client.conversations.messages.create(
                conversation_id=conversation_id,
                role=role,
                content=content
            )
            return result
        except Exception as e:
            raise Exception(f"Save message failed: {str(e)}")

    def get_conversation(self, conversation_id: str) -> Dict:
        """Get conversation details"""
        try:
            # 使用SDK获取对话详情
            result = self.client.conversations.get(conversation_id=conversation_id)
            return result
        except Exception as e:
            raise Exception(f"Get conversation failed: {str(e)}")

    # 文档/知识管理
    def upload_document(self, user_id: str, file_path: str, document_type: str) -> Dict:
        """Upload document"""
        try:
            # 使用SDK上传文档
            result = self.client.documents.upload(
                user_id=user_id,
                file_path=file_path,
                document_type=document_type
            )
            return result
        except Exception as e:
            raise Exception(f"Upload document failed: {str(e)}")

    def get_documents(self, user_id: str) -> List[Dict]:
        """Get user documents"""
        try:
            # 使用SDK获取文档列表
            result = self.client.documents.list(user_id=user_id)
            return result.get('documents', [])
        except Exception as e:
            raise Exception(f"Get documents failed: {str(e)}")

    # 大模型增强
    def get_enhanced_context(self, user_id: str, query: str) -> Dict:
        """Get enhanced context for LLM"""
        try:
            # 使用SDK获取增强上下文
            result = self.client.llm.context(
                user_id=user_id,
                query=query
            )
            return result
        except Exception as e:
            raise Exception(f"Get enhanced context failed: {str(e)}")

    # 记忆图谱
    def get_memory_graph(self, user_id: str) -> Dict:
        """Get memory graph data"""
        try:
            # 使用SDK获取记忆图谱
            result = self.client.memories.graph(user_id=user_id)
            return result
        except Exception as e:
            raise Exception(f"Get memory graph failed: {str(e)}")


# 全局客户端实例
memos_client = MemOSClient()
