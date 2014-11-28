import os
from time import time
from uuid import uuid4
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.urlresolvers import reverse

from imagekit.models import ProcessedImageField
from taggit.managers import TaggableManager

from main.processors import Watermark

def path_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        dir = str(int(time()))
        return os.path.join(path, dir, filename)
    return wrapper

class Image(models.Model):
    image = ProcessedImageField(upload_to=path_rename('images'),processors=[Watermark()])
    title = models.CharField(max_length=100, validators=[MinLengthValidator(3)], blank=True, help_text='Title of the image')
    description = models.CharField(max_length=300, validators=[MinLengthValidator(3)], blank=True, help_text='Short description of the image')
    nsfw = models.BooleanField()
    user = models.ForeignKey('auth.User', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)
    
    def get_absolute_url(self):
        return reverse('main:image', kwargs={'pk':str(self.id)})
    
    def __unicode__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']
        
    class OEmbed:
        type = 'photo'
        title = staticmethod(lambda obj: obj.title if obj.title else None)
        photo_field = 'image'
        html = staticmethod(lambda obj, width, height, request: '<img src="' + request.build_absolute_uri(obj.image.url) + '" alt="' + obj.title + '" style="width:500px">')
        author_name = staticmethod(lambda obj: obj.user.username if obj.user else None)
        author_url = staticmethod(lambda obj: reverse('main:user', args=(obj.user.username,)) if obj.user else None)
        thumbnail_sizes = [[100,0],[400,0],]
