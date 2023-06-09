"""
URL configuration for blog_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Auth
    path('register/', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),

    # User Pages
    path('account/<int:id>', views.account, name='account'),
    path('account/settings', views.settings, name='settings'),

    # Post Links
    path('new-post', views.new_post, name='new-post'),
    path('edit-post/<int:id_post>', views.edit_post, name='edit-post'),

    # Page
    path('posts', views.all_posts, name='all-posts'),
    path('posts/tag/<str:tag>', views.tag_posts, name='tag-posts'),
    path('users', views.all_users, name='all-users'),
    path('post/<int:id_post>', views.page_post, name='post-page'),
    path('support', views.support, name='support'),
    path('search', views.search_page, name='search'),

    path('test', views.get_search),


    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = 'blog.views.handler404'
# handler500 = 'blog.views.handler500'