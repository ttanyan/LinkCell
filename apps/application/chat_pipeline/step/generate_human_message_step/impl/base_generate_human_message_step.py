from application.chat_pipeline.I_base_chat_pipeline import IBaseChatPipelineStep
from rest_framework.serializers import Serializer, CharField, ListField, IntegerField
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

def flat_map(lst):
    result = []
    for item in lst:
        result.extend(item)
    return result

class GenerateHumanMessageSerializer(Serializer):
    problem_text = CharField(required=True)
    paragraph_list = ListField(required=False, default=list)
    history_chat_record = ListField(required=False, default=list)
    prompt = CharField(required=False, default='')
    dialogue_number = IntegerField(required=False, default=3)
    max_paragraph_char_number = IntegerField(required=False, default=2000)

class BaseGenerateHumanMessageStep(IBaseChatPipelineStep):
    def get_step_serializer(self, manage):
        return GenerateHumanMessageSerializer
    
    def _run(self, manage):
        args = self.context['step_args']
        message_list = self.execute(**args)
        manage.context['message_list'] = message_list
    
    def execute(self, problem_text, paragraph_list=None, history_chat_record=None, 
                dialogue_number=3, max_paragraph_char_number=2000, prompt='', **kwargs):
        if paragraph_list is None:
            paragraph_list = []
        if history_chat_record is None:
            history_chat_record = []
        
        system_prompt = prompt if prompt else 'You are a helpful assistant.'
        
        start_index = len(history_chat_record) - dialogue_number
        if start_index < 0:
            start_index = 0
        
        history_messages = []
        for record in history_chat_record[start_index:]:
            human_msg = HumanMessage(content=record.get('problem_text', ''))
            ai_msg = AIMessage(content=record.get('answer_text', ''))
            history_messages.append([human_msg, ai_msg])
        
        current_message = self.to_human_message(
            system_prompt, problem_text, max_paragraph_char_number, paragraph_list
        )
        
        return [
            SystemMessage(content=system_prompt),
            *flat_map(history_messages),
            current_message
        ]
    
    def to_human_message(self, prompt, problem_text, max_paragraph_char_number, paragraph_list):
        context = '\n'.join([p.get('content', '') for p in paragraph_list])
        if len(context) > max_paragraph_char_number:
            context = context[:max_paragraph_char_number] + '...'
        
        if context:
            content = f"Context:\n{context}\n\nQuestion:{problem_text}"
        else:
            content = problem_text
        
        return HumanMessage(content=content)