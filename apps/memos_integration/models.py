"""MemOS Models"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class Memory(models.Model):
    """Memory model for user memories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    content = models.TextField()
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    memory_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    class Meta:
        verbose_name = "Memory"
        verbose_name_plural = "Memories"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}..."


class Conversation(models.Model):
    """Conversation model for chat history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255)
    conversation_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.user.username}: {self.title}"


class Message(models.Model):
    """Message model for chat messages"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('assistant', 'Assistant')])
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class Document(models.Model):
    """Document model for uploaded documents"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500)
    document_type = models.CharField(max_length=50)
    document_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.filename}"


class MemoryGraph(models.Model):
    """Memory graph model for memory relationships"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memory_graphs')
    nodes = models.JSONField(default=list)
    edges = models.JSONField(default=list)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Memory Graph"
        verbose_name_plural = "Memory Graphs"

    def __str__(self):
        return f"{self.user.username}'s Memory Graph"
