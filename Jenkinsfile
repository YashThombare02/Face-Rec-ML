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
                bat """
                    "${PUPPET_BIN}" --version
                    if exist puppet\\manifests (
                        "${PUPPET_BIN}" parser validate puppet\\manifests\\*.pp
                    ) else (
                        echo No puppet manifests found - skipping validation
                    )
                """
            }
        }

        // ---------------- PYTHON SETUP ----------------
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
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

        // ---------------- DEPENDENCIES ----------------
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    pip install -r requirements.txt
                    pip install pytest pytest-cov pylint flake8 great_expectations pandas
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

                    echo -------- Workspace Files --------
                    dir
                    echo ---------------------------------
                """
            }
        }

        // ---------------- GREAT EXPECTATIONS ----------------
        stage('Data Quality Validation') {
            steps {
                echo 'Running Great Expectations validation...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python run_ge_checkpoint.py
                """
            }
        }

        // ---------------- LINTING (SAFE + FAST) ----------------
        stage('Linting') {
            steps {
                echo 'Running lint checks...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat

                    if exist src (
                        pylint src --ignore=venv --exit-zero > pylint-report.txt
                        flake8 src --exclude=venv,__pycache__ --format=json --output-file=flake8-report.json || exit /b 0
                    ) else (
                        echo No src folder found - running lint on python files only
                        pylint *.py --exit-zero > pylint-report.txt
                        flake8 *.py --format=json --output-file=flake8-report.json || exit /b 0
                    )
                """
            }
        }

        // ---------------- UNIT TESTS ----------------
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat

                    if exist tests (
                        pytest ^
                          --junitxml=test-results.xml
                    ) else (
                        echo No tests folder found - skipping tests
                        echo.> test-results.xml
                    )
                """
            }
        }

        // ---------------- ARCHIVE ----------------
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving reports...'
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

    post {
        always {
            junit testResults: 'test-results.xml', allowEmptyResults: true
            cleanWs()
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed — check logs.'
        }
    }
}
