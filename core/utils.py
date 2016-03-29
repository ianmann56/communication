from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from .models import Worker, Desk

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)
    
def get_worker(request):
    """Return the worker object"""
    try:
        worker = Worker.objects.get(globalid=request.user)
        return worker
    # Trying to make it so that all that has to happen for a new desk worker to use centraldesk is for them to get added to a desk AD group
    except ObjectDoesNotExist: 
        group_names = [group['name'] for group in request.user.groups.values()]
        if "aux-dept-reslife-desk" in group_names or "aux-dept-reslife-dsk" in group_names:
            worker = Worker(globalid=request.user)
            worker.save()
            return worker
        #if user does not have an aux-dept-reslife group, loop will finish without returning.
        return None