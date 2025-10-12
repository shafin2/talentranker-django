from rest_framework import serializers
from .models import CV


class CVSerializer(serializers.ModelSerializer):
    """Serializer for CV model."""
    
    # Add camelCase aliases for frontend compatibility
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    fileSize = serializers.IntegerField(source='file_size', read_only=True)
    
    class Meta:
        model = CV
        fields = ['id', 'filename', 'content', 'file_size', 'fileSize', 'status', 
                  'created_at', 'createdAt', 'updated_at', 'updatedAt']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CVCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a CV."""
    
    class Meta:
        model = CV
        fields = ['filename', 'content', 'file_size']


class CVListSerializer(serializers.ModelSerializer):
    """Serializer for listing CVs (minimal fields)."""
    
    # Add camelCase aliases for frontend compatibility
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    fileSize = serializers.IntegerField(source='file_size', read_only=True)
    
    class Meta:
        model = CV
        fields = ['id', 'filename', 'file_size', 'fileSize', 'status', 
                  'created_at', 'createdAt']
