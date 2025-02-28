from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user.username


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

# class Feedback(models.Model):
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

#     feedback = models.TextField()

#     def __str__(self):
#         return self.user.username


# # main_app/models.py
# from django.db import models

class Feedback(models.Model):
    # name = models.CharField(max_length=100, default='Anonymous')
    # email = models.EmailField(default='default@example.com')
    # message = models.TextField()
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
