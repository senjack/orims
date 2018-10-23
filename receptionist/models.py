from django.db import models
from django.contrib.auth.hashers import check_password
from orims.custom import RandomFileName
from django.utils import timezone


class Receptionist(models.Model):
    Receptionist_id = models.AutoField(primary_key=True)
    Receptionist_user_name = models.CharField(max_length=254)
    Receptionist_first_name = models.CharField(max_length=254)
    Receptionist_last_name = models.CharField(max_length=254)
    Receptionist_password = models.CharField(max_length=500)
    Receptionist_email = models.EmailField(max_length=500)
    Receptionist_profile_photo = models.FileField(upload_to=RandomFileName('photos/uploads/Receptionist/profile_photos/'),
                                                  max_length=1024,null = True,blank = True)
    Receptionist_cover_photo = models.FileField(upload_to=RandomFileName('photos/uploads/Receptionist/cover_photos/'),
                                                  max_length=1024,null = True,blank = True)
    registration_date = models.DateTimeField(default=timezone.now)

    # Defining a display string for each instance
    def __str__(self):
        return self.Receptionist_user_name
    # End function __str__()

    # Defining a function to display a given user id
    def get_user_id(self):
        return self.Receptionist_id
    # End function get_user_id

    def get_password(self,pwd):
        check = check_password(pwd,self.Receptionist_password)
        return check

    # Defining a display string for each instance
    def get_data(self):

        return self.Receptionist_user_name
    # End function __str__()

# End of class SystemAdmin
