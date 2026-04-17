from django.urls import path, include
from apps.models_provider.views import ModelProviderList, ModelList, ModelCredentialValid, ModelCreate, ModelListAll, ModelDelete
from apps.application.views import ChatView, OpenAIChatView, DocumentUploadView, DocumentListView, DocumentDetailView, DocumentReindexView, DocumentStatusUpdateView

urlpatterns = [
    # 模型管理API
    path('api/model/provider/list', ModelProviderList.as_view(), name='model_provider_list'),
    path('api/model/provider/<str:provider>/model/list', ModelList.as_view(), name='model_list'),
    path('api/model/provider/<str:provider>/valid', ModelCredentialValid.as_view(), name='model_credential_valid'),
    path('api/model', ModelListAll.as_view(), name='model_list_all'),
    path('api/model/create', ModelCreate.as_view(), name='model_create'),
    path('api/model/<str:model_id>', ModelDelete.as_view(), name='model_delete'),
    
    # 对话API
    path('api/chat/<str:chat_id>/chat', ChatView.as_view(), name='chat'),
    path('api/application/<str:app_id>/chat/openai', OpenAIChatView.as_view(), name='openai_chat'),
    
    # 文档API
    path('api/documents', DocumentListView.as_view(), name='document_list'),
    path('api/documents/upload', DocumentUploadView.as_view(), name='document_upload'),
    path('api/documents/<str:document_id>', DocumentDetailView.as_view(), name='document_detail'),
    path('api/documents/<str:document_id>/reindex', DocumentReindexView.as_view(), name='document_reindex'),
    path('api/documents/<str:document_id>/update-status', DocumentStatusUpdateView.as_view(), name='document_status_update'),
    
    # 记忆管理API
    path('api/', include('apps.memos_integration.urls')),
]