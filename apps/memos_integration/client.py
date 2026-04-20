"""MemOS Client Implementation"""

import os
from typing import List, Dict, Optional, Any

# 添加系统路径，确保能正确导入MemoryOS SDK
import sys
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
            from django.conf import settings
            self.api_key = getattr(settings, 'MEMOS_API_KEY', 'mpg-t1HLqL8Jev+CeaeWC5vc97AHeaTsn/dNo5rwgCkk')
            # 初始化 SDK 客户端
            self.client = SDKMemOSClient(api_key=self.api_key)
            self._initialized = True

    # 存储对话
    def add_message(self, messages: List[Dict], user_id: str, conversation_id: str) -> Dict:
        """Add messages to conversation"""
        try:
            # 使用SDK添加消息
            result = self.client.add_message(
                messages=messages,
                user_id=user_id,
                conversation_id=conversation_id
            )
            return result
        except Exception as e:
            print(f"Add message failed: {str(e)}")
            return {"status": "error", "message": str(e)}

    # 检索记忆
    def search_memory(self, query: str, user_id: str, conversation_id: str):
        """Search memory semantically"""
        try:
            # 使用SDK搜索记忆
            result = self.client.search_memory(
                query=query,
                user_id=user_id,
                conversation_id=conversation_id
            )
            return result
        except Exception as e:
            print(f"Search memory failed: {str(e)}")
            return None

    # 获取记忆列表
    def get_memories(self, user_id: str, limit: int = 100, offset: int = 0, query: str = ""):
        """Get memory list"""
        try:
            # 使用搜索方法获取记忆，传递查询参数
            result = self.client.search_memory(
                query=query or "all",  # 如果没有查询参数，使用 "all"
                user_id=user_id,
                conversation_id=""
            )
            return result
        except Exception as e:
            print(f"Get memories failed: {str(e)}")
            return None

    # 记忆图谱
    def get_memory_graph(self, user_id: str, query: str = "") -> Dict:
        """Get memory graph data"""
        try:
            # 获取记忆列表
            memory_data = self.get_memories(user_id, query=query)
            # 构建简单的图谱数据
            nodes = []
            edges = []
            node_id = 1
            
            # 处理 memory_detail_list
            if memory_data and hasattr(memory_data, 'memory_detail_list') and memory_data.memory_detail_list:
                for memory in memory_data.memory_detail_list:
                    if hasattr(memory, 'memory_key'):
                        nodes.append({
                            "id": str(node_id),
                            "label": memory.memory_key[:20] + '...',
                            "size": 20 + node_id * 5,
                            "color": f"#{node_id * 50 % 255:02x}{node_id * 100 % 255:02x}{node_id * 150 % 255:02x}"
                        })
                        if node_id > 1:
                            edges.append({"source": str(node_id - 1), "target": str(node_id)})
                        node_id += 1
            
            # 处理 preference_detail_list
            if memory_data and hasattr(memory_data, 'preference_detail_list') and memory_data.preference_detail_list:
                for preference in memory_data.preference_detail_list:
                    if hasattr(preference, 'preference'):
                        nodes.append({
                            "id": str(node_id),
                            "label": preference.preference[:20] + '...',
                            "size": 20 + node_id * 5,
                            "color": f"#{node_id * 50 % 255:02x}{node_id * 100 % 255:02x}{node_id * 150 % 255:02x}"
                        })
                        if node_id > 1:
                            edges.append({"source": str(node_id - 1), "target": str(node_id)})
                        node_id += 1
            
            return {"nodes": nodes, "edges": edges}
        except Exception as e:
            print(f"Get memory graph failed: {str(e)}")
            return {"nodes": [], "edges": []}


# 全局客户端实例
memos_client = MemOSClient()
