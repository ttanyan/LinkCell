"""MemOS Views"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import Memory, Conversation, Message, Document, MemoryGraph
from .client import memos_client


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MemoryListView(View):
    """Get current user's memory list"""
    def get(self, request):
        try:
            # 从MemOS API获取记忆列表
            memories = memos_client.get_memories(str(request.user.id))
            return JsonResponse({'memories': memories, 'status': 'success'})
        except Exception as e:
            #  fallback到本地数据库
            memories = Memory.objects.filter(user=request.user)
            memory_list = []
            for memory in memories:
                memory_list.append({
                    'id': memory.memory_id or str(memory.id),
                    'content': memory.content,
                    'metadata': memory.metadata,
                    'created_at': memory.created_at.isoformat(),
                    'updated_at': memory.updated_at.isoformat()
                })
            return JsonResponse({'memories': memory_list, 'status': 'success'})


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MemoryGraphView(View):
    """Get memory graph data"""
    def get(self, request):
        try:
            # 从MemOS API获取记忆图谱
            graph_data = memos_client.get_memory_graph(str(request.user.id))
            return JsonResponse(graph_data)
        except Exception as e:
            #  fallback到本地数据库
            try:
                memory_graph = MemoryGraph.objects.get(user=request.user)
                return JsonResponse({
                    'nodes': memory_graph.nodes,
                    'edges': memory_graph.edges
                })
            except MemoryGraph.DoesNotExist:
                return JsonResponse({'nodes': [], 'edges': []})


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MemoryCreateView(View):
    """Create new memory"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            content = data.get('content')
            metadata = data.get('metadata', {})

            # 调用MemOS API创建记忆
            result = memos_client.create_memory(str(request.user.id), content, metadata)

            # 同时保存到本地数据库
            memory = Memory.objects.create(
                user=request.user,
                content=content,
                metadata=metadata,
                memory_id=result.get('id')
            )

            return JsonResponse({'memory': result, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MemoryUpdateView(View):
    """Update existing memory"""
    def put(self, request, memory_id):
        try:
            data = json.loads(request.body)
            content = data.get('content')
            metadata = data.get('metadata', {})

            # 调用MemOS API更新记忆
            result = memos_client.update_memory(memory_id, content, metadata)

            # 同时更新本地数据库
            memory = Memory.objects.filter(memory_id=memory_id, user=request.user).first()
            if memory:
                memory.content = content
                memory.metadata = metadata
                memory.save()

            return JsonResponse({'memory': result, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MemoryDeleteView(View):
    """Delete memory"""
    def delete(self, request, memory_id):
        try:
            # 调用MemOS API删除记忆
            result = memos_client.delete_memory(memory_id)

            # 同时从本地数据库删除
            Memory.objects.filter(memory_id=memory_id, user=request.user).delete()

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MemorySearchView(View):
    """Search memories semantically"""
    def get(self, request):
        try:
            query = request.GET.get('query', '')
            # 调用MemOS API搜索记忆
            memories = memos_client.search_memory(str(request.user.id), query)
            return JsonResponse({'memories': memories, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class ConversationCreateView(View):
    """Create conversation"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            title = data.get('title')

            # 调用MemOS API创建对话
            result = memos_client.create_conversation(str(request.user.id), title)

            # 同时保存到本地数据库
            conversation = Conversation.objects.create(
                user=request.user,
                title=title,
                conversation_id=result.get('id')
            )

            return JsonResponse({'conversation': result, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class DocumentUploadView(View):
    """Upload document"""
    def post(self, request):
        try:
            # 注意：实际实现需要处理文件上传
            data = json.loads(request.body)
            file_path = data.get('file_path')
            document_type = data.get('document_type')

            # 调用MemOS API上传文档
            result = memos_client.upload_document(str(request.user.id), file_path, document_type)

            # 同时保存到本地数据库
            document = Document.objects.create(
                user=request.user,
                filename=file_path.split('/')[-1],
                file_path=file_path,
                document_type=document_type,
                document_id=result.get('id')
            )

            return JsonResponse({'document': result, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class RAGRetrieveView(View):
    """Retrieve relevant memories for RAG"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            query = data.get('query')
            top_k = data.get('top_k', 5)

            # 调用MemOS API进行RAG检索
            memories = memos_client.rag_retrieve(str(request.user.id), query, top_k)
            return JsonResponse({'memories': memories, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class LLMContextView(View):
    """Get enhanced context for LLM"""
    def post(self, request):
        try:
            data = json.loads(request.body)
            query = data.get('query')

            # 调用MemOS API获取增强上下文
            context = memos_client.get_enhanced_context(str(request.user.id), query)
            return JsonResponse({'context': context, 'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e), 'status': 'error'}, status=400)
