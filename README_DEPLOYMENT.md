# 🚀 TalentRanker Backend - cPanel Deployment Package

## 📦 What's Included

This deployment package contains everything you need to deploy your TalentRanker Django backend to cPanel hosting with your frontend on Vercel.

---

## 🎯 Quick Start Guide

### **For First-Time Deployment**

1. **Read This First** 📖  
   Open: `CPANEL_DEPLOYMENT_GUIDE.md`  
   Time: 5-10 minutes  
   Purpose: Understand the complete process

2. **Generate Your Secrets** 🔐  
   Run: `generate_secrets.bat` (Windows) or `bash generate_secrets.sh` (Linux/Mac)  
   Time: 1 minute  
   Purpose: Create secure keys for production

3. **Follow The Checklist** ✅  
   Open: `DEPLOYMENT_CHECKLIST.md`  
   Time: 30-60 minutes  
   Purpose: Step-by-step deployment with checkboxes

4. **Keep Reference Handy** 🚀  
   Open: `QUICK_REFERENCE.md`  
   Purpose: Quick commands while working

---

## 📚 Documentation Guide

### Choose Your Path:

#### 🆕 **First Time Deploying?**
```
START HERE → CPANEL_DEPLOYMENT_GUIDE.md
              ↓
         DEPLOYMENT_CHECKLIST.md
              ↓
         QUICK_REFERENCE.md (bookmark this!)
```

#### 🔧 **Re-deploying or Updating?**
```
QUICK_REFERENCE.md → Find your command
```

#### 🐛 **Having Issues?**
```
QUICK_REFERENCE.md → Common Issues section
              ↓
CPANEL_DEPLOYMENT_GUIDE.md → Troubleshooting
```

#### 📖 **Understanding Recent Changes?**
```
ADMIN_CRUD_FIX.md → Technical details
```

---

## 📄 File Reference

### **Documentation** (Read These)

| File | When to Use | Time Needed |
|------|-------------|-------------|
| `CPANEL_DEPLOYMENT_GUIDE.md` | First deployment | 5-10 min read |
| `DEPLOYMENT_CHECKLIST.md` | During deployment | Follow along |
| `QUICK_REFERENCE.md` | Daily operations | Quick lookup |
| `ADMIN_CRUD_FIX.md` | Understanding fixes | Reference |
| `DEPLOYMENT_FILES_SUMMARY.md` | File overview | Reference |
| `README.md` (this file) | Starting point | 2 min |

### **Configuration** (Update These)

| File | Action Required | Priority |
|------|----------------|----------|
| `.env.production` | Update ALL values | 🔴 CRITICAL |
| `passenger_wsgi.py` | Update line 13 (venv path) | 🔴 CRITICAL |
| `.htaccess.example` | Update paths, rename to `.htaccess` | 🔴 CRITICAL |

### **Utilities** (Use These)

| File | Purpose |
|------|---------|
| `generate_secrets.bat` | Generate secrets (Windows) |
| `generate_secrets.sh` | Generate secrets (Linux/Mac) |

---

## ⚡ Super Quick Deployment (TL;DR)

```bash
# 1. LOCALLY: Generate secrets
generate_secrets.bat  # Windows

# 2. LOCALLY: Update .env.production with:
#    - Generated secrets
#    - Your domains
#    - Google OAuth credentials

# 3. UPLOAD: All files to cPanel (except venv, .git, db.sqlite3)

# 4. SERVER: Setup Python app in cPanel
#    - Get virtual environment path
#    - Update passenger_wsgi.py line 13
#    - Update .htaccess with your paths

# 5. SERVER: Install & setup
source /home/user/virtualenv/xxx/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python scripts/seed-plans.py
python manage.py collectstatic --noinput
chmod 666 db.sqlite3
touch passenger_wsgi.py

# 6. UPDATE: Vercel environment
VITE_API_BASE_URL=https://api.yourdomain.com/api

# 7. TEST: Visit your frontend and test everything!
```

---

## 🎓 Deployment Steps Overview

### Phase 1: Google OAuth Setup (5 minutes)
- Update Authorized JavaScript origins
- Update Authorized redirect URIs
- Copy Client ID and Secret

### Phase 2: Local Preparation (10 minutes)
- Generate production secrets
- Update `.env.production`
- Update `passenger_wsgi.py`
- Update `.htaccess.example`

### Phase 3: cPanel Upload (15 minutes)
- Create Python application
- Upload project files
- Rename configuration files
- Note virtual environment path

### Phase 4: Server Configuration (20 minutes)
- Install Python dependencies
- Run database migrations
- Create admin user
- Seed initial data
- Collect static files
- Set file permissions

### Phase 5: Testing (10 minutes)
- Test API endpoints
- Test Google OAuth
- Test file uploads
- Test admin panel
- Update Vercel environment

**Total Time: ~60 minutes** ⏱️

