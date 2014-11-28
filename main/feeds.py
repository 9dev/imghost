from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.syndication.views import FeedDoesNotExist
from django.shortcuts import get_object_or_404

from main.models import Image

from taggit.models import Tag

class ImageFeed(Feed):
    
    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description
    
    def item_author_name(self, item):
        return item.user or 'Guest'
    
    def item_author_link(self, item):
        if not item.user:
            return None
        return reverse('main:user', args=(item.user.username,))

    def item_pubdate(self, item):
        return item.created
    
    def item_categories(self, item):
        return item.tags.names()
    
class IndexFeed(ImageFeed):
    title = 'Index Feed - Imghost'
    link = ''
    description = 'Latest images from Imghost'
    
    def items(self):
        return Image.objects.order_by('-created')[:5]

class UserFeed(ImageFeed):
    
    def get_object(self, request, user):
        return get_object_or_404(User, username=user)
    
    def items(self, obj):
        return Image.objects.filter(user=obj).order_by('-created')[:5]

    def title(self, obj):
        return "%s's Feed - Imghost" % obj.username

    def link(self, obj):
        return reverse('main:user', args=(obj.username,))

    def description(self, obj):
        return "Latest images uploaded by user %s" % obj.username

class TagFeed(ImageFeed):
    
    def get_object(self, request, tag):
        return get_object_or_404(Tag, name=tag)
    
    def items(self, obj):
        return Image.objects.filter(tags__in=[obj,]).order_by('-created')[:5]

    def title(self, obj):
        return "%s - Tag Feed - Imghost" % obj.name

    def link(self, obj):
        return reverse('main:tag', args=(obj.name,))

    def description(self, obj):
        return "Latest images tagged with tag '%s'" % obj.name
    