pipeline {
    agent any

    environment {
        PROJECT_NAME = 'face_recognition'
        PYTHON_HOME  = 'C:/Users/ythom/AppData/Local/Programs/Python/Python310/python.exe'
        VENV_DIR     = 'venv'
        PUPPET_BIN   = 'C:/Program Files/Puppet Labs/Puppet/bin/puppet.bat'
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

        // ================= PYTHON ENVIRONMENT =================
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
                    pip install pytest pytest-cov pylint flake8 great_expectations pandas
                """
            }
        }

        // ================= GENERATE METADATA =================
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

        // ================= LINTING =================
        stage('Linting') {
            steps {
                echo '🧹 Running lint checks...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat

                    if exist src (
                        pylint src --ignore=venv --exit-zero > pylint-report.txt
                        flake8 src --exclude=venv,__pycache__ --format=json --output-file=flake8-report.json || exit /b 0
                    ) else (
                        pylint *.py --exit-zero > pylint-report.txt
                        flake8 *.py --format=json --output-file=flake8-report.json || exit /b 0
                    )
                """
            }
        }

        // ================= UNIT TESTS =================
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

        // ================= DEPLOYMENT =================
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
                    pylint-report.txt,
                    flake8-report.json,
                    gx/**,
                    great_expectations/**
                ''', allowEmptyArchive: true
            }
        }
    }

    // ================= POST ACTIONS =================
    post {
        always {
            junit testResults: 'test-results.xml', allowEmptyResults: true

            echo '🧹 Cleaning up workspace (Windows-safe)...'

            bat '''
                if exist venv\\Scripts\\deactivate.bat (
                    call venv\\Scripts\\deactivate.bat
                )
                taskkill /F /IM python.exe /T >nul 2>&1 || exit /b 0
            '''

            // Prevent cleanup failure from failing the pipeline
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                cleanWs(
                    deleteDirs: true,
                    notFailBuild: true,
                    retryCount: 5,
                    retryDelay: 5
                )
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
