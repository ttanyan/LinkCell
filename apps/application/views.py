from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from apps.application.chat_pipeline.pipeline_manage import PipelineManage
from apps.application.chat_pipeline.step.generate_human_message_step.impl.base_generate_human_message_step import BaseGenerateHumanMessageStep
from apps.application.chat_pipeline.step.chat_step.impl.base_chat_step import BaseChatStep
from apps.application.utils.pageindex_client import PageIndexClientManager
from apps.application.models.document import Document
from apps.memos_integration.client import memos_client
import uuid
import os
from django.conf import settings

def build_memory_prompt(memory_data, user_query):
    """
    构建记忆Prompt
    :param memory_data: MemOS SDK返回的完整记忆数据
    :param user_query: 用户当前输入的问题原文
    :return: 拼接完成的结构化记忆Prompt字符串，无记忆时返回空字符串
    """
    try:
        if not memory_data:
            return ""
        
        # 第一步：先校验接口返回状态
        if hasattr(memory_data, 'code') and memory_data.code != 0:
            print(f"Memory search failed with code: {memory_data.code}")
            return ""
        
        # 从memory_data.data中提取数据
        memory_data_inner = getattr(memory_data, 'data', memory_data)
        if not memory_data_inner:
            print("No data in memory response")
            return ""
        
        # 数据预处理
        memory_detail_list = getattr(memory_data_inner, 'memory_detail_list', []) or []
        preference_detail_list = getattr(memory_data_inner, 'preference_detail_list', []) or []
        preference_note = getattr(memory_data_inner, 'preference_note', '') or "请结合上述用户记忆，给出自然、有温度、贴合用户情况的回答，禁止编造不存在的记忆。"
        
        print(f"Extracted memory_detail_list: {memory_detail_list}")
        print(f"Extracted preference_detail_list: {preference_detail_list}")
        
        # 按relativity相关性从高到低排序
        memory_detail_list.sort(key=lambda x: getattr(x, 'relativity', 0), reverse=True)
        preference_detail_list.sort(key=lambda x: getattr(x, 'relativity', 0), reverse=True)
        
        # 长度控制
        memory_detail_list = memory_detail_list[:5]  # 最多取前5条
        preference_detail_list = preference_detail_list[:3]  # 最多取前3条
        
        if not memory_detail_list and not preference_detail_list:
            return ""
        
        # 结构化拼接
        prompt_parts = []
        prompt_parts.append("# 【用户专属记忆档案】")
        prompt_parts.append("以下是关于当前用户的真实记忆信息，你必须严格基于这些信息回答问题，绝对不得违背用户的任何偏好，回答需贴合用户的个人情况，给出个性化内容。")
        prompt_parts.append("")
        prompt_parts.append("---")
        prompt_parts.append("")
        
        # 1. 事实记忆
        if memory_detail_list:
            prompt_parts.append("## 1. 关于用户的事实记忆")
            for memory in memory_detail_list:
                memory_key = getattr(memory, 'memory_key', '')
                memory_value = getattr(memory, 'memory_value', '')
                tags = getattr(memory, 'tags', []) or []
                confidence = getattr(memory, 'confidence', 0)
                
                if memory_value:
                    tags_str = ", ".join(tags) if tags else "无"
                    prompt_parts.append(f"- 【{memory_key}】：{memory_value}")
                    prompt_parts.append(f"  标签：{tags_str} | 置信度：{confidence}")
            prompt_parts.append("")
            prompt_parts.append("---")
            prompt_parts.append("")
        
        # 2. 用户偏好
        if preference_detail_list:
            prompt_parts.append("## 2. 用户的核心偏好（必须100%遵守）")
            for pref in preference_detail_list:
                preference = getattr(pref, 'preference', '')
                reasoning = getattr(pref, 'reasoning', '')
                
                if preference:
                    prompt_parts.append(f"- ✅ 必须遵守：{preference}")
                    if reasoning:
                        prompt_parts.append(f"  偏好说明：{reasoning}")
            prompt_parts.append("")
            prompt_parts.append("---")
            prompt_parts.append("")
        
        # 3. 回答规则
        prompt_parts.append("## 3. 回答规则")
        prompt_parts.append(preference_note)
        prompt_parts.append("")
        prompt_parts.append("---")
        prompt_parts.append("")
        
        # 用户当前问题
        prompt_parts.append(f"【用户当前的问题】：{user_query}")
        prompt_parts.append("")
        prompt_parts.append("【你的回答】：")
        
        final_prompt = "\n".join(prompt_parts)
        print(f"Built memory prompt: {final_prompt}")
        return final_prompt
    except Exception as e:
        print(f"Error building memory prompt: {e}")
        return ""

