from django.db import models
from orims.models import Staff

# SERVICE UNIT ADMINISTRATORS' MODELS.
class Administrator(models.Model):
    """"Creates and associates with a database relation that store data about a system administrator"""
    # Setting foreign key
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    # User attributes
    # branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    admin_level_choices = (
        ('unit-admin', 'Unit Level Administrator'),
        ('branch-admin', 'Branch Level administrator'),
        ('dept-admin', 'Department Level Administrator'),
        ('ofc-admin', 'Office Level Administrator'),
        ('select','Select Administrator Level')
    )
    # Creating choices for staff
    admin_level = models.CharField(
        max_length=30,
        choices=admin_level_choices,
        default='select',
    )
    # Defining a display string for each instance
    def __str__(self):
        return '%s %s(%s)', Staff.staff_first_name, Staff.staff_last_name, self.staff_id
    # End function __str__()

    #Enforcing custom table name
    class Meta:
        db_table = "Administrator"
    # End class Meta
# End class Administrator
