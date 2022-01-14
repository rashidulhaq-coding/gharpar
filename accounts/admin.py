from django.contrib import admin
from .models import User, Employee, Shift, Holiday
from django.contrib.auth.models import Group
# Register your models here.

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Shift)
admin.site.register(Holiday)


admin.site.unregister(Group)
