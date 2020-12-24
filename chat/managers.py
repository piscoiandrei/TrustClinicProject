from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()


class MessageManager(models.Manager):
    def from_to_obj(self, user1, user2):
        return self.filter(source=user1, endpoint=user2)

    def from_to_id(self, id1, id2):
        user1 = get_object_or_404(User, pk=id1)
        user2 = get_object_or_404(User, pk=id2)
        return self.filter(source=user1, endpoint=user2)

    def from_to_email(self, email1, email2):
        user1 = get_object_or_404(User, pk=email1)
        user2 = get_object_or_404(User, pk=email2)
        return self.filter(source=user1, endpoint=user2)

    def create_from_to_obj(self, user1, user2, content):
        msg = self.model(source=user1, endpoint=user2, content=content)
        msg.save(using=self._db)

    def create_from_to_id(self, id1, id2, content):
        user1 = get_object_or_404(User, pk=id1)
        user2 = get_object_or_404(User, pk=id2)
        msg = self.model(source=user1, endpoint=user2, content=content)
        msg.save(using=self._db)
