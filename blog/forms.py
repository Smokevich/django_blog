from django import forms
from django.contrib.auth.models import User
from .models import Post, UserProfile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'seo_description', 'seo_keys', 'image', 'text']


class SettingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']