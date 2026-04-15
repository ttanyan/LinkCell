from models_provider.base_model_provider import BaseModelCredential

class BedrockLLMCredential(BaseModelCredential):
    def is_valid(self, model_type, model_name, model_credential, 
                 model_params, provider, raise_exception=True):
        try:
            access_key = model_credential.get('access_key')
            secret_key = model_credential.get('secret_key')
            region = model_credential.get('region')
            
            if not access_key:
                if raise_exception:
                    raise ValueError('Access key is required')
                return False
            
            if not secret_key:
                if raise_exception:
                    raise ValueError('Secret key is required')
                return False
            
            if not region:
                if raise_exception:
                    raise ValueError('Region is required')
                return False
            
            # 这里可以添加实际的验证逻辑，比如调用AWS Bedrock的API进行验证
            # 暂时返回True，模拟验证通过
            return True
        except Exception as e:
            if raise_exception:
                raise
            return False
    
    def encryption_dict(self, model_info):
        return model_info