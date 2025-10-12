from rest_framework import serializers
from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for Plan model."""
    
    display_name = serializers.CharField(read_only=True)
    _id = serializers.IntegerField(source='id', read_only=True)
    # CamelCase aliases for frontend compatibility
    jdLimit = serializers.IntegerField(source='jd_limit', read_only=True)
    cvLimit = serializers.IntegerField(source='cv_limit', read_only=True)
    billingCycle = serializers.CharField(source='billing_cycle', read_only=True)
    isActive = serializers.BooleanField(source='is_active', read_only=True)
    sortOrder = serializers.IntegerField(source='sort_order', read_only=True)
    displayName = serializers.CharField(source='display_name', read_only=True)
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    
    class Meta:
        model = Plan
        fields = ['id', '_id', 'name', 'region', 'billing_cycle', 'billingCycle', 
                  'price', 'currency', 'jd_limit', 'jdLimit', 'cv_limit', 'cvLimit',
                  'description', 'features', 'is_active', 'isActive',
                  'sort_order', 'sortOrder', 'display_name', 'displayName',
                  'created_at', 'createdAt', 'updated_at', 'updatedAt']
        read_only_fields = ['id', '_id', 'created_at', 'updated_at']


class PlanCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new plan."""
    
    # Accept camelCase fields from frontend
    jdLimit = serializers.IntegerField(source='jd_limit', required=False, allow_null=True)
    cvLimit = serializers.IntegerField(source='cv_limit', required=False, allow_null=True)
    billingCycle = serializers.CharField(source='billing_cycle', required=False, allow_blank=True, allow_null=True)
    isActive = serializers.BooleanField(source='is_active', required=False)
    sortOrder = serializers.IntegerField(source='sort_order', required=False)
    
    class Meta:
        model = Plan
        fields = ['name', 'region', 'billing_cycle', 'billingCycle', 'price', 'currency',
                  'jd_limit', 'jdLimit', 'cv_limit', 'cvLimit', 
                  'description', 'features', 'is_active', 'isActive', 
                  'sort_order', 'sortOrder']
        extra_kwargs = {
            'jd_limit': {'required': False, 'allow_null': True},
            'cv_limit': {'required': False, 'allow_null': True},
            'billing_cycle': {'required': False, 'allow_blank': True, 'allow_null': True},
        }
        # Override validators to prevent unique_together conflict with duplicate fields
        validators = []
    
    def validate(self, data):
        """
        Custom validation for unique_together constraint.
        Check manually since we have duplicate field names.
        """
        name = data.get('name')
        region = data.get('region')
        billing_cycle = data.get('billing_cycle')
        
        # Check if plan with same combination exists
        existing = Plan.objects.filter(
            name=name,
            region=region,
            billing_cycle=billing_cycle
        ).first()
        
        if existing:
            raise serializers.ValidationError({
                'name': f'A plan with name "{name}", region "{region}", and billing cycle "{billing_cycle}" already exists.'
            })
        
        return data


class PlanUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating plan details."""
    
    # Accept camelCase fields from frontend
    jdLimit = serializers.IntegerField(source='jd_limit', required=False, allow_null=True)
    cvLimit = serializers.IntegerField(source='cv_limit', required=False, allow_null=True)
    billingCycle = serializers.CharField(source='billing_cycle', required=False, allow_blank=True, allow_null=True)
    isActive = serializers.BooleanField(source='is_active', required=False)
    sortOrder = serializers.IntegerField(source='sort_order', required=False)
    
    class Meta:
        model = Plan
        fields = ['name', 'region', 'billing_cycle', 'billingCycle', 'price', 'currency',
                  'jd_limit', 'jdLimit', 'cv_limit', 'cvLimit', 
                  'description', 'features', 'is_active', 'isActive', 
                  'sort_order', 'sortOrder']
        extra_kwargs = {
            'jd_limit': {'required': False, 'allow_null': True},
            'cv_limit': {'required': False, 'allow_null': True},
            'name': {'required': False},
            'region': {'required': False},
            'billing_cycle': {'required': False, 'allow_blank': True, 'allow_null': True},
        }
        # Override validators to prevent unique_together conflict with duplicate fields
        validators = []
    
    def validate(self, data):
        """
        Custom validation for unique_together constraint.
        Check manually since we have duplicate field names.
        """
        if self.instance:
            # For updates, only validate if these fields are being changed
            name = data.get('name', self.instance.name)
            region = data.get('region', self.instance.region)
            billing_cycle = data.get('billing_cycle', self.instance.billing_cycle)
            
            # Check if another plan exists with same combination
            existing = Plan.objects.filter(
                name=name,
                region=region,
                billing_cycle=billing_cycle
            ).exclude(id=self.instance.id).first()
            
            if existing:
                raise serializers.ValidationError({
                    'name': f'A plan with name "{name}", region "{region}", and billing cycle "{billing_cycle}" already exists.'
                })
        
        return data
