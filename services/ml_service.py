"""
Machine Learning Service
Handles communication with the ML API for CV ranking
"""
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

ML_API_URL = getattr(settings, 'ML_API_URL', 'https://ahmadmahmood447.pythonanywhere.com/api')
ML_API_TIMEOUT = getattr(settings, 'ML_API_TIMEOUT', 30)


def rank_cv(jd_text, resume_text):
    """
    Rank a single CV against a JD using ML model.
    
    Args:
        jd_text (str): Job description text
        resume_text (str): Resume/CV text
    
    Returns:
        dict: Prediction result with 'prediction' and 'confidence' keys
    
    Raises:
        Exception: If ML API call fails
    """
    try:
        logger.info('🔄 Sending request to ML API...')
        logger.info(f'📝 JD text length: {len(jd_text)} chars')
        logger.info(f'📄 Resume text length: {len(resume_text)} chars')
        
        response = requests.post(
            ML_API_URL,
            json={
                'jd': jd_text,
                'resume': resume_text
            },
            headers={'Content-Type': 'application/json'},
            timeout=ML_API_TIMEOUT
        )
        
        response.raise_for_status()
        data = response.json()
        
        logger.info(f'✅ ML API Response: {data}')
        
        if data and 'result' in data:
            result = {
                'prediction': data['result']['prediction'],
                'confidence': round(float(data['result']['confidence']), 2)
            }
            logger.info(f'🎯 Prediction: {result["prediction"]} ({result["confidence"]}% confidence)')
            return result
        
        raise Exception('Invalid response from ML model')
    
    except requests.exceptions.Timeout:
        logger.error('❌ ML API request timeout')
        raise Exception('ML model request timeout')
    
    except requests.exceptions.RequestException as e:
        logger.error(f'❌ ML API Error: {str(e)}')
        if hasattr(e.response, 'status_code'):
            raise Exception(f'ML model error: {e.response.status_code}')
        raise Exception('Failed to get prediction from ML model')
    
    except Exception as e:
        logger.error(f'❌ Unexpected error: {str(e)}')
        raise


def rank_multiple_cvs(jd_text, cvs):
    """
    Rank multiple CVs against a JD.
    
    Args:
        jd_text (str): Job description text
        cvs (list): List of CV dicts with 'id', 'filename', and 'content' keys
    
    Returns:
        list: Array of ranking results sorted by confidence
    """
    results = []
    
    logger.info('\n' + '=' * 60)
    logger.info(f'📊 Starting batch ranking: {len(cvs)} CVs')
    logger.info('=' * 60 + '\n')
    
    for i, cv in enumerate(cvs):
        logger.info(f'\n[{i + 1}/{len(cvs)}] Processing: {cv["filename"]}')
        try:
            prediction = rank_cv(jd_text, cv['content'])
            results.append({
                'cv': cv['id'],
                'filename': cv['filename'],
                'prediction': prediction['prediction'],
                'confidence': prediction['confidence']
            })
            logger.info(f'✅ Success: {cv["filename"]} - {prediction["prediction"]} ({prediction["confidence"]}%)')
        except Exception as e:
            logger.error(f'❌ Error ranking CV {cv["filename"]}: {str(e)}')
            results.append({
                'cv': cv['id'],
                'filename': cv['filename'],
                'prediction': 'Error',
                'confidence': 0,
                'error': str(e)
            })
    
    # Sort by confidence (highest first), then by prediction (Relevant first)
    results.sort(key=lambda x: (x['prediction'] == 'Relevant', x['confidence']), reverse=True)
    
    logger.info('\n' + '=' * 60)
    logger.info('✅ Batch ranking completed!')
    logger.info('=' * 60 + '\n')
    
    return results
