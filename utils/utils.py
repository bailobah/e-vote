from django.http import HttpResponse
from django.shortcuts import redirect
from datetime import datetime
import os
def unauthenticated_user(view_func):
    def wrapper_func(request,  *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args, **kwargs)

        return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

def _set_filename_format(now, instance, filename):
    return "{user}-{date}-{microsecond}{extension}".format(
        user=instance.user.id,
        date=str(now.date()),
        microsecond=now.microsecond,
        extension=os.path.splitext(filename)[1],
    )
def user_directory_path(instance, filename):
    """
    image upload directory setting
            images/2016/7/12/hjh/hjh-2016-07-12-158859.png
    """
    now = datetime.datetime.now()
    filename = _set_filename_format(now, instance, filename)
    path = "pv/{user}/{now}/{filename}".format(
        now=now,
        user=instance.user.id,
        filename=_set_filename_format(now, instance, filename),
    )

    return path