from models_provider.base_model_provider import MaxKBBaseModel
from langchain_aws import ChatBedrock

class BedrockChatModel(MaxKBBaseModel, ChatBedrock):
    @staticmethod
    def is_cache_model():
        return False
    
    @staticmethod
    def new_instance(model_type, model_name, model_credential, **kwargs):
        optional_params = MaxKBBaseModel.filter_optional_params(kwargs)
        return BedrockChatModel(
            model_id=model_name,
            region_name=model_credential.get('region'),
            aws_access_key_id=model_credential.get('access_key'),
            aws_secret_access_key=model_credential.get('secret_key'),
            streaming=kwargs.get('streaming', True),
            **optional_params
        )