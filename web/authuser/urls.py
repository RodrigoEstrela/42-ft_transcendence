from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "authuser"
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('home/', views.home, name='home'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit/', views.edit_profile, name='edit_profile'),
]
