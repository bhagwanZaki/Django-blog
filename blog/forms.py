from django.forms import ModelForm
from .models import *

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs['placeholder'] = "Post a comment"
    
    class Meta:
        model = Comment
        fields = ['body']

