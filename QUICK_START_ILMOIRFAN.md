# 🚀 Quick Start - Deploy to ilmoirfan.ai

## Super Quick Summary (TL;DR)

**Your Setup:**
- Frontend: https://talentranker.ilmoirfan.ai/ (already on Vercel)
- Backend: https://talentrankerapi.ilmoirfan.ai/ (deploying to cPanel)
- cPanel: ilmoirfa account
- All config files are already updated with your domains!

---

## ⚡ 5-Step Deployment

### 1️⃣ Generate Secrets (2 min)
```bash
generate_secrets.bat
```
Copy the two secrets that appear.

### 2️⃣ Update .env.production (1 min)
Open `.env.production` and paste:
- Line 9: Your DJANGO_SECRET_KEY
- Line 18: Your JWT_SECRET

### 3️⃣ Push to GitHub (3 min)
```bash
git add .
git commit -m "Deploy to cPanel"
git push origin main
```
Then download ZIP from GitHub.

### 4️⃣ Upload to cPanel (30 min)
1. Upload ZIP to `/home/ilmoirfa/talentrankerapi.ilmoirfan.ai/`
2. Extract
3. Rename `.env.production` to `.env`
4. Rename `.htaccess.example` to `.htaccess`
5. Create Python App in cPanel (Python 3.9+)
6. Install dependencies
7. Run migrations
8. Create admin user

### 5️⃣ Update Vercel + Test (10 min)
1. Vercel: Set `VITE_API_BASE_URL=https://talentrankerapi.ilmoirfan.ai/api`
2. Redeploy
3. Test everything!

---

## 📋 Follow These Files in Order

1. **DEPLOYMENT_GUIDE_ILMOIRFAN.md** ← Main guide (detailed steps)
2. **DEPLOYMENT_CHECKLIST_ILMOIRFAN.md** ← Print and check off each step

---

## ⚙️ Configuration Status

✅ **Already Configured** (no changes needed):
- `.env.production` - domains set
- `passenger_wsgi.py` - paths set for ilmoirfa
- `.htaccess.example` - paths set for /home/ilmoirfa/
- `.gitignore` - updated to exclude sensitive files

⚠️ **You Must Update**:
- `.env.production` - DJANGO_SECRET_KEY and JWT_SECRET (lines 9 & 18)

---

## 🔐 Google OAuth Setup

**Add these URLs to Google Cloud Console:**

Authorized JavaScript origins:
```
https://talentranker.ilmoirfan.ai
https://talentrankerapi.ilmoirfan.ai
```

Authorized redirect URIs:
```
https://talentranker.ilmoirfan.ai
https://talentrankerapi.ilmoirfan.ai/api/auth/google/callback
```

---

## 📁 What Gets Uploaded to GitHub

✅ **Included** (safe to commit):
- All Python code
- Configuration templates (.env.production, .htaccess.example)
- Documentation
- Requirements.txt
- Scripts

❌ **Excluded** (in .gitignore):
- .env (actual secrets)
- db.sqlite3 (database)
- uploads/ (user files)
- __pycache__/
- venv/

---

## 🎯 Quick Commands

### On Local Machine:
```bash
# Generate secrets
generate_secrets.bat

# Push to GitHub
git add .
git commit -m "Deploy"
git push
```

### On cPanel Terminal:
```bash
# Activate venv
source /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9/bin/activate

# Go to project
cd ~/talentrankerapi.ilmoirfan.ai

# Install deps
pip install -r requirements.txt

# Setup DB
python manage.py migrate
python manage.py createsuperuser
python scripts/seed-plans.py
python manage.py collectstatic --noinput

# Set permissions
chmod 666 db.sqlite3
chmod 755 passenger_wsgi.py

# Restart
touch passenger_wsgi.py
```

---

## ✅ Success Checklist

You're done when all these work:

- [ ] https://talentrankerapi.ilmoirfan.ai/ returns response
- [ ] https://talentrankerapi.ilmoirfan.ai/api/users/plans returns JSON
- [ ] https://talentranker.ilmoirfan.ai/ loads frontend
- [ ] Google OAuth login works
- [ ] Can upload and rank CVs
- [ ] Admin panel works

---

## 🆘 If Something Breaks

**Check logs:**
```bash
tail -n 50 ~/logs/talentrankerapi.ilmoirfan.ai/error.log
```

**Restart app:**
```bash
touch ~/talentrankerapi.ilmoirfan.ai/passenger_wsgi.py
```

**Common issues:**
1. "Module not found" → Reinstall: `pip install -r requirements.txt`
2. "Database locked" → Fix permissions: `chmod 666 db.sqlite3`
3. "CORS error" → Check .env has correct FRONTEND_URL
4. "Google OAuth error" → Verify redirect URIs in Google Console

---

## 📞 Important Info

**Admin Credentials (you'll create these):**
- Email: admin@ilmoirfan.ai
- Password: [Choose strong password]

**Paths:**
- Project: /home/ilmoirfa/talentrankerapi.ilmoirfan.ai
- Venv: /home/ilmoirfa/virtualenv/talentrankerapi_ilmoirfan_ai/3.9

**URLs:**
- Frontend: https://talentranker.ilmoirfan.ai/
- Backend: https://talentrankerapi.ilmoirfan.ai/api
- Admin: https://talentrankerapi.ilmoirfan.ai/admin/

---

## ⏱️ Time Estimate

- Secrets & prep: 5 min
- GitHub upload: 5 min
- cPanel setup: 30 min
- Testing: 10 min

**Total: ~50 minutes**

---

## 🎉 Let's Go!

1. Read: **DEPLOYMENT_GUIDE_ILMOIRFAN.md**
2. Follow: **DEPLOYMENT_CHECKLIST_ILMOIRFAN.md**
3. Keep this file handy for quick reference

**Good luck! 🚀**
