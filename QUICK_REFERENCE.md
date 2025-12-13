# Quick Reference - DevOps Testing Portfolio

## 🚀 Quick Start Commands

```bash
# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f user-service

# Stop everything
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## 🧪 Testing Commands

```bash
# Run all tests
./ci-cd/scripts/run-all-tests.sh

# Unit tests only
pytest tests/unit/ -v --cov

# E2E tests only
pytest tests/e2e/ -v

# Robot Framework
cd tests/robot-framework && robot user_tests.robot
```

## 📝 Development Commands

```bash
# User Service (Python)
cd services/user-service
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Run with environment variables
export DATABASE_URL=postgresql://admin:admin123@localhost:5432/ecommerce
export FLASK_ENV=development
python app.py
```

## 🐳 Docker Commands

```bash
# Build specific service
docker-compose build user-service

# Restart a service
docker-compose restart user-service

# View service logs
docker-compose logs -f user-service

# Execute command in container
docker-compose exec user-service bash

# Check database
docker-compose exec postgres psql -U admin -d ecommerce
```

## 🔍 Testing the API

```bash
# Health check
curl http://localhost:5000/health

# Register user
curl -X POST http://localhost:5000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"Demo123!"}'

# Login
curl -X POST http://localhost:5000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"Demo123!"}'

# Get current user (with token)
curl http://localhost:5000/api/users/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📊 Useful Git Commands

```bash
# Create feature branch
git checkout -b feature/your-feature

# Stage and commit
git add .
git commit -m "Add: description"

# Push to remote
git push origin feature/your-feature

# View status
git status

# View commit history
git log --oneline --graph
```

## 🔧 Troubleshooting

```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres

# Clear Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# Port in use (Windows)
netstat -ano | findstr :5000

# Check Docker resources
docker system df
docker system prune  # Clean up
```

## 📈 CI/CD Pipeline Triggers

### GitLab CI
```bash
# Push triggers pipeline
git push origin main

# Manual pipeline
# Go to GitLab → CI/CD → Pipelines → Run Pipeline
```

### Jenkins
```bash
# Configure webhook in Jenkins
# Pipeline runs on push to repository

# Or trigger manually in Jenkins UI
```

## 📁 Important Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Service orchestration |
| `.gitlab-ci.yml` | GitLab CI/CD pipeline |
| `Jenkinsfile` | Jenkins pipeline |
| `README.md` | Project documentation |
| `PROJECT_STATUS.md` | Implementation status |
| `docs/GETTING_STARTED.md` | Setup guide |

## 🎯 Key Endpoints

| Service | URL | Health |
|---------|-----|--------|
| User Service | http://localhost:5000 | /health |
| Product Service | http://localhost:8080 | /actuator/health |
| Order Service | http://localhost:4000 | /health |
| Frontend | http://localhost:3000 | / |
| Selenium Hub | http://localhost:4444 | /ui |
| PostgreSQL | localhost:5432 | - |

## 📚 Documentation URLs

- [README](../README.md)
- [Getting Started](../docs/GETTING_STARTED.md)
- [Project Status](../PROJECT_STATUS.md)
- [Test Reports](../reports/)

## 💡 Pro Tips

1. **Always check logs first**: `docker-compose logs service-name`
2. **Use health endpoints**: Quick way to verify services
3. **Run tests locally first**: Before pushing to CI/CD
4. **Keep services updated**: `docker-compose pull`
5. **Document as you go**: Update README with changes

## 🎓 Skills Checklist for Job

- [x] CI/CD Pipeline Design (Jenkins, GitLab CI)
- [x] Test Automation (Selenium, Robot Framework)
- [x] Docker & Containerization
- [x] Python Development (Flask, pytest)
- [ ] Java Development (Spring Boot, JUnit)
- [ ] JavaScript (Node.js, Jest)
- [x] Database Management (PostgreSQL)
- [x] API Testing (REST, curl)
- [x] Git Version Control
- [x] Agile Testing Practices

---

**Keep this file handy for quick reference! 📌**
