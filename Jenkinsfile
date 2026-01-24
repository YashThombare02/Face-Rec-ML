pipeline {
    agent any

    environment {
        PROJECT_NAME = 'face_recognition'
        PYTHON_VERSION = '3.9'
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                script {
                    sh '''
                        python -m venv venv
                        . venv/bin/activate || source venv/Scripts/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'
                script {
                    sh '''
                        . venv/bin/activate || source venv/Scripts/activate
                        pip install pytest pytest-cov pylint flake8
                    '''
                }
            }
        }

        stage('Linting') {
            steps {
                echo 'Running linting checks...'
                script {
                    sh '''
                        . venv/bin/activate || source venv/Scripts/activate
                        find . -name "*.py" -not -path "./venv/*" | xargs pylint --exit-zero > pylint-report.txt || true
                        find . -name "*.py" -not -path "./venv/*" | xargs flake8 --format json > flake8-report.json || true
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                script {
                    sh '''
                        . venv/bin/activate || source venv/Scripts/activate
                        pytest --cov=. --cov-report=xml --cov-report=html --junitxml=test-results.xml || true
                    '''
                }
            }
        }

        stage('Code Quality Analysis - SonarQube') {
            steps {
                echo 'Running SonarQube analysis...'
                script {
                    sh '''
                        . venv/bin/activate || source venv/Scripts/activate
                        pip install sonarscan
                        sonarscan \
                            -Dsonar.projectKey=${PROJECT_NAME} \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=http://localhost:9000 \
                            -Dsonar.login=${SONAR_AUTH_TOKEN} \
                            -Dsonar.python.coverage.reportPath=coverage.xml \
                            -Dsonar.exclusions="venv/**,*.npy,model/**,subjects_photos/**"
                    '''
                }
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo 'Archiving test and coverage reports...'
                script {
                    archiveArtifacts artifacts: '**/test-results.xml,**/coverage.xml,**/htmlcov/**,pylint-report.txt,flake8-report.json', 
                        allowEmptyArchive: true
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            script {
                junit testResults: '**/test-results.xml', allowEmptyResults: true
            }
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed! Check the logs for details.'
        }
    }
}
