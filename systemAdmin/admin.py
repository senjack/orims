from django.contrib import admin

from .models import SystemAdmin


class ManageSystemAdmin(admin.ModelAdmin):
    fieldsets = [
        # ('System Administrator\'s ID', {'fields': ['system_admin_id']}),
        ('System Administrator\'s Details', {'fields': ['system_admin_user_name']}),
        # (None, {'fields': ['system_admin_password']}),
        (None, {'fields': ['system_admin_email']}),
        (None, {'fields': ['system_admin_profile_photo']}),
    ]


admin.site.register(SystemAdmin, ManageSystemAdmin)
