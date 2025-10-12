from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import RankingResult
from .serializers import RankingResultSerializer, RankingRequestSerializer
from apps.job_descriptions.models import JobDescription
from apps.cvs.models import CV
from services.ml_service import rank_multiple_cvs
from services.pdf_service import extract_text_from_pdf
import logging

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rank_cvs(request):
    """
    Rank CVs against a Job Description using ML model.
    """
    try:
        logger.info(f'📥 Received ranking request body: {request.data}')
        
        serializer = RankingRequestSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f'❌ Validation failed: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        jd_id = serializer.validated_data['jd_id']
        cv_ids = serializer.validated_data['cv_ids']
        
        logger.info(f'🔍 Validation - jd_id: {jd_id}')
        logger.info(f'🔍 Validation - cv_ids: {cv_ids}')
        
        # Get Job Description
        try:
            jd = JobDescription.objects.get(
                id=jd_id,
                user=request.user,
                status='active'
            )
        except JobDescription.DoesNotExist:
            return Response(
                {'message': 'Job Description not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Get CVs
        cvs = CV.objects.filter(
            id__in=cv_ids,
            user=request.user,
            status='active'
        )
        
        if not cvs.exists():
            return Response(
                {'message': 'No valid CVs found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Prepare CV data for ML model
        cv_data = [
            {
                'id': cv.id,
                'filename': cv.filename,
                'content': cv.content
            }
            for cv in cvs
        ]
        
        logger.info(f'🎯 Starting ranking process for JD: {jd.title}')
        logger.info(f'📊 Number of CVs to rank: {len(cv_data)}')
        logger.info(f'📝 JD content length: {len(jd.content)} chars')
        
        # Create ranking result record (initially processing)
        ranking_result = RankingResult.objects.create(
            user=request.user,
            job_description=jd,
            status='processing',
            results=[]
        )
        
        # Rank CVs using ML model
        try:
            logger.info('🤖 Calling ML API to rank CVs...')
            rankings = rank_multiple_cvs(jd.content, cv_data)
            logger.info('✅ ML API ranking completed successfully!')
            logger.info(f'📈 Rankings: {rankings}')
            
            # Update ranking result with results
            ranking_result.results = rankings
            ranking_result.status = 'completed'
            ranking_result.save()
            
            # Update JD ranked CVs count
            jd.ranked_cvs_count += len(cvs)
            jd.save()
            
            return Response({
                'success': True,
                'message': 'CVs ranked successfully',
                'rankingResult': {
                    '_id': ranking_result.id,
                    'jdTitle': jd.title,
                    'results': ranking_result.results,
                    'createdAt': ranking_result.created_at.isoformat()
                }
            })
        
        except Exception as e:
            # Update ranking result with error
            ranking_result.status = 'failed'
            ranking_result.error = str(e)
            ranking_result.save()
            
            logger.error(f'❌ Ranking error: {str(e)}')
            raise
    
    except Exception as e:
        logger.error(f'Ranking error: {str(e)}')
        return Response(
            {'message': str(e) or 'Failed to rank CVs'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ranking_results(request):
    """
    Get all ranking results for user.
    """
    try:
        results = RankingResult.objects.filter(
            user=request.user
        ).select_related('job_description').order_by('-created_at')[:50]  # Last 50 results
        
        return Response({
            'success': True,
            'count': results.count(),
            'data': [
                {
                    '_id': result.id,
                    'jobDescription': {
                        'id': result.job_description.id,
                        'title': result.job_description.title
                    } if result.job_description else None,
                    'results': result.results,
                    'status': result.status,
                    'error': result.error,
                    'createdAt': result.created_at.isoformat()
                }
                for result in results
            ]
        })
    
    except Exception as e:
        logger.error(f'Get ranking results error: {str(e)}')
        return Response(
            {'message': 'Failed to fetch ranking results'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ranking_result_by_id(request, id):
    """
    Get single ranking result.
    """
    try:
        result = RankingResult.objects.select_related('job_description').get(
            id=id,
            user=request.user
        )
        
        return Response({
            'success': True,
            'data': {
                '_id': result.id,
                'jobDescription': {
                    'id': result.job_description.id,
                    'title': result.job_description.title,
                    'description': result.job_description.description
                } if result.job_description else None,
                'results': result.results,
                'status': result.status,
                'error': result.error,
                'createdAt': result.created_at.isoformat()
            }
        })
    
    except RankingResult.DoesNotExist:
        return Response(
            {'message': 'Ranking result not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f'Get ranking result error: {str(e)}')
        return Response(
            {'message': 'Failed to fetch ranking result'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_ranking_result(request, id):
    """
    Delete ranking result.
    """
    try:
        result = RankingResult.objects.get(id=id, user=request.user)
        result.delete()
        
        return Response({
            'success': True,
            'message': 'Ranking result deleted successfully'
        })
    
    except RankingResult.DoesNotExist:
        return Response(
            {'message': 'Ranking result not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        logger.error(f'Delete ranking result error: {str(e)}')
        return Response(
            {'message': 'Failed to delete ranking result'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def rank_with_files(request):
    """
    Rank CVs with direct file uploads.
    This endpoint handles the complete flow:
    1. Accept JD and CV file uploads
    2. Parse PDFs on backend
    3. Check credit limits
    4. Create JD, CV, and RankingResult records
    5. Deduct credits
    6. Rank CVs using ML model
    """
    try:
        logger.info('📥 New ranking request with files')
        
        # Check if files were uploaded
        jd_file = request.FILES.get('jd')
        cv_files = request.FILES.getlist('cvs')
        
        if not jd_file:
            return Response(
                {'message': 'Please upload a JD file'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not cv_files or len(cv_files) == 0:
            return Response(
                {'message': 'Please upload at least one CV file'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f'📄 JD file: {jd_file.name}')
        logger.info(f'📄 CV files count: {len(cv_files)}')
        
        # Get user with plan
        user = request.user
        plan = user.plan
        
        # Check credits BEFORE processing
        jd_limit = plan.jd_limit if plan else 0
        cv_limit = plan.cv_limit if plan else 0
        jd_used = user.jd_used or 0
        cv_used = user.cv_used or 0
        
        # Handle unlimited plans (None or -1)
        jd_remaining = float('inf') if (jd_limit is None or jd_limit == -1) else (jd_limit - jd_used)
        cv_remaining = float('inf') if (cv_limit is None or cv_limit == -1) else (cv_limit - cv_used)
        
        logger.info(f'💳 Credits check - JD: {jd_used}/{jd_limit}, CV: {cv_used}/{cv_limit}')
        
        if jd_remaining < 1:
            return Response(
                {'message': 'Insufficient JD credits. Please upgrade your plan.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if cv_remaining < len(cv_files):
            return Response(
                {'message': f'Insufficient CV credits. You have {int(cv_remaining)} remaining but selected {len(cv_files)} CVs.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Extract text from JD
        logger.info('📖 Extracting text from JD...')
        try:
            if jd_file.content_type == 'application/pdf':
                jd_content = extract_text_from_pdf(jd_file.read())
            else:
                jd_content = jd_file.read().decode('utf-8')
        except Exception as e:
            logger.error(f'Failed to extract JD text: {str(e)}')
            return Response(
                {'message': f'Failed to extract text from JD: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        logger.info(f'✅ JD text extracted: {len(jd_content)} characters')
        
        # Create JD record in database
        jd_title = jd_file.name.rsplit('.', 1)[0]  # Remove extension
        jd = JobDescription.objects.create(
            user=user,
            title=jd_title,
            description=jd_content[:500],  # First 500 chars as description
            filename=jd_file.name,
            content=jd_content,
            status='active'
        )
        
        logger.info(f'✅ JD created in DB: {jd.id}')
        
        # Extract text from CVs and create records
        logger.info('📖 Extracting text from CVs...')
        cv_records = []
        cv_data = []
        
        for cv_file in cv_files:
            try:
                if cv_file.content_type == 'application/pdf':
                    cv_content = extract_text_from_pdf(cv_file.read())
                else:
                    cv_content = cv_file.read().decode('utf-8')
                
                cv = CV.objects.create(
                    user=user,
                    filename=cv_file.name,
                    content=cv_content,
                    file_size=cv_file.size,
                    status='active'
                )
                
                cv_records.append(cv)
                cv_data.append({
                    'id': cv.id,
                    'filename': cv.filename,
                    'content': cv.content
                })
                
                logger.info(f'✅ CV created in DB: {cv.id} - {cv.filename}')
            except Exception as e:
                logger.error(f'Failed to process CV {cv_file.name}: {str(e)}')
                # Continue with other CVs
                continue
        
        if not cv_data:
            return Response(
                {'message': 'Failed to process any CV files'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Deduct credits
        user.jd_used = (user.jd_used or 0) + 1
        user.cv_used = (user.cv_used or 0) + len(cv_data)
        user.save()
        
        logger.info(f'💳 Credits deducted - New usage: JD {user.jd_used}/{jd_limit}, CV {user.cv_used}/{cv_limit}')
        
        # Create ranking result record
        ranking_result = RankingResult.objects.create(
            user=user,
            job_description=jd,
            status='processing',
            results=[]
        )
        
        # Rank CVs using ML model
        try:
            logger.info('🤖 Calling ML API to rank CVs...')
            rankings = rank_multiple_cvs(jd_content, cv_data)
            logger.info('✅ ML API ranking completed successfully!')
            
            # Update ranking result with results
            ranking_result.results = rankings
            ranking_result.status = 'completed'
            ranking_result.save()
            
            # Update JD ranked CVs count
            jd.ranked_cvs_count = len(cv_data)
            jd.save()
            
            return Response({
                'success': True,
                'message': 'CVs ranked successfully',
                'rankingResult': {
                    '_id': ranking_result.id,
                    'jdTitle': jd.title,
                    'results': ranking_result.results,
                    'createdAt': ranking_result.created_at.isoformat()
                }
            })
        except Exception as e:
            # Update ranking result with error
            ranking_result.status = 'failed'
            ranking_result.error = str(e)
            ranking_result.save()
            
            logger.error(f'❌ Ranking error: {str(e)}')
            raise
    
    except Exception as e:
        logger.error(f'Ranking with files error: {str(e)}')
        return Response(
            {'message': str(e) or 'Failed to rank CVs'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

