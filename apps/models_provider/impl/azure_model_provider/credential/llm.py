from models_provider.base_model_provider import BaseModelCredential

class AzureLLMCredential(BaseModelCredential):
    def is_valid(self, model_type, model_name, model_credential, 
                 model_params, provider, raise_exception=True):
        try:
            api_key = model_credential.get('api_key')
            api_base = model_credential.get('api_base')
            api_version = model_credential.get('api_version', '2024-02-15-preview')
            deployment_name = model_credential.get('deployment_name')
            
            if not api_key:
                if raise_exception:
                    raise ValueError('API key is required')
                return False
            
            if not api_base:
                if raise_exception:
                    raise ValueError('API base is required')
                return False
            
            if not deployment_name:
                if raise_exception:
                    raise ValueError('Deployment name is required')
                return False
            
            # 这里可以添加实际的验证逻辑，比如调用Azure OpenAI的API进行验证
            # 暂时返回True，模拟验证通过
            return True
        except Exception as e:
            if raise_exception:
                raise
            return False
    
    def encryption_dict(self, model_info):
        return model_info