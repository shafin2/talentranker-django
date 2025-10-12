# 🚀 Quick Deployment Checklist

Use this checklist during deployment to ensure nothing is missed.

## Before Deployment

### 1. Google OAuth Setup ✅
- [ ] Login to https://console.cloud.google.com/
- [ ] Select your project
- [ ] Go to **Credentials** → Click your OAuth 2.0 Client
- [ ] Under **Authorized JavaScript origins**, add:
  - `https://your-frontend.vercel.app`
  - `https://api.yourdomain.com`
- [ ] Under **Authorized redirect URIs**, add:
  - `https://your-frontend.vercel.app`
  - `https://api.yourdomain.com/api/auth/google/callback`
- [ ] Click **Save**
- [ ] Copy your **Client ID** and **Client Secret**

### 2. Generate Production Secrets ✅
```bash
# Windows
generate_secrets.bat

# Linux/Mac
bash generate_secrets.sh
```
- [ ] Copy generated `DJANGO_SECRET_KEY`
- [ ] Copy generated `JWT_SECRET`
- [ ] Save these in a secure location

### 3. Prepare Files ✅
- [ ] Update `.env.production` with your values
- [ ] Update `passenger_wsgi.py` with your cPanel paths
- [ ] Update `.htaccess.example` with your cPanel paths

---

## cPanel Setup

### 4. Upload Files ✅
- [ ] Login to cPanel
- [ ] Go to **File Manager**
- [ ] Navigate to subdomain directory (e.g., `api.yourdomain.com`)
- [ ] Upload all project files EXCEPT:
  - `venv/`
  - `db.sqlite3`
  - `.env` (use `.env.production` instead)
  - `__pycache__/`
  - `.git/`
  - `*.pyc` files

### 5. Create Python Application ✅
- [ ] cPanel → **Setup Python App**
- [ ] Click **Create Application**
- [ ] Python Version: **3.9** or higher
- [ ] Application Root: `/home/yourusername/api.yourdomain.com`
- [ ] Application URL: `api.yourdomain.com`
- [ ] Application Startup File: `passenger_wsgi.py`
- [ ] Application Entry Point: `application`
- [ ] Click **Create**
- [ ] **COPY the virtual environment path shown!** Example:
  ```
  /home/yourusername/virtualenv/api_yourdomain_com/3.9/bin/python
  ```

### 6. Update Configuration Files ✅
- [ ] Update `passenger_wsgi.py` line 13 with YOUR virtual environment path
- [ ] Upload updated `passenger_wsgi.py`
- [ ] Rename `.htaccess.example` to `.htaccess`
- [ ] Update `.htaccess` with YOUR username and paths
- [ ] Upload `.htaccess`

### 7. Setup Environment File ✅
- [ ] Rename `.env.production` to `.env`
- [ ] Update all placeholder values:
  - [ ] `DJANGO_SECRET_KEY` (from step 2)
  - [ ] `JWT_SECRET` (from step 2)
  - [ ] `ALLOWED_HOSTS` (your subdomain)
  - [ ] `FRONTEND_URL` (your Vercel URL)
  - [ ] `GOOGLE_CLIENT_ID` (from step 1)
  - [ ] `GOOGLE_CLIENT_SECRET` (from step 1)
  - [ ] `GOOGLE_REDIRECT_URI` (your subdomain callback URL)
  - [ ] `DEBUG=False`
- [ ] Upload `.env` to project root

---

## Terminal Setup (SSH or cPanel Terminal)

### 8. Install Dependencies ✅
```bash
# Activate virtual environment
source /home/yourusername/virtualenv/api_yourdomain_com/3.9/bin/activate

# Navigate to project
cd ~/api.yourdomain.com

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify
pip list
```

- [ ] All packages installed successfully
- [ ] No errors in installation

### 9. Database Setup ✅
```bash
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Email: admin@yourdomain.com
# Password: [CREATE STRONG PASSWORD]

# Seed plans
python scripts/seed-plans.py

# Collect static files
python manage.py collectstatic --noinput
```

- [ ] Migrations completed
- [ ] Admin user created (SAVE CREDENTIALS!)
- [ ] Plans seeded successfully
- [ ] Static files collected

### 10. File Permissions ✅
```bash
# Set directory permissions
chmod 755 ~/api.yourdomain.com
chmod 755 ~/api.yourdomain.com/uploads
chmod 755 ~/api.yourdomain.com/uploads/temp
chmod 755 ~/api.yourdomain.com/staticfiles

# Set database permissions
chmod 666 ~/api.yourdomain.com/db.sqlite3

# Make startup file executable
chmod 755 ~/api.yourdomain.com/passenger_wsgi.py
```

