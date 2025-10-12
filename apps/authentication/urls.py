from django.urls import path
from . import views

urlpatterns = [
    path('health', views.health_check, name='health'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('refresh', views.refresh_token, name='refresh_token'),
    path('google', views.google_auth, name='google_auth'),
]
