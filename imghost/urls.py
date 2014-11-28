from django.conf.urls import patterns, include, url, handler403
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^info', include('django.contrib.flatpages.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^oembed', include('oembed9.urls', namespace='oembed9')),
    url(r"^ratings/", include("agon_ratings.urls")),
    url(r"^comments/", include("dialogos.urls")),
    url(r'^', include('main.urls',namespace='main')),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# sitemap

from django.contrib.sitemaps import views, Sitemap
from django.views.decorators.cache import cache_page
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.auth.models import User
from django.conf import settings

from main.models import Image

from taggit.models import Tag

class TagSitemap(Sitemap):
    def items(self):
        return Tag.objects.all()
    
    def location(self, item):
        return reverse('main:tag', args=(item.name,))
    
class UserSitemap(Sitemap):
    def items(self):
        return User.objects.all().exclude(id=settings.ANONYMOUS_USER_ID)
    
    def location(self, item):
        return reverse('main:user', args=(item.username,))

sitemaps = {
    'flatpages': FlatPageSitemap,
    'images': GenericSitemap({'queryset': Image.objects.all(),}),
    'tags': TagSitemap,
    'users': UserSitemap,
}

urlpatterns = urlpatterns + [
    url(r'^sitemap\.xml$',
        cache_page(86400)(views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(86400)(views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),
]
