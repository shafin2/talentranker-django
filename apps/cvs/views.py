from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CV
from .serializers import CVSerializer, CVListSerializer
from services.pdf_service import extract_text_from_pdf, validate_pdf
from middleware.usage_limits import check_cv_limit, update_usage_stats
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
@check_cv_limit
def upload_cvs(request):
    """
    Upload CV(s) - supports multiple PDF files.
    """
    try:
        files = request.FILES.getlist('cvFiles')
        
        if not files:
            return Response(
                {'message': 'Please upload at least one PDF file'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_cvs = []
        errors = []
        
        # Process each PDF
        for file in files:
            try:
                # Validate PDF
                validate_pdf(file)
                
                # Extract text from PDF
                logger.info(f'📄 Extracting text from CV: {file.name}')
                content = extract_text_from_pdf(file.read())
                logger.info(f'✅ CV text extracted! Length: {len(content)} chars')
                logger.info(f'📝 First 150 chars: {content[:150]}...')
                
                # Create CV record
                cv = CV.objects.create(
                    user=request.user,
                    filename=file.name,
                    content=content,
                    file_size=file.size
                )
                
                uploaded_cvs.append({
                    '_id': cv.id,
                    'filename': cv.filename,
                    'createdAt': cv.created_at.isoformat()
                })
                logger.info(f'💾 CV saved to database: {cv.filename}')
                
                # Update usage stats
                update_usage_stats(request.user, 'cv')
            
            except Exception as e:
                logger.error(f'Error processing {file.name}: {str(e)}')
                errors.append({
                    'filename': file.name,
                    'error': str(e)
                })
        
        response_data = {
            'success': True,
            'message': f'{len(uploaded_cvs)} CV(s) uploaded successfully',
            'data': uploaded_cvs
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        logger.error(f'CV upload error: {str(e)}')
        return Response(
            {'message': str(e) or 'Failed to upload CVs'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_cvs(request):
    """
    Get all user's CVs.
    """
    try:
        cvs = CV.objects.filter(
            user=request.user,
            status='active'
        ).order_by('-created_at')
        
        serializer = CVSerializer(cvs, many=True)
        
        return Response({
            'success': True,
            'count': len(serializer.data),
            'data': [
                {
                    '_id': cv['id'],
                    'filename': cv['filename'],
                    'content': cv['content'],
                    'fileSize': cv.get('file_size'),
                    'status': cv['status'],
                    'createdAt': cv['created_at']
                }
                for cv in serializer.data
            ]
        })
    
    except Exception as e:
        logger.error(f'Get CVs error: {str(e)}')
        return Response(
            {'message': 'Failed to fetch CVs'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cv_by_id(request, id):
    """
    Get single CV.
    """
    try:
        cv = CV.objects.get(id=id, user=request.user)
        serializer = CVSerializer(cv)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    except CV.DoesNotExist:
        return Response(
            {'message': 'CV not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f'Get CV error: {str(e)}')
        return Response(
            {'message': 'Failed to fetch CV'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cv(request, id):
    """
    Delete (archive) CV.
    """
    try:
        cv = CV.objects.get(id=id, user=request.user)
        
        # Soft delete (archive)
        cv.status = 'archived'
        cv.save()
        
        return Response({
            'success': True,
            'message': 'CV deleted successfully'
        })
    
    except CV.DoesNotExist:
        return Response(
            {'message': 'CV not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f'Delete CV error: {str(e)}')
        return Response(
            {'message': 'Failed to delete CV'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
