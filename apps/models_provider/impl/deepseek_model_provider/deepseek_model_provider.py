from models_provider.base_model_provider import IModelProvider, ModelInfo, ModelTypeConst, ModelInfoManage, ModelProvideInfo
from models_provider.impl.deepseek_model_provider.credential.llm import DeepSeekLLMCredential
from models_provider.impl.deepseek_model_provider.model.llm import DeepSeekChatModel

deepseek_llm_model_credential = DeepSeekLLMCredential()

model_info_list = [
    ModelInfo('deepseek-chat', 'DeepSeek Chat', ModelTypeConst.LLM, 
              deepseek_llm_model_credential, DeepSeekChatModel
              ),
    ModelInfo('deepseek-coder', 'DeepSeek Coder', ModelTypeConst.LLM, 
              deepseek_llm_model_credential, DeepSeekChatModel
              ),
    ModelInfo('deepseek-llm', 'DeepSeek LLM', ModelTypeConst.LLM, 
              deepseek_llm_model_credential, DeepSeekChatModel
              ),
]

model_info_manage = (
    ModelInfoManage.builder()
    .append_model_info_list(model_info_list)
    .append_default_model_info(ModelInfo('deepseek-chat', 'DeepSeek Chat', ModelTypeConst.LLM, 
                                         deepseek_llm_model_credential, DeepSeekChatModel
                                         ))
    .build()
)

class DeepSeekModelProvider(IModelProvider):
    def get_model_info_manage(self):
        return model_info_manage
    
    def get_model_provide_info(self):
        return ModelProvideInfo(provider='model_deepseek_provider', name='DeepSeek', icon='deepseek')