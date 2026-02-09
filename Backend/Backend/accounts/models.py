from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expiret(self):
        return timezone.now() >= self.expires_at
