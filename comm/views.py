from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from core.views import BaseGenericTemplate
from core.utils import get_worker
from .models import Request, Comment
from .forms import RequestCreateForm, CommentCreateForm
from core.models import Project

# Create your views here.
class ProjectList(BaseGenericTemplate, TemplateView):
    """docstring for ProjectList"""
    
    template_name = 'comm/project_list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProjectList, self).get_context_data(*args, **kwargs)
        
        context['projects'] = get_worker(self.request).projects.all()
        
        return context
        
class RequestList(BaseGenericTemplate, TemplateView):
    """docstring for RequestList"""
    
    template_name = 'comm/request_list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(RequestList, self).get_context_data(*args, **kwargs)
        # li_requests = [[]]
        # 
        # requests = Request.objects.filter(project=context['project'])
        # for r in requests:
        #     comments = requests.comments.all()
        #     li_requests.append
        
        context['project'] = Project.objects.get(pk=kwargs['project_id'])
        context['requests'] = Request.objects.filter(project=context['project'])
        print context['requests'][0].comment_set.all()
        context['create_form'] = RequestCreateForm()
        context['comment_forms'] = CommentCreateForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(*args, **kwargs)
        context['create_form'] = RequestCreateForm(request.POST or None)
        
        if context['create_form'].is_valid():
            context['create_form'].save(request, context['project'])
            context['create_form'] = RequestCreateForm()
        else:
            return render(request, self.template_name, context)
        
        return HttpResponseRedirect(reverse('comm:request_list', kwargs={"project_id": kwargs['project_id']}))
        
class CommentCreate(BaseGenericTemplate):
    """docstring for CommentCreate"""
    def post(self, request, *args, **kwargs):
        form = CommentCreateForm(request.POST)
        
        request_object = Request.objects.get(pk=kwargs['request_id'])
        
        if form.is_valid():
            form.save(request, request_object)
            print form
        return HttpResponseRedirect(reverse('comm:request_list', kwargs={"project_id": request_object.project.id}))
        
        
        