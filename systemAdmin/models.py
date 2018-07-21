from django.db import models
from django.contrib.auth.hashers import check_password
# SYSTEM ADMINISTRATOR MODELS.


class SystemAdmin(models.Model):
    system_admin_id = models.AutoField(primary_key=True)
    system_admin_user_name = models.CharField(max_length=254)
    system_admin_password = models.CharField(max_length=500)
    system_admin_email = models.EmailField(max_length=500)

    # Defining a display string for each instance
    def __str__(self):
        return self.system_admin_user_name
    # End function __str__()

    # Defining a function to display a given user id
    def get_user_id(self):
        return self.system_admin_id
    # End function get_user_id

    def get_password(self,pwd):
        check = check_password(pwd,self.system_admin_password)
        return check
# End of class SystemAdmin

