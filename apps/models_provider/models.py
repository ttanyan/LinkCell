from django.db import models
from uuid import uuid4

class Model(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=256)
    model_type = models.CharField(max_length=64)
    model_name = models.CharField(max_length=256)
    provider = models.CharField(max_length=256)
    credential = models.TextField()
    status = models.CharField(max_length=64, default='VALID')
    workspace_id = models.UUIDField()
    model_params_setting = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'model'
        unique_together = ('name', 'workspace_id')
        app_label = 'models_provider'