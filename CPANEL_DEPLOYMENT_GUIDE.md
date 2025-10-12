# 🚀 Django Backend Deployment Guide for cPanel

## Prerequisites
- ✅ cPanel hosting account with Python support
- ✅ Subdomain created (e.g., `api.yourdomain.com`)
- ✅ SSH access (recommended)
- ✅ Frontend deployed on Vercel

---

## 📋 STEP-BY-STEP DEPLOYMENT GUIDE

### **STEP 1: Update Google OAuth Credentials** 🔐

#### 1.1 Go to Google Cloud Console
- Visit: https://console.cloud.google.com/
- Select your project (or create one)

#### 1.2 Update Authorized JavaScript Origins
Add your production URLs:
```
https://your-frontend-domain.vercel.app
https://api.yourdomain.com
```

#### 1.3 Update Authorized Redirect URIs
Add:
```
https://your-frontend-domain.vercel.app
https://api.yourdomain.com/api/auth/google/callback
```

#### 1.4 Copy Credentials
- Copy your `Client ID` (format: `xxx.apps.googleusercontent.com`)
- Copy your `Client Secret` (format: `GOCSPX-xxx`)

**You'll need these for your .env file!**

---

### **STEP 2: Prepare Production Settings** ⚙️

#### 2.1 Update `settings.py`

Update the ALLOWED_HOSTS in settings.py:

```python
# Around line 11
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
```

Update CORS settings:

```python
# Around line 118
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS_ALLOWED_ORIGINS = [
    FRONTEND_URL,
]
if DEBUG:
    CORS_ALLOWED_ORIGINS.extend([
        "http://localhost:5173",
        "http://localhost:3000"
    ])
CORS_ALLOW_CREDENTIALS = True
```

#### 2.2 Create Production .env File

Create a new file `.env.production` with production values:

```env
# Django Settings
DJANGO_SECRET_KEY=<GENERATE-STRONG-SECRET-KEY-HERE>
DEBUG=False
ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com

# JWT
JWT_SECRET=<GENERATE-STRONG-JWT-SECRET-HERE>

# Frontend URL (your Vercel deployment)
FRONTEND_URL=https://your-frontend-domain.vercel.app

# Google OAuth (from Google Cloud Console)
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=https://api.yourdomain.com/api/auth/google/callback

# Server
PORT=8000
```

