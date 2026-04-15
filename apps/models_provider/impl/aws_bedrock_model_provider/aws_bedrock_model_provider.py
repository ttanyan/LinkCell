from models_provider.base_model_provider import IModelProvider, ModelInfo, ModelTypeConst, ModelInfoManage, ModelProvideInfo
from models_provider.impl.aws_bedrock_model_provider.credential.llm import BedrockLLMCredential
from models_provider.impl.aws_bedrock_model_provider.model.llm import BedrockChatModel

bedrock_llm_model_credential = BedrockLLMCredential()

model_info_list = [
    ModelInfo('anthropic.claude-3-opus-20240229-v1:0', 'AWS Bedrock Claude 3 Opus', ModelTypeConst.LLM, 
              bedrock_llm_model_credential, BedrockChatModel
              ),
    ModelInfo('anthropic.claude-3-sonnet-20240229-v1:0', 'AWS Bedrock Claude 3 Sonnet', ModelTypeConst.LLM, 
              bedrock_llm_model_credential, BedrockChatModel
              ),
    ModelInfo('anthropic.claude-3-haiku-20240307-v1:0', 'AWS Bedrock Claude 3 Haiku', ModelTypeConst.LLM, 
              bedrock_llm_model_credential, BedrockChatModel
              ),
    ModelInfo('anthropic.claude-2.1', 'AWS Bedrock Claude 2.1', ModelTypeConst.LLM, 
              bedrock_llm_model_credential, BedrockChatModel
              ),
    ModelInfo('anthropic.claude-2', 'AWS Bedrock Claude 2', ModelTypeConst.LLM, 
              bedrock_llm_model_credential, BedrockChatModel
              ),
    ModelInfo('meta.llama3-8b-instruct-v1:0', 'AWS Bedrock Llama 3 8B', ModelTypeConst.LLM, 
              bedrock_llm_model_credential, BedrockChatModel
              ),
    ModelInfo('meta.llama3-70b-instruct-v1:0', 'AWS Bedrock Llama 3 70B', ModelTypeConst.LLM, 
              bedrock_llm_model_credential, BedrockChatModel
              ),
]

model_info_manage = (
    ModelInfoManage.builder()
    .append_model_info_list(model_info_list)
    .append_default_model_info(ModelInfo('anthropic.claude-3-sonnet-20240229-v1:0', 'AWS Bedrock Claude 3 Sonnet', ModelTypeConst.LLM, 
                                         bedrock_llm_model_credential, BedrockChatModel
                                         ))
    .build()
)

class BedrockModelProvider(IModelProvider):
    def get_model_info_manage(self):
        return model_info_manage
    
    def get_model_provide_info(self):
        return ModelProvideInfo(provider='model_aws_bedrock_provider', name='Amazon Bedrock', icon='bedrock')