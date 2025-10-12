# ✅ Deployment Checklist - ilmoirfan.ai

**Date**: _______________  
**Time Started**: _______________

---

## BEFORE YOU START

- [ ] Coffee/Tea ready ☕
- [ ] 60 minutes of uninterrupted time
- [ ] cPanel login ready
- [ ] Google Cloud Console access
- [ ] GitHub account access
- [ ] Vercel dashboard access

---

## STEP 1: GOOGLE OAUTH (5 min)

Visit: https://console.cloud.google.com/

- [ ] Go to Credentials
- [ ] Click OAuth 2.0 Client
- [ ] Add JavaScript origins:
  - [ ] `https://talentranker.ilmoirfan.ai`
  - [ ] `https://talentrankerapi.ilmoirfan.ai`
- [ ] Add Redirect URIs:
  - [ ] `https://talentranker.ilmoirfan.ai`
  - [ ] `https://talentrankerapi.ilmoirfan.ai/api/auth/google/callback`
- [ ] Click Save
- [ ] Credentials are correct (already in .env.production)

---

## STEP 2: GENERATE SECRETS (2 min)

- [ ] Run `generate_secrets.bat` (Windows) OR `bash generate_secrets.sh`
- [ ] Copy DJANGO_SECRET_KEY: _______________________________
- [ ] Copy JWT_SECRET: _______________________________

---

## STEP 3: UPDATE .ENV.PRODUCTION (3 min)

Open `.env.production` file:

- [ ] Paste DJANGO_SECRET_KEY (line 9)
- [ ] Paste JWT_SECRET (line 18)
- [ ] Verify other values are correct:
  - [ ] DEBUG=False ✅
  - [ ] ALLOWED_HOSTS=talentrankerapi.ilmoirfan.ai,ilmoirfan.ai ✅
  - [ ] FRONTEND_URL=https://talentranker.ilmoirfan.ai ✅
  - [ ] GOOGLE_REDIRECT_URI=https://talentrankerapi.ilmoirfan.ai/api/auth/google/callback ✅

---

## STEP 4: PUSH TO GITHUB (5 min)

```bash
cd "e:\OtherWork\Sir rao\TalentRanker\talentranker-django"
git add .
git commit -m "Deploy to cPanel - ilmoirfan.ai"
git push origin main
```

- [ ] Git push successful
- [ ] Go to GitHub repo
- [ ] Click Code → Download ZIP
- [ ] Save ZIP file
- [ ] ZIP file downloaded successfully

---

## STEP 5: UPLOAD TO CPANEL (10 min)

- [ ] Login to cPanel (ilmoirfa account)
- [ ] Open File Manager
- [ ] Navigate to `/home/ilmoirfa/`
- [ ] Create new folder: `talentrankerapi.ilmoirfan.ai`
- [ ] Enter the folder
- [ ] Click Upload
- [ ] Upload the ZIP file
- [ ] Wait for upload to complete
- [ ] Extract the ZIP file
- [ ] Move all files from extracted folder to `talentrankerapi.ilmoirfan.ai/`
- [ ] Delete ZIP and empty folders
- [ ] Verify all files are in place

---

## STEP 6: SETUP .ENV FILE (3 min)

- [ ] Navigate to `/home/ilmoirfa/talentrankerapi.ilmoirfan.ai/`
- [ ] Find `.env.production`
- [ ] Right-click → Edit
- [ ] Verify DJANGO_SECRET_KEY is updated
- [ ] Verify JWT_SECRET is updated
- [ ] Save file
- [ ] Right-click `.env.production` → Rename to `.env`
- [ ] Verify `.env` file exists

---

## STEP 7: CREATE PYTHON APP (5 min)

- [ ] cPanel → Setup Python App
- [ ] Click Create Application
- [ ] Python Version: **3.9** or higher
- [ ] Application Root: `/home/ilmoirfa/talentrankerapi.ilmoirfan.ai`
- [ ] Application URL: `talentrankerapi.ilmoirfan.ai`
- [ ] Application Startup File: `passenger_wsgi.py`
- [ ] Application Entry Point: `application`
- [ ] Click Create
- [ ] Copy virtual environment path shown:
  ```
  _________________________________________________
  ```

---

## STEP 8: UPDATE CONFIG FILES (3 min)

### A. Check passenger_wsgi.py
- [ ] Open `passenger_wsgi.py`
- [ ] Line 13 should have: `/home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/python`
- [ ] If different, update with path from Step 7
- [ ] Save file

### B. Setup .htaccess
- [ ] Find `.htaccess.example`
- [ ] Rename to `.htaccess`
- [ ] File renamed successfully

---

## STEP 9: INSTALL DEPENDENCIES (10 min)

Open Terminal in cPanel:

```bash
source /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/activate
cd ~/talentrankerapi.ilmoirfan.ai
pip install --upgrade pip
pip install -r requirements.txt
```

- [ ] Virtual environment activated
- [ ] Navigated to project directory
- [ ] Pip upgraded
- [ ] Requirements installed (wait ~5-10 min)
- [ ] No errors in installation
- [ ] Run `pip list | grep Django` - shows Django 4.2.7

