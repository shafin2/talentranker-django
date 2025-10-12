"""
Usage Limits Middleware
Checks if users can upload JDs and CVs based on their plan limits
"""
from rest_framework.response import Response
from rest_framework import status
from apps.job_descriptions.models import JobDescription
from apps.cvs.models import CV


def check_jd_limit(view_func):
    """
    Decorator to check if user can upload JD based on plan limit.
    """
    def wrapper(request, *args, **kwargs):
        user = request.user
        
        if not user.is_authenticated:
            return Response(
                {'message': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.plan:
            return Response(
                {'message': 'No active plan. Please subscribe to a plan to use this feature.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        jd_limit = user.plan.jd_limit
        
        # -1 or None means unlimited
        if jd_limit == -1 or jd_limit is None:
            return view_func(request, *args, **kwargs)
        
        # Count active JDs
        active_jd_count = JobDescription.objects.filter(
            user=user,
            status='active'
        ).count()
        
        if active_jd_count >= jd_limit:
            return Response(
                {
                    'message': f'Job Description limit reached. Your plan allows {jd_limit} JD(s). Please upgrade your plan or archive existing JDs.',
                    'limit': jd_limit,
                    'current': active_jd_count
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def check_cv_limit(view_func):
    """
    Decorator to check if user can upload CV based on plan limit.
    """
    def wrapper(request, *args, **kwargs):
        user = request.user
        
        if not user.is_authenticated:
            return Response(
                {'message': 'Authentication required.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.plan:
            return Response(
                {'message': 'No active plan. Please subscribe to a plan to use this feature.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        cv_limit = user.plan.cv_limit
        
        # -1 or None means unlimited
        if cv_limit == -1 or cv_limit is None:
            return view_func(request, *args, **kwargs)
        
        # Count active CVs
        active_cv_count = CV.objects.filter(
            user=user,
            status='active'
        ).count()
        
        # Check how many CVs are being uploaded
        files = request.FILES.getlist('cvFiles') or request.FILES.getlist('files')
        upload_count = len(files) if files else 1
        
        if active_cv_count + upload_count > cv_limit:
            return Response(
                {
                    'message': f'CV limit exceeded. Your plan allows {cv_limit} CV(s). You have {active_cv_count} and trying to upload {upload_count} more.',
                    'limit': cv_limit,
                    'current': active_cv_count,
                    'attempting': upload_count
                },
                status=status.HTTP_403_FORBIDDEN
            )
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def update_usage_stats(user, usage_type):
    """
    Update user usage statistics.
    
    Args:
        user: User instance
        usage_type (str): 'jd' or 'cv'
    """
    try:
        if usage_type == 'jd':
            user.jd_used += 1
        elif usage_type == 'cv':
            user.cv_used += 1
        user.save()
    except Exception as e:
        print(f'Error updating usage stats: {str(e)}')
