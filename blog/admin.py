from django.contrib import admin
from .models import UserProfile, Post, Tag, Promotion

# Register your models here.
admin.site.register([UserProfile])

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'tag_id', 'author_id', 'is_active', 'created_at']
    list_filter = ['is_active', 'tag_id']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_field = ['name']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):

    list_filter = ['is_enabled']
    actions = ['make_enabled' , 'make_disabled']

    @admin.action(description="Отключить отображение")
    def make_disabled(self, request, queryset):
        queryset.update(is_enabled=False)

    @admin.action(description='Включить отображение')
    def make_enabled(self, request, queryset):
        queryset.update(is_enabled=True)