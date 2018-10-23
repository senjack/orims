from django.contrib import admin

from .models import Receptionist


class ManageReceptionist(admin.ModelAdmin):
    fieldsets = [
        # ('System Administrator\'s ID', {'fields': ['system_admin_id']}),
        ('Receptionist Details', {'fields': ['Receptionist_user_name']}),
        # (None, {'fields': ['system_admin_password']}),
        (None, {'fields': ['Receptionist_email']}),
        (None, {'fields': ['Receptionist_profile_photo']}),
        (None, {'fields': ['Receptionist_cover_photo']}),
    ]


admin.site.register(Receptionist, ManageReceptionist)
