from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from main.models import Image

from sorl.thumbnail import get_thumbnail

class ImageAdmin(GuardedModelAdmin):
    list_display = ['thumb','title','created']
    readonly_fields = ('created',)
    
    def thumb(self, obj):
        im = get_thumbnail(obj.image, '100x100')
        return '<img src="%s" alt="" />' % (im.url)
    thumb.allow_tags = True

admin.site.register(Image, ImageAdmin)