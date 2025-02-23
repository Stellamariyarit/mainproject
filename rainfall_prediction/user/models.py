from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)