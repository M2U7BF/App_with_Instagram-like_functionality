from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from post_app.models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)