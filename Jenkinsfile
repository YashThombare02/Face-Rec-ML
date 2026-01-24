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
                    bat '''
                        python -m venv venv
                        call venv\\Scripts\\activate.bat
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing project dependencies...'
                script {
                    bat '''
                        call venv\\Scripts\\activate.bat
                        pip install pytest pytest-cov pylint flake8
                    '''
                }
            }
        }

        stage('Linting') {
            steps {
                echo 'Running linting checks...'
                script {
                    bat '''
                        call venv\\Scripts\\activate.bat
                        for /r . %%f in (*.py) do (
                            if not "%%f"==".\\venv\\*" (
                                pylint --exit-zero "%%f" >> pylint-report.txt 2>&1
                            )
                        )
                        for /r . %%f in (*.py) do (
                            if not "%%f"==".\\venv\\*" (
                                flake8 --format json "%%f" >> flake8-report.json 2>&1
                            )
                        )
                    '''
                }
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                script {
                    bat '''
                        call venv\\Scripts\\activate.bat
                        pytest --cov=. --cov-report=xml --cov-report=html --junitxml=test-results.xml
                    '''
                }
            }
        }

        stage('Code Quality Analysis - SonarQube') {
            steps {
                echo 'Running SonarQube analysis...'
                script {
                    bat '''
                        call venv\\Scripts\\activate.bat
                        pip install sonarscan
                        sonarscan ^
                            -Dsonar.projectKey=%PROJECT_NAME% ^
                            -Dsonar.sources=. ^
                            -Dsonar.host.url=http://localhost:9000 ^
                            -Dsonar.login=%SONAR_AUTH_TOKEN% ^
                            -Dsonar.python.coverage.reportPath=coverage.xml ^
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
