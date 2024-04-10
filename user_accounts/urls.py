"""Defines URL patterns for accounts."""
from django.urls import path, include
from .import views
from django.contrib.auth import views as auth_views  # Import the auth views

app_name = 'user_accounts'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    # Registeration page.
    path('register/', views.register, name='register'),
    # Logout page
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]