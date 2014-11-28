from django.core.management.base import BaseCommand, CommandError
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

def create_flatpage(url, title, content):
    try:
        FlatPage.objects.get(url=url)
    except FlatPage.DoesNotExist:
        fp = FlatPage.objects.create(url=url,title=title,content=content)
        fp.sites.add(Site.objects.get(id=1))

class Command(BaseCommand):
    def handle(self, *args, **options):
        FlatPage.objects.all().delete()
        
        create_flatpage('/about', 'About', '<p><b>Imghost</b> is a place where everyone can store their images as well as browse thousands of pictures already uploaded by our users.</p>')
        create_flatpage('/contact', 'Contact', '<p>You can contact us at <b>imghost@imghost</b></p>')
        create_flatpage('/tos', 'Terms Of Service', '<ul><li>Do not upload copyrighted images</li><li>Do not offend other users</li><li>Have fun ;)</li></ul>')
        create_flatpage('/oembed', 'oEmbed', '<p><b>Imghost</b> allows you to embed our images on your website or blog free of charge. In order to do that, use embed code provided with every image.</p><p>If you need to customize embed code feel free to use our <b>oEmbed API</b>. Example usage:<br><a href="/oembed?url=http://imghost/image/3">oEmbed for image with ID 3</a></p>')