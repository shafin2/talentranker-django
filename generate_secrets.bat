@echo off
REM Generate secure secret keys for Django deployment (Windows version)

echo ==================================================
echo 🔐 GENERATING SECURE SECRETS FOR PRODUCTION
echo ==================================================
echo.

REM Generate Django Secret Key
echo 📝 Generating DJANGO_SECRET_KEY...
python -c "from django.core.management.utils import get_random_secret_key; print('DJANGO_SECRET_KEY=' + get_random_secret_key())"
echo.

REM Generate JWT Secret
echo 📝 Generating JWT_SECRET...
python -c "import secrets; print('JWT_SECRET=' + secrets.token_urlsafe(50))"
echo.

echo ==================================================
echo ✅ SECRETS GENERATED SUCCESSFULLY!
echo ==================================================
echo.
echo ⚠️  IMPORTANT:
echo 1. Copy these secrets to your .env file on cPanel
echo 2. NEVER commit these secrets to Git
echo 3. Keep them secure and backed up
echo.
echo ==================================================
pause
