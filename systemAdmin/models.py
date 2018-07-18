from django.db import models

# SYSTEM ADMINISTRATOR MODELS.


class SystemAdmin(models.Model):
    system_admin_id = models.AutoField(primary_key=True)
    system_admin_user_name = models.CharField(max_length=254)
    system_admin_password = models.CharField(max_length=254)
    system_admin_email = models.EmailField(max_length=150)

    # Defining a display string for each instance
    def __str__(self):
        return self.system_admin_user_name
    # End function __str__()
# End of class SystemAdmin

