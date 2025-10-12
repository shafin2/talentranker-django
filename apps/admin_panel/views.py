from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Sum
from apps.plans.models import Plan
from apps.users.serializers import UserSerializer, AdminUserUpdateSerializer
from apps.plans.serializers import PlanSerializer, PlanCreateSerializer, PlanUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


def is_admin(user):
    """Check if user is admin."""
    return user and user.is_authenticated and user.role == 'admin'


@api_view(['POST'])
@permission_classes([])
def admin_login(request):
    """
    Login admin user only.
    """
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'message': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find admin user by email
        try:
            user = User.objects.select_related('plan').get(
                email=email,
                role='admin',
                is_active=True
            )
        except User.DoesNotExist:
            return Response(
                {'message': 'Invalid admin credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check password
        if not user.check_password(password):
            return Response(
                {'message': 'Invalid admin credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Set refresh token as cookie
        response = Response({
            'message': 'Admin login successful',
            'accessToken': str(refresh.access_token),
            'user': UserSerializer(user).data
        })
        
        response.set_cookie(
            key='refreshToken',
            value=str(refresh),
            httponly=True,
            secure=not request.META.get('HTTP_HOST', '').startswith('localhost'),
            samesite='Strict',
            max_age=7 * 24 * 60 * 60  # 7 days
        )
        
        return response
    
    except Exception as e:
        logger.error(f'Admin login error: {str(e)}')
        return Response(
            {'message': 'Server error during admin login'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_logout(request):
    """
    Logout admin user.
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        response = Response({'message': 'Admin logged out successfully'})
        response.delete_cookie('refreshToken')
        return response
    
    except Exception as e:
        logger.error(f'Admin logout error: {str(e)}')
        return Response(
            {'message': 'Server error during admin logout'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admin_profile(request):
    """
    Get admin profile.
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    return Response({
        'message': 'Admin profile retrieved',
        'user': UserSerializer(request.user).data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_admin_dashboard(request):
    """
    Get admin dashboard statistics.
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Get comprehensive stats
        total_users = User.objects.filter(role='user', is_active=True).count()
        active_plans = Plan.objects.filter(is_active=True).count()
        
        # Calculate total JDs and CVs processed
        total_jds = User.objects.filter(role='user').aggregate(
            total=Sum('jd_used')
        )['total'] or 0
        
        total_cvs = User.objects.filter(role='user').aggregate(
            total=Sum('cv_used')
        )['total'] or 0
        
        return Response({
            'message': 'Admin dashboard data retrieved',
            'stats': {
                'totalUsers': total_users,
                'activePlans': active_plans,
                'totalJDsProcessed': total_jds,
                'totalCVsProcessed': total_cvs,
                'systemStatus': 'online'
            }
        })
    
    except Exception as e:
        logger.error(f'Admin dashboard error: {str(e)}')
        return Response(
            {'message': 'Server error during admin dashboard fetch'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== USER MANAGEMENT ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """
    List all users (admin only).
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        users = User.objects.filter(role='user').select_related('plan').order_by('-created_at')
        serializer = UserSerializer(users, many=True)
        
        return Response({
            'message': 'Users retrieved successfully',
            'users': serializer.data,
            'total': users.count()
        })
    
    except Exception as e:
        logger.error(f'Get users error: {str(e)}')
        return Response(
            {'message': 'Server error during user retrieval'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, id):
    """
    Get, update, or delete a specific user (admin only).
    GET: Retrieve user details
    PUT: Update user details
    DELETE: Delete user
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user = User.objects.select_related('plan').get(id=id, role='user')
    except User.DoesNotExist:
        return Response(
            {'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response({
            'message': 'User retrieved successfully',
            'user': serializer.data
        })
    
    elif request.method == 'PUT':
        try:
            serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'User updated successfully',
                    'user': UserSerializer(user).data
                })
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Update user error: {str(e)}')
            return Response(
                {'message': 'Server error during user update'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'DELETE':
        try:
            # Prevent self-deletion
            if user.id == request.user.id:
                return Response(
                    {'message': 'Cannot delete your own account'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.delete()
            
            return Response({
                'message': 'User deleted successfully'
            })
        except Exception as e:
            logger.error(f'Delete user error: {str(e)}')
            return Response(
                {'message': 'Server error during user deletion'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== PLAN MANAGEMENT ====================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def plans_list(request):
    """
    List all plans or create a new plan (admin only).
    GET: List all plans with optional filters
    POST: Create new plan
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        try:
            region = request.query_params.get('region')
            name = request.query_params.get('name')
            is_active = request.query_params.get('isActive')
            
            plans = Plan.objects.all()
            
            if region:
                plans = plans.filter(region=region)
            if name:
                plans = plans.filter(name=name)
            if is_active is not None:
                plans = plans.filter(is_active=is_active.lower() == 'true')
            
            plans = plans.order_by('region', 'sort_order', 'name')
            serializer = PlanSerializer(plans, many=True)
            
            return Response({
                'message': 'Plans retrieved successfully',
                'plans': serializer.data,
                'total': plans.count()
            })
        except Exception as e:
            logger.error(f'Get plans error: {str(e)}')
            return Response(
                {'message': 'Server error during plan retrieval'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'POST':
        try:
            serializer = PlanCreateSerializer(data=request.data)
            
            if serializer.is_valid():
                plan = serializer.save()
                return Response({
                    'message': 'Plan created successfully',
                    'plan': PlanSerializer(plan).data
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Create plan error: {str(e)}')
            return Response(
                {'message': 'Server error during plan creation'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def plan_detail(request, id):
    """
    Update or delete a specific plan (admin only).
    PUT: Update plan details
    DELETE: Delete plan
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        plan = Plan.objects.get(id=id)
    except Plan.DoesNotExist:
        return Response(
            {'message': 'Plan not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'PUT':
        try:
            # Log incoming data for debugging
            logger.info(f'Plan update request for plan {id}: {request.data}')
            
            serializer = PlanUpdateSerializer(plan, data=request.data, partial=True)
            
            if serializer.is_valid():
                updated_plan = serializer.save()
                logger.info(f'Plan {id} updated successfully: jd_limit={updated_plan.jd_limit}, cv_limit={updated_plan.cv_limit}')
                return Response({
                    'message': 'Plan updated successfully',
                    'plan': PlanSerializer(updated_plan).data
                })
            
            logger.error(f'Plan update validation failed: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f'Update plan error: {str(e)}')
            return Response(
                {'message': 'Server error during plan update'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    elif request.method == 'DELETE':
        try:
            # Check if any users are using this plan
            users_count = User.objects.filter(plan=plan).count()
            if users_count > 0:
                return Response(
                    {'message': f'Cannot delete plan. {users_count} user(s) are currently using this plan.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            plan.delete()
            
            return Response({
                'message': 'Plan deleted successfully'
            })
        except Exception as e:
            logger.error(f'Delete plan error: {str(e)}')
            return Response(
                {'message': 'Server error during plan deletion'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== ADDITIONAL USER MANAGEMENT ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, id):
    """
    Get single user by ID (admin only).
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user = User.objects.select_related('plan').get(id=id, role='user')
        serializer = UserSerializer(user)
        
        return Response({
            'message': 'User retrieved successfully',
            'user': serializer.data
        })
    
    except User.DoesNotExist:
        return Response(
            {'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f'Get user by ID error: {str(e)}')
        return Response(
            {'message': 'Server error during user retrieval'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_plan(request, id):
    """
    Update user's plan (admin only).
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user = User.objects.get(id=id, role='user')
        plan_id = request.data.get('planId')
        reset_usage = request.data.get('resetUsageOnUpgrade', False)
        
        if not plan_id:
            return Response(
                {'message': 'Plan ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response(
                {'message': 'Plan not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Update user's plan
        user.plan = plan
        
        # Reset usage if requested
        if reset_usage:
            user.jd_used = 0
            user.cv_used = 0
        
        user.save()
        
        return Response({
            'message': 'User plan updated successfully',
            'user': UserSerializer(user).data
        })
    
    except User.DoesNotExist:
        return Response(
            {'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f'Update user plan error: {str(e)}')
        return Response(
            {'message': 'Server error during plan update'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==================== ANALYTICS ====================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analytics(request):
    """
    Get analytics data (admin only).
    """
    if not is_admin(request.user):
        return Response(
            {'message': 'Admin access required.'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        from django.db.models import Count, Q
        from datetime import datetime, timedelta
        
        # Date range filter (default: last 30 days)
        date_range = request.query_params.get('dateRange', '30')
        days = int(date_range) if date_range.isdigit() else 30
        start_date = datetime.now() - timedelta(days=days)
        
        # User statistics
        total_users = User.objects.filter(role='user').count()
        active_users = User.objects.filter(role='user', is_active=True).count()
        new_users = User.objects.filter(role='user', created_at__gte=start_date).count()
        
        # Plan distribution
        plan_distribution = Plan.objects.filter(users__role='user').annotate(
            user_count=Count('users')
        ).values('name', 'region', 'user_count').order_by('-user_count')
        
        # Usage statistics
        total_jds = User.objects.filter(role='user').aggregate(
            total=Sum('jd_used')
        )['total'] or 0
        
        total_cvs = User.objects.filter(role='user').aggregate(
            total=Sum('cv_used')
        )['total'] or 0
        
        return Response({
            'message': 'Analytics retrieved successfully',
            'analytics': {
                'users': {
                    'total': total_users,
                    'active': active_users,
                    'new': new_users
                },
                'usage': {
                    'totalJDs': total_jds,
                    'totalCVs': total_cvs
                },
                'planDistribution': list(plan_distribution)
            }
        })
    
    except Exception as e:
        logger.error(f'Get analytics error: {str(e)}')
        return Response(
            {'message': 'Server error during analytics retrieval'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

