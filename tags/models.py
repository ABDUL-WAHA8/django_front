from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class TagManager(models.Manager):
    def CustomManager(self,obj_type,obj_id):
        content_type=ContentType.objects.get_for_model(obj_type)

        query_set=TaggedItem.objects.select_related('Tag').filter(content_type=content_type,object_id=obj_id)

        return query_set


class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    active=TagManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
