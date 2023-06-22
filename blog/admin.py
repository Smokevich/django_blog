from django.contrib import admin
from .models import UserProfile, Post, Tag, Promotion, HistoryViews, RatingPost, RatingAuthor

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'tag_id', 'author_id', 'is_active', 'created_at']
    list_filter = ['is_active', 'tag_id']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ['user', 'avatar']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):

    search_fields = ['post__name']
    list_display = ['post', 'is_enabled']
    list_filter = ['is_enabled']
    actions = ['make_enabled' , 'make_disabled']

    @admin.action(description="Отключить отображение")
    def make_disabled(self, request, queryset):
        queryset.update(is_enabled=False)

    @admin.action(description='Включить отображение')
    def make_enabled(self, request, queryset):
        queryset.update(is_enabled=True)

@admin.register(HistoryViews)
class HistoryViewsAdmin(admin.ModelAdmin):
    search_fields = ['user', 'post_id__name']
    list_display = ['user', 'post_id', 'author_id', 'datetime']

@admin.register(RatingPost)
class RatingPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'count_views']

@admin.register(RatingAuthor)
class RatingAuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'count_views']