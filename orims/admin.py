from django.contrib import admin

from .models import *


class ManageServiceUnit(admin.ModelAdmin):
    fieldsets = [
        ('Service Unit Details', {'fields': ['system_admin_id']}),
        (None, {'fields': ['unit_name']}),
        (None, {'fields': ['unit_type']}),
        (None, {'fields': ['unit_description']}),
        (None, {'fields': ['unit_logo']}),
        (None, {'fields': ['unit_featured_image']}),
        (None, {'fields': ['unit_cover_photo']}),
    ]


class ManageUnitBranch(admin.ModelAdmin):
    fieldsets = [
        ('Unit Branch Details', {'fields': ['unit_id']}),
        (None, {'fields': ['branch_name']}),
        (None, {'fields': ['branch_level']}),
        (None, {'fields': ['registration_date']}),
    ]


class ManageBranchLocation(admin.ModelAdmin):
    fieldsets = [
        ('Branch Location Details', {'fields': ['branch_id']}),
        (None, {'fields': ['district']}),
        ('These Fields are Optional', {'fields': ['county']}),
        (None, {'fields': ['sub_county']}),
        (None, {'fields': ['parish']}),
        ('This field is required', {'fields': ['town']}),
        ('These Fields are Optional', {'fields': ['zone']}),
        (None, {'fields': ['plot_no']}),
        (None, {'fields': ['building']}),
        (None, {'fields': ['unique_direction']}),
    ]


class ManageBranchContact(admin.ModelAdmin):
    fieldsets = [
        ('Branch Contacts Details', {'fields': ['branch_id']}),
        (None, {'fields': ['mobile_number']}),
        (None, {'fields': ['office_number']}),
        (None, {'fields': ['fax_number']}),
        (None, {'fields': ['email_address']}),
    ]


class ManageBranchDepartment(admin.ModelAdmin):
    fieldsets = [
        ('Department Details', {'fields': ['branch_id']}),
        (None, {'fields': ['department_id']}),
        (None, {'fields': ['department_name']}),
        (None, {'fields': ['department_description']}),
    ]


class ManageDepartmentOffice(admin.ModelAdmin):
    fieldsets = [
        ('Office Details', {'fields': ['department_id']}),
        (None, {'fields': ['office_id']}),
        (None, {'fields': ['office_name']}),
        (None, {'fields': ['office_description']}),
        (None, {'fields': ['office_working_time']}),
    ]


class ManageOfficeWorkingTime(admin.ModelAdmin):
    fieldsets = [
        ('Office Working Time Details', {'fields': ['office_id']}),
        (None, {'fields': ['week_day']}),
        (None, {'fields': ['work_start_time']}),
        (None, {'fields': ['work_end_time']}),
    ]


admin.site.register(ServiceUnit, ManageServiceUnit)

admin.site.register(Branch, ManageUnitBranch)

admin.site.register(Location, ManageBranchLocation)

admin.site.register(Contact, ManageBranchContact)

admin.site.register(Department, ManageBranchDepartment)

admin.site.register(Office, ManageDepartmentOffice)

admin.site.register(WorkingTime, ManageOfficeWorkingTime)
