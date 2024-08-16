from django.db import models

class ErrorLog(models.Model):
    error_message = models.TextField()
    error_type = models.CharField(max_length=255)
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.error_type} - {self.status_code}"