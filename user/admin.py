from django.contrib import admin

from .models import User


class ManageUser(admin.ModelAdmin):
    fieldsets = [
        ('User Details', {'fields': ['staff_id']}),
        (None, {'fields': ['user_name']}),
        (None, {'fields': ['user_password']}),
    ]


admin.site.register(User, ManageUser)
