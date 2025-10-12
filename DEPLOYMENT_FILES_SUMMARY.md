# 📚 cPanel Deployment - Files Summary

## Overview
This document lists all deployment-related files created for deploying TalentRanker Django backend to cPanel.

---

## 📄 Documentation Files

### 1. **CPANEL_DEPLOYMENT_GUIDE.md** 📖
**Purpose**: Complete step-by-step deployment guide  
**Use**: Follow this for first-time deployment  
**Contains**:
- Google OAuth setup instructions
- cPanel Python app configuration
- Database setup
- Security checklist
- Troubleshooting guide

### 2. **DEPLOYMENT_CHECKLIST.md** ✅
**Purpose**: Interactive checklist for deployment  
**Use**: Check off each step as you complete it  
**Contains**:
- Pre-deployment tasks
- cPanel setup steps
- Testing procedures
- Post-deployment verification

### 3. **QUICK_REFERENCE.md** 🚀
**Purpose**: Quick command reference  
**Use**: Keep open while working on server  
**Contains**:
- Most-used commands
- Quick fixes for common issues
- File structure overview
- Emergency procedures

### 4. **ADMIN_CRUD_FIX.md** 🔧
**Purpose**: Documentation of admin panel fixes  
**Use**: Reference for understanding recent changes  
**Contains**:
- Problem description
- Solution implementation
- Test results
- Technical details

---

## ⚙️ Configuration Files

### 5. **passenger_wsgi.py** 🚂
**Purpose**: cPanel Passenger WSGI entry point  
**Location**: Project root (same level as manage.py)  
**IMPORTANT**: 
- Must update line 13 with YOUR virtual environment path
- Get path from cPanel → Setup Python App

```python
# Line 13 - UPDATE THIS!
INTERP = "/home/yourusername/virtualenv/api_yourdomain_com/3.9/bin/python"
```

### 6. **.env.production** 🔐
**Purpose**: Production environment variables template  
**Location**: Project root  
**Usage**:
1. Update all placeholder values
2. Upload to server as `.env`
3. NEVER commit real `.env` to Git

**Must Update**:
- `DJANGO_SECRET_KEY` (generate new)
- `JWT_SECRET` (generate new)
- `ALLOWED_HOSTS` (your domains)
- `FRONTEND_URL` (Vercel URL)
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`
- Set `DEBUG=False`

### 7. **.htaccess.example** 🌐
**Purpose**: Apache configuration for cPanel  
**Location**: Subdomain root directory  
**Usage**:
1. Update all paths with your cPanel username
2. Rename to `.htaccess`
3. Upload to subdomain root

**Must Update**:
- Line 18: `PassengerAppRoot /home/yourusername/api.yourdomain.com`
- Line 21: `PassengerPython /home/yourusername/virtualenv/.../python`
- Line 28: Static files path
- Line 32: Media files path

---

## 🛠️ Utility Scripts

### 8. **generate_secrets.bat** (Windows) 🪟
**Purpose**: Generate secure Django and JWT secrets  
**Usage**:
```cmd
generate_secrets.bat
```
**Output**: Prints secure random keys to copy

### 9. **generate_secrets.sh** (Linux/Mac) 🐧
**Purpose**: Same as above for Unix systems  
**Usage**:
```bash
bash generate_secrets.sh
```
**Output**: Prints secure random keys to copy

---

## 📋 Updated Project Files

### 10. **settings.py** (Modified)
**Changes Made**:
- Line 11: `ALLOWED_HOSTS` now reads from .env
- Line 118-125: `CORS_ALLOWED_ORIGINS` conditional based on DEBUG

**Production-Ready**: ✅

### 11. **requirements.txt** (Existing)
**Status**: Already contains all needed packages  
**Packages**:
- Django 4.2.7
- djangorestframework 3.14.0
- django-cors-headers 4.3.1
- djangorestframework-simplejwt 5.3.0
- bcrypt, PyPDF2, requests
- python-dotenv
- google-auth packages

---

## 📂 File Locations Summary

```
talentranker-django/
│
├── 📖 Documentation
│   ├── CPANEL_DEPLOYMENT_GUIDE.md      # Main guide
│   ├── DEPLOYMENT_CHECKLIST.md         # Step-by-step checklist
│   ├── QUICK_REFERENCE.md              # Quick commands
│   └── ADMIN_CRUD_FIX.md              # Technical docs
│
├── ⚙️ Configuration
│   ├── passenger_wsgi.py               # Passenger entry point
│   ├── .env.production                 # Production env template
│   ├── .htaccess.example              # Apache config template
│   └── talentranker/settings.py       # Django settings (updated)
│
├── 🛠️ Scripts
│   ├── generate_secrets.bat           # Windows secret generator
│   └── generate_secrets.sh            # Unix secret generator
│
└── 📄 Project Files (existing)
    ├── manage.py
    ├── requirements.txt
    ├── apps/
    ├── scripts/
    └── ...
