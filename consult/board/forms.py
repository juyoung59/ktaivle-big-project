from django import forms
from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget
from .models import Post

CATEGORY = (('FAQ', 'FAQ'), ('Inquiry', 'Inquiry'))

class BoardWriteForm(forms.ModelForm):
    title = forms.CharField()
    contents = SummernoteWidget()
    category =  forms.ChoiceField(choices=CATEGORY)
    class Meta:
        model = Post
        fields = ['title', 'contents', 'category']
        widgets = {
            'contents':SummernoteWidget()
        }
        