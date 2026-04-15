import time
from typing import Dict, List, Type
from application.chat_pipeline.I_base_chat_pipeline import IBaseChatPipelineStep

class PipelineManage:
    def __init__(self, step_list, base_to_response=None, debug=False):
        self.step_list = [step() for step in step_list]
        self.context = {
            'message_tokens': 0,
            'answer_tokens': 0,
            'start_time': None
        }
        self.base_to_response = base_to_response if base_to_response else SystemToResponse()
        self.debug = debug
    
    def run(self, context: Dict):
        self.context['start_time'] = time.time()
        self.context.update(context)
        
        for step in self.step_list:
            step.run(self)
        
        return self.context.get('chat_result')
    
    class Builder:
        def __init__(self):
            self.step_list = []
            self.base_to_response = SystemToResponse()
            self.debug = False
        
        def append_step(self, step_class: Type[IBaseChatPipelineStep]):
            self.step_list.append(step_class)
            return self
        
        def add_base_to_response(self, handler):
            self.base_to_response = handler
            return self
        
        def build(self):
            return PipelineManage(
                step_list=self.step_list,
                base_to_response=self.base_to_response,
                debug=self.debug
            )

class SystemToResponse:
    def to_stream_chunk_response(self, chat_id, record_id, node_id, 
                               paragraph_list, content, is_end, 
                               request_token, answer_token, other):
        import json
        data = {
            'chat_id': str(chat_id),
            'record_id': str(record_id),
            'node_id': node_id,
            'paragraph_list': paragraph_list,
            'content': content,
            'is_end': is_end,
            'request_token': request_token,
            'answer_token': answer_token,
            'other': other
        }
        return f"data: {json.dumps(data)}\n\n"