from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class TaggedItemManager(models.Manager):
    def get_for_tags(self,obj_type,obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects \
                .select_related('tag') \
                .filter(
                   content_type = content_type,
                   object_id = obj_id 
                )   
class Tag(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey('Tag',on_delete=models.CASCADE,default=2)
    content_type = models.ForeignKey(ContentType,models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
