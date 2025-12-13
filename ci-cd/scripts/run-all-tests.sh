#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "  DevOps Testing Portfolio"
echo "  Test Runner Script"
echo "======================================"
echo ""

# Function to print colored output
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ $2${NC}"
    else
        echo -e "${RED}✗ $2${NC}"
    fi
}

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -q -r services/user-service/requirements.txt
pip install -q pytest pytest-cov pytest-html selenium robotframework robotframework-seleniumlibrary

# Create reports directory
mkdir -p reports/{unit,integration,e2e,robot,coverage}

echo ""
echo "======================================"
echo "  Running Unit Tests"
echo "======================================"
pytest tests/unit/ \
    -v \
    --cov=services/user-service/app \
    --cov-report=html:reports/coverage \
    --cov-report=term \
    --junitxml=reports/unit/junit.xml
UNIT_RESULT=$?
print_status $UNIT_RESULT "Unit Tests"

echo ""
echo "======================================"
echo "  Running Integration Tests"
echo "======================================"
if docker-compose ps | grep -q "Up"; then
    pytest tests/integration/ \
        -v \
        --junitxml=reports/integration/junit.xml
    INTEGRATION_RESULT=$?
    print_status $INTEGRATION_RESULT "Integration Tests"
else
    echo -e "${YELLOW}⚠ Docker services not running. Skipping integration tests.${NC}"
    echo -e "${YELLOW}  Run 'docker-compose up -d' to start services.${NC}"
    INTEGRATION_RESULT=0
fi

echo ""
echo "======================================"
echo "  Running E2E Selenium Tests"
echo "======================================"
if docker-compose ps | grep selenium-hub | grep -q "Up"; then
    pytest tests/e2e/ \
        -v \
        --html=reports/e2e/report.html \
        --self-contained-html
    E2E_RESULT=$?
    print_status $E2E_RESULT "E2E Selenium Tests"
else
    echo -e "${YELLOW}⚠ Selenium Grid not running. Skipping E2E tests.${NC}"
    echo -e "${YELLOW}  Run 'docker-compose up -d selenium-hub selenium-chrome' to start.${NC}"
    E2E_RESULT=0
fi

echo ""
echo "======================================"
echo "  Running Robot Framework Tests"
echo "======================================"
if docker-compose ps | grep -q "Up"; then
    cd tests/robot-framework
    robot --outputdir ../../reports/robot \
        --loglevel INFO \
        user_tests.robot
    ROBOT_RESULT=$?
    cd ../..
    print_status $ROBOT_RESULT "Robot Framework Tests"
else
    echo -e "${YELLOW}⚠ Services not running. Skipping Robot tests.${NC}"
    ROBOT_RESULT=0
fi

echo ""
echo "======================================"
echo "  Test Summary"
echo "======================================"
print_status $UNIT_RESULT "Unit Tests"
print_status $INTEGRATION_RESULT "Integration Tests"
print_status $E2E_RESULT "E2E Selenium Tests"
print_status $ROBOT_RESULT "Robot Framework Tests"

echo ""
echo "======================================"
echo "  Test Reports Generated"
echo "======================================"
echo "Unit Test Coverage: reports/coverage/index.html"
echo "E2E Test Report: reports/e2e/report.html"
echo "Robot Framework: reports/robot/report.html"
echo ""

# Calculate overall result
OVERALL_RESULT=$((UNIT_RESULT + INTEGRATION_RESULT + E2E_RESULT + ROBOT_RESULT))

if [ $OVERALL_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed. Check reports for details.${NC}"
    exit 1
fi
