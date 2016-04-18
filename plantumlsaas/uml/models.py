from django.db import models
import uuid

# Create your models here.
class UML(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.TextField('query')
    image = models.FileField('image')
    image_url = models.URLField('image_url')
