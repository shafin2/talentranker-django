# 🚀 TalentRanker Backend - cPanel Deployment (ilmoirfan.ai)

## Your Deployment Configuration

**Frontend URL**: https://talentranker.ilmoirfan.ai/  
**Backend API URL**: https://talentrankerapi.ilmoirfan.ai/  
**cPanel Username**: ilmoirfa  
**cPanel Root**: /home/ilmoirfa

---

## 📋 PRE-DEPLOYMENT CHECKLIST

### 1. Update Google OAuth (5 minutes) ⚠️ CRITICAL

1. Go to https://console.cloud.google.com/
2. Select your project → Credentials
3. Click your OAuth 2.0 Client ID

**Add Authorized JavaScript origins:**
```
https://talentranker.ilmoirfan.ai
https://talentrankerapi.ilmoirfan.ai
```

**Add Authorized redirect URIs:**
```
https://talentranker.ilmoirfan.ai
https://talentrankerapi.ilmoirfan.ai/api/auth/google/callback
```

4. Click **Save**

---

### 2. Generate Production Secrets (2 minutes)

Run this command:
```bash
# Windows
generate_secrets.bat

# Linux/Mac
bash generate_secrets.sh
```

**Copy the output** - you'll need these values!

---

### 3. Update .env.production (3 minutes)

Open `.env.production` and update:

```env
# CHANGE THESE (from generate_secrets output):
DJANGO_SECRET_KEY=<paste-generated-key-here>
JWT_SECRET=<paste-generated-key-here>

# THESE ARE ALREADY SET CORRECTLY:
DEBUG=False
ALLOWED_HOSTS=talentrankerapi.ilmoirfan.ai,ilmoirfan.ai
FRONTEND_URL=https://talentranker.ilmoirfan.ai
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=***
GOOGLE_REDIRECT_URI=https://talentrankerapi.ilmoirfan.ai/api/auth/google/callback
```

⚠️ **Only update DJANGO_SECRET_KEY and JWT_SECRET - everything else is correct!**

---

### 4. Push to GitHub (5 minutes)

```bash
cd "e:\OtherWork\Sir rao\TalentRanker\talentranker-django"

# Add all files
git add .

# Commit
git commit -m "Prepare for cPanel deployment - ilmoirfan.ai"

# Push to GitHub
git push origin main
```

**Note**: .env, db.sqlite3, and uploads/ are gitignored and won't be uploaded ✅

---

## 📥 CPANEL DEPLOYMENT STEPS

### Step 1: Download from GitHub (2 minutes)

1. Go to your GitHub repository
2. Click **Code** → **Download ZIP**
3. Save the ZIP file

---

### Step 2: Upload to cPanel (5 minutes)

1. Login to cPanel
2. Go to **File Manager**
3. Navigate to `/home/ilmoirfa/`
4. Create directory: `talentrankerapi.ilmoirfan.ai`
5. Enter the directory
6. Click **Upload**
7. Upload the ZIP file
8. Click **Extract** on the ZIP file
9. Move all files from the extracted folder to `talentrankerapi.ilmoirfan.ai`
10. Delete the ZIP and empty folder

---

### Step 3: Setup .env File (3 minutes)

1. In File Manager, navigate to `/home/ilmoirfa/talentrankerapi.ilmoirfan.ai/`
2. Find `.env.production`
3. Right-click → **Edit**
4. Update `DJANGO_SECRET_KEY` and `JWT_SECRET` (from step 2)
5. Save the file
6. Right-click on `.env.production` → **Rename** → Rename to `.env`

---

### Step 4: Create Python Application (5 minutes)

1. In cPanel, go to **Setup Python App**
2. Click **Create Application**
3. Configure:
   - **Python Version**: 3.9 or higher
   - **Application Root**: `/home/ilmoirfa/talentrankerapi.ilmoirfan.ai`
   - **Application URL**: `talentrankerapi.ilmoirfan.ai`
   - **Application Startup File**: `passenger_wsgi.py`
   - **Application Entry Point**: `application`
4. Click **Create**

5. **IMPORTANT**: Copy the virtual environment path shown (something like):
   ```
   /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/python
   ```

---

### Step 5: Update Configuration Files (3 minutes)

#### A. Update passenger_wsgi.py
1. In File Manager, open `passenger_wsgi.py`
2. Line 13 should already have:
   ```python
   INTERP = "/home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/python"
   ```
3. If the path is different from step 4, update it
4. Save

#### B. Setup .htaccess
1. Find `.htaccess.example`
2. Right-click → **Rename** → `.htaccess`
3. The paths are already configured for `/home/ilmoirfa/`
4. Verify lines 18, 21, 28, 32 have correct paths

---

### Step 6: Install Dependencies (10 minutes)

Open **Terminal** in cPanel or use SSH:

```bash
# Activate virtual environment (use YOUR path from Step 4)
source /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/activate

# Navigate to project
cd ~/talentrankerapi.ilmoirfan.ai

# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -i django
```

Wait for installation to complete (may take 5-10 minutes).

---

### Step 7: Setup Database (5 minutes)

```bash
# Make sure you're in the project directory and venv is activated
cd ~/talentrankerapi.ilmoirfan.ai
source /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/activate

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Email: admin@ilmoirfan.ai
# Name: Admin
# Password: [CREATE A STRONG PASSWORD AND SAVE IT!]

# Seed plans
python scripts/seed-plans.py

# Collect static files
python manage.py collectstatic --noinput

# Create upload directories
mkdir -p uploads/temp
```

---

### Step 8: Set File Permissions (2 minutes)

