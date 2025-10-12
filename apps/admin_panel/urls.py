from django.urls import path
from . import views

urlpatterns = [
    # Admin Auth
    path('login', views.admin_login, name='admin_login'),
    path('logout', views.admin_logout, name='admin_logout'),
    path('profile', views.get_admin_profile, name='admin_profile'),
    path('dashboard', views.get_admin_dashboard, name='admin_dashboard'),
    
    # User Management
    path('users', views.get_all_users, name='get_all_users'),
    path('users/<int:id>/plan', views.update_user_plan, name='update_user_plan'),
    path('users/<int:id>', views.user_detail, name='user_detail'),  # Handles GET, PUT, DELETE
    
    # Plan Management
    path('plans', views.plans_list, name='plans_list'),  # Handles GET, POST
    path('plans/<int:id>', views.plan_detail, name='plan_detail'),  # Handles PUT, DELETE
    
    # Analytics
    path('analytics', views.get_analytics, name='get_analytics'),
]
