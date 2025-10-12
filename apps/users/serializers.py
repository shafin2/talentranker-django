from rest_framework import serializers
from .models import User, RefreshToken
from apps.plans.models import Plan


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model (used in user serializer)."""
    
    _id = serializers.IntegerField(source='id', read_only=True)
    # CamelCase aliases
    jdLimit = serializers.IntegerField(source='jd_limit', read_only=True)
    cvLimit = serializers.IntegerField(source='cv_limit', read_only=True)
    billingCycle = serializers.CharField(source='billing_cycle', read_only=True)
    displayName = serializers.CharField(source='display_name', read_only=True)
    
    class Meta:
        model = Plan
        fields = ['id', '_id', 'name', 'region', 
                  'billing_cycle', 'billingCycle',
                  'price', 'currency', 
                  'jd_limit', 'jdLimit',
                  'cv_limit', 'cvLimit',
                  'features', 
                  'display_name', 'displayName']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    plan = PlanSerializer(read_only=True)
    _id = serializers.IntegerField(source='id', read_only=True)
    # CamelCase aliases
    jdUsed = serializers.IntegerField(source='jd_used', read_only=True)
    cvUsed = serializers.IntegerField(source='cv_used', read_only=True)
    googleId = serializers.CharField(source='google_id', read_only=True)
    isActive = serializers.BooleanField(source='is_active', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', '_id', 'name', 'email', 'role', 'plan', 
                  'jd_used', 'jdUsed',
                  'cv_used', 'cvUsed', 
                  'google_id', 'googleId',
                  'avatar', 
                  'is_active', 'isActive',
                  'created_at', 'createdAt',
                  'updated_at', 'updatedAt']
        read_only_fields = ['id', '_id', 'role', 'jd_used', 'cv_used', 'google_id', 
                           'avatar', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user."""
    
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
    
    def create(self, validated_data):
        """Create a new user with hashed password."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user details."""
    
    class Meta:
        model = User
        fields = ['name', 'email']


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for admin to update user details including plan."""
    
    plan_id = serializers.IntegerField(write_only=True, required=False)
    planId = serializers.IntegerField(source='plan_id', write_only=True, required=False)  # CamelCase alias
    
    class Meta:
        model = User
        fields = ['name', 'email', 'role', 'plan_id', 'planId', 'is_active']
    
    def update(self, instance, validated_data):
        """Update user with plan change."""
        # Handle both plan_id (snake_case) and planId (camelCase)
        plan_id = validated_data.pop('plan_id', None)
        
        if plan_id is not None:
            try:
                plan = Plan.objects.get(id=plan_id)
                instance.plan = plan
            except Plan.DoesNotExist:
                raise serializers.ValidationError({'plan_id': 'Plan not found'})
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
