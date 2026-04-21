from application.chat_pipeline.I_base_chat_pipeline import IBaseChatPipelineStep
from rest_framework.serializers import Serializer, CharField, ListField, BooleanField, UUIDField
from django.http import StreamingHttpResponse
from langchain_core.messages import AIMessageChunk
import uuid
from models_provider.tools import get_model_instance_by_model_workspace_id

class ChatStepSerializer(Serializer):
    message_list = ListField(required=True)
    model_id = UUIDField(required=True)
    stream = BooleanField(required=False, default=True)
    chat_id = UUIDField(required=True)
    problem_text = CharField(required=True)
    workspace_id = UUIDField(required=True)
    paragraph_list = ListField(required=False, default=list)

class BaseChatStep(IBaseChatPipelineStep):
    def get_step_serializer(self, manage):
        return ChatStepSerializer
    
    def _run(self, manage):
        args = self.context['step_args']
        chat_result = self.execute(
            message_list=args['message_list'],
            chat_id=args['chat_id'],
            problem_text=args['problem_text'],
            model_id=args['model_id'],
            workspace_id=args['workspace_id'],
            paragraph_list=args['paragraph_list'],
            stream=args['stream'],
            manage=manage
        )
        manage.context['chat_result'] = chat_result
    
    def execute(self, message_list, chat_id, problem_text, model_id, workspace_id, 
                paragraph_list=None, stream=True, manage=None, **kwargs):
        if paragraph_list is None:
            paragraph_list = []
        
        chat_model = get_model_instance_by_model_workspace_id(
            model_id, workspace_id, streaming=stream
        )
        
        if stream:
            return self.execute_stream(
                message_list, chat_id, problem_text, chat_model, 
                paragraph_list, manage, **kwargs
            )
        else:
            return self.execute_block(
                message_list, chat_id, problem_text, chat_model, 
                paragraph_list, manage, **kwargs
            )
    
    def execute_stream(self, message_list, chat_id, problem_text, chat_model, 
                      paragraph_list, manage, **kwargs):
        # 传递 problem_text 和 chat_id 给 get_stream_result
        chat_result, is_ai_chat, relevant_memories = self.get_stream_result(
            message_list, chat_model, paragraph_list, 
            problem_text=problem_text, chat_id=chat_id, **kwargs
        )
        
        chat_record_id = uuid.uuid4()
        
        response = StreamingHttpResponse(
            streaming_content=event_content(
                chat_result, chat_id, chat_record_id, 
                paragraph_list, manage, self, problem_text, chat_model, message_list, relevant_memories
            ),
            content_type='text/event-stream'
        )
        
        return response
    
    def execute_block(self, message_list, chat_id, problem_text, chat_model, 
                     paragraph_list, manage, **kwargs):
        # 直接使用原始消息列表，不添加记忆上下文
        enhanced_message_list = message_list.copy()
        
        # 调用模型
        result = chat_model.invoke(enhanced_message_list)
        
        try:
            request_token = chat_model.get_num_tokens_from_messages(enhanced_message_list)
        except Exception as e:
            request_token = 0
        
        try:
            response_token = chat_model.get_num_tokens(result.content)
        except Exception as e:
            response_token = 0
        
        self.context['message_tokens'] = request_token
        self.context['answer_tokens'] = response_token
        self.context['answer_text'] = result.content
        
        return {
            'content': result.content,
            'request_token': request_token,
            'answer_token': response_token
        }
    
    def get_stream_result(self, message_list, chat_model, paragraph_list, **kwargs):
        if chat_model is None:
            return iter([AIMessageChunk(content="模型未配置")]), False
        
        # 直接使用原始消息列表，不添加记忆上下文
        enhanced_message_list = message_list.copy()
        
        return chat_model.stream(enhanced_message_list), True, None

def event_content(response, chat_id, chat_record_id, paragraph_list, 
                 manage, step, problem_text, chat_model, message_list, relevant_memories):
    all_text = ''
    reasoning_content = ''
    
    # 直接使用原始消息列表
    enhanced_message_list = message_list.copy()
    
    try:
        for chunk in response:
            content_chunk = extract_content(chunk)
            reasoning_chunk = extract_reasoning_content(chunk)
            
            all_text += content_chunk
            reasoning_content += reasoning_chunk
            
            yield manage.base_to_response.to_stream_chunk_response(
                chat_id, chat_record_id, 'ai-chat-node',
                [], content_chunk, False, 0, 0,
                {'reasoning_content': reasoning_content}
            )
        
        try:
            request_token = chat_model.get_num_tokens_from_messages(enhanced_message_list)
        except Exception as e:
            request_token = 0
        
        try:
            response_token = chat_model.get_num_tokens(all_text)
        except Exception as e:
            response_token = 0
        
        step.context['message_tokens'] = request_token
        step.context['answer_tokens'] = response_token
        step.context['answer_text'] = all_text
        
        yield manage.base_to_response.to_stream_chunk_response(
            chat_id, chat_record_id, 'ai-chat-node',
            [], '', True, request_token, response_token,
            {'node_is_end': True}
        )
        
    except Exception as e:
        yield error_response(chat_id, chat_record_id, str(e))

def extract_content(chunk):
    if hasattr(chunk, 'content'):
        return chunk.content or ''
    return ''

def extract_reasoning_content(chunk):
    return ''

def process_messages(messages):
    """处理消息列表，确保所有消息都是纯字符串格式"""
    processed_messages = []
    for message in messages:
        # 检查是否是 LangChain 消息对象
        if hasattr(message, 'role') and hasattr(message, 'content'):
            processed_messages.append({
                'role': message.role,
                'content': message.content
            })
        # 检查是否是字典
        elif isinstance(message, dict) and 'role' in message and 'content' in message:
            # 确保 content 是字符串
            content = message['content']
            if hasattr(content, 'content'):
                content = content.content
            processed_messages.append({
                'role': message['role'],
                'content': str(content)
            })
    return processed_messages

def error_response(chat_id, chat_record_id, error_message):
    import json
    data = {
        'chat_id': str(chat_id),
        'record_id': str(chat_record_id),
        'node_id': 'ai-chat-node',
        'paragraph_list': [],
        'content': f'Error: {error_message}',
        'is_end': True,
        'request_token': 0,
        'answer_token': 0,
        'other': {'error': error_message}
    }
    return f"data: {json.dumps(data)}\n\n"