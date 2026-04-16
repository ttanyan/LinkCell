from pageindex import PageIndexClient
from django.conf import settings

class PageIndexClientManager:
    """PageIndex客户端管理器，负责管理客户端的生命周期"""
    
    _instance = None
    
    @classmethod
    def get_client(cls):
        """获取PageIndex客户端实例"""
        if cls._instance is None:
            cls._instance = PageIndexClient(api_key=settings.PAGEINDEX_API_KEY)
        return cls._instance
    
    @classmethod
    def reset_client(cls):
        """重置客户端实例，用于重新初始化"""
        cls._instance = None
        return cls.get_client()
