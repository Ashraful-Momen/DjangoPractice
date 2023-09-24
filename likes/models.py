from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.contrib.auth.models import User 
from core.models import User
from django.conf import settings

# Create your models here.
class LikeItem(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE) 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()