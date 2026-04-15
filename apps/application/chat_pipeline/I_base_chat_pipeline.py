from abc import ABC, abstractmethod
from typing import Type, Dict
from rest_framework.serializers import Serializer

class IBaseChatPipelineStep(ABC):
    def __init__(self):
        self.context = {}
    
    def run(self, manage):
        import time
        start_time = time.time()
        self.valid_args(manage)
        self._run(manage)
        self.context['run_time'] = time.time() - start_time
    
    def valid_args(self, manage):
        serializer_class = self.get_step_serializer(manage)
        serializer = serializer_class(data=manage.context)
        serializer.is_valid(raise_exception=True)
        self.context['step_args'] = serializer.data
    
    @abstractmethod
    def get_step_serializer(self, manage) -> Type[Serializer]:
        pass
    
    @abstractmethod
    def _run(self, manage):
        pass
    
    def execute(self, **kwargs):
        pass