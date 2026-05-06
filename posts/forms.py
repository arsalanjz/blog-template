from django import forms
from django.core.exceptions import ValidationError

from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 18, 'placeholder': 'Enter Content'}),
        }



