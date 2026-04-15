from enum import Enum
from models_provider.impl.openai_model_provider.openai_model_provider import OpenAIModelProvider
from models_provider.impl.aliyun_bai_lian_model_provider.aliyun_bai_lian_model_provider import AliyunBaiLianModelProvider
from models_provider.impl.anthropic_model_provider.anthropic_model_provider import AnthropicModelProvider
from models_provider.impl.aws_bedrock_model_provider.aws_bedrock_model_provider import BedrockModelProvider
from models_provider.impl.azure_model_provider.azure_model_provider import AzureModelProvider
from models_provider.impl.deepseek_model_provider.deepseek_model_provider import DeepSeekModelProvider

class ModelProvideConstants(Enum):
    model_openai_provider = OpenAIModelProvider()
    aliyun_bai_lian_model_provider = AliyunBaiLianModelProvider()
    model_anthropic_provider = AnthropicModelProvider()
    model_aws_bedrock_provider = BedrockModelProvider()
    model_azure_provider = AzureModelProvider()
    model_deepseek_provider = DeepSeekModelProvider()

    @classmethod
    def get_provider(cls, provider_name):
        for member in cls:
            if member.name == provider_name:
                return member.value
        return None

    @classmethod
    def get_all_providers(cls):
        return [member.value for member in cls]