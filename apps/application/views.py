from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from application.chat_pipeline.pipeline_manage import PipelineManage
from application.chat_pipeline.step.generate_human_message_step.impl.base_generate_human_message_step import BaseGenerateHumanMessageStep
from application.chat_pipeline.step.chat_step.impl.base_chat_step import BaseChatStep
from application.models.document import Document
from application.utils.pageindex_client import PageIndexClientManager
import uuid
import os
from django.conf import settings

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