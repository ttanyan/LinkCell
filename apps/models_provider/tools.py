from models_provider.constants.model_provider_constants import ModelProvideConstants

def get_provider(provider_name):
    return ModelProvideConstants.get_provider(provider_name)

def get_model_instance_by_model_workspace_id(model_id, workspace_id, **kwargs):
    model = get_model_by_id(model_id, workspace_id)
    provider = get_provider(model.provider)
    credential = decrypt(model.credential)
    return provider.get_model(
        model.model_type, 
        model.model_name, 
        credential, 
        **kwargs
    )

def get_model_by_id(model_id, workspace_id):
    from apps.models_provider.models import Model
    return Model.objects.get(id=model_id, workspace_id=workspace_id)

def decrypt(credential):
    import json
    return json.loads(credential)

def encrypt(credential):
    import json
    return json.dumps(credential)