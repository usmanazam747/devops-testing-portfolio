pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.azurecr.io'
        DOCKER_CREDENTIALS = credentials('docker-registry-credentials')
        POSTGRES_CREDENTIALS = credentials('postgres-credentials')
        SONARQUBE_SERVER = 'sonarqube'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "Checking out code from repository..."
            }
        }
        
        stage('Build') {
            parallel {
                stage('Build User Service') {
                    steps {
                        dir('services/user-service') {
                            sh '''
                                python3 -m venv venv
                                . venv/bin/activate
                                pip install -r requirements.txt
                                echo "User service built successfully"
                            '''
                        }
                    }
                }
                
                stage('Build Product Service') {
                    steps {
                        dir('services/product-service') {
                            sh '''
                                echo "Building Java Product Service..."
                                mvn clean compile
                            '''
                        }
                    }
                }
                
                stage('Build Order Service') {
                    steps {
                        dir('services/order-service') {
                            sh '''
                                echo "Building Node.js Order Service..."
                                npm install
                            '''
                        }
                    }
                }
            }
        }
        
        stage('Unit Tests') {
            parallel {
                stage('Test User Service') {
                    steps {
                        dir('services/user-service') {
                            sh '''
                                . venv/bin/activate
                                pytest ../../tests/unit/test_user_service.py \
                                    -v \
                                    --cov=app \
                                    --cov-report=xml \
                                    --cov-report=html \
                                    --junitxml=test-results.xml
                            '''
                        }
                    }
                    post {
                        always {
                            junit 'services/user-service/test-results.xml'
                            publishHTML([
                                reportDir: 'services/user-service/htmlcov',
                                reportFiles: 'index.html',
                                reportName: 'User Service Coverage Report'
                            ])
                        }
                    }
                }
                
                stage('Test Product Service') {
                    steps {
                        dir('services/product-service') {
                            sh '''
                                mvn test
                            '''
                        }
                    }
                    post {
                        always {
                            junit 'services/product-service/target/surefire-reports/*.xml'
                        }
                    }
                }
                
                stage('Test Order Service') {
                    steps {
                        dir('services/order-service') {
                            sh '''
                                npm test -- --coverage --ci
                            '''
                        }
                    }
                    post {
                        always {
                            junit 'services/order-service/test-results/*.xml'
                        }
                    }
                }
            }
        }
        
        stage('Code Quality Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarQubeScanner'
                    withSonarQubeEnv('sonarqube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                                -Dsonar.projectKey=devops-testing-portfolio \
                                -Dsonar.sources=services \
                                -Dsonar.tests=tests \
                                -Dsonar.python.coverage.reportPaths=services/user-service/coverage.xml
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                sh '''
                    echo "Starting integration test environment..."
                    docker-compose -f docker-compose.test.yml up -d
                    sleep 30
                    
                    cd tests/integration
                    pytest -v --junitxml=integration-results.xml
                '''
            }
            post {
                always {
                    junit 'tests/integration/integration-results.xml'
                    sh 'docker-compose -f docker-compose.test.yml down'
                }
            }
        }
        
        stage('Security Scanning') {
            parallel {
                stage('Dependency Check') {
                    steps {
                        sh '''
                            pip install safety
                            safety check --file services/user-service/requirements.txt --json || true
                        '''
                    }
                }
                
                stage('Container Scanning') {
                    steps {
                        sh '''
                            docker run --rm aquasec/trivy image \
                                ${DOCKER_REGISTRY}/user-service:latest || true
                        '''
                    }
                }
                
                stage('SAST Scan') {
                    steps {
                        sh '''
                            pip install bandit
                            bandit -r services/ -f json -o bandit-report.json || true
                        '''
                    }
                }
            }
        }
        
        stage('Build Docker Images') {
            steps {
                script {
                    docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-credentials') {
                        def userServiceImage = docker.build(
                            "${DOCKER_REGISTRY}/user-service:${BUILD_NUMBER}",
                            "./services/user-service"
                        )
                        userServiceImage.push()
                        userServiceImage.push('latest')
                        
                        // Build other services similarly
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                sh '''
                    echo "Deploying to staging environment..."
                    docker-compose -f docker-compose.staging.yml up -d
                    sleep 30
                    docker-compose -f docker-compose.staging.yml ps
                '''
            }
        }
        
        stage('E2E Tests - Selenium') {
            steps {
                sh '''
                    cd tests/e2e
                    pip install selenium pytest pytest-html
                    pytest test_*.py -v \
                        --html=selenium-report.html \
                        --self-contained-html
                '''
            }
            post {
                always {
                    publishHTML([
                        reportDir: 'tests/e2e',
                        reportFiles: 'selenium-report.html',
                        reportName: 'Selenium E2E Tests'
                    ])
                    archiveArtifacts artifacts: 'tests/e2e/screenshots/*.png', allowEmptyArchive: true
                }
            }
        }
        
        stage('E2E Tests - Robot Framework') {
            steps {
                sh '''
                    cd tests/robot-framework
                    pip install robotframework robotframework-seleniumlibrary
                    robot --outputdir results .
                '''
            }
            post {
                always {
                    publishHTML([
                        reportDir: 'tests/robot-framework/results',
                        reportFiles: 'report.html',
                        reportName: 'Robot Framework Tests'
                    ])
                }
            }
        }
        
        stage('Performance Tests') {
            steps {
                sh '''
                    cd tests/performance
                    jmeter -n -t load-test.jmx -l results.jtl -e -o reports/
                '''
            }
            post {
                always {
                    publishHTML([
                        reportDir: 'tests/performance/reports',
                        reportFiles: 'index.html',
                        reportName: 'Performance Test Report'
                    ])
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to Production?', ok: 'Deploy'
                sh '''
                    echo "Deploying to production..."
                    docker-compose -f docker-compose.prod.yml up -d
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
            emailext(
                subject: "Pipeline ${currentBuild.result}: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                    Build Status: ${currentBuild.result}
                    Project: ${env.JOB_NAME}
                    Build Number: ${env.BUILD_NUMBER}
                    Build URL: ${env.BUILD_URL}
                """,
                to: 'team@example.com'
            )
        }
        success {
            slackSend(
                color: 'good',
                message: "✅ Pipeline SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
        failure {
            slackSend(
                color: 'danger',
                message: "❌ Pipeline FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            )
        }
    }
}
