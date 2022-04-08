from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.ListClass.as_view(), name='home'),
    path('detail/<pk>/', views.CommentForm.as_view(), name='detail'),
    path('new-post/', views.FormClass.as_view(), name="new-post"),
    path('accounts/login/', views.MyLoginView.as_view(), name="login"),
    path('accounts/logout/', views.MyLogoutView.as_view(), name="logout"),
    path('accounts/create/', views.UserCreateView.as_view(),name="create"), 
]