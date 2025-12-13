# Getting Started Guide

## 🚀 Quick Setup

This guide will help you get the DevOps Testing Portfolio project running locally.

### Prerequisites

Before you begin, ensure you have the following installed:

- **Docker Desktop** (20.10+) - [Download](https://www.docker.com/products/docker-desktop)
- **Git** - [Download](https://git-scm.com/downloads)
- **Python** 3.11+ - [Download](https://www.python.org/downloads/)
- **(Optional) Java 17+** - [Download](https://adoptium.net/)
- **(Optional) Node.js 18+** - [Download](https://nodejs.org/)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/devops-testing-portfolio.git
cd devops-testing-portfolio
```

### Step 2: Start All Services with Docker

The easiest way to run the entire application:

```bash
# Start all services
docker-compose up -d

# Check service health
docker-compose ps

# View logs
docker-compose logs -f
```

**Services will be available at:**
- Frontend: http://localhost:3000
- User Service API: http://localhost:5000
- Product Service API: http://localhost:8080
- Order Service API: http://localhost:4000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- Selenium Hub: http://localhost:4444

### Step 3: Verify Everything is Running

Test the health endpoints:

```bash
# User Service
curl http://localhost:5000/health

# Expected response:
# {"status":"healthy","service":"user-service"}
```

### Step 4: Run Tests

#### Run All Tests

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install test dependencies
pip install -r services/user-service/requirements.txt
pip install pytest pytest-cov selenium robotframework robotframework-seleniumlibrary

# Run unit tests
pytest tests/unit/ -v --cov

# Run integration tests
pytest tests/integration/ -v

# Run E2E Selenium tests
pytest tests/e2e/ -v

# Run Robot Framework tests
cd tests/robot-framework
robot user_tests.robot
```

#### Run Tests in Docker

```bash
# Run unit tests in container
docker-compose run --rm user-service pytest /app/tests/unit/ -v
```

### Step 5: Run Individual Services Locally (Optional)

If you want to develop a specific service without Docker:

#### User Service (Python/Flask)

```bash
cd services/user-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql://admin:admin123@localhost:5432/ecommerce
export FLASK_ENV=development

# Run the service
python app.py
```

Access at: http://localhost:5000

### Step 6: Test the API with curl

```bash
# Register a new user
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123!"
  }'

# Save the token from the response and use it:
TOKEN="your_token_here"

# Get current user
curl -X GET http://localhost:5000/api/users/me \
  -H "Authorization: Bearer $TOKEN"
```

## 🧪 Running CI/CD Pipelines

### Local Jenkins Setup

1. **Install Jenkins** (or use Docker):
```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  --name jenkins jenkins/jenkins:lts
```

2. **Access Jenkins**: http://localhost:8080

3. **Initial Setup**:
   - Get initial password: `docker logs jenkins`
   - Install suggested plugins
   - Install additional plugins: Docker, Pipeline, Git, HTML Publisher

4. **Create Pipeline**:
   - New Item → Pipeline
   - Configure → Pipeline Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: your repository
   - Script Path: Jenkinsfile

### GitLab CI/CD

If using GitLab:

1. Push your code to GitLab
2. The `.gitlab-ci.yml` will automatically trigger
3. View pipeline in GitLab → CI/CD → Pipelines

### GitHub Actions (Alternative)

Create `.github/workflows/ci.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Run tests
        run: |
          cd services/user-service
          pip install -r requirements.txt
          pytest ../../tests/unit/ -v --cov
```

## 🔧 Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit code and write tests

### 3. Run Tests Locally

```bash
pytest tests/unit/ -v
pytest tests/integration/ -v
```

### 4. Commit and Push

```bash
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

### 5. Create Pull Request

- CI/CD pipeline will run automatically
- Review test results
- Merge when all checks pass

## 📊 Monitoring and Observability (Optional)

### Add Prometheus + Grafana

```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

Access:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

## 🐛 Troubleshooting

### Services won't start

```bash
# Check logs
docker-compose logs user-service

# Restart services
docker-compose restart

# Rebuild containers
docker-compose up -d --build
```

### Database connection issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Connect to database
docker-compose exec postgres psql -U admin -d ecommerce

# Reset database
docker-compose down -v
docker-compose up -d
```

### Port already in use

```bash
# Find what's using the port (example for port 5000)
# On Windows:
netstat -ano | findstr :5000

# On Linux/Mac:
lsof -i :5000

# Stop the process or change ports in docker-compose.yml
```

### Tests failing

```bash
# Ensure services are running
docker-compose ps

# Check service health
curl http://localhost:5000/health

# Run tests with more output
pytest tests/unit/ -vv -s

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +
```

## 📚 Next Steps

1. **Explore the API**: Try the endpoints with Postman or curl
2. **Run all tests**: Verify your setup with the test suite
3. **Check CI/CD**: Push changes and watch the pipeline
4. **Read Documentation**: Check out `docs/` for more details
5. **Customize**: Add your own features and tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review logs: `docker-compose logs [service-name]`
3. Open an issue on GitHub
4. Contact: your.email@example.com

---

**Happy Testing! 🚀**
