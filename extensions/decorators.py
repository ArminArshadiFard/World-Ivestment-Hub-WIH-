import functools
from functools import wraps
from django.shortcuts import render
from django.db import connection, reset_queries
import time


class PermissionCode:
    Accountants_Authority = 'حسابدار'

    Keeper_Authority = 'انباردار'

    Viewer_Authority = 'بیننده'


def authority(perm_list):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.profile_user.get_type_display() in perm_list:
                return view_method(request, *args, **kwargs)
            else:
                return render(request, "home/404.html")

        return _arguments_wrapper

    return _method_wrapper


def debugger(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        st = time.time()
        value = func(*args, **kwargs)
        et = time.time()
        queries = len(connection.queries)
        print(queries)
        print(et - st)
        return value

    return wrapper
