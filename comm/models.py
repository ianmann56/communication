from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models

from core.models import Worker, Project

# Create your models here.
class Request(models.Model):
    """docstring for Request"""
    
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Worker)
    body = models.TextField()
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"),auto_now=True)
    active = models.BooleanField("active", default=True)
    deactivated = models.DateTimeField(_("Deleted"), blank=True, null=True)
    users_read = models.ManyToManyField(Worker, related_name="viewers_request", blank=True)
    
class Comment(models.Model):
    """docstring for Comment"""
    
    request = models.ForeignKey(Request)
    author = models.ForeignKey(Worker)
    body = models.TextField()
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    updated = models.DateTimeField(_("Updated"),auto_now=True)
    active = models.BooleanField("active", default=True)
    deactivated = models.DateTimeField(_("Deleted"), blank=True, null=True)
    users_read = models.ManyToManyField(Worker, related_name="viewers_comment", blank=True)
        
        