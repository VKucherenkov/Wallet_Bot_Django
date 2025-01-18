"""
URL configuration for MyBot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from debug_toolbar.toolbar import debug_toolbar_urls
from django import views

from django.urls import path, include

from .wiews import index, about, contact, Cards, Categoryes, Types, TelegramUserShow, TelegramUsersShow, AllOperation, \
    RegisterUser, LoginUser, logout_user

urlpatterns = [
    path('', index, name='home'),
    path('home/', index, name='home'),
    path('about/', about, name='about'),
    path('users/', TelegramUsersShow.as_view(), name='users'),
    path('contact/', contact, name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('user/<slug:userdetail_slug>/', TelegramUserShow.as_view(), name='userdetail'),
    path('user/<slug:userdetail_slug>/cards/', Cards.as_view(), name='cards'),
    path('user/<slug:userdetail_slug>/types/', Types.as_view(), name='types'),
    path('user/<slug:userdetail_slug>/categoryes/', Categoryes.as_view(), name='categoryes'),
    path('user/<slug:userdetail_slug>/all_operation/', AllOperation.as_view(), name='all_operation'),

]
