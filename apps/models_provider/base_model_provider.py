from abc import ABC, abstractmethod
from enum import Enum
from functools import reduce
from typing import Dict, Type, List

class ModelTypeConst(Enum):
    LLM = {'code': 'LLM', 'message': 'LLM'}
    EMBEDDING = {'code': 'EMBEDDING', 'message': 'Embedding Model'}
    STT = {'code': 'STT', 'message': 'Speech2Text'}
    TTS = {'code': 'TTS', 'message': 'TTS'}
    IMAGE = {'code': 'IMAGE', 'message': 'Vision Model'}
    TTI = {'code': 'TTI', 'message': 'Image Generation'}
    RERANKER = {'code': 'RERANKER', 'message': 'Rerank'}
    TTV = {'code': 'TTV', 'message': 'Text to Video'}
    ITV = {'code': 'ITV', 'message': 'Image to Video'}

class MaxKBBaseModel(ABC):
    @staticmethod
    @abstractmethod
    def new_instance(model_type, model_name, model_credential, **model_kwargs):
        pass
    
    @staticmethod
    def is_cache_model():
        return True
    
    @staticmethod
    def filter_optional_params(model_kwargs):
        optional_params = {}
        for key, value in model_kwargs.items():
            if key not in ['model_id', 'use_local', 'streaming', 'show_ref_label', 'stream']:
                if key == 'extra_body' and isinstance(value, dict):
                    optional_params = {**optional_params, **value}
                else:
                    optional_params[key] = value
        return optional_params

class BaseModelCredential(ABC):
    @abstractmethod
    def is_valid(self, model_type, model_name, model_credential, 
                 model_params, provider, raise_exception=True):
        pass
    
    @abstractmethod
    def encryption_dict(self, model_info):
        pass
    
    def get_model_params_setting_form(self, model_name):
        pass
    
    @staticmethod
    def encryption(message):
        return message

class ModelInfo:
    def __init__(self, name, desc, model_type, model_credential, model_class, **keywords):
        self.name = name
        self.desc = desc
        self.model_type = model_type.name if hasattr(model_type, 'name') else model_type
        self.model_credential = model_credential
        self.model_class = model_class
        if keywords:
            for key in keywords:
                setattr(self, key, keywords.get(key))
    
    def get_name(self):
        return self.name
    
    def get_desc(self):
        return self.desc
    
    def get_model_type(self):
        return self.model_type
    
    def get_model_class(self):
        return self.model_class
    
    def to_dict(self):
        return reduce(lambda x, y: {**x, **y}, 
                      [{attr: getattr(self, attr)} for attr in vars(self) if 
                       not attr.startswith("__") and not attr == 'model_credential' and not attr == 'model_class'], {})

class IModelProvider(ABC):
    @abstractmethod
    def get_model_info_manage(self):
        pass
    
    @abstractmethod
    def get_model_provide_info(self):
        pass
    
    def get_model_type_list(self):
        return self.get_model_info_manage().get_model_type_list()
    
    def get_model(self, model_type, model_name, model_credential, **kwargs):
        model_info = self.get_model_info_manage().get_model_info(model_type, model_name)
        return model_info.model_class.new_instance(
            model_type, model_name, model_credential, **kwargs
        )
    
    def get_model_list(self, model_type):
        return self.get_model_info_manage().get_model_list_by_model_type(model_type)
    
    def is_valid_credential(self, model_type, model_name, 
                           model_credential, model_params, raise_exception=False):
        model_info = self.get_model_info_manage().get_model_info(model_type, model_name)
        return model_info.model_credential.is_valid(
            model_type, model_name, model_credential, model_params, self, raise_exception=raise_exception
        )
    
    def get_dialogue_number(self):
        return 3

class ModelProvideInfo:
    def __init__(self, provider, name, icon):
        self.provider = provider
        self.name = name
        self.icon = icon
    
    def to_dict(self):
        return reduce(lambda x, y: {**x, **y}, 
                      [{attr: getattr(self, attr)} for attr in vars(self) if 
                       not attr.startswith("__")], {})

class ModelInfoManage:
    def __init__(self):
        self.model_dict = {}
        self.model_list = []
        self.default_model_list = []
        self.default_model_dict = {}
    
    def append_model_info(self, model_info):
        self.model_list.append(model_info)
        model_type_dict = self.model_dict.get(model_info.model_type)
        if model_type_dict is None:
            self.model_dict[model_info.model_type] = {model_info.name: model_info}
        else:
            model_type_dict[model_info.name] = model_info
    
    def append_default_model_info(self, model_info):
        self.default_model_list.append(model_info)
        self.default_model_dict[model_info.model_type] = model_info
    
    def get_model_list(self):
        return [model.to_dict() for model in self.model_list]
    
    def get_model_list_by_model_type(self, model_type):
        return [model.to_dict() for model in self.model_list if model.model_type == model_type]
    
    def get_model_type_list(self):
        return [{'key': _type.value.get('message'), 'value': _type.value.get('code')} for _type in ModelTypeConst if 
                len([model for model in self.model_list if model.model_type == _type.name]) > 0]
    
    def get_model_info(self, model_type, model_name):
        # 首先尝试从预定义模型列表中获取
        model_info = self.model_dict.get(model_type, {}).get(model_name)
        # 如果没有找到，使用默认模型的配置
        if model_info is None:
            model_info = self.default_model_dict.get(model_type)
            if model_info is None:
                raise ValueError(f"Model {model_name} not found for type {model_type}")
            # 创建一个新的 ModelInfo 对象，使用用户输入的模型名称
            model_info = ModelInfo(
                name=model_name,
                desc=model_info.desc,
                model_type=model_info.model_type,
                model_credential=model_info.model_credential,
                model_class=model_info.model_class
            )
        return model_info
    
    class builder:
        def __init__(self):
            self.modelInfoManage = ModelInfoManage()
        
        def append_model_info(self, model_info):
            self.modelInfoManage.append_model_info(model_info)
            return self
        
        def append_model_info_list(self, model_info_list):
            for model_info in model_info_list:
                self.modelInfoManage.append_model_info(model_info)
            return self
        
        def append_default_model_info(self, model_info):
            self.modelInfoManage.append_default_model_info(model_info)
            return self
        
        def build(self):
            return self.modelInfoManage