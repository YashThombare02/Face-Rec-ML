pipeline {
    agent any

    environment {
        PROJECT_NAME      = 'face_recognition'
        PYTHON_HOME       = 'C:/Users/ythom/AppData/Local/Programs/Python/Python310/python.exe'
        VENV_DIR          = 'venv'
        PUPPET_BIN        = 'C:/Program Files/Puppet Labs/Puppet/bin/puppet.bat'
        SONAR_PROJECT_KEY = 'face-recognition-ml'
    }

    options {
        timeout(time: 1, unit: 'HOURS')
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
            }
        }

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

        // ================= SONARQUBE (JAVA 25 FORCED) =================
        stage('Code Quality - SonarQube') {
            steps {
                echo '🔍 Running SonarQube code analysis...'
                withSonarQubeEnv('sonar-token') {
                    script {
                        def scannerHome = tool 'SonarScanner'
                        def javaHome    = tool 'JDK25'

                        withEnv([
                            "JAVA_HOME=${javaHome}",
                            "PATH=${javaHome}\\bin;${env.PATH}"
                        ]) {
                            bat """
                            echo ===== JAVA DEBUG =====
                            echo JAVA_HOME=%JAVA_HOME%
                            where java
                            java -version
                            echo ======================

                            "${scannerHome}\\bin\\sonar-scanner.bat" ^
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} ^
                            -Dsonar.projectName=${PROJECT_NAME} ^
                            -Dsonar.sources=. ^
                            -Dsonar.python.version=3.10 ^
                            -Dsonar.exclusions=venv/**,tests/**,gx/**,great_expectations/**
                            """
                        }
                    }
                }
            }
        }

        stage('Generate Image Metadata') {
            steps {
                echo '🧾 Generating image metadata CSV...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python generate_image_metadata.py
                """
            }
        }

        stage('Great Expectations Validation') {
            steps {
                echo '📊 Running data quality validation...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python run_ge_checkpoint.py || exit /b 1
                """
            }
        }

        stage('Unit Tests') {
            steps {
                echo '🧪 Running unit tests...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    if exist tests (
                        pytest --junitxml=test-results.xml
                    ) else (
                        echo No tests found
                        echo.> test-results.xml
                    )
                """
            }
        }

        stage('Deploy using Puppet') {
            steps {
                echo '🚀 Deploying application using Puppet...'
                bat """
                    "${PUPPET_BIN}" apply puppet\\manifests\\site.pp
                """
            }
        }

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

            cleanWs(deleteDirs: true, notFailBuild: true)
        }

        success {
            echo '✅ Pipeline executed successfully!'
        }

        failure {
            echo '❌ Pipeline failed — check logs.'
        }
    }
}
