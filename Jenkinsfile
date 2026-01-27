pipeline {
    agent any

    environment {
        PROJECT_NAME = 'face_recognition'
        PYTHON_HOME  = 'C:/Users/ythom/AppData/Local/Programs/Python/Python39'
        VENV_DIR     = 'venv'
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // ---------------- CHECKOUT ----------------
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        // ---------------- PUPPET ----------------
        stage('Puppet Validation') {
            steps {
                echo 'Validating Puppet manifests...'
                bat '''
                    puppet --version
                    puppet parser validate puppet/manifests/*.pp
                '''
            }
        }

        // ---------------- PYTHON SETUP ----------------
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat '''
                    C:/Users/ythom/AppData/Local/Programs/Python/Python39/python.exe -m venv venv
                    call venv/Scripts/activate.bat
                    python -m pip install --upgrade pip
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat '''
                    call venv/Scripts/activate.bat
                    pip install -r requirements.txt
                    pip install pytest pytest-cov pylint flake8 great_expectations
                '''
            }
        }

        // ---------------- GREAT EXPECTATIONS ----------------
        stage('Data Quality Validation') {
            steps {
                echo 'Running Great Expectations checkpoint...'
                bat '''
                    call venv/Scripts/activate.bat
                    great_expectations checkpoint run data_checkpoint
                '''
            }
        }

        // ---------------- LINTING ----------------
        stage('Linting') {
            steps {
                echo 'Running lint checks...'
                bat '''
                    call venv/Scripts/activate.bat
                    pylint src --exit-zero > pylint-report.txt
                    flake8 src --format=json --output-file=flake8-report.json
                '''
            }
        }

        // ---------------- UNIT TESTS ----------------
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                bat '''
                    call venv/Scripts/activate.bat
                    pytest ^
                      --cov=src ^
                      --cov-report=xml:coverage.xml ^
                      --cov-report=html ^
                      --junitxml=test-results.xml
                '''
            }
        }

        // ---------------- SONARQUBE ----------------
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube scan...'
                withSonarQubeEnv('SonarQube') {
                    bat '''
                        sonar-scanner ^
                          -Dsonar.projectKey=face_recognition ^
                          -Dsonar.sources=src ^
                          -Dsonar.python.coverage.reportPaths=coverage.xml ^
                          -Dsonar.junit.reportPaths=test-results.xml ^
                          -Dsonar.exclusions=venv/**,*.npy,model/**,subjects_photos/**
                    '''
                }
            }
        }

        // ---------------- QUALITY GATE ----------------
        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ---------------- ARCHIVE ----------------
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving reports...'
                archiveArtifacts artifacts: '''
                    test-results.xml,
                    coverage.xml,
                    htmlcov/**,
                    pylint-report.txt,
                    flake8-report.json,
                    great_expectations/uncommitted/data_docs/**
                ''', allowEmptyArchive: true

                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,   // ✅ REQUIRED FIX
                    keepAll: true,
                    reportDir: 'htmlcov',
                    reportFiles: 'index.html',
                    reportName: 'Coverage Report'
                ])
            }
        }
    }

    post {
        always {
            junit testResults: 'test-results.xml', allowEmptyResults: true
            cleanWs()
        }
        success {
            echo '✅ Pipeline executed successfully!'
        }
        failure {
            echo '❌ Pipeline failed — check logs.'
        }
    }
}
