"""
Authentication Views - Clean Django + SQLite Implementation
Includes: Signup, Login, Logout, Refresh Token, Google OAuth
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings
from apps.plans.models import Plan
from apps.users.serializers import UserSerializer
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


def get_tokens_for_user(user):
    """Generate JWT tokens for user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint."""
    from datetime import datetime
    return Response({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'database': 'SQLite'
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Register a new user.
    Auto-assigns Freemium plan.
    """
    try:
        name = request.data.get('name', '').strip()
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')
        
        # Validation
        if not all([name, email, password]):
            return Response(
                {'message': 'Name, email, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(password) < 6:
            return Response(
                {'message': 'Password must be at least 6 characters'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'message': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get Freemium plan
        try:
            freemium_plan = Plan.objects.get(name='Freemium')
        except Plan.DoesNotExist:
            logger.error("Freemium plan not found")
            return Response(
                {'message': 'System configuration error. Please contact support.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            role='user',
            plan=freemium_plan
        )
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        # Response
        response = Response({
            'message': 'User registered successfully',
            'accessToken': tokens['access'],
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
        
        # Set refresh token cookie
        response.set_cookie(
            key='refreshToken',
            value=tokens['refresh'],
            httponly=True,
            secure=False,  # Set True in production with HTTPS
            samesite='Lax',
            max_age=7 * 24 * 60 * 60  # 7 days
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Signup error: {str(e)}", exc_info=True)
        return Response(
            {'message': f'Server error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user."""
    try:
        email = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')
        
        if not email or not password:
            return Response(
                {'message': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user - ONLY role='user', exclude admins
        try:
            user = User.objects.get(email=email, role='user')
        except User.DoesNotExist:
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Check password
        if not user.check_password(password):
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        # Response
        response = Response({
            'message': 'Login successful',
            'accessToken': tokens['access'],
            'user': UserSerializer(user).data
        })
        
        # Set refresh token cookie
        response.set_cookie(
            key='refreshToken',
            value=tokens['refresh'],
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=7 * 24 * 60 * 60
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return Response(
            {'message': f'Server error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    """
    Google OAuth authentication.
    Accepts Google ID token and creates/logs in user.
    """
    try:
        token = request.data.get('token')
        
        if not token:
            return Response(
                {'message': 'Google token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify Google token
        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')
            
            google_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo.get('name', '')
            avatar = idinfo.get('picture', '')
            
        except ValueError as e:
            return Response(
                {'message': f'Invalid Google token: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user exists
        user = User.objects.filter(email=email).first()
        
        if user:
            # Update Google ID if not set
            if not user.google_id:
                user.google_id = google_id
                user.avatar = avatar
                user.save()
        else:
            # Create new user
            freemium_plan = Plan.objects.get(name='Freemium')
            user = User.objects.create(
                email=email,
                name=name,
                role='user',
                plan=freemium_plan,
                google_id=google_id,
                avatar=avatar
            )
            # No password for Google users
        
        # Generate tokens
        tokens = get_tokens_for_user(user)
        
        # Response
        response = Response({
            'message': 'Google authentication successful',
            'accessToken': tokens['access'],
            'user': UserSerializer(user).data
        })
        
        # Set refresh token cookie
        response.set_cookie(
            key='refreshToken',
            value=tokens['refresh'],
            httponly=True,
            secure=False,
            samesite='Lax',
            max_age=7 * 24 * 60 * 60
        )
        
        return response
        
    except Plan.DoesNotExist:
        return Response(
            {'message': 'System configuration error'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        logger.error(f"Google auth error: {str(e)}", exc_info=True)
        return Response(
            {'message': f'Server error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout user."""
    response = Response({'message': 'Logged out successfully'})
    response.delete_cookie('refreshToken')
    return response


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """Refresh access token."""
    try:
        refresh = request.COOKIES.get('refreshToken')
        
        if not refresh:
            return Response(
                {'message': 'Refresh token not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token = RefreshToken(refresh)
        
        return Response({
            'message': 'Token refreshed successfully',
            'accessToken': str(token.access_token)
        })
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        return Response(
            {'message': 'Invalid refresh token'},
            status=status.HTTP_401_UNAUTHORIZED
        )
