from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import User, Group
from django.conf import settings

# Create your models here.

class Project(models.Model):
    """docstring for project"""
    
    name = models.CharField(max_length=50)
    groups_required = models.ManyToManyField(Group)
    url = models.CharField(max_length=200)
    
    def __str__(self):
        return '%s' % self.name

class Desk(models.Model):
    """
        Should mimik the desk class on centraldesk.
    """

    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=2, unique=True)
    
    def __str__(self):
        return '%s' % self.name
        
    
class Worker(models.Model):
    """
        Should mimik the worker class on centraldesk.
    """
    
    globalid = models.ForeignKey(User)
    desks = models.ManyToManyField(Desk)
    desk_manager = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    developer = models.BooleanField(default=False)
    picture_field = models.ImageField(upload_to=settings.PROFILE_PICS_DIR, blank=True, null=True)
    projects = models.ManyToManyField(Project)
    
    def get_projects(self):
        """
        Get all the projects available to this user.
        For example, if you have access to sodium but not centraldesk than you
            don't need to see centraldesk posts.
        """    
        if self.is_developer():
            self.projects = Project.objects.all()
        else:
            for project in Project.objects.all():
                for group in project.groups_required.all():
                    if self.globalid.groups.contains(group):
                        self.projects.add(group)
        
        projects = self.projects.all()
        self.save()
        """
        TODO:
            Go out to a page on each project to get the users that have access
            to that site.
        """
        return projects
    
    def get_desks(self):
        """Returns the desk based on the AD group of the person"""

        groups = self.globalid.groups.values()
        desks = []
        
        self.desks.clear()
        if self.is_developer():
            self.desks.add(Desk.objects.get(name='dev-desk'))
        for group in groups:
            hall_code = ''
            if "aux-dept-reslife-desk-" in group['name'] and len(group['name']) == 24:
                hall_code = group['name'][-2:]
            elif "aux-dept-reslife-dskmgr-" in group['name'] and len(group['name']) == 26:
                hall_code = group['name'][-2:]

            try:
                desk = Desk.objects.get(code=hall_code)
                if desk not in self.desks.all():
                    self.desks.add(desk)
                    self.save()
            except Desk.DoesNotExist:
                desk = None

        return self.desks.all()
        
    def is_developer(self):
        if 'aux-dept-to-developers' in [group.name for group in self.globalid.groups.all()]:
            self.developer = True
            self.save()
            return True
        else:
            return False
            
    def is_manager(self):
        mgr_group = self.globalid.groups.filter(name__icontains='aux-dept-reslife-dskmgr')
        if mgr.count() > 0 or self.is_developer():
            self.desk_manager = True
            self.save()
            return True
        else:
            return False
            
    def save(self):
        print self.picture_field
        if not self.picture_field:
            student_photo = os.path.join(settings.STUDENT_PHOTO_URL, '%s.jpg' % self.globalid)
            self.picture_field = student_photo
        super(Worker, self).save()
        
    def __str__(self):
        return '%s %s' % (self.globalid.first_name, self.globalid.last_name)
        