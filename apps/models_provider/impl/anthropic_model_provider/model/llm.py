from models_provider.base_model_provider import MaxKBBaseModel
from langchain_anthropic import ChatAnthropic

class AnthropicChatModel(MaxKBBaseModel, ChatAnthropic):
    @staticmethod
    def is_cache_model():
        return False
    
    @staticmethod
    def new_instance(model_type, model_name, model_credential, **kwargs):
        optional_params = MaxKBBaseModel.filter_optional_params(kwargs)
        return AnthropicChatModel(
            model=model_name,
            anthropic_api_key=model_credential.get('api_key'),
            streaming=kwargs.get('streaming', True),
            **optional_params
        )