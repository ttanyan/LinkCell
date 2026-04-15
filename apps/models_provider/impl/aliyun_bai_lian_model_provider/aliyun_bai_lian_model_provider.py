from models_provider.base_model_provider import IModelProvider, ModelInfo, ModelTypeConst, ModelInfoManage, ModelProvideInfo
from models_provider.impl.aliyun_bai_lian_model_provider.credential.llm import AliyunBaiLianLLMCredential
from models_provider.impl.aliyun_bai_lian_model_provider.model.llm import AliyunBaiLianChatModel
import os
from models_provider.utils import get_file_content

aliyun_bai_lian_llm_model_credential = AliyunBaiLianLLMCredential()

model_info_list = [
    ModelInfo('qwen-plus', '阿里云百炼 qwen-plus', ModelTypeConst.LLM, 
              aliyun_bai_lian_llm_model_credential, AliyunBaiLianChatModel
              ),
    ModelInfo('qwen-max', '阿里云百炼 qwen-max', ModelTypeConst.LLM, 
              aliyun_bai_lian_llm_model_credential, AliyunBaiLianChatModel
              ),
    ModelInfo('qwen-turbo', '阿里云百炼 qwen-turbo', ModelTypeConst.LLM, 
              aliyun_bai_lian_llm_model_credential, AliyunBaiLianChatModel
              ),
]

model_info_manage = (
    ModelInfoManage.builder()
    .append_model_info_list(model_info_list)
    .append_default_model_info(ModelInfo('qwen-plus', '阿里云百炼 qwen-plus', ModelTypeConst.LLM, 
                                         aliyun_bai_lian_llm_model_credential, AliyunBaiLianChatModel
                                         ))
    .build()
)

class AliyunBaiLianModelProvider(IModelProvider):
    def get_model_info_manage(self):
        return model_info_manage
    
    def get_model_provide_info(self):
        return ModelProvideInfo(provider='aliyun_bai_lian_model_provider', name='阿里云百炼', icon='aliyun')