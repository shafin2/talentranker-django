from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer
from apps.job_descriptions.models import JobDescription
from apps.job_descriptions.serializers import JobDescriptionSerializer
from apps.cvs.models import CV
from apps.cvs.serializers import CVSerializer
from apps.plans.models import Plan
from apps.plans.serializers import PlanSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """Get current user profile."""
    serializer = UserSerializer(request.user)
    return Response({
        'success': True,
        'user': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_usage_stats(request):
    """Get user usage statistics."""
    user = request.user
    return Response({
        'success': True,
        'stats': {
            'jdUsed': user.jd_used,
            'cvUsed': user.cv_used,
            'jdLimit': user.plan.jd_limit if user.plan else None,
            'cvLimit': user.plan.cv_limit if user.plan else None,
            'planName': user.plan.name if user.plan else None
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_jds(request):
    """Get all job descriptions for the current user."""
    jds = JobDescription.objects.filter(user=request.user).order_by('-created_at')
    serializer = JobDescriptionSerializer(jds, many=True)
    return Response({
        'success': True,
        'jds': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cvs(request):
    """Get all CVs for the current user."""
    cvs = CV.objects.filter(user=request.user).order_by('-created_at')
    serializer = CVSerializer(cvs, many=True)
    return Response({
        'success': True,
        'cvs': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_available_plans(request):
    """Get all available plans."""
    plans = Plan.objects.filter(is_active=True).order_by('sort_order')
    serializer = PlanSerializer(plans, many=True)
    return Response({
        'success': True,
        'plans': serializer.data
    })

urlpatterns = [
    path('me', get_current_user, name='get_current_user'),
    path('usage', get_usage_stats, name='get_usage_stats'),
    path('jds', get_user_jds, name='get_user_jds'),
    path('cvs', get_user_cvs, name='get_user_cvs'),
    path('plans', get_available_plans, name='get_available_plans'),
]
