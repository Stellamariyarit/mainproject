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


class Feedback(models.Model):

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name



class RainfallPrediction(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    rainfall_intensity = models.FloatField()  # mm
    alert_level = models.CharField(max_length=50)  # Green, Yellow, Orange, Red




class RainfallData(models.Model):
    date = models.DateField()
    rainfall_amount = models.FloatField()



class Alert(models.Model):
    alert_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



from django.db import models
from django.contrib.auth.models import User
from datetime import date

class RainfallForecast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    predicted_rainfall = models.FloatField()
    alert_level = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user} - {self.date} - {self.alert_level}"



from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Allow null values
    message = models.TextField()
    alert_level = models.CharField(
        max_length=20,
        choices=[("Green", "Green"), ("Yellow", "Yellow"), ("Orange", "Orange"), ("Red", "Red")],
        default="Green",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'No User'} - {self.alert_level}"




from django.db import models
from django.contrib.auth.models import User

class AlertLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=50)  # Example: "Email" or "SMS"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.alert_type} ({self.timestamp})"
