from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User 

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=255)

class TaggItem(models.Model):
    tag = models.ForeignKey(Tag , on_delete=models.CASCADE) 

    #Dynamicly catch the object we need 3 thing : 
    # 1. ContentType (Article, Video, Product ... )
    # 2. ID (Get From DataBase Primary Keys) 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # 3.if the primary key is not positive integer then use => GenericKey
    content_object = GenericForeignKey()