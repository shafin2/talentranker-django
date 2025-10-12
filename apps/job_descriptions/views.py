from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import JobDescription
from .serializers import (
    JobDescriptionSerializer,
    JobDescriptionCreateSerializer,
    JobDescriptionListSerializer
)
from services.pdf_service import extract_text_from_pdf, validate_pdf
from middleware.usage_limits import check_jd_limit, update_usage_stats
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@check_jd_limit
def upload_jd(request):
    """
    Upload Job Description (PDF or text).
    """
    try:
        title = request.data.get('title')
        description = request.data.get('description')
        content = request.data.get('content')
        file = request.FILES.get('jdFile')
        
        jd_content = ''
        
        # If file uploaded, extract text
        if file:
            logger.info(f'📄 Extracting text from JD PDF: {file.name}')
            try:
                validate_pdf(file)
                jd_content = extract_text_from_pdf(file.read())
                logger.info(f'✅ JD Text extracted successfully!')
                logger.info(f'📝 First 200 chars: {jd_content[:200]}')
                logger.info(f'📊 Total length: {len(jd_content)} characters')
            except Exception as e:
                return Response(
                    {'message': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif content:
            # Use direct text input
            logger.info('📝 Using direct text input for JD')
            jd_content = content
            logger.info(f'📊 Content length: {len(jd_content)} characters')
        elif description:
            # Fallback to description field
            jd_content = description
        else:
            return Response(
                {'message': 'Please provide either a PDF file or job description text'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create JD
        jd = JobDescription.objects.create(
            user=request.user,
            title=title or 'Untitled Job Description',
            description=description or jd_content[:500],
            content=jd_content,
            filename=file.name if file else None
        )
        
        # Update usage stats
        update_usage_stats(request.user, 'jd')
        
        return Response({
            'success': True,
            'message': 'Job Description uploaded successfully',
            'data': {
                '_id': jd.id,
                'title': jd.title,
                'description': jd.description,
                'content': jd.content,
                'filename': jd.filename,
                'createdAt': jd.created_at.isoformat()
            }
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        logger.error(f'JD upload error: {str(e)}')
        return Response(
            {'message': str(e) or 'Failed to upload Job Description'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_jds(request):
    """
    Get all user's Job Descriptions.
    """
    try:
        jds = JobDescription.objects.filter(
            user=request.user,
            status='active'
        ).order_by('-created_at')
        
        serializer = JobDescriptionListSerializer(jds, many=True)
        
        return Response({
            'success': True,
            'count': len(serializer.data),
            'data': [
                {
                    '_id': jd['id'],
                    'title': jd['title'],
                    'description': jd['description'],
                    'filename': jd.get('filename'),
                    'rankedCVsCount': jd['ranked_cvs_count'],
                    'status': jd['status'],
                    'createdAt': jd['created_at']
                }
                for jd in serializer.data
            ]
        })
    
    except Exception as e:
        logger.error(f'Get JDs error: {str(e)}')
        return Response(
            {'message': 'Failed to fetch Job Descriptions'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_jd_by_id(request, id):
    """
    Get single Job Description.
    """
    try:
        jd = JobDescription.objects.get(id=id, user=request.user)
        serializer = JobDescriptionSerializer(jd)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    except JobDescription.DoesNotExist:
        return Response(
            {'message': 'Job Description not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f'Get JD error: {str(e)}')
        return Response(
            {'message': 'Failed to fetch Job Description'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_jd(request, id):
    """
    Delete (archive) Job Description.
    """
    try:
        jd = JobDescription.objects.get(id=id, user=request.user)
        
        # Soft delete (archive)
        jd.status = 'archived'
        jd.save()
        
        return Response({
            'success': True,
            'message': 'Job Description deleted successfully'
        })
    
    except JobDescription.DoesNotExist:
        return Response(
            {'message': 'Job Description not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f'Delete JD error: {str(e)}')
        return Response(
            {'message': 'Failed to delete Job Description'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
