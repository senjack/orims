from django.contrib import admin

from .models import Administrator


class ManageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Administrator Information', {'fields': ['staff_id']}),
        (None, {'fields': ['admin_level']}),
    ]


admin.site.register(Administrator, ManageAdmin)
