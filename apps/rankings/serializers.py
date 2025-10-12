from rest_framework import serializers
from .models import RankingResult, UpgradeRequest
from apps.job_descriptions.serializers import JobDescriptionListSerializer


class RankingResultSerializer(serializers.ModelSerializer):
    """Serializer for RankingResult model."""
    
    job_description = JobDescriptionListSerializer(read_only=True)
    
    class Meta:
        model = RankingResult
        fields = ['id', 'job_description', 'results', 'status', 'error', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RankingRequestSerializer(serializers.Serializer):
    """Serializer for ranking request."""
    
    jdId = serializers.IntegerField(required=True, source='jd_id')
    cvIds = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False,
        source='cv_ids'
    )


class UpgradeRequestSerializer(serializers.ModelSerializer):
    """Serializer for UpgradeRequest model."""
    
    class Meta:
        model = UpgradeRequest
        fields = ['id', 'user', 'current_plan', 'requested_plan', 'status', 
                  'message', 'admin_notes', 'processed_by', 'processed_at', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'status', 'processed_by', 
                           'processed_at', 'created_at', 'updated_at']
