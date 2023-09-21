from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User 

# Create your models here.
class TagItemMangar(models.Manager):
    def get_tags_for(object_type,objec_id):

        conten_type = ContentType.objects.get_for_model(object_type)
    
        querySet = TaggItem.objects \
                            .select_related('tag') \
                            .filter(
                                    conten_type = conten_type,
                                    object_id = objec_id
                                    )



class Tag(models.Model):
    tag = models.CharField(max_length=255)

class TaggItem(models.Model):
    objects = TagItemMangar()

    tag = models.ForeignKey(Tag , on_delete=models.CASCADE) 

    #Dynamicly catch the object we need 3 thing : 
    # 1. ContentType (Article, Video, Product ... )
    # 2. ID (Get From DataBase Primary Keys) 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # 3.if the primary key is not positive integer then use => GenericKey
    content_object = GenericForeignKey()