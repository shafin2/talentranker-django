# 🚀 cPanel Deployment - Quick Reference

## 📋 Essential Information

### Your Details (Fill this in!)
```
cPanel Username:    _________________
Subdomain:          api.yourdomain.com
Virtual Env Path:   /home/______/virtualenv/api_yourdomain_com/3.9/bin/python
Project Path:       /home/______/api.yourdomain.com
Frontend URL:       https://______.vercel.app
Admin Email:        _________________
Admin Password:     _________________ (KEEP SECRET!)
```

---

## 🔑 Most Important Commands

### Activate Virtual Environment
```bash
source /home/yourusername/virtualenv/api_yourdomain_com/3.9/bin/activate
```

### Restart Application
```bash
touch ~/api.yourdomain.com/passenger_wsgi.py
```
OR: cPanel → Setup Python App → Restart

### Check Error Logs
```bash
tail -n 50 ~/logs/api.yourdomain.com/error.log
```

### Run Migrations
```bash
python manage.py migrate
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Create Admin User
```bash
python manage.py createsuperuser
```

---

## 🔧 Common Issues & Quick Fixes

### "Application Error"
```bash
# Check logs
tail -n 100 ~/logs/api.yourdomain_com/error.log

# Restart
touch ~/api.yourdomain.com/passenger_wsgi.py
```

### "Module Not Found"
```bash
source /home/yourusername/virtualenv/api_yourdomain_com/3.9/bin/activate
cd ~/api.yourdomain.com
pip install -r requirements.txt --force-reinstall
touch passenger_wsgi.py
```

### "Static Files Not Loading"
```bash
python manage.py collectstatic --noinput --clear
chmod 755 ~/api.yourdomain.com/staticfiles
touch ~/api.yourdomain.com/passenger_wsgi.py
```

### "Database Locked"
```bash
chmod 666 ~/api.yourdomain.com/db.sqlite3
chmod 755 ~/api.yourdomain.com
```

### "CORS Error"
Check `.env` file:
- FRONTEND_URL must match Vercel URL exactly
- ALLOWED_HOSTS must include your subdomain
- Restart after changes

---

## 📁 File Structure on cPanel

```
/home/yourusername/
├── api.yourdomain.com/          # Your Django project
│   ├── passenger_wsgi.py        # Passenger startup file
│   ├── .htaccess                # Apache configuration
│   ├── .env                     # Environment variables (SECRET!)
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3              # Database (chmod 666)
│   ├── talentranker/           # Django project folder
│   ├── apps/                   # Django apps
│   ├── staticfiles/            # Collected static files
│   ├── uploads/                # User uploaded files
│   └── scripts/                # Management scripts
│
├── virtualenv/
│   └── api_yourdomain_com/     # Virtual environment
│       └── 3.9/
│           └── bin/
│               └── python      # Python interpreter
│
└── logs/
    └── api.yourdomain.com/
        └── error.log           # Application error logs
```

---

## 🌐 Important URLs

| Purpose | URL |
|---------|-----|
| Frontend | https://your-app.vercel.app |
| API Base | https://api.yourdomain.com/api |
| Django Admin | https://api.yourdomain.com/admin/ |
| Health Check | https://api.yourdomain.com/ |
| Plans API | https://api.yourdomain.com/api/users/plans |
| Admin Login | https://api.yourdomain.com/api/admin/login |

---

## 🔐 Google OAuth Setup

### 1. Google Cloud Console
https://console.cloud.google.com/

### 2. Authorized JavaScript Origins
```
https://your-frontend.vercel.app
https://api.yourdomain.com
```

### 3. Authorized Redirect URIs
```
https://your-frontend.vercel.app
https://api.yourdomain.com/api/auth/google/callback
```

---

## 📝 Environment Variables (.env)

```env
# Security (CHANGE THESE!)
DJANGO_SECRET_KEY=<generate-with-script>
JWT_SECRET=<generate-with-script>
DEBUG=False

# Domains
ALLOWED_HOSTS=api.yourdomain.com,yourdomain.com
FRONTEND_URL=https://your-app.vercel.app

# Google OAuth
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxx
GOOGLE_REDIRECT_URI=https://api.yourdomain.com/api/auth/google/callback
```

---

## ✅ Quick Test Commands

```bash
# Test API is running
curl https://api.yourdomain.com/

# Test database
python manage.py shell
>>> from apps.users.models import User
>>> User.objects.count()
>>> exit()

# Test admin login
curl -X POST https://api.yourdomain.com/api/admin/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@yourdomain.com","password":"YOUR_PASSWORD"}'

# Get plans
curl https://api.yourdomain.com/api/users/plans
```

---

## 🔄 Update/Redeploy Process

### 1. Upload New Code
- Upload changed files via cPanel File Manager or FTP

### 2. Update Dependencies (if changed)
```bash
source /home/yourusername/virtualenv/api_yourdomain_com/3.9/bin/activate
cd ~/api.yourdomain.com
pip install -r requirements.txt
```

### 3. Run Migrations (if models changed)
```bash
python manage.py migrate
```

### 4. Collect Static Files (if static changed)
```bash
python manage.py collectstatic --noinput
```

### 5. Restart Application
```bash
touch passenger_wsgi.py
```

---

## 🆘 Emergency Contacts

**cPanel Support**: _________________
**Domain Registrar**: _________________
**Hosting Provider**: _________________

---

## 📊 Monitoring

### Daily Checks
- [ ] Check error logs
- [ ] Verify site is accessible
- [ ] Test Google OAuth login

### Weekly Checks
- [ ] Backup database
- [ ] Check disk space usage
- [ ] Review access logs

### Monthly Checks
- [ ] Update dependencies (security patches)
- [ ] Review and rotate secrets if needed
- [ ] Clean up old uploaded files

---

## 💾 Backup Commands

### Backup Database
```bash
cp ~/api.yourdomain.com/db.sqlite3 ~/backups/db-$(date +%Y%m%d).sqlite3
```

### Download Database (via SSH)
```bash
scp yourusername@yourdomain.com:~/api.yourdomain.com/db.sqlite3 ./db-backup.sqlite3
```

---

## 📞 Support Resources

1. **Full Guide**: `CPANEL_DEPLOYMENT_GUIDE.md`
2. **Detailed Checklist**: `DEPLOYMENT_CHECKLIST.md`
3. **Admin CRUD Fix**: `ADMIN_CRUD_FIX.md`
4. **Django Docs**: https://docs.djangoproject.com/
5. **DRF Docs**: https://www.django-rest-framework.org/

---

**Keep this reference handy for quick troubleshooting!** 🎯
