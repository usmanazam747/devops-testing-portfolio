# Deployment to Render.com

Render.com is the easiest way to deploy your portfolio project with a live demo URL.

## 🚀 Why Render?

- ✅ Free tier with PostgreSQL database
- ✅ Auto-deploy from GitHub
- ✅ HTTPS included
- ✅ No credit card required
- ✅ Great for portfolio demos

## 📋 Prerequisites

1. GitHub account with your project pushed
2. Render.com account (free): https://render.com

## 🔧 Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
cd devops-testing-portfolio

# Create GitHub repo first, then:
git remote add origin https://github.com/yourusername/devops-testing-portfolio.git
git branch -M main
git push -u origin main
```

### Step 2: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name:** `ecommerce-db`
   - **Database:** `ecommerce`
   - **User:** `admin`
   - **Region:** Choose closest to you
   - **Plan:** Free
4. Click "Create Database"
5. **Copy the Internal Database URL** (starts with `postgresql://`)

### Step 3: Deploy User Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `user-service`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Root Directory:** `services/user-service`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

4. Click "Advanced" → Add Environment Variables:
   ```
   DATABASE_URL = <paste Internal Database URL from Step 2>
   SECRET_KEY = <generate with: python -c "import secrets; print(secrets.token_urlsafe(32))">
   FLASK_ENV = production
   ```

5. Click "Create Web Service"

### Step 4: Wait for Deployment

- Watch the deployment logs
- First deploy takes 2-3 minutes
- Your app will be live at: `https://user-service-xxxx.onrender.com`

### Step 5: Test Your Deployed API

```bash
# Health check
curl https://your-service.onrender.com/health

# Register a user
curl -X POST https://your-service.onrender.com/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "demo",
    "email": "demo@example.com",
    "password": "Demo123!",
    "first_name": "Demo",
    "last_name": "User"
  }'
```

## 🔄 Auto-Deploy on Git Push

Render automatically redeploys when you push to `main`:

```bash
git add .
git commit -m "Update feature"
git push origin main
# Render automatically deploys!
```

## 📝 Additional Configuration

### Add gunicorn to requirements.txt

```bash
cd services/user-service
echo "gunicorn==21.2.0" >> requirements.txt
git add requirements.txt
git commit -m "Add gunicorn for production"
git push
```

### Configure Health Check

In Render dashboard → Settings:
- **Health Check Path:** `/health`

### Add Redis (Optional)

1. New → Redis
2. Copy Redis URL
3. Add to environment variables: `REDIS_URL`

## 🎯 Final Result

Your portfolio now has:
- ✅ Live demo URL: `https://your-service.onrender.com`
- ✅ Automatic deployments from GitHub
- ✅ Free PostgreSQL database
- ✅ HTTPS encryption
- ✅ Professional deployment platform

## 💡 Pro Tips

1. **Custom Domain:** Render allows custom domains on free tier
2. **Logs:** View logs in Render dashboard for debugging
3. **Sleep Mode:** Free tier sleeps after 15 min inactivity (wakes on request)
4. **Multiple Services:** Deploy all microservices separately

## 🔍 Troubleshooting

### Service won't start
- Check logs in Render dashboard
- Verify environment variables are set
- Ensure gunicorn is in requirements.txt

### Database connection errors
- Verify DATABASE_URL is correct
- Check database is in same region
- Ensure database is running

### 502 Bad Gateway
- Service is starting (wait 30 seconds)
- Check build logs for errors
- Verify start command is correct

## 📚 Next Steps

1. Deploy other services (Product, Order)
2. Add frontend deployment
3. Set up monitoring
4. Add custom domain
5. Update resume with live demo URL!

---

**Your live demo URL is your best portfolio asset!** 🌟
