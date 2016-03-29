from django.contrib import admin

from core.models import Worker, Desk, Project

# Register your models here.
admin.site.register(Worker)
admin.site.register(Desk)
admin.site.register(Project)