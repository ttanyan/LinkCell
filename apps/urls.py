from django.urls import path
from models_provider.views import ModelProviderList, ModelList, ModelCredentialValid, ModelCreate, ModelListAll
from application.views import ChatView, OpenAIChatView

urlpatterns = [
    # 模型管理API
    path('api/model/provider/list', ModelProviderList.as_view(), name='model_provider_list'),
    path('api/model/provider/<str:provider>/model/list', ModelList.as_view(), name='model_list'),
    path('api/model/provider/<str:provider>/valid', ModelCredentialValid.as_view(), name='model_credential_valid'),
    path('api/model', ModelListAll.as_view(), name='model_list_all'),
    path('api/model/create', ModelCreate.as_view(), name='model_create'),
    
    # 对话API
    path('api/chat/<str:chat_id>/chat', ChatView.as_view(), name='chat'),
    path('api/application/<str:app_id>/chat/openai', OpenAIChatView.as_view(), name='openai_chat'),
]