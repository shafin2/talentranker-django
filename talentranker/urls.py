"""
URL configuration for TalentRanker project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.utils import timezone


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({
        'status': 'ok',
        'timestamp': timezone.now().isoformat()
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health', health_check, name='health_check'),
    
    # API Routes
    path('api/auth/', include('apps.authentication.urls')),
    path('api/admin/', include('apps.admin_panel.urls')),
    path('api/jd/', include('apps.job_descriptions.urls')),
    path('api/cv/', include('apps.cvs.urls')),
    path('api/ranking/', include('apps.rankings.urls')),
    path('api/plans/', include('apps.plans.urls')),
    path('api/users/', include('apps.users.urls')),
]