---

## STEP 10: SETUP DATABASE (5 min)

```bash
# Make sure venv is activated and in project directory
python manage.py migrate
python manage.py createsuperuser
python scripts/seed-plans.py
python manage.py collectstatic --noinput
mkdir -p uploads/temp
```

- [ ] Migrations completed
- [ ] Admin user created:
  - Email: admin@ilmoirfan.ai
  - Name: Admin
  - Password: _________________________ (SAVE THIS!)
- [ ] Plans seeded (should show 21 plans created)
- [ ] Static files collected
- [ ] Upload directories created

---

## STEP 11: FILE PERMISSIONS (2 min)

```bash
chmod 755 ~/talentrankerapi.ilmoirfan.ai
chmod 755 ~/talentrankerapi.ilmoirfan.ai/uploads
chmod 755 ~/talentrankerapi.ilmoirfan.ai/uploads/temp
chmod 755 ~/talentrankerapi.ilmoirfan.ai/staticfiles
chmod 666 ~/talentrankerapi.ilmoirfan.ai/db.sqlite3
chmod 755 ~/talentrankerapi.ilmoirfan.ai/passenger_wsgi.py
```

- [ ] All permissions set

---

## STEP 12: RESTART APP (1 min)

```bash
touch ~/talentrankerapi.ilmoirfan.ai/passenger_wsgi.py
```

- [ ] Application restarted

---

## STEP 13: TEST API (3 min)

```bash
curl https://talentrankerapi.ilmoirfan.ai/
curl https://talentrankerapi.ilmoirfan.ai/api/users/plans
```

- [ ] Health check returns response
- [ ] Plans endpoint returns JSON (21 plans)
- [ ] No errors

If errors, check logs:
```bash
tail -n 50 ~/logs/talentrankerapi.ilmoirfan.ai/error.log
```

---

## STEP 14: UPDATE VERCEL (5 min)

- [ ] Go to https://vercel.com/dashboard
- [ ] Select TalentRanker project
- [ ] Settings → Environment Variables
- [ ] Update/Add:
  - [ ] `VITE_API_BASE_URL` = `https://talentrankerapi.ilmoirfan.ai/api`
  - [ ] `VITE_GOOGLE_CLIENT_ID` = ``
- [ ] Click Save
- [ ] Deployments → Latest → Redeploy
- [ ] Wait for redeployment (~2 min)
- [ ] Deployment successful

---

## STEP 15: FINAL TESTING (10 min)

### Frontend Tests
Visit: https://talentranker.ilmoirfan.ai/

- [ ] Landing page loads correctly
- [ ] Sign up with email works
- [ ] Login with email works
- [ ] **Google OAuth login works** ⭐⭐⭐
- [ ] Dashboard loads
- [ ] Upload JD (PDF) works
- [ ] Upload CV (PDF) works
- [ ] Run CV ranking works
- [ ] Results display correctly
- [ ] Usage stats show credits deducted
- [ ] All tabs (JDs, CVs, Rankings, Plans) work

### Admin Panel Tests
Visit: https://talentrankerapi.ilmoirfan.ai/admin/

- [ ] Admin login works
- [ ] Can view Users
- [ ] Can view Plans
- [ ] Can view Job Descriptions
- [ ] Can view CVs
- [ ] Can view Ranking Results

### User Dashboard Admin Panel
- [ ] Frontend admin login works
- [ ] Can view all users
- [ ] Can edit user plans
- [ ] Can view/edit plans
- [ ] Changes persist in database

---

## 🎉 DEPLOYMENT COMPLETE!

**Time Finished**: _______________  
**Total Time Taken**: _______________ minutes

### Important Information

**URLs:**
- Frontend: https://talentranker.ilmoirfan.ai/
- Backend: https://talentrankerapi.ilmoirfan.ai/api
- Django Admin: https://talentrankerapi.ilmoirfan.ai/admin/

**Admin Credentials:**
- Email: admin@ilmoirfan.ai
- Password: _________________________

**cPanel:**
- Username: ilmoirfa
- Project Path: /home/ilmoirfa/talentrankerapi.ilmoirfan.ai

---

## 📝 POST-DEPLOYMENT

- [ ] Save admin password in password manager
- [ ] Bookmark error log location
- [ ] Set reminder for database backup (weekly)
- [ ] Test all features one more time tomorrow
- [ ] Monitor error logs for 48 hours

---

## ✅ SUCCESS CRITERIA

All must be checked:
- [ ] API responds at https://talentrankerapi.ilmoirfan.ai/
- [ ] Frontend works at https://talentranker.ilmoirfan.ai/
- [ ] Google OAuth login works perfectly
- [ ] File upload and ranking works
- [ ] Credits system works correctly
- [ ] Admin panel fully functional
- [ ] No errors in logs

---

**DEPLOYMENT STATUS**: ⬜ IN PROGRESS / ✅ SUCCESS / ❌ NEEDS ATTENTION

**Notes:**
_____________________________________________
_____________________________________________
_____________________________________________
