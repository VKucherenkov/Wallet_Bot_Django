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

from django.urls import path

from Bot.wiews import Cards, Categoryes, Types, TelegramUserShow, TelegramUsersShow, AllOperation, \
    RegisterUser, LoginUser, logout_user, IndexShow, MyUserUpdate, AboutShow, ContactShow, AnaliticsShow, SecurityShow, \
    InterfaceShow, AnalizShow, AddOperationShow, AddOperationView, AddCardView, AddCategoryView, AddRecipientView, \
    AddTypeView, AddBankView

urlpatterns = [
    path('', IndexShow.as_view(), name='home'),
    path('home/', IndexShow.as_view(), name='home'),
    path('analitics/', AnaliticsShow.as_view(), name='analitics'),
    path('security/', SecurityShow.as_view(), name='security'),
    path('interface/', InterfaceShow.as_view(), name='interface'),
    path('analiz/', AnalizShow.as_view(), name='analiz'),
    path('add-operation/', AddOperationShow.as_view(), name='add-operation'),
    path('add-operation-form/', AddOperationView.as_view(), name='add-operation-form'),
    path('add-card-form/', AddCardView.as_view(), name='add-card-form'),
    path('add-category-form/', AddCategoryView.as_view(), name='add-category-form'),
    path('add-recipient-form/', AddRecipientView.as_view(), name='add-recipient-form'),
    path('add-type-form/', AddTypeView.as_view(), name='add-type-form'),
    path('add-bank-form/', AddBankView.as_view(), name='add-bank-form'),
    path('about/', AboutShow.as_view(), name='about'),
    path('users/', TelegramUsersShow.as_view(), name='users'),
    path('contact/', ContactShow.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/<slug:profile_slug>/', MyUserUpdate.as_view(), name='profile'),
    path('user/<slug:userdetail_slug>/', TelegramUserShow.as_view(), name='userdetail'),
    path('user/<slug:userdetail_slug>/cards/', Cards.as_view(), name='cards'),
    path('user/<slug:userdetail_slug>/types/', Types.as_view(), name='types'),
    path('user/<slug:userdetail_slug>/categoryes/', Categoryes.as_view(), name='categoryes'),
    path('user/<slug:userdetail_slug>/all_operation/', AllOperation.as_view(), name='all_operation'),

]
