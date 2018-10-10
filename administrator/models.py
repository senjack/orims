from django.db import models
from orims.models import Staff
from django.utils import timezone

# SERVICE UNIT ADMINISTRATORS' MODELS.
class Administrator(models.Model):
    """"Creates and associates with a database relation that store data about a system administrator"""
    # Setting foreign key
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE,)
    # User attributes
    # branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    admin_level_choices = (
        ('unit-admin', 'Unit Level Administrator'),
        ('branch-admin', 'Branch Level administrator'),
        ('dept-admin', 'Department Level Administrator'),
        ('ofc-admin', 'Office Level Administrator'),
        ('select','Select Administration Level')
    )
    # Creating choices for staff
    admin_level = models.CharField(
        'Administrator Operation Scope',
        max_length=30,
        choices=admin_level_choices,
        default='select',
    )
    registration_date = models.DateTimeField(default=timezone.now)

    # Defining a display string for each instance
    def __str__(self):
        return str(Staff.staff_first_name) + ' ' + str(Staff.staff_last_name) + ' [ ID: ' + str(self.staff_id) + ' ]'
    # End function __str__()

# End class Administrator
