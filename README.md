# DevOps Testing Portfolio - E-Commerce Platform

[![CI/CD Pipeline](https://img.shields.io/badge/CI%2FCD-Active-brightgreen)]()
[![Test Coverage](https://img.shields.io/badge/Coverage-85%25-green)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)]()

## 🎯 Project Overview

This is a comprehensive DevOps and Testing portfolio project demonstrating end-to-end automation, CI/CD practices, and quality assurance expertise. The project showcases a microservices-based e-commerce platform with complete test automation at all levels.

**Skills Demonstrated:**
- ✅ CI/CD Pipeline Design & Implementation (Jenkins + GitLab CI)
- ✅ Test Automation (Selenium, Robot Framework, pytest)
- ✅ Multiple Programming Languages (Python, Java, JavaScript)
- ✅ Containerization & Orchestration (Docker, Docker Compose)
- ✅ Infrastructure as Code (Ansible, Docker Compose)
- ✅ API Testing & Integration Testing
- ✅ Version Control & Git Workflows
- ✅ Agile Testing Practices

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer                        │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
   ┌────▼────┐ ┌───▼────┐ ┌───▼─────┐
   │ Product │ │ User   │ │ Order   │
   │ Service │ │ Service│ │ Service │
   │ (Java)  │ │(Python)│ │ (Node)  │
   └────┬────┘ └───┬────┘ └───┬─────┘
        │          │           │
        └──────────┼───────────┘
                   │
            ┌──────▼──────┐
            │  PostgreSQL │
            └─────────────┘
```

### Services:
1. **Product Service** (Java/Spring Boot) - Product catalog management
2. **User Service** (Python/Flask) - User authentication and management
3. **Order Service** (Node.js/Express) - Order processing
4. **Frontend** (React) - Web interface

## 🧪 Testing Strategy

### Testing Pyramid Implementation

```
           /\
          /  \         End-to-End Tests (Selenium + Robot Framework)
         /____\
        /      \
       /  Int.  \      API Integration Tests (RestAssured, Requests)
      /___________\
     /             \
    /  Unit Tests   \  Unit Tests (JUnit, pytest, Jest)
   /_________________\
```

### Test Coverage:
- **Unit Tests:** 85%+ coverage per service
- **Integration Tests:** API contract testing, database integration
- **End-to-End Tests:** Critical user journeys
- **Performance Tests:** Load testing with JMeter

## 📁 Project Structure

```
devops-testing-portfolio/
├── services/
│   ├── product-service/        # Java Spring Boot microservice
│   ├── user-service/           # Python Flask microservice
│   ├── order-service/          # Node.js Express microservice
│   └── frontend/               # React web application
├── tests/
│   ├── unit/                   # Unit tests for each service
│   ├── integration/            # API integration tests
│   ├── e2e/                    # End-to-end Selenium tests
│   ├── robot-framework/        # Robot Framework test suites
│   └── performance/            # JMeter performance tests
├── infrastructure/
│   ├── docker/                 # Dockerfiles and compose files
│   ├── ansible/                # Infrastructure automation
│   └── kubernetes/             # K8s manifests (optional)
├── ci-cd/
│   ├── jenkins/                # Jenkinsfile and Jenkins config
│   ├── gitlab-ci/              # .gitlab-ci.yml
│   └── scripts/                # Build and deployment scripts
├── docs/
│   ├── architecture.md         # Architecture documentation
│   ├── testing-strategy.md     # Test strategy document
│   └── deployment-guide.md     # Deployment instructions
└── README.md

```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.9+
- Java 17+
- Node.js 18+
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/devops-testing-portfolio.git
cd devops-testing-portfolio

# Start all services with Docker Compose
docker-compose up -d

# Run tests
./scripts/run-all-tests.sh

# Access the application
# Frontend: http://localhost:3000
# Product API: http://localhost:8080
# User API: http://localhost:5000
# Order API: http://localhost:4000
```

## 🔄 CI/CD Pipeline

### Pipeline Stages:

1. **Build** - Compile and build all services
2. **Unit Test** - Run unit tests with coverage reports
3. **Integration Test** - API contract and integration testing
4. **Build Docker Images** - Create containerized services
5. **E2E Test** - Run Selenium and Robot Framework tests
6. **Security Scan** - Dependency and vulnerability scanning
7. **Deploy to Staging** - Automated staging deployment
8. **Performance Test** - Load testing on staging
9. **Deploy to Production** - Manual approval gate

### Pipeline Tools:
- **Jenkins:** Primary CI/CD orchestration
- **GitLab CI:** Alternative pipeline implementation
- **SonarQube:** Code quality and coverage
- **Docker Registry:** Container image storage

## 🧰 Technologies & Tools

### Backend Development:
- Java 17, Spring Boot 3.x, Maven
- Python 3.11, Flask, SQLAlchemy
- Node.js 18, Express.js

### Testing Frameworks:
- **Unit Testing:** JUnit 5, pytest, Jest
- **Integration Testing:** RestAssured, requests, supertest
- **E2E Testing:** Selenium WebDriver, Robot Framework
- **Performance:** Apache JMeter
- **Mocking:** Mockito, unittest.mock, Sinon

### DevOps & Infrastructure:
- Docker & Docker Compose
- Jenkins, GitLab CI
- Ansible
- Git & GitHub/GitLab

### Databases:
- PostgreSQL
- Redis (caching)

### Monitoring & Logging:
- Prometheus (metrics)
- Grafana (visualization)
- ELK Stack (logging)

## 📊 Test Reports & Metrics

Test results and coverage reports are automatically generated and published:
- **Coverage Reports:** Available in `reports/coverage/`
- **Test Results:** JUnit XML format in `reports/junit/`
- **E2E Reports:** HTML reports in `reports/e2e/`
- **Performance Reports:** JMeter results in `reports/performance/`

## 🔐 Security

- Dependency scanning with OWASP Dependency Check
- Container scanning with Trivy
- Static code analysis with SonarQube
- Secrets management with environment variables
- Security testing in CI/CD pipeline

## 📝 Documentation

- [Architecture Documentation](docs/architecture.md)
- [Testing Strategy](docs/testing-strategy.md)
- [Deployment Guide](docs/deployment-guide.md)
- [API Documentation](docs/api-documentation.md)
- [CI/CD Pipeline Guide](docs/ci-cd-guide.md)

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

1. **DevOps Practices:** Complete CI/CD implementation with multiple tools
2. **Test Automation:** Multi-layer testing strategy covering unit to E2E
3. **Microservices:** Polyglot microservices architecture
4. **Containerization:** Docker expertise and orchestration
5. **Infrastructure as Code:** Automated infrastructure provisioning
6. **Quality Assurance:** Comprehensive QA practices and methodologies
7. **Agile Development:** Sprint-based development with test-first approach
8. **Collaboration:** Git workflows, code reviews, documentation

## 🌟 Highlights

- **95+ Tests:** Comprehensive test suite across all layers
- **Automated CI/CD:** Zero-touch deployment pipeline
- **Multi-Language:** Demonstrates versatility across Java, Python, Node.js
- **Production-Ready:** Health checks, monitoring, logging, error handling
- **Best Practices:** Clean code, SOLID principles, 12-factor app methodology

## 📧 Contact

**Your Name**  
Email: your.email@example.com  
LinkedIn: [your-profile](https://linkedin.com/in/your-profile)  
Portfolio: [your-website.com](https://your-website.com)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Status:** ✅ Active Development  
**Last Updated:** December 2025  
**Version:** 1.0.0
