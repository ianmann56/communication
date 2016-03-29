from django.conf.urls import url, include
from django.contrib import admin

from .views import ProjectList, RequestList, CommentCreate

urlpatterns = [
    url(r'^projects/list/$', ProjectList.as_view(), name='project_list'),
    url(r'^projects/(?P<project_id>\d+)/requests/list/$', RequestList.as_view(), name='request_list'),
    url(r'^requests/(?P<request_id>\d+)/new_comment/$', CommentCreate.as_view(), name='new_comment'),
]