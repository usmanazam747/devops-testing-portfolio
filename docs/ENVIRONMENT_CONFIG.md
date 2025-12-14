# Environment Configuration Guide

## 🔐 Security: SECRET_KEY Setup

**IMPORTANT:** Never commit your SECRET_KEY to version control!

### Generate a Secure Secret Key

```bash
# Method 1: Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Method 2: OpenSSL
openssl rand -base64 32

# Method 3: PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Minimum 0 -Maximum 256 }))
```

### Local Development Setup

Create a `.env` file in the project root (already in .gitignore):

```bash
# .env
SECRET_KEY=your-generated-secret-key-here
DATABASE_URL=postgresql://admin:admin123@localhost:5432/ecommerce
REDIS_URL=redis://localhost:6379/0
FLASK_ENV=development
```

Load environment variables:

```bash
# Linux/Mac
source .env
export $(cat .env | xargs)

# Windows PowerShell
Get-Content .env | ForEach-Object { 
    if ($_ -match '^([^=]+)=(.*)$') { 
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2]) 
    }
}

# Or use python-dotenv (recommended)
pip install python-dotenv
```

Update `app.py` to use dotenv:

```python
from dotenv import load_dotenv
load_dotenv()  # Load .env file
```

### CI/CD Setup

#### GitHub Actions

1. Go to your repository on GitHub
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add:
   - Name: `SECRET_KEY`
   - Value: Your generated secret key

The workflow already uses it:
```yaml
env:
  SECRET_KEY: ${{ secrets.SECRET_KEY }}
```

#### GitLab CI

1. Go to your project on GitLab
2. Settings → CI/CD → Variables
3. Add variable:
   - Key: `SECRET_KEY`
   - Value: Your generated secret key
   - Protected: ✅
   - Masked: ✅

### Cloud Deployment

#### Render.com

1. Dashboard → Environment
2. Add environment variable:
   - Key: `SECRET_KEY`
   - Value: Your secret key

#### Azure App Service

```bash
az webapp config appsettings set \
  --resource-group myResourceGroup \
  --name myAppName \
  --settings SECRET_KEY="your-secret-key"
```

#### Railway.app

```bash
railway variables set SECRET_KEY="your-secret-key"
```

#### Heroku

```bash
heroku config:set SECRET_KEY="your-secret-key"
```

### Docker Compose

For local Docker development, create `docker-compose.override.yml`:

```yaml
version: '3.8'

services:
  user-service:
    environment:
      - SECRET_KEY=your-local-dev-secret-key
```

This file is in `.gitignore` and won't be committed.

### Production Checklist

- [ ] SECRET_KEY is set as environment variable
- [ ] SECRET_KEY is at least 32 characters
- [ ] SECRET_KEY is not in any code or config files
- [ ] SECRET_KEY is different for each environment
- [ ] FLASK_ENV is set to 'production'
- [ ] Database credentials are secure
- [ ] All secrets are in environment variables or secret manager

### Best Practices

1. **Different keys for different environments** (dev, staging, prod)
2. **Rotate keys periodically** (every 90 days)
3. **Use secret management services** in production:
   - AWS Secrets Manager
   - Azure Key Vault
   - HashiCorp Vault
4. **Never log or print secret keys**
5. **Revoke and regenerate if exposed**

### Troubleshooting

**Error: "SECRET_KEY environment variable must be set"**
- Check if SECRET_KEY is in your environment
- Verify .env file is being loaded
- In CI/CD, check secrets are configured

**Warning: "Using insecure development secret key"**
- This is normal in development
- Set SECRET_KEY env var to remove warning
- Make sure it's set in production!
