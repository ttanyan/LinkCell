from models_provider.base_model_provider import BaseModelCredential

class OpenAILLMCredential(BaseModelCredential):
    def is_valid(self, model_type, model_name, model_credential, 
                 model_params, provider, raise_exception=True):
        try:
            api_key = model_credential.get('api_key')
            if not api_key:
                if raise_exception:
                    raise ValueError('API key is required')
                return False
            
            from openai import OpenAI
            client = OpenAI(
                api_key=api_key,
                base_url=model_credential.get('api_base')
            )
            client.models.list()
            return True
        except Exception as e:
            if raise_exception:
                raise
            return False
    
    def encryption_dict(self, model_info):
        credential = model_info.get('credential', {})
        encrypted_credential = {**credential}
        if 'api_key' in encrypted_credential:
            encrypted_credential['api_key'] = '******'
        return encrypted_credential