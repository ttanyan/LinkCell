from models_provider.base_model_provider import IModelProvider, ModelInfo, ModelTypeConst, ModelInfoManage, ModelProvideInfo
from models_provider.impl.azure_model_provider.credential.llm import AzureLLMCredential
from models_provider.impl.azure_model_provider.model.llm import AzureChatModel

azure_llm_model_credential = AzureLLMCredential()

model_info_list = [
    ModelInfo('gpt-4', 'Azure OpenAI GPT-4', ModelTypeConst.LLM, 
              azure_llm_model_credential, AzureChatModel
              ),
    ModelInfo('gpt-4-turbo', 'Azure OpenAI GPT-4 Turbo', ModelTypeConst.LLM, 
              azure_llm_model_credential, AzureChatModel
              ),
    ModelInfo('gpt-35-turbo', 'Azure OpenAI GPT-3.5 Turbo', ModelTypeConst.LLM, 
              azure_llm_model_credential, AzureChatModel
              ),
    ModelInfo('gpt-35-turbo-16k', 'Azure OpenAI GPT-3.5 Turbo 16K', ModelTypeConst.LLM, 
              azure_llm_model_credential, AzureChatModel
              ),
]

model_info_manage = (
    ModelInfoManage.builder()
    .append_model_info_list(model_info_list)
    .append_default_model_info(ModelInfo('gpt-35-turbo', 'Azure OpenAI GPT-3.5 Turbo', ModelTypeConst.LLM, 
                                         azure_llm_model_credential, AzureChatModel
                                         ))
    .build()
)

class AzureModelProvider(IModelProvider):
    def get_model_info_manage(self):
        return model_info_manage
    
    def get_model_provide_info(self):
        return ModelProvideInfo(provider='model_azure_provider', name='Azure OpenAI', icon='azure')