class ChatView(APIView):
    def post(self, request, chat_id):
        data = request.data
        message = data.get('message')
        stream = data.get('stream', True)
        selected_documents = data.get('selected_documents', [])
        
        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            chat_id = uuid.UUID(chat_id)
        except ValueError:
            return Response({'error': 'Invalid chat_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 如果选择了文档，使用PageIndex进行对话
        if selected_documents:
            try:
                # 获取PageIndex客户端实例
                pi = PageIndexClientManager.get_client()
                
                # 获取文档的pageindex_id
                pageindex_ids = []
                for doc_id in selected_documents:
                    try:
                        doc = Document.objects.get(id=doc_id)
                        if doc.pageindex_id:
                            pageindex_ids.append(doc.pageindex_id)
                    except Document.DoesNotExist:
                        pass
                
                if pageindex_ids:
                    # 使用PageIndex的Chat API
                    response = pi.chat_completions(
                        messages=[{"role": "user", "content": message}],
                        doc_id=pageindex_ids
                    )
                    
                    # 构建响应
                    content = response["choices"][0]["message"]["content"]
                    return Response({'content': content}, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"PageIndex chat failed: {e}")
        
        # 否则使用原有的对话流程
        # 【新增第一步】：调用memos_client.search_memory获取完整记忆数据
        memory_data = None
        try:
            # 获取conversation_id，如果没有则使用chat_id
            conversation_id = data.get('conversation_id', str(chat_id))
            memory_data = memos_client.search_memory(
                query=message,
                user_id='test_user_123',
                conversation_id=conversation_id
            )
            print(f"Retrieved memory data: {memory_data}")
        except Exception as e:
            print(f"Error searching memory: {e}")
        
        # 【新增第二步】：调用build_memory_prompt函数生成记忆Prompt
        memory_prompt = build_memory_prompt(memory_data, message)
        print(f"Memory prompt: {memory_prompt}")
        
        pipeline = PipelineManage.Builder()
        pipeline.append_step(BaseGenerateHumanMessageStep)
        pipeline.append_step(BaseChatStep)
        
        context = {
            'problem_text': message,
            'chat_id': chat_id,
            'model_id': data.get('model_id'),
            'workspace_id': data.get('workspace_id', uuid.uuid4()),
            'stream': stream,
            'history_chat_record': data.get('history', []),
            'paragraph_list': data.get('paragraphs', [])
        }
        
        # 只有当memory_prompt非空时才添加到上下文
        if memory_prompt:
            context['memory_prompt'] = memory_prompt  # 【新增】添加记忆Prompt到上下文
        else:
            print("No memory prompt to add to context")
        
        result = pipeline.build().run(context)
        return result

class OpenAIChatView(APIView):
    def post(self, request, app_id):
        data = request.data
        messages = data.get('messages', [])
        stream = data.get('stream', True)
        
        if not messages:
            return Response({'error': 'Messages are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        last_message = messages[-1]
        if last_message.get('role') != 'user':
            return Response({'error': 'Last message must be from user'}, status=status.HTTP_400_BAD_REQUEST)
        
        chat_id = uuid.uuid4()
        pipeline = PipelineManage.Builder()
        pipeline.append_step(BaseGenerateHumanMessageStep)
        pipeline.append_step(BaseChatStep)
        
        context = {
            'problem_text': last_message.get('content'),
            'chat_id': chat_id,
            'model_id': data.get('model_id'),
            'workspace_id': data.get('workspace_id', uuid.uuid4()),
            'stream': stream,
            'history_chat_record': [],
            'paragraph_list': []
        }
        
        result = pipeline.build().run(context)
        return result

class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        try:
            file = request.FILES.get('file')
            if not file:
                return Response({'error': 'File is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 确保上传目录存在
            upload_dir = 'uploads'
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # 保存文件
            file_path = os.path.join(upload_dir, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # 创建文档记录
            document = Document.objects.create(
                name=file.name,
                file_path=file_path,
                status='INDEXING'
            )
            
            # 调用PageIndex创建索引
            try:
                # 获取PageIndex客户端实例
                pi = PageIndexClientManager.get_client()
                # 上传文档
                result = pi.submit_document(file_path)
                document.pageindex_id = result["doc_id"]
                # 检查处理状态
                status_check = pi.get_document(document.pageindex_id)["status"]
                if status_check == "completed":
                    document.status = 'COMPLETED'
                else:
                    document.status = 'INDEXING'  # 保持索引中状态，后续可通过定时任务检查
            except Exception as e:
                document.status = 'FAILED'
                print(f"PageIndex indexing failed: {e}")
            
            document.save()
            
            return Response({'id': str(document.id), 'name': document.name, 'status': document.status}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DocumentListView(APIView):
    def get(self, request):
        documents = Document.objects.all()
        data = [{
            'id': str(doc.id),
            'name': doc.name,
            'status': doc.status,
            'upload_time': doc.upload_time,
            'pageindex_id': doc.pageindex_id
        } for doc in documents]
        return Response(data)

class DocumentDetailView(APIView):
    def get(self, request, document_id):
        try:
            document = Document.objects.get(id=document_id)
            data = {
                'id': str(document.id),
                'name': document.name,
                'status': document.status,
                'upload_time': document.upload_time,
                'pageindex_id': document.pageindex_id
            }
            return Response(data)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, document_id):
        try:
            document = Document.objects.get(id=document_id)
            # 删除文件
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
            # 删除文档记录
            document.delete()
            return Response({'message': 'Document deleted successfully'}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

class DocumentReindexView(APIView):
    def post(self, request, document_id):
        try:
            document = Document.objects.get(id=document_id)
            document.status = 'INDEXING'
            document.save()
            
            # 重新索引
            try:
                # 获取PageIndex客户端实例
                pi = PageIndexClientManager.get_client()
                # 上传文档
                result = pi.submit_document(document.file_path)
                document.pageindex_id = result["doc_id"]
                # 检查处理状态
                status_check = pi.get_document(document.pageindex_id)["status"]
                if status_check == "completed":
                    document.status = 'COMPLETED'
                else:
                    document.status = 'INDEXING'  # 保持索引中状态，后续可通过定时任务检查
            except Exception as e:
                document.status = 'FAILED'
                print(f"PageIndex reindexing failed: {e}")
            
            document.save()
            return Response({'id': str(document.id), 'status': document.status}, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

class DocumentStatusUpdateView(APIView):
    def post(self, request, document_id):
        try:
            document = Document.objects.get(id=document_id)
            
            if document.pageindex_id:
                # 获取PageIndex客户端实例
                pi = PageIndexClientManager.get_client()
                # 检查处理状态
                status_check = pi.get_document(document.pageindex_id)["status"]
                if status_check == "completed":
                    document.status = 'COMPLETED'
                elif status_check == "processing":
                    document.status = 'INDEXING'
                else:
                    document.status = 'FAILED'
                document.save()
                return Response({'id': str(document.id), 'status': document.status}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Document has no pageindex_id'}, status=status.HTTP_400_BAD_REQUEST)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)