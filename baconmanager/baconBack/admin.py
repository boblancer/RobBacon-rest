from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Attendance)
admin.site.register(Session)
admin.site.register(Member)
admin.site.register(Class)
