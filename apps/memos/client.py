"""MemOS Client Implementation"""

import os
import requests
import json
from typing import List, Dict, Optional, Any


class MemOSClient:
    """MemOS Client for interacting with MemOS API"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemOSClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize MemOS Client"""
        if not hasattr(self, '_initialized'):
            self.api_key = os.environ.get('MEMOS_API_KEY', '')
            self.api_url = os.environ.get('MEMOS_API_URL', 'https://api.memos-dashboard.openmem.net')
            self.headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            }
            self._initialized = True

    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make API request"""
        url = f"{self.api_url}{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers, params=data)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PUT':
                response = requests.put(url, headers=self.headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers, json=data)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    # 记忆管理
    def create_memory(self, user_id: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """Create memory"""
        data = {
            'user_id': user_id,
            'content': content,
            'metadata': metadata or {}
        }
        return self._request('POST', '/memories', data)

    def search_memory(self, user_id: str, query: str) -> List[Dict]:
        """Search memory semantically"""
        data = {
            'user_id': user_id,
            'query': query
        }
        result = self._request('GET', '/memories/search', data)
        return result.get('memories', [])

    def update_memory(self, memory_id: str, content: str, metadata: Optional[Dict] = None) -> Dict:
        """Update memory"""
        data = {
            'content': content,
            'metadata': metadata or {}
        }
        return self._request('PUT', f'/memories/{memory_id}', data)

    def delete_memory(self, memory_id: str) -> Dict:
        """Delete memory"""
        return self._request('DELETE', f'/memories/{memory_id}')

    def get_memories(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get memory list"""
        data = {
            'user_id': user_id,
            'limit': limit,
            'offset': offset
        }
        result = self._request('GET', '/memories', data)
        return result.get('memories', [])

    # 智能语义检索 (RAG)
    def rag_retrieve(self, user_id: str, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve relevant memories for RAG"""
        data = {
            'user_id': user_id,
            'query': query,
            'top_k': top_k
        }
        result = self._request('POST', '/rag/retrieve', data)
        return result.get('memories', [])

    # 会话/对话管理
    def create_conversation(self, user_id: str, title: str) -> Dict:
        """Create conversation"""
        data = {
            'user_id': user_id,
            'title': title
        }
        return self._request('POST', '/conversations', data)

    def save_message(self, conversation_id: str, role: str, content: str) -> Dict:
        """Save message to conversation"""
        data = {
            'role': role,
            'content': content
        }
        return self._request('POST', f'/conversations/{conversation_id}/messages', data)

    def get_conversation(self, conversation_id: str) -> Dict:
        """Get conversation details"""
        return self._request('GET', f'/conversations/{conversation_id}')

    # 文档/知识管理
    def upload_document(self, user_id: str, file_path: str, document_type: str) -> Dict:
        """Upload document"""
        # 注意：实际实现需要处理文件上传
        data = {
            'user_id': user_id,
            'file_path': file_path,
            'document_type': document_type
        }
        return self._request('POST', '/documents', data)

    def get_documents(self, user_id: str) -> List[Dict]:
        """Get user documents"""
        data = {'user_id': user_id}
        result = self._request('GET', '/documents', data)
        return result.get('documents', [])

    # 大模型增强
    def get_enhanced_context(self, user_id: str, query: str) -> Dict:
        """Get enhanced context for LLM"""
        data = {
            'user_id': user_id,
            'query': query
        }
        return self._request('POST', '/llm/context', data)

    # 记忆图谱
    def get_memory_graph(self, user_id: str) -> Dict:
        """Get memory graph data"""
        data = {'user_id': user_id}
        return self._request('GET', '/memories/graph', data)


# 全局客户端实例
memos_client = MemOSClient()
