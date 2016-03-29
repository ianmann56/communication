from django.shortcuts import render
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .forms import DeskForm
from .utils import get_worker

# Create your views here.
class BaseGenericTemplate(View):
    """
    lists all projects that are available and their respectable forum.
    """
    
    def dispatch(self, *args, **kwargs):
        dispatch_tmp = super(BaseGenericTemplate, self).dispatch(*args, **kwargs)
        
        if 'desk' not in self.request.session.keys():
            return HttpResponseRedirect(reverse('logout'))
        
        return dispatch_tmp
    
    def get_context_data(self, *args, **kwargs):
        context = super(BaseGenericTemplate, self).get_context_data(*args, **kwargs)
        
        context['form'] = DeskForm(worker=get_worker(self.request), current=self.request.session['desk'])
        
        return context
