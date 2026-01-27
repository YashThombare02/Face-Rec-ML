pipeline {
    agent any

    environment {
        PROJECT_NAME = 'face_recognition'
        PYTHON_HOME  = 'C:/Users/ythom/AppData/Local/Programs/Python/Python39/python.exe'
        VENV_DIR     = 'venv'
        PUPPET_HOME  = 'C:/Program Files/Puppet Labs/Puppet/bin/puppet.bat'
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
                    "${PUPPET_HOME}" --version
                    "${PUPPET_HOME}" parser validate puppet\\manifests\\site.pp
                """
            }
        }

        // ---------------- PYTHON SETUP ----------------
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat """
                    "${PYTHON_HOME}" -m venv ${VENV_DIR}
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                """
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    pip install -r requirements.txt
                """
            }
        }

        // ---------------- GENERATE IMAGE METADATA ----------------
        stage('Generate Image Metadata') {
            steps {
                echo 'Generating image metadata...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python generate_image_metadata.py
                """
            }
        }

        // ---------------- GREAT EXPECTATIONS ----------------
        stage('Data Quality Validation') {
            steps {
                echo 'Running Great Expectations validation...'
                bat """
                    call ${VENV_DIR}\\Scripts\\activate.bat
                    python run_validation.py
                """
            }
        }

        // ---------------- ARCHIVE ----------------
        stage('Archive Artifacts') {
            steps {
                echo 'Archiving reports...'
                archiveArtifacts artifacts: '''
                    image_metadata.csv,
                    great_expectations/**,
                    *.log
                ''', allowEmptyArchive: true

                publishHTML([
                    allowMissing: true,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'great_expectations/uncommitted/data_docs',
                    reportFiles: 'index.html',
                    reportName: 'Data Quality Report'
                ])
            }
        }
    }

    post {
        always {
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
