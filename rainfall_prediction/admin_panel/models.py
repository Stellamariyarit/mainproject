from django.db import models

class RainfallAlert(models.Model):
    alert_level = models.CharField(max_length=50)
    description = models.TextField()
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.alert_level