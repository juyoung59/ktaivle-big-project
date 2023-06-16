from django import forms
from django_summernote.fields import SummernoteTextFormField
from django_summernote.widgets import SummernoteWidget
from .models import Post

CATEGORY = (('FAQ', 'FAQ'), ('Inquiry', 'Inquiry'))

class PostingForm(forms.Form):
    title = forms.CharField(label='Title')
    # detail = forms.CharField(label='detail', widget=SummernoteWidget())
    detail = forms.CharField(label='Detail')
    category =  forms.ChoiceField(label='Category', choices=CATEGORY)
    class Meta:
        model = Post
        fields = ['title', 'detail', 'category']
        # widgets = {
        #     'detail': SummernoteWidget(),
        # }
        
class PostingUpdateForm(forms.ModelForm):
    title = forms.CharField(label='Title')
    detail = forms.CharField(label='Detail')
    class Meta:
        model = Post
        fields = ['title', 'detail']