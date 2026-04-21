"""MemOS URLs"""

from django.urls import path
from .views import (
    MemoryListView,
    MemoryGraphView,
    MemoryCreateView,
    MemoryUpdateView,
    MemoryDeleteView,
    MemorySearchView,
    MemoryAddView,
    ConversationCreateView,
    DocumentUploadView,
    RAGRetrieveView,
    LLMContextView
)

urlpatterns = [
    # 记忆管理
    path('memos/list', MemoryListView.as_view(), name='memory-list'),
    path('memos/graph', MemoryGraphView.as_view(), name='memory-graph'),
    path('memos/create', MemoryCreateView.as_view(), name='memory-create'),
    path('memos/update/<str:memory_id>', MemoryUpdateView.as_view(), name='memory-update'),
    path('memos/delete/<str:memory_id>', MemoryDeleteView.as_view(), name='memory-delete'),
    path('memos/search', MemorySearchView.as_view(), name='memory-search'),
    path('memos/add', MemoryAddView.as_view(), name='memory-add'),
    
    # 会话管理
    path('conversations/create', ConversationCreateView.as_view(), name='conversation-create'),
    
    # 文档管理
    path('documents/upload', DocumentUploadView.as_view(), name='document-upload'),
    
    # 智能语义检索
    path('rag/retrieve', RAGRetrieveView.as_view(), name='rag-retrieve'),
    
    # 大模型增强
    path('llm/context', LLMContextView.as_view(), name='llm-context'),
]
