pipeline {
    agent any

    environment {
        PROJECT_NAME = 'face_recognition'
        PYTHON_HOME  = 'C:/Users/ythom/AppData/Local/Programs/Python/Python310/python.exe'
        VENV_DIR     = 'venv'
        PUPPET_BIN   = 'C:/Program Files/Puppet Labs/Puppet/bin/puppet.bat'
        SONAR_PROJECT_KEY = 'face-recognition-ml'
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        // ================= CHECKOUT =================
        stage('Checkout Code') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

        // ================= PYTHON ENV =================
        stage('Setup Python Environment') {
            steps {
                echo '🐍 Creating Python virtual environment...'
                bat """
                    "${PYTHON_HOME}" --version
                    if not exist ${VENV_DIR} (
                        "${PYTHON_HOME}" -m venv ${VENV_DIR}
                    )
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                """
            }
        }

        // ================= DEPENDENCIES =================
        stage('Install Dependencies') {
            steps {
                echo '📦 Installing project dependencies...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    pip install -r requirements.txt
                    pip install pytest pytest-cov great_expectations pandas
                """
            }
        }

        // ================= SONARQUBE =================
        stage('Code Quality - SonarQube') {
            steps {
                echo '🔍 Running SonarQube code analysis...'
                withSonarQubeEnv('SonarQubeServer') {
                    bat """
                        sonar-scanner ^
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} ^
                        -Dsonar.projectName=${PROJECT_NAME} ^
                        -Dsonar.sources=. ^
                        -Dsonar.language=py ^
                        -Dsonar.python.version=3.10 ^
                        -Dsonar.exclusions=venv/**,tests/**,gx/**,great_expectations/**
                    """
                }
            }
        }

        // ================= QUALITY GATE =================
        stage('Quality Gate') {
            steps {
                echo '🚦 Waiting for SonarQube Quality Gate...'
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ================= METADATA =================
        stage('Generate Image Metadata') {
            steps {
                echo '🧾 Generating image metadata CSV...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python generate_image_metadata.py
                """
            }
        }

        // ================= DATA QUALITY =================
        stage('Great Expectations Validation') {
            steps {
                echo '📊 Running data quality validation...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python run_ge_checkpoint.py || exit /b 1
                """
            }
        }

        // ================= TESTS =================
        stage('Unit Tests') {
            steps {
                echo '🧪 Running unit tests...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    if exist tests (
                        pytest --junitxml=test-results.xml
                    ) else (
                        echo No tests folder found - skipping tests
                        echo.> test-results.xml
                    )
                """
            }
        }

        // ================= DEPLOY =================
        stage('Deploy using Puppet') {
            steps {
                echo '🚀 Deploying application using Puppet...'
                bat """
                    "${PUPPET_BIN}" apply puppet\\manifests\\site.pp
                """
            }
        }

        // ================= ARCHIVE =================
        stage('Archive Artifacts') {
            steps {
                echo '📦 Archiving reports...'
                archiveArtifacts artifacts: '''
                    image_metadata.csv,
                    test-results.xml,
                    gx/**,
                    great_expectations/**
                ''', allowEmptyArchive: true
            }
        }
    }

    // ================= POST =================
    post {
        always {
            junit testResults: 'test-results.xml', allowEmptyResults: true

            echo '🧹 Cleaning workspace (Windows-safe)...'

            bat '''
                if exist venv\\Scripts\\deactivate.bat (
                    call venv\\Scripts\\deactivate.bat
                )
                taskkill /F /IM python.exe /T >nul 2>&1 || exit /b 0
            '''

            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                cleanWs(deleteDirs: true, notFailBuild: true)
            }
        }

        success {
            echo '✅ Pipeline executed successfully!'
        }

        failure {
            echo '❌ Pipeline failed — check logs.'
        }
    }
}
