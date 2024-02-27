from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    vitorias = models.IntegerField(default=0)

