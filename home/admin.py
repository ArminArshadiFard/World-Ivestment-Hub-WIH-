from django.contrib import admin
from django.contrib.auth.models import Group
from home.models import Share,Ticket,SystemExceptions

admin.site.unregister(Group)
admin.site.register(Share)
admin.site.register(Ticket)
admin.site.register(SystemExceptions)
