import sys

from urlparse import urlsplit
from importlib import import_module

from django.db import models
from django.core import urlresolvers
from django.http import HttpResponse, Http404, HttpResponse
from django.conf import settings
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from sorl.thumbnail import get_thumbnail

from utils import *

def index(request):
    
    # validate arguments
    
    input_url = request.GET.get('url', None)
    if not input_url:
        raise Http404
        
    maxwidth = request.GET.get('maxwidth', sys.maxsize)
    maxheight = request.GET.get('maxheight', sys.maxsize)    
    format = request.GET.get('format', 'json')
    
    maxheight = int(maxheight)
    if maxheight <= 0:
        return HttpResponse('400 Bad Request', status=400)
    
    maxwidth = int(maxwidth)
    if maxwidth <= 0:
        return HttpResponse('400 Bad Request', status=400)
    
    if format != 'xml' and format != 'json':
        return HttpResponse('501 Not Implemented', status=501)
    
    # get the view and kwargs
    
    match = urlresolvers.resolve(urlsplit(input_url).path) # returns 404 on bad URL
    view = match.func
    params = match.kwargs
    
    module = import_module(view.__module__)
    cls = getattr(module, view.__name__)
    
    # get the model and pk
    
    model = getattr(cls, 'model', None)
    pk = params.get('pk', None)
    
    if not model or not pk:
        raise Http404
    
    if not isinstance(model(), models.Model):
        if settings.DEBUG:
            raise Exception('You need to define "model" variable as a class that extends django.db.models.Model')
        raise Http404
    
    try:
        model.OEmbed
    except Exception:
        if settings.DEBUG:
            raise Exception('You need to define an inner class OEmbed in your model')
        raise Http404
    
    # get the object and set initial data
    
    obj = get_object_or_404(model, pk=pk)
    
    data = {}
    data['version'] = '1.0'
    data['provider_name'] = getattr(settings, 'OEMBED9_PROVIDER_NAME', None)
    data['provider_url'] = getattr(settings, 'OEMBED9_PROVIDER_URL', None)
    
    # value getter from model.OEmbed
        
    def get_value(name, obj):
        if not isinstance(obj, list):
            obj = [obj,]
        
        attr = getattr(model.OEmbed, name, None)
        
        if attr:
            if hasattr(attr, '__call__'):
                attr = attr(*obj)
                
        return attr
        
    # set the data obtained from the model.OEmbed
         
    data['type'] = getattr(model.OEmbed, 'type', 'link')
    data['cache_age'] = get_value('cache_age', obj)
    data['title'] = get_value('title', obj)
    data['author_name'] = get_value('author_name', obj)
    data['author_url'] = get_value('author_url', obj)
    data['html'] = get_value('html', [obj, maxwidth, maxheight, request])
    photo_field = get_value('photo_field', obj)
    thumbnail_field = get_value('thumbnail_field', obj)
    
    if data.get('html'):
        from django.utils.html import escape
        data['html'] = escape(data['html'])
    
    sizes = get_value('sizes', obj)
    thumbnail_sizes = get_value('thumbnail_sizes', obj)
    
    # ensure all required fields are set
    
    if data.get('type') != 'link':
        if data.get('type') == 'photo':
            if not photo_field:
                missing('photo_field')
        else:
            if not sizes:
                missing('sizes')
            if not data.get('html'):
                missing('html')
                
    if thumbnail_sizes:
        if not thumbnail_field:
            if not photo_field:
                missing('thumbnail_field')
            else:
                thumbnail_field = photo_field
    
    # calculate the sizes and set them
    
    if sizes:
        data['width'], data['height'] = get_size(sizes, maxwidth, maxheight)
    
    if thumbnail_sizes:
        data['thumbnail_width'], data['thumbnail_height'] = get_size(thumbnail_sizes, maxwidth, maxheight)
        im = get_thumbnail(getattr(obj,thumbnail_field), str(data['thumbnail_width']) + 'x' + str(data['thumbnail_height']))
        data['thumbnail_width'], data['thumbnail_height'] = im.width, im.height
        data['thumbnail_url'] = request.build_absolute_uri(im.url)
    
    # build URLs
    
    if data.get('author_url'):                
        data['author_url'] = request.build_absolute_uri(data['author_url'])
        
    if photo_field:
        data['url'] = request.build_absolute_uri(getattr(obj,photo_field).url)

    # set the cache time

    if data.get('cache_age', False):
        data['cache_age'] = getattr(settings, 'OEMBED9_CACHE_AGE', None)      
    
    # clean, format and then return the data
    
    data = format_data(data, format)
    return HttpResponse(data)
