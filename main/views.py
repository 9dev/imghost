from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.conf import settings

from taggit.models import Tag
from guardian.shortcuts import assign_perm
from guardian.decorators import permission_required_or_403
from ratelimit.decorators import ratelimit

from main.forms import ImageForm
from main.models import Image

class ImageCreateView(CreateView):
    form_class = ImageForm
    model = Image

    def dispatch(self, *args, **kwargs):
        return ratelimit(rate='5/m')(super(ImageCreateView, self).dispatch)(*args, **kwargs)

    def form_valid(self, form):
        if self.request.user.is_authenticated():
            form.instance.user = self.request.user
            image = form.save()
            assign_perm('delete_image', self.request.user, image)
        return super(ImageCreateView, self).form_valid(form)
    
    def get_form_kwargs(self, *args, **kwargs):
        result = super(ImageCreateView, self).get_form_kwargs(*args, **kwargs)
         
        try:
            result['data']['recaptcha_response_field']
            result['captcha'] = True
        except KeyError:
            # check if user should complete the captcha
            if getattr(self.request, 'limited', False):
                result['captcha'] = True
        
        return result

class ImageDeleteView(DeleteView):
    model = Image
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Image was successfully deleted.')
        
        # example e-mail usage - notify about deleting an image
        from django.core.mail import send_mail
        send_mail('An image was deleted', 'Body of the message.', settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=False)
        
        return reverse('main:index')
    
    @method_decorator(permission_required_or_403('main.delete_image', (Image, 'id', 'pk')))
    def dispatch(self, request, *args, **kwargs):
        return DeleteView.dispatch(self, request, *args, **kwargs)

class ImageDetailView(DetailView):
    model = Image
    
    def get_context_data(self, **kwargs):        
        context = super(ImageDetailView, self).get_context_data(**kwargs)
        context['embed'] = Image.OEmbed.html(context['image'], None, None, self.request)
        return context
    
class ImageListView(ListView):
    model = Image
    paginate_by = settings.RESULTS_PER_PAGE
    
    def get_queryset(self):
        return super(ImageListView, self).get_queryset().prefetch_related('tags')
    
class UserView(ImageListView):
    template_name = 'main/image_list_user.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        context['user_info'] = self.user
        return context
    
    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['user'])
        return Image.objects.filter(user=self.user).prefetch_related('tags')

class TagView(ImageListView):
    template_name = 'main/image_list_tag.html'
    
    def get_context_data(self, **kwargs):        
        context = super(TagView, self).get_context_data(**kwargs)
        context['tag_info'] = self.tag
        return context
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag'])
        return Image.objects.filter(tags__in=[self.tag,]).prefetch_related('tags')
    