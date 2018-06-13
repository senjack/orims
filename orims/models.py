from django.db import models

# Added imports
from django.utils import timezone

# CREATION OF ORIMS DATABASE MODELS.

# Model for service unit object
class service_unit(models.Model):
	'This is the common base class (model) for all service facility units. i.e. [Ministries, Organisations, firms, etc.]'

    # Setting custom Primary key
    unit_id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=30)
    
    #Defining possible service unit types to form a lookup.
    ministry = 'min'
    organization = 'org'
    firm = 'firm'
    other = 'other'
    unit_choice = (
    	ministry, 'Ministry'
    	organization,'Organization'
    	firm,'Firm'
    	other,'Others'
    )

    #Creating a choice of service units
    unit_type = models.CharField(
    	max_length=15,
    	choices=unit_choice,
        default=ministry,
    )

    unit_description = models.TextField(max_length=1024)
    unit_logo = models.ImageField(upload_to='/uploads/images/unit_images/logo_images',height_field=None, width_field=None,max_length=500)
    unit_featured_image = models.ImageField(upload_to='/uploads/images/unit_images/feutured_images',height_field=None, width_field=None,max_length=1024)
    unit_cover_photo = models.ImageField(upload_to='/uploads/images/unit_images/cover_images',height_field=None, width_field=None,max_length=2048)

    #Defining what to be returned for each instance
    def __str__(self):
        return self.unit_name

    #Enforcing custom table name
    class Meta:
    db_table = "service_unit"



# Model for service unit branches
class branch(models.Model):
    'This is the common base class (model) for all service units branches.'

    # Setting custom Primary key
    branch_id = models.AutoField(primary_key=True)

    # Setting foreign key
    unit_id = models.AutoField(primary_key=True)

    branch_name = models.CharField(max_length=30)
    
    #Defining possible branch levels to form a lookup.
    
    branch_level_choice = (
        'main', 'Main Branch'
        'other','Other Branch'
    )
    #Creating a choice of service units Branch levels
    branch_level = models.CharField(
        max_length=15,
        choices=branch_level_choice,
        default='other',
    )

    registration_date = models.DateTimeField()


    #Defining a display string for each instance
    def __str__(self):
        return self.branch_name

    #Enforcing custom table name
    class Meta:
    db_table = "branch"


# Model for branch location
class location(models.Model):
    'This is the common base class (model) for all branch locations'

    # Setting foreign key
    branch_id = models.AutoField(primary_key=True)
 
    #Location attributes
    district = models.CharField(max_length=15)
    county = models.CharField(max_length=15)
    sub_county = models.CharField(max_length=15)
    parish = models.CharField(max_length=15)
    town = models.CharField(max_length=15)
    zone = models.CharField(max_length=15)
    unique_direction = models.CharField(max_length=15)

    #Defining a display string for each instance
    def __str__(self):
        return self.branch_name

    #Enforcing custom table name
    class Meta:
    db_table = "location"