**Generate strong secrets:**
```bash
# For DJANGO_SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# For JWT_SECRET
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

### **STEP 3: Upload Files to cPanel** 📤

#### 3.1 Via cPanel File Manager
1. Login to cPanel
2. Go to **File Manager**
3. Navigate to your subdomain's root directory (usually `/home/username/public_html/api` or `/home/username/api.yourdomain.com`)
4. Upload all Django project files EXCEPT:
   - `venv/` (virtual environment)
   - `db.sqlite3` (local database)
   - `.env` (local environment)
   - `__pycache__/` folders
   - `.git/` folder

#### 3.2 Via SSH/FTP (Recommended)
```bash
# Using SCP
scp -r talentranker-django/* username@yourdomain.com:~/api.yourdomain.com/

# Or use FileZilla/WinSCP
```

---

### **STEP 4: Setup Python Application in cPanel** 🐍

#### 4.1 Create Python Application
1. In cPanel, go to **"Setup Python App"**
2. Click **"Create Application"**
3. Configure:
   - **Python Version**: 3.8 or higher (3.9/3.10/3.11 recommended)
   - **Application Root**: `/home/username/api.yourdomain.com` (or your path)
   - **Application URL**: `api.yourdomain.com` (your subdomain)
   - **Application Startup File**: `passenger_wsgi.py`
   - **Application Entry Point**: `application`

4. Click **"Create"**

#### 4.2 Note the Virtual Environment Path
cPanel will show something like:
```
/home/username/virtualenv/api_yourdomain_com/3.9/bin/python
```
**Save this path!**

---

### **STEP 5: Install Dependencies** 📦

#### 5.1 Via cPanel Terminal (or SSH)
```bash
# Activate virtual environment (use path from Step 4.2)
source /home/username/virtualenv/api_yourdomain_com/3.9/bin/activate

# Navigate to project directory
cd ~/api.yourdomain.com

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

---

### **STEP 6: Create passenger_wsgi.py** 🚂

Create `passenger_wsgi.py` in your project root (same level as `manage.py`):

```python
import os
import sys
from pathlib import Path

# Add project directory to Python path
INTERP = "/home/username/virtualenv/api_yourdomain_com/3.9/bin/python"
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentranker.settings')

# Add project to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**⚠️ IMPORTANT**: Replace `/home/username/virtualenv/api_yourdomain_com/3.9/bin/python` with YOUR actual path from Step 4.2!

---

### **STEP 7: Upload .env File** 🔒

#### Via cPanel File Manager:
1. Upload `.env.production` to project root
2. Rename it to `.env`

#### Via SSH:
```bash
cd ~/api.yourdomain.com
nano .env
# Paste production environment variables
# Save: Ctrl+O, Enter, Ctrl+X
```

---

### **STEP 8: Setup Database & Static Files** 💾

```bash
# Activate virtual environment
source /home/username/virtualenv/api_yourdomain_com/3.9/bin/activate

# Navigate to project
cd ~/api.yourdomain.com

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser
# Email: admin@yourdomain.com
# Password: <create-strong-password>

# Seed plans
python scripts/seed-plans.py

# Collect static files
python manage.py collectstatic --noinput

# Create upload directories
mkdir -p uploads/temp
chmod 755 uploads
chmod 755 uploads/temp
```

---

### **STEP 9: Configure File Permissions** 🔐

```bash
# Make directories writable
chmod 755 ~/api.yourdomain.com
chmod 755 ~/api.yourdomain.com/uploads
chmod 755 ~/api.yourdomain.com/uploads/temp
chmod 666 ~/api.yourdomain.com/db.sqlite3
chmod 755 ~/api.yourdomain.com/staticfiles

# Make passenger_wsgi.py executable
chmod 755 ~/api.yourdomain.com/passenger_wsgi.py
```

---

### **STEP 10: Setup .htaccess** 📄

Create `.htaccess` in your subdomain root:

```apache
# Force HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# Passenger Configuration
PassengerEnabled On
PassengerAppRoot /home/username/api.yourdomain.com

# Static and Media files
RewriteRule ^static/(.*)$ /home/username/api.yourdomain.com/staticfiles/$1 [L]
RewriteRule ^media/(.*)$ /home/username/api.yourdomain.com/uploads/$1 [L]

# API requests
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py [L]
```

**Replace `/home/username/api.yourdomain.com` with your actual path!**

---

### **STEP 11: Update Vercel Frontend Environment** 🌐

Update your Vercel environment variables:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Update:
   ```
   VITE_API_BASE_URL=https://api.yourdomain.com/api
   VITE_GOOGLE_CLIENT_ID=<your-google-client-id>
   ```
3. Redeploy frontend

---

### **STEP 12: Restart Application** 🔄

In cPanel:
1. Go to **"Setup Python App"**
2. Find your application
3. Click **"Restart"** button

Or via command line:
```bash
touch ~/api.yourdomain.com/passenger_wsgi.py
```

---

### **STEP 13: Test Deployment** ✅

#### Test API endpoints:
```bash
# Health check
curl https://api.yourdomain.com/

# Admin login
curl -X POST https://api.yourdomain.com/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@yourdomain.com","password":"your-password"}'

# Get plans
curl https://api.yourdomain.com/api/users/plans
```

#### Test in browser:
- Visit: `https://api.yourdomain.com/admin/` (Django admin)
- Visit your Vercel frontend and test:
  - ✅ Google OAuth login
  - ✅ Regular login/signup
  - ✅ Upload CV and JD
  - ✅ Ranking functionality
  - ✅ Admin panel

---

## 🔧 TROUBLESHOOTING

### Issue: "Application Error"
**Solution:**
```bash
# Check error logs
tail -n 100 ~/logs/api.yourdomain.com/error.log

# Check if virtual environment is activated
which python

# Restart application
touch ~/api.yourdomain.com/passenger_wsgi.py
```

### Issue: "Module not found"
**Solution:**
```bash
# Reinstall dependencies
source /home/username/virtualenv/api_yourdomain_com/3.9/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Issue: "Static files not loading"
**Solution:**
```bash
python manage.py collectstatic --noinput --clear
chmod 755 ~/api.yourdomain.com/staticfiles
```

### Issue: "Database is locked"
**Solution:**
```bash
chmod 666 ~/api.yourdomain.com/db.sqlite3
chmod 755 ~/api.yourdomain.com
```

### Issue: "CORS errors"
**Check:**
- FRONTEND_URL in .env matches Vercel URL exactly
- ALLOWED_HOSTS includes your subdomain
- Vercel environment variables are correct

---

## 📝 POST-DEPLOYMENT CHECKLIST

- [ ] Google OAuth credentials updated
- [ ] Production .env file configured
- [ ] All dependencies installed
- [ ] Database migrated
- [ ] Admin user created
- [ ] Plans seeded
- [ ] Static files collected
- [ ] File permissions set correctly
- [ ] .htaccess configured
- [ ] Application restarted
- [ ] Vercel frontend updated
- [ ] API endpoints tested
- [ ] Google login tested
- [ ] File upload tested
- [ ] Admin panel tested

---

## 🔒 SECURITY CHECKLIST

- [ ] DEBUG=False in production
- [ ] Strong DJANGO_SECRET_KEY
- [ ] Strong JWT_SECRET
- [ ] HTTPS enforced (SSL certificate installed)
- [ ] ALLOWED_HOSTS properly configured
- [ ] CORS_ALLOWED_ORIGINS limited to your domains
- [ ] db.sqlite3 file permissions: 666
- [ ] Admin password is strong
- [ ] Google OAuth redirects limited to your domains

---

## 📞 SUPPORT

If you encounter issues:

1. **Check Error Logs:**
   ```bash
   tail -n 100 ~/logs/api.yourdomain.com/error.log
   ```

2. **Check Application Status:**
   - cPanel → Setup Python App → View app status

3. **Test Database:**
   ```bash
   python manage.py shell
   >>> from apps.users.models import User
   >>> User.objects.count()
   ```

4. **Common Commands:**
   ```bash
   # Activate environment
   source /home/username/virtualenv/api_yourdomain_com/3.9/bin/activate
   
   # Restart app
   touch ~/api.yourdomain.com/passenger_wsgi.py
   
   # Check migrations
   python manage.py showmigrations
   
   # Run migrations
   python manage.py migrate
   ```

---

## 🎉 SUCCESS!

Your Django backend is now deployed on cPanel! 

**Next Steps:**
1. Test all functionality thoroughly
2. Monitor error logs for first few days
3. Set up automated backups for `db.sqlite3`
4. Consider upgrading to PostgreSQL/MySQL for production (optional)

---

**Deployment Date:** _________________
**Subdomain:** api.yourdomain.com
**Vercel Frontend:** your-app.vercel.app
**Admin Email:** admin@yourdomain.com

---

Good luck! 🚀
