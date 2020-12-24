from django.db import models
from django.contrib.auth import get_user_model
from .managers import MessageManager

User = get_user_model()


class Message(models.Model):
    source = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='sources')
    endpoint = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='endpoints')
    content = models.CharField(max_length=255, blank=True, null=True)

    objects = MessageManager()
