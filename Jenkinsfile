pipeline {
    agent any

    environment {
        PROJECT_NAME = 'face_recognition'
        PYTHON_HOME  = 'C:/Users/ythom/AppData/Local/Programs/Python/Python310/python.exe'
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
                    "C:/Program Files/Puppet Labs/Puppet/bin/puppet.bat" --version
                    "C:/Program Files/Puppet Labs/Puppet/bin/puppet.bat" parser validate puppet/manifests/*.pp
                '''
            }
        }

        // ---------------- PYTHON SETUP ----------------
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat """
                    "${PYTHON_HOME}" --version
                    "${PYTHON_HOME}" -m venv ${VENV_DIR}
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                """
            }
        }

        // ---------------- INSTALL DEPENDENCIES ----------------
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python -m pip install -r requirements.txt
                    python -m pip install pytest pytest-cov pylint flake8 great_expectations
                """
            }
        }

        // ---------------- GENERATE IMAGE METADATA ----------------
        stage('Generate Image Metadata') {
            steps {
                echo 'Generating image metadata CSV...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python generate_image_metadata.py
                """
            }
        }

        // ---------------- GREAT EXPECTATIONS ----------------
        stage('Data Quality Validation') {
            steps {
                echo 'Running Great Expectations checkpoint...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    venv\\Scripts\\great_expectations.exe checkpoint run data_checkpoint
                """
            }
        }

        // ---------------- LINTING ----------------
        stage('Linting') {
            steps {
                echo 'Running lint checks...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    pylint . --exit-zero > pylint-report.txt
                    flake8 . --format=json --output-file=flake8-report.json
                """
            }
        }

        // ---------------- UNIT TESTS ----------------
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    pytest ^
                      --cov=. ^
                      --cov-report=xml:coverage.xml ^
                      --cov-report=html ^
                      --junitxml=test-results.xml
                """
            }
        }

        // ---------------- SONARQUBE ----------------
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube scan...'
                withSonarQubeEnv('SonarQube') {
                    bat """
                        sonar-scanner ^
                          -Dsonar.projectKey=${PROJECT_NAME} ^
                          -Dsonar.sources=. ^
                          -Dsonar.python.coverage.reportPaths=coverage.xml ^
                          -Dsonar.junit.reportPaths=test-results.xml ^
                          -Dsonar.exclusions=venv/**,*.npy,model/**,subjects_photos/**
                    """
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
                    alwaysLinkToLastBuild: true,
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
