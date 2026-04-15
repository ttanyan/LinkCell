from models_provider.base_model_provider import MaxKBBaseModel
from models_provider.impl.base_chat_open_ai import BaseChatOpenAI

class OpenAIChatModel(MaxKBBaseModel, BaseChatOpenAI):
    @staticmethod
    def is_cache_model():
        return False
    
    @staticmethod
    def new_instance(model_type, model_name, model_credential, **kwargs):
        optional_params = MaxKBBaseModel.filter_optional_params(kwargs)
        streaming = kwargs.get('streaming', True)
        if 'o1' in model_name:
            streaming = False
        return OpenAIChatModel(
            model=model_name,
            openai_api_base=model_credential.get('api_base'),
            openai_api_key=model_credential.get('api_key'),
            extra_body=optional_params,
            streaming=streaming
        )