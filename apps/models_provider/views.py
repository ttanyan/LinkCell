from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models_provider.constants.model_provider_constants import ModelProvideConstants
from apps.models_provider.models import Model
from models_provider.tools import encrypt
import json

class ModelProviderList(APIView):
    def get(self, request):
        providers = ModelProvideConstants.get_all_providers()
        result = []
        for provider in providers:
            provide_info = provider.get_model_provide_info()
            # 如果返回的是ModelProvideInfo对象，转换为字典
            if hasattr(provide_info, 'to_dict'):
                result.append(provide_info.to_dict())
            else:
                result.append(provide_info)
        return Response(result)

class ModelList(APIView):
    def get(self, request, provider):
        model_type = request.query_params.get('model_type', 'LLM')
        provider_instance = ModelProvideConstants.get_provider(provider)
        if not provider_instance:
            return Response({'error': 'Provider not found'}, status=status.HTTP_404_NOT_FOUND)
        
        models = provider_instance.get_model_list(model_type)
        return Response(models)

class ModelCredentialValid(APIView):
    def post(self, request, provider):
        data = request.data
        model_type = data.get('model_type')
        model_name = data.get('model_name')
        model_credential = data.get('model_credential')
        model_params = data.get('model_params', {})
        
        provider_instance = ModelProvideConstants.get_provider(provider)
        if not provider_instance:
            return Response({'error': 'Provider not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            is_valid = provider_instance.is_valid_credential(
                model_type, model_name, model_credential, model_params, raise_exception=True
            )
            return Response({'valid': is_valid})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ModelListAll(APIView):
    def get(self, request):
        workspace_id = request.query_params.get('workspace_id', '00000000-0000-0000-0000-000000000000')
        models = Model.objects.filter(workspace_id=workspace_id)
        result = []
        for model in models:
            result.append({
                'id': str(model.id),
                'name': model.name,
                'model_type': model.model_type,
                'model_name': model.model_name,
                'provider': model.provider,
                'status': model.status
            })
        return Response(result)

class ModelCreate(APIView):
    def post(self, request):
        data = request.data
        name = data.get('name')
        model_type = data.get('model_type')
        model_name = data.get('model_name')
        provider = data.get('provider')
        credential = data.get('credential')
        workspace_id = data.get('workspace_id')
        
        if not all([name, model_type, model_name, provider, credential, workspace_id]):
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            encrypted_credential = encrypt(credential)
            model = Model.objects.create(
                name=name,
                model_type=model_type,
                model_name=model_name,
                provider=provider,
                credential=encrypted_credential,
                workspace_id=workspace_id
            )
            return Response({
                'id': str(model.id),
                'name': model.name,
                'model_type': model.model_type,
                'model_name': model.model_name,
                'provider': model.provider,
                'status': model.status
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ModelDelete(APIView):
    def delete(self, request, model_id):
        try:
            model = Model.objects.get(id=model_id)
            model.delete()
            return Response({'success': True})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)