```

---

## 🎯 Deployment Workflow

### Quick Start (3 Steps)

#### STEP 1: Prepare Locally
```bash
# Generate secrets
generate_secrets.bat  # Windows
# OR
bash generate_secrets.sh  # Linux/Mac

# Update .env.production with:
# - Generated secrets
# - Your domain names
# - Google OAuth credentials
```

#### STEP 2: Upload to cPanel
1. Upload all files (except venv, .git, db.sqlite3)
2. Rename `.env.production` → `.env`
3. Update `passenger_wsgi.py` with your virtual env path
4. Rename `.htaccess.example` → `.htaccess`
5. Update `.htaccess` with your paths

#### STEP 3: Setup on Server
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py migrate
python manage.py createsuperuser
python scripts/seed-plans.py
python manage.py collectstatic --noinput

# Restart
touch passenger_wsgi.py
```

---

## ✅ Pre-Deployment Checklist

Before uploading to cPanel:

- [ ] Read `CPANEL_DEPLOYMENT_GUIDE.md`
- [ ] Generate secrets using `generate_secrets.bat/.sh`
- [ ] Update `.env.production` with all values
- [ ] Update Google OAuth credentials
- [ ] Get cPanel virtual environment path
- [ ] Update `passenger_wsgi.py` line 13
- [ ] Update `.htaccess.example` with your paths
- [ ] Test locally one more time

---

## 🆘 Need Help?

1. **First Time?** → Read `CPANEL_DEPLOYMENT_GUIDE.md`
2. **During Deployment?** → Follow `DEPLOYMENT_CHECKLIST.md`
3. **Quick Command?** → Check `QUICK_REFERENCE.md`
4. **Issue After Deployment?** → See Troubleshooting in guides

---

## 📞 Support Files

| Issue | Check This File |
|-------|----------------|
| Don't know where to start | `CPANEL_DEPLOYMENT_GUIDE.md` |
| Forgot a step | `DEPLOYMENT_CHECKLIST.md` |
| Need quick command | `QUICK_REFERENCE.md` |
| Application not starting | `passenger_wsgi.py` config |
| CORS errors | `.env` FRONTEND_URL |
| Google OAuth not working | Google OAuth setup section |
| Static files missing | `.htaccess` configuration |
| Database locked | File permissions section |

---

## 🎉 Success Indicators

You know deployment worked when:

- ✅ `https://api.yourdomain.com/` returns response
- ✅ `https://api.yourdomain.com/api/users/plans` returns JSON
- ✅ Django admin accessible at `/admin/`
- ✅ Google OAuth login works from Vercel frontend
- ✅ Can upload CV and JD from frontend
- ✅ CV ranking works and credits deduct
- ✅ Admin panel shows users and plans

---

## 📝 Notes

### Important Reminders

1. **Never commit these to Git**:
   - `.env` (production)
   - `db.sqlite3`
   - Any file with real credentials

2. **Always keep backups**:
   - Database (`db.sqlite3`)
   - `.env` file (in password manager)
   - Admin credentials

3. **Security checklist**:
   - `DEBUG=False` in production
   - Strong secret keys
   - HTTPS enforced
   - CORS restricted to your domains

---

**All files are ready for deployment!** 🚀

Follow the guides in order:
1. Read main guide
2. Use checklist during deployment
3. Keep quick reference handy
4. Celebrate success! 🎊
