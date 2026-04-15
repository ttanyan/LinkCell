from models_provider.base_model_provider import BaseModelCredential

class AnthropicLLMCredential(BaseModelCredential):
    def is_valid(self, model_type, model_name, model_credential, 
                 model_params, provider, raise_exception=True):
        try:
            api_key = model_credential.get('api_key')
            
            if not api_key:
                if raise_exception:
                    raise ValueError('API key is required')
                return False
            
            # 这里可以添加实际的验证逻辑，比如调用Anthropic的API进行验证
            # 暂时返回True，模拟验证通过
            return True
        except Exception as e:
            if raise_exception:
                raise
            return False
    
    def encryption_dict(self, model_info):
        return model_info