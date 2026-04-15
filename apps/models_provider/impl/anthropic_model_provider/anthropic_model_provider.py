from models_provider.base_model_provider import IModelProvider, ModelInfo, ModelTypeConst, ModelInfoManage, ModelProvideInfo
from models_provider.impl.anthropic_model_provider.credential.llm import AnthropicLLMCredential
from models_provider.impl.anthropic_model_provider.model.llm import AnthropicChatModel

anthropic_llm_model_credential = AnthropicLLMCredential()

model_info_list = [
    ModelInfo('claude-3-opus-20240229', 'Anthropic Claude 3 Opus', ModelTypeConst.LLM, 
              anthropic_llm_model_credential, AnthropicChatModel
              ),
    ModelInfo('claude-3-sonnet-20240229', 'Anthropic Claude 3 Sonnet', ModelTypeConst.LLM, 
              anthropic_llm_model_credential, AnthropicChatModel
              ),
    ModelInfo('claude-3-haiku-20240307', 'Anthropic Claude 3 Haiku', ModelTypeConst.LLM, 
              anthropic_llm_model_credential, AnthropicChatModel
              ),
    ModelInfo('claude-2.1', 'Anthropic Claude 2.1', ModelTypeConst.LLM, 
              anthropic_llm_model_credential, AnthropicChatModel
              ),
    ModelInfo('claude-2', 'Anthropic Claude 2', ModelTypeConst.LLM, 
              anthropic_llm_model_credential, AnthropicChatModel
              ),
]

model_info_manage = (
    ModelInfoManage.builder()
    .append_model_info_list(model_info_list)
    .append_default_model_info(ModelInfo('claude-3-sonnet-20240229', 'Anthropic Claude 3 Sonnet', ModelTypeConst.LLM, 
                                         anthropic_llm_model_credential, AnthropicChatModel
                                         ))
    .build()
)

class AnthropicModelProvider(IModelProvider):
    def get_model_info_manage(self):
        return model_info_manage
    
    def get_model_provide_info(self):
        return ModelProvideInfo(provider='model_anthropic_provider', name='Anthropic', icon='anthropic')