---

## ✅ Pre-Flight Checklist

Before you begin:

- [ ] Have cPanel login credentials ready
- [ ] Have subdomain created (e.g., `api.yourdomain.com`)
- [ ] Have SSH/terminal access to cPanel
- [ ] Have Google Cloud Console access
- [ ] Have frontend deployed on Vercel
- [ ] Have 60 minutes of uninterrupted time
- [ ] Have coffee/tea ready ☕

---

## 🎯 Success Criteria

You're done when:

1. ✅ API responds at `https://api.yourdomain.com/`
2. ✅ Plans endpoint returns data
3. ✅ Admin can login via frontend
4. ✅ Google OAuth works from Vercel
5. ✅ Can upload and rank CVs
6. ✅ Admin panel CRUD operations work
7. ✅ Credits deduct correctly

---

## 🆘 Help & Support

### If You Get Stuck

1. **Check Error Logs**
   ```bash
   tail -n 50 ~/logs/api.yourdomain.com/error.log
   ```

2. **Consult Troubleshooting**
   - `QUICK_REFERENCE.md` → Common Issues
   - `CPANEL_DEPLOYMENT_GUIDE.md` → Troubleshooting section

3. **Verify Configuration**
   - Is `.env` file correct?
   - Is `passenger_wsgi.py` path updated?
   - Is `.htaccess` configured?

4. **Restart Application**
   ```bash
   touch ~/api.yourdomain.com/passenger_wsgi.py
   ```

---

## 🔒 Security Reminders

**NEVER commit these to Git:**
- `.env` (production file)
- `db.sqlite3`
- Any file with real credentials

**ALWAYS use in production:**
- `DEBUG=False`
- Strong `DJANGO_SECRET_KEY`
- Strong `JWT_SECRET`
- HTTPS enforced
- Restricted CORS origins

---

## 📞 Quick Links

| Resource | Link |
|----------|------|
| Google Cloud Console | https://console.cloud.google.com/ |
| Vercel Dashboard | https://vercel.com/dashboard |
| Django Documentation | https://docs.djangoproject.com/ |
| DRF Documentation | https://www.django-rest-framework.org/ |

---

## 📝 Post-Deployment

After successful deployment:

1. **Document Everything**
   - Save admin credentials in password manager
   - Note down cPanel paths
   - Record deployment date

2. **Set Up Monitoring**
   - Bookmark error log location
   - Set up database backup schedule
   - Monitor for first 24-48 hours

3. **Test Thoroughly**
   - All user flows
   - All admin operations
   - Google OAuth
   - File uploads
   - Credit system

---

## 🎉 Ready to Deploy?

**Recommended Order:**

1. ☕ Get coffee/tea
2. 📖 Read `CPANEL_DEPLOYMENT_GUIDE.md` (10 min)
3. 🔐 Run `generate_secrets.bat` to get keys
4. 📝 Open `DEPLOYMENT_CHECKLIST.md`
5. ✅ Follow checklist step-by-step
6. 🚀 Deploy and test!
7. 🎊 Celebrate success!

---

## 💡 Pro Tips

1. **Use Split Screen**: Keep `DEPLOYMENT_CHECKLIST.md` on one side, terminal on other
2. **Copy/Paste Carefully**: Double-check paths and secrets
3. **Don't Skip Steps**: Each step matters
4. **Test As You Go**: Verify each phase before moving on
5. **Save Credentials**: Use password manager for all credentials
6. **Backup First**: Download local database before migrating

---

## 📊 File Status

| Component | Status | Notes |
|-----------|--------|-------|
| Documentation | ✅ Complete | 6 comprehensive guides |
| Configuration Files | ✅ Ready | Need updating with your values |
| Utility Scripts | ✅ Ready | Generate secrets |
| Django Settings | ✅ Updated | Production-ready |
| WSGI Entry Point | ✅ Created | Update virtual env path |
| Apache Config | ✅ Created | Update paths |

---

## 🌟 Features Included

- ✅ Complete step-by-step guide
- ✅ Interactive checklist
- ✅ Quick reference card
- ✅ Secret generation scripts
- ✅ Production-ready configuration
- ✅ Security best practices
- ✅ Troubleshooting guide
- ✅ Testing procedures
- ✅ Post-deployment monitoring

---

## 📮 Feedback

After deployment, consider:
- How long did it take?
- What was confusing?
- What worked perfectly?

Use this feedback to improve the process!

---

## 🎊 Let's Deploy!

**Everything you need is in this package.**  
**Follow the guides, trust the process, and you'll have a working deployment in about an hour.**

**Good luck! 🚀**

---

**Version**: 1.0  
**Last Updated**: October 2025  
**Prepared For**: cPanel + Vercel Deployment  
**Backend**: Django 4.2.7 + SQLite  
**Frontend**: React + Vite (Vercel)
