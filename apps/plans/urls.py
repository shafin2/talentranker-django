from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Plan
from .serializers import PlanSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_plans(request):
    """Get all active plans."""
    plans = Plan.objects.filter(is_active=True).order_by('region', 'sort_order', 'name')
    serializer = PlanSerializer(plans, many=True)
    return Response({
        'success': True,
        'plans': serializer.data
    })

urlpatterns = [
    path('', get_all_plans, name='get_plans'),
]
