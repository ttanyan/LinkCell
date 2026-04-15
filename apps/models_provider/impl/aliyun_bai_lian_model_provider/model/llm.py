from models_provider.base_model_provider import MaxKBBaseModel
from langchain_openai import ChatOpenAI

class AliyunBaiLianChatModel(MaxKBBaseModel, ChatOpenAI):
    @staticmethod
    def is_cache_model():
        return False
    
    @staticmethod
    def new_instance(model_type, model_name, model_credential, **kwargs):
        optional_params = MaxKBBaseModel.filter_optional_params(kwargs)
        return AliyunBaiLianChatModel(
            model=model_name,
            openai_api_base=model_credential.get('api_url'),
            openai_api_key=model_credential.get('api_key'),
            streaming=kwargs.get('streaming', True),
            extra_body=optional_params
        )