```bash
# Set permissions
chmod 755 ~/talentrankerapi.ilmoirfan.ai
chmod 755 ~/talentrankerapi.ilmoirfan.ai/uploads
chmod 755 ~/talentrankerapi.ilmoirfan.ai/uploads/temp
chmod 755 ~/talentrankerapi.ilmoirfan.ai/staticfiles
chmod 666 ~/talentrankerapi.ilmoirfan.ai/db.sqlite3
chmod 755 ~/talentrankerapi.ilmoirfan.ai/passenger_wsgi.py
```

---

### Step 9: Restart Application (1 minute)

```bash
touch ~/talentrankerapi.ilmoirfan.ai/passenger_wsgi.py
```

OR: cPanel → **Setup Python App** → Find your app → Click **Restart**

---

### Step 10: Test API (3 minutes)

```bash
# Test 1: Health check
curl https://talentrankerapi.ilmoirfan.ai/

# Test 2: Get plans
curl https://talentrankerapi.ilmoirfan.ai/api/users/plans

# Test 3: Admin login (use YOUR password)
curl -X POST https://talentrankerapi.ilmoirfan.ai/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@ilmoirfan.ai","password":"YOUR_PASSWORD"}'
```

**All should return JSON responses!**

If any errors, check logs:
```bash
tail -n 50 ~/logs/talentrankerapi.ilmoirfan.ai/error.log
```

---

### Step 11: Update Vercel Frontend (5 minutes)

1. Go to https://vercel.com/dashboard
2. Select your TalentRanker project
3. Go to **Settings** → **Environment Variables**
4. Update/Add:
   ```
   VITE_API_BASE_URL=https://talentrankerapi.ilmoirfan.ai/api
   VITE_GOOGLE_CLIENT_ID=**
   ```
5. Click **Save**
6. Go to **Deployments** → Latest → **⋯** → **Redeploy**

Wait for redeployment (~2 minutes).

---

## ✅ FINAL TESTING

### Test Frontend (10 minutes)

Visit: https://talentranker.ilmoirfan.ai/

Test these features:
- [ ] Landing page loads
- [ ] Sign up with email
- [ ] Login with email
- [ ] **Google OAuth login** ⭐ (most important!)
- [ ] Upload Job Description (PDF)
- [ ] Upload CV (PDF)
- [ ] Run CV ranking
- [ ] View results
- [ ] Check usage stats (credits deducted correctly)

### Test Admin Panel

Visit: https://talentrankerapi.ilmoirfan.ai/admin/

- [ ] Login with admin credentials
- [ ] View Users model
- [ ] View Plans model
- [ ] View Job Descriptions
- [ ] View CVs
- [ ] View Ranking Results

---

## 🎉 SUCCESS CHECKLIST

- [ ] API responds at https://talentrankerapi.ilmoirfan.ai/
- [ ] Plans endpoint returns data
- [ ] Admin login works
- [ ] Google OAuth works from frontend
- [ ] File upload works
- [ ] CV ranking works
- [ ] Credits deduct correctly
- [ ] Admin panel accessible
- [ ] All CRUD operations work

---

## 🔧 QUICK COMMANDS REFERENCE

### Restart Application
```bash
touch ~/talentrankerapi.ilmoirfan.ai/passenger_wsgi.py
```

### Check Error Logs
```bash
tail -n 50 ~/logs/talentrankerapi.ilmoirfan.ai/error.log
```

### Activate Virtual Environment
```bash
source /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/activate
```

### Navigate to Project
```bash
cd ~/talentrankerapi.ilmoirfan.ai
```

### Database Shell
```bash
python manage.py shell
```

### Create Backup
```bash
cp ~/talentrankerapi.ilmoirfan.ai/db.sqlite3 ~/db-backup-$(date +%Y%m%d).sqlite3
```

---

## 🆘 TROUBLESHOOTING

### "Application Error"
```bash
# Check logs
tail -n 100 ~/logs/talentrankerapi.ilmoirfan.ai/error.log

# Restart
touch ~/talentrankerapi.ilmoirfan.ai/passenger_wsgi.py
```

### "Module Not Found"
```bash
source /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/activate
cd ~/talentrankerapi.ilmoirfan.ai
pip install -r requirements.txt --force-reinstall
touch passenger_wsgi.py
```

### "CORS Error"
- Check `.env` file has correct FRONTEND_URL
- Restart application after changes

### "Database Locked"
```bash
chmod 666 ~/talentrankerapi.ilmoirfan.ai/db.sqlite3
chmod 755 ~/talentrankerapi.ilmoirfan.ai
```

---

## 📝 IMPORTANT INFORMATION

**URLs:**
- Frontend: https://talentranker.ilmoirfan.ai/
- Backend API: https://talentrankerapi.ilmoirfan.ai/api
- Django Admin: https://talentrankerapi.ilmoirfan.ai/admin/

**cPanel Info:**
- Username: ilmoirfa
- Project Path: /home/ilmoirfa/talentrankerapi.ilmoirfan.ai
- Virtual Env: /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9

**Admin Credentials:**
- Email: admin@ilmoirfan.ai
- Password: [YOU CREATED THIS - SAVE IT SECURELY!]

**Google OAuth:**
- Client ID: ff
- Authorized origins: talentranker.ilmoirfan.ai, talentrankerapi.ilmoirfan.ai
- Redirect URI: https://talentrankerapi.ilmoirfan.ai/api/auth/google/callback

---

## ⏱️ ESTIMATED TIME

- Pre-deployment: 15 minutes
- Upload & Setup: 20 minutes
- Database & Dependencies: 15 minutes
- Testing: 15 minutes

**Total: ~60 minutes**

---

**Good luck with your deployment! 🚀**
