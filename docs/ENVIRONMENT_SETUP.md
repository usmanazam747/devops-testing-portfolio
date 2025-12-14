# Environment Variables Setup Guide

## Critical Variables (MUST HAVE)

### 1. **SECRET_KEY** ⚠️ CRITICAL
- **Purpose**: Signs JWT tokens, encrypts sessions
- **Required**: YES - App will use insecure fallback without it
- **Generate**: 
  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```
- **Example**: `SECRET_KEY=n9kG2IoQTovSq1Crt0JIoSwaujStBurgYgzVMSE7xr8`
- **⚠️ WARNING**: NEVER commit this to Git! NEVER reuse between environments!

### 2. **DATABASE_URL** ⚠️ REQUIRED
- **Purpose**: PostgreSQL database connection
- **Required**: YES - App cannot run without database
- **Format**: `postgresql://username:password@host:port/database`
- **Local**: `postgresql://admin:admin123@localhost:5432/ecommerce`
- **Production**: Provided by hosting platform (Render/Azure/AWS)

### 3. **FLASK_ENV** ⚠️ REQUIRED
- **Purpose**: Controls debug mode and security checks
- **Required**: YES - Defaults to production if not set
- **Values**: 
  - `development` - Local testing (debug enabled)
  - `production` - Deployed environments (strict security)

## Optional Variables (Recommended)

### 4. **REDIS_URL** (Optional)
- **Purpose**: Session storage, caching
- **Required**: NO - App works without it
- **Format**: `redis://hostname:port/db_number`
- **Local**: `redis://localhost:6379/0`

### 5. **FLASK_APP** (Optional)
- **Purpose**: Flask CLI commands (`flask run`, `flask db`, etc.)
- **Required**: NO - Only needed for CLI
- **Value**: `app.py`

---

## Quick Setup

### For Local Development:

1. **Copy the template**:
   ```bash
   cp .env.example services/user-service/.env
   ```

2. **Generate SECRET_KEY**:
   ```bash
   python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
   ```

3. **Edit `.env` file** with your SECRET_KEY

4. **Verify variables are loaded**:
   ```bash
   cd services/user-service
   python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('SECRET_KEY:', 'SET' if os.getenv('SECRET_KEY') else 'MISSING')"
   ```

### For Production (Render/Azure):

Set these in your hosting platform's dashboard:

```bash
SECRET_KEY=<new-production-key>
DATABASE_URL=<provided-by-platform>
REDIS_URL=<provided-by-platform>
FLASK_ENV=production
```

---

## Current Setup Status

✅ **Created**: `services/user-service/.env` with secure defaults  
✅ **SECRET_KEY**: Generated and configured  
✅ **DATABASE_URL**: Set to local PostgreSQL  
✅ **REDIS_URL**: Set to local Redis  
✅ **FLASK_ENV**: Set to development  

---

## Testing Your Setup

```bash
cd services/user-service
python app.py
```

**Expected output**:
- No warnings about missing SECRET_KEY
- "Running on http://127.0.0.1:5000"
- Database connection successful

**If you see** "⚠️ WARNING: Using insecure development secret key":
- Your `.env` file is not being loaded
- Check file location: `services/user-service/.env`
- Check if `python-dotenv` is installed

---

## Security Checklist

- [ ] `.env` files are in `.gitignore` ✅ (already done)
- [ ] SECRET_KEY is unique and secure ✅ (generated)
- [ ] Production uses different SECRET_KEY than development
- [ ] Never commit `.env` files
- [ ] Never share SECRET_KEY in chat/email/Slack
- [ ] Rotate SECRET_KEY if compromised

---

## What Happens Without These Variables?

| Variable | Missing Consequence |
|----------|-------------------|
| `SECRET_KEY` | ⚠️ Insecure fallback used, JWT tokens can be forged |
| `DATABASE_URL` | ❌ App crashes, cannot start |
| `FLASK_ENV` | ⚠️ Defaults to production mode |
| `REDIS_URL` | ℹ️ No impact, app works without Redis |
| `FLASK_APP` | ℹ️ Flask CLI won't work |
