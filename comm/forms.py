from django import forms

from core.models import Worker, Desk
from .models import Request, Comment
from core.utils import get_worker

class RequestCreateForm(forms.ModelForm):
    """docstring for Request"""
    
    class Meta:
        model = Request
        fields = ['title', 'body']
        
    def save(self, django_request, project, commit=True):
        #django_request is a request object from the view, not a Request object
        #   from comm.models.
        request_to_create = super(RequestCreateForm, self).save(commit=False)
        request_to_create.project = project
        request_to_create.author = get_worker(django_request)
        
        if commit:
            request_to_create.save()
            request_to_create.users_read = [get_worker(django_request)]
        return request_to_create
        
class CommentCreateForm(forms.ModelForm):
    """docstring for CommentCreateForm"""
    
    class Meta:
        model = Comment
        fields = ['body']
        
    def save(self, django_request, request_object, commit=True):
        #django_request is a request object from the view, not a Request object
        #   from comm.models.
        
        #request_object is a Request object from comm.models, not a request
        #   from the views.
        
        comment = super(CommentCreateForm, self).save(commit=False)
        comment.request = request_object
        comment.author = get_worker(django_request)
        
        if commit:
            comment.save()
            comment.users_read = [get_worker(django_request)]
        return comment
        
            
        