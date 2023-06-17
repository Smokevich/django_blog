from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

# Create your models here.
class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Аватар'
        verbose_name_plural = 'Аватары'
        
    user   = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='upload/avatar', default='')

    def __str__(self) -> str:
        return self.user.username

class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(verbose_name='Название тега', max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    name            = models.CharField(verbose_name='Название поста', max_length=150)
    seo_description = models.CharField(verbose_name='Описание поста', max_length=200, blank=True)
    seo_keys        = models.CharField(verbose_name="Ключевые слова", max_length=300, blank=True)
    image           = models.ImageField(verbose_name='Картинка поста', upload_to='upload/images')
    text            = tinymce_models.HTMLField(verbose_name='Текст поста')
    author_id       = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    tag_id          = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='Тег')
    created_at      = models.DateTimeField(verbose_name='Пост создан', auto_now_add=True)
    is_active       = models.BooleanField(verbose_name='Включить отображение', default=False)

    def __str__(self) -> str:
        return self.name
    
class Promotion(models.Model):
    class Meta:
        verbose_name = 'Промо'
        verbose_name_plural = 'Промо'

    post = models.OneToOneField(Post, on_delete=models.CASCADE, verbose_name='Пост')
    is_enabled = models.BooleanField(default=False, verbose_name='Включить промо отображение')