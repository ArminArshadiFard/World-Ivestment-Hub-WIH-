from django.contrib import admin
from account.models import User
from .models import *

admin.site.register(ValidationCode)
