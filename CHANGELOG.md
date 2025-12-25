# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-12-25 - Phase 2 Release

### Added
- **Product Service (Java/Spring Boot 3.2.0)** - Complete REST API with Swagger
- **Performance Testing (Locust)** - Load testing suite with realistic scenarios
- **Enhanced CI/CD** - Multi-language pipeline (Python + Java)
- **API Documentation** - Interactive Swagger UI and HTML docs
- LinkedIn & GitHub badges in README

### Changed
- Replaced old CI/CD workflow with enhanced version
- Performance tests configured for CI (UserServiceUser only)

### Fixed
- Java tests use H2 in-memory database
- Locust accepts minor failure rates (<1%)
- Removed duplicate workflows

## [1.0.0] - 2024-12-14 - Phase 1 Release

### Added
- User Service (Python/Flask) with JWT authentication
- Unit & integration tests (85%+ coverage)
- GitHub Actions CI/CD pipeline
- Docker containerization
- Security & code quality scanning

### Tagged
- v1.0-working-pipeline - Stable Phase 1
