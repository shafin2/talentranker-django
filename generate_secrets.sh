#!/bin/bash
# Generate secure secret keys for Django deployment

echo "=================================================="
echo "🔐 GENERATING SECURE SECRETS FOR PRODUCTION"
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed or not in PATH"
    exit 1
fi

# Generate Django Secret Key
echo "📝 Generating DJANGO_SECRET_KEY..."
DJANGO_SECRET=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
echo "DJANGO_SECRET_KEY=$DJANGO_SECRET"
echo ""

# Generate JWT Secret
echo "📝 Generating JWT_SECRET..."
JWT_SECRET=$(python -c "import secrets; print(secrets.token_urlsafe(50))")
echo "JWT_SECRET=$JWT_SECRET"
echo ""

echo "=================================================="
echo "✅ SECRETS GENERATED SUCCESSFULLY!"
echo "=================================================="
echo ""
echo "⚠️  IMPORTANT:"
echo "1. Copy these secrets to your .env file on cPanel"
echo "2. NEVER commit these secrets to Git"
echo "3. Keep them secure and backed up"
echo ""
echo "=================================================="
