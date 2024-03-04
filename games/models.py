import uuid

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Game(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    answer = models.CharField(max_length=5)
    completed = models.BooleanField(default=False)
    win = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.GenericIPAddressField(unpack_ipv4=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['uuid']),
        ]

    def get_absolute_url(self):
        return reverse('games:detail', kwargs={'uuid': self.uuid})


class Attempt(models.Model):
    answer = models.CharField(max_length=5)
    parent = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='attempts')
    result = models.CharField(max_length=254)
    created_at = models.DateTimeField(auto_now_add=True)
