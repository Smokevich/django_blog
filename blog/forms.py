from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'seo_description', 'seo_keys', 'image', 'text']