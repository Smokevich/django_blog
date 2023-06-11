from django.contrib import admin
from .models import UserProfile, Post, Tag

# Register your models here.
admin.site.register([UserProfile, Post, Tag])