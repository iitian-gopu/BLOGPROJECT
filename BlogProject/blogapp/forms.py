from django import forms
from .models import *

  
# creating a form 
class EmailForm(forms.Form):
  
    name = forms.CharField(max_length = 200)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,widget=forms.Textarea)





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
    
    # overriding default form setting and adding bootstrap class
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs = {'placeholder': 'Enter name','class':'form-control'}
        self.fields['email'].widget.attrs = {'placeholder': 'Enter email', 'class':'form-control'}
        self.fields['body'].widget.attrs = {'placeholder': 'Comment here...', 'class':'form-control', 'rows':'5'}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'    