- [ ] All permissions set correctly

---

## Application Launch

### 11. Restart Application ✅
```bash
touch ~/api.yourdomain.com/passenger_wsgi.py
```
OR
- [ ] cPanel → **Setup Python App** → Find your app → Click **Restart**

### 12. Test API ✅
```bash
# Test health check
curl https://api.yourdomain.com/

# Test plans endpoint
curl https://api.yourdomain.com/api/users/plans

# Test admin login
curl -X POST https://api.yourdomain.com/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@yourdomain.com","password":"YOUR_PASSWORD"}'
```

- [ ] Health check returns response
- [ ] Plans endpoint returns data
- [ ] Admin login works
- [ ] Check error logs if any issues:
  ```bash
  tail -n 50 ~/logs/api.yourdomain.com/error.log
  ```

---

## Frontend Update

### 13. Update Vercel Environment ✅
- [ ] Go to Vercel Dashboard
- [ ] Select your project
- [ ] Settings → **Environment Variables**
- [ ] Update/Add:
  ```
  VITE_API_BASE_URL=https://api.yourdomain.com/api
  VITE_GOOGLE_CLIENT_ID=<your-google-client-id>
  ```
- [ ] Click **Save**
- [ ] Redeploy:
  - Deployments → Latest → **⋯** → **Redeploy**

---

## Final Testing

### 14. End-to-End Testing ✅
Visit your Vercel frontend and test:

- [ ] **Landing Page** loads correctly
- [ ] **Sign Up** with email works
- [ ] **Login** with email works
- [ ] **Google OAuth** login works
- [ ] Navigate to **Dashboard**
- [ ] Upload **Job Description** (PDF)
- [ ] Upload **CV** (PDF)
- [ ] Run **CV Ranking**
- [ ] View **Ranking Results**
- [ ] Check **Usage Stats** (credits deducted)
- [ ] Test **Admin Panel**:
  - [ ] Admin login works
  - [ ] View users
  - [ ] View plans
  - [ ] Edit plan limits
  - [ ] Changes persist in database

### 15. Admin Panel Testing ✅
- [ ] Visit `https://api.yourdomain.com/admin/`
- [ ] Login with admin credentials
- [ ] Verify all models appear:
  - [ ] Users
  - [ ] Plans
  - [ ] Job Descriptions
  - [ ] CVs
  - [ ] Ranking Results

---

## Post-Deployment

### 16. Security Check ✅
- [ ] `DEBUG=False` in `.env`
- [ ] Strong passwords used
- [ ] HTTPS enforced
- [ ] Google OAuth restricted to your domains
- [ ] Database file permissions correct (666)
- [ ] `.env` file NOT accessible via web

### 17. Monitoring Setup ✅
- [ ] Bookmark error log path:
  ```
  ~/logs/api.yourdomain.com/error.log
  ```
- [ ] Set up daily database backups
- [ ] Test backup restoration

### 18. Documentation ✅
- [ ] Save admin credentials in password manager
- [ ] Document virtual environment path
- [ ] Save cPanel username and paths
- [ ] Record deployment date

---

## 🎉 Deployment Complete!

### Important URLs
- **Frontend**: https://your-app.vercel.app
- **Backend API**: https://api.yourdomain.com/api
- **Django Admin**: https://api.yourdomain.com/admin/

### Important Credentials
- **Admin Email**: ___________________________
- **Admin Password**: _______________________ (KEEP SECRET!)
- **cPanel Username**: _____________________
- **Virtual Env Path**: _____________________

### Next Steps
1. Monitor error logs for 24-48 hours
2. Test all features thoroughly
3. Set up automated backups
4. Consider upgrading to PostgreSQL/MySQL for better performance

---

## Troubleshooting

If something doesn't work:

1. **Check Error Logs**:
   ```bash
   tail -n 100 ~/logs/api.yourdomain.com/error.log
   ```

2. **Restart Application**:
   ```bash
   touch ~/api.yourdomain.com/passenger_wsgi.py
   ```

3. **Check Environment**:
   ```bash
   cat ~/api.yourdomain.com/.env
   ```

4. **Test Database**:
   ```bash
   python manage.py shell
   >>> from apps.users.models import User
   >>> User.objects.count()
   ```

5. **Re-run Migrations**:
   ```bash
   python manage.py migrate --run-syncdb
   ```

---

**Deployed By**: _________________
**Date**: _________________
**Status**: ✅ SUCCESS / ❌ NEEDS ATTENTION
