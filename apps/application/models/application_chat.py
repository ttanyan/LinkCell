from django.db import models
from uuid import uuid4

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    application_id = models.UUIDField()
    abstract = models.CharField(max_length=1024)
    chat_user_id = models.CharField(max_length=128)
    chat_user_type = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat'
        app_label = 'application'

class ChatRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    problem_text = models.CharField(max_length=10240)
    answer_text = models.CharField(max_length=40960)
    message_tokens = models.IntegerField()
    answer_tokens = models.IntegerField()
    details = models.JSONField(default=dict)
    run_time = models.FloatField()
    index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_record'
        ordering = ['index']
        app_label = 'application'