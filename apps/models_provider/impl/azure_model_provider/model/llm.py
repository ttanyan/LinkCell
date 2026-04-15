from models_provider.base_model_provider import MaxKBBaseModel
from langchain_openai import AzureChatOpenAI

class AzureChatModel(MaxKBBaseModel, AzureChatOpenAI):
    @staticmethod
    def is_cache_model():
        return False
    
    @staticmethod
    def new_instance(model_type, model_name, model_credential, **kwargs):
        optional_params = MaxKBBaseModel.filter_optional_params(kwargs)
        return AzureChatModel(
            deployment_name=model_credential.get('deployment_name'),
            openai_api_version=model_credential.get('api_version', '2024-02-15-preview'),
            openai_api_key=model_credential.get('api_key'),
            openai_api_base=model_credential.get('api_base'),
            streaming=kwargs.get('streaming', True),
            **optional_params
        )