from django.db import models
import uuid

class Document(models.Model):
    STATUS_CHOICES = [
        ('UPLOADING', '上传中'),
        ('INDEXING', '索引中'),
        ('COMPLETED', '完成'),
        ('FAILED', '失败'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    pageindex_id = models.CharField(max_length=255, blank=True, null=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UPLOADING')
    workspace_id = models.UUIDField(default=uuid.uuid4)
    
    class Meta:
        ordering = ['-upload_time']
    
    def __str__(self):
        return self.name
