from django.forms import ModelForm, Textarea, ValidationError
from django.core.urlresolvers import reverse
from django.core.files.images import get_image_dimensions

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Field, Div
from crispy_forms.bootstrap import FormActions

from captcha.fields import ReCaptchaField

from main.models import Image

class ImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        
        captcha = kwargs.pop('captcha', None)
        super(ImageForm, self).__init__(*args, **kwargs)
        
        if captcha:
            self.fields['captcha'] = ReCaptchaField(
                attrs={'theme':'white'},
                error_messages={
                    'required': 'Enter the CAPTCHA code.',
                    'captcha_invalid': 'The CAPTCHA code you entered is invalid. Try again.',
                }
            )
        
        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('main:upload')
        self.helper.layout = Layout(
            Fieldset('Upload an image', 'image', 'title', 'description', 'tags', 'nsfw', 'captcha'),
            Submit('Upload', 'Upload'),
        )
    
    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            raise ValidationError("You have not selected any image.")
        else:
            w, h = get_image_dimensions(image)
            if w <= 50 or h <=50:
                raise ValidationError("Your image is too small.")
        return image
    
    class Meta:
        model = Image
        fields = ['image', 'title', 'description', 'tags', 'nsfw']
        widgets = {'description': Textarea(attrs={'rows':3})}
        