from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    score = models.IntegerField(default=0)
