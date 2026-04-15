from models_provider.base_model_provider import IModelProvider, ModelInfo, ModelTypeConst, ModelInfoManage, ModelProvideInfo
from models_provider.impl.openai_model_provider.credential.llm import OpenAILLMCredential
from models_provider.impl.openai_model_provider.model.llm import OpenAIChatModel

openai_llm_model_credential = OpenAILLMCredential()

model_info_list = [
    ModelInfo('gpt-3.5-turbo', 'The latest gpt-3.5-turbo, updated with OpenAI adjustments', ModelTypeConst.LLM, 
              openai_llm_model_credential, OpenAIChatModel
              ),
    ModelInfo('gpt-4', 'Latest gpt-4, updated with OpenAI adjustments', ModelTypeConst.LLM, openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-4o', 'The latest GPT-4o, cheaper and faster than gpt-4-turbo, updated with OpenAI adjustments', 
              ModelTypeConst.LLM, openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-4o-mini', 'The latest gpt-4o-mini, cheaper and faster than gpt-4o, updated with OpenAI adjustments', 
              ModelTypeConst.LLM, openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-4-turbo', 'The latest gpt-4-turbo, updated with OpenAI adjustments', ModelTypeConst.LLM, 
              openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-3.5-turbo-0125', 
              'gpt-3.5-turbo snapshot on January 25, 2024, supporting context length 16,385 tokens', ModelTypeConst.LLM, 
              openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-3.5-turbo-1106', 
              'gpt-3.5-turbo snapshot on November 6, 2023, supporting context length 16,385 tokens', ModelTypeConst.LLM, 
              openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-3.5-turbo-0613', 
              '[Legacy] gpt-3.5-turbo snapshot on June 13, 2023, will be deprecated on June 13, 2024', 
              ModelTypeConst.LLM, openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-4o-2024-05-13', 
              'gpt-4o snapshot on May 13, 2024, supporting context length 128,000 tokens', 
              ModelTypeConst.LLM, openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-4-turbo-2024-04-09', 
              'gpt-4-turbo snapshot on April 9, 2024, supporting context length 128,000 tokens', 
              ModelTypeConst.LLM, openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-4-0125-preview', 'gpt-4-turbo snapshot on January 25, 2024, supporting context length 128,000 tokens', 
              ModelTypeConst.LLM, openai_llm_model_credential, 
              OpenAIChatModel),
    ModelInfo('gpt-4-1106-preview', 'gpt-4-turbo snapshot on November 6, 2023, supporting context length 128,000 tokens', 
              ModelTypeConst.LLM, openai_llm_model_credential, 
              OpenAIChatModel),
]

model_info_manage = (
    ModelInfoManage.builder()
    .append_model_info_list(model_info_list)
    .append_default_model_info(ModelInfo('gpt-3.5-turbo', 'The latest gpt-3.5-turbo, updated with OpenAI adjustments', ModelTypeConst.LLM, 
                                         openai_llm_model_credential, OpenAIChatModel
                                         ))
    .build()
)

class OpenAIModelProvider(IModelProvider):
    def get_model_info_manage(self):
        return model_info_manage
    
    def get_model_provide_info(self):
        return ModelProvideInfo(provider='model_openai_provider', name='OpenAI', icon='openai')