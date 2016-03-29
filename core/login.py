from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import LoginForm
from .models import Worker
from .utils import get_worker


def login_set_desk(request):
    context = {}
    error = ''
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            worker, created = Worker.objects.get_or_create(globalid=form.user_cache)
            desks = worker.get_desks()
            
            if desks:
                request.session['desk'] = desks[0].pk
                login(request, form.user_cache)
                get_worker(request).get_projects()
                print get_worker(request).projects.all()
                return redirect(request.GET.get('next', 'comm:project_list'))
                
            else:
                error = 'Please contact your RHD to add this desk to your AD groups.'
                
        else:
            error = 'Please make sure your global id and password is correct'
            
        context['form'] = form
        context['error'] = error
        
    else:
        context['form'] = LoginForm()

    return render(request, 'login.html', context)