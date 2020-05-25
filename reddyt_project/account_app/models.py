from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PasswordResetRequest(models.Model):
    token = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Password Reset User: {self.user}"
