from rest_framework import serializers
from .models import JobDescription


class JobDescriptionSerializer(serializers.ModelSerializer):
    """Serializer for JobDescription model."""
    
    # Add camelCase aliases for frontend compatibility
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    updatedAt = serializers.DateTimeField(source='updated_at', read_only=True)
    rankedCvsCount = serializers.IntegerField(source='ranked_cvs_count', read_only=True)
    
    class Meta:
        model = JobDescription
        fields = ['id', 'title', 'description', 'content', 'filename', 
                  'status', 'ranked_cvs_count', 'rankedCvsCount', 
                  'created_at', 'createdAt', 'updated_at', 'updatedAt']
        read_only_fields = ['id', 'ranked_cvs_count', 'created_at', 'updated_at']


class JobDescriptionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a job description."""
    
    class Meta:
        model = JobDescription
        fields = ['title', 'description', 'content', 'filename']


class JobDescriptionListSerializer(serializers.ModelSerializer):
    """Serializer for listing job descriptions (minimal fields)."""
    
    # Add camelCase aliases for frontend compatibility
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    rankedCvsCount = serializers.IntegerField(source='ranked_cvs_count', read_only=True)
    
    class Meta:
        model = JobDescription
        fields = ['id', 'title', 'description', 'filename', 'status', 
                  'ranked_cvs_count', 'rankedCvsCount', 'created_at', 'createdAt']
