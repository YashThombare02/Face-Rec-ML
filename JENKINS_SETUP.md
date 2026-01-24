# Jenkins Pipeline Configuration

This project uses Jenkins for continuous integration and SonarQube for code quality analysis.

## Prerequisites

1. **Jenkins Installation**
   - Jenkins server up and running
   - Git plugin installed
   - SonarQube plugin installed
   - Cobertura plugin installed
   - HTML Publisher plugin installed

2. **SonarQube Installation**
   - SonarQube server running (default: http://localhost:9000)
   - Python plugin installed in SonarQube

3. **Python Environment**
   - Python 3.7+ installed on Jenkins agents
   - Git installed on Jenkins agents

## Jenkins Configuration

### 1. Configure SonarQube Server in Jenkins

1. Go to **Manage Jenkins** → **Configure System**
2. Find **SonarQube servers**
3. Add SonarQube server:
   - **Name**: `SonarQube`
   - **Server URL**: `http://sonarqube-host:9000`
   - **Server authentication token**: (create token in SonarQube)

### 2. Configure SonarQube Scanner in Jenkins

1. Go to **Manage Jenkins** → **Global Tool Configuration**
2. Find **SonarQube Scanner**
3. Add SonarQube Scanner:
   - **Name**: `SonarQube`
   - **Install from Maven Central**: Yes (auto-install)

### 3. Create Jenkins Pipeline Job

1. Create a new **Pipeline** job
2. Under **Pipeline** section, select **Pipeline script from SCM**
3. Configure Git repository:
   - **Repository URL**: `https://github.com/YOUR-USERNAME/face_recognition.git`
   - **Branch**: `*/main`
   - **Script Path**: `Jenkinsfile`

## Pipeline Stages

1. **Checkout** - Clone the repository
2. **Setup Environment** - Create Python virtual environment
3. **Install Dependencies** - Install required packages
4. **Linting** - Run pylint and flake8 checks
5. **Unit Tests** - Run pytest with coverage
6. **Code Quality Analysis** - SonarQube analysis
7. **Quality Gate** - Check SonarQube Quality Gate
8. **Archive Artifacts** - Store reports

## SonarQube Configuration

The `sonar-project.properties` file contains:
- Project key and name
- Python source exclusions (venv, model files, data files)
- Coverage report paths
- Test result paths

## Running the Pipeline

1. Push changes to GitHub
2. Jenkins will automatically trigger the pipeline
3. Monitor progress in Jenkins UI
4. View SonarQube results in the Quality Gate stage
5. Check test coverage reports in Jenkins artifacts

## Environment Variables Required

Set these in Jenkins credentials or Jenkins configuration:

- `SONAR_HOST_URL` - SonarQube server URL
- `SONAR_AUTH_TOKEN` - SonarQube authentication token

## Troubleshooting

**Pipeline fails on SonarQube step:**
- Verify SonarQube server is running
- Check authentication token is correct
- Ensure sonar-scanner is installed

**Coverage reports not generated:**
- Verify pytest-cov is installed
- Check pytest is finding tests
- Verify coverage.xml path matches in configuration

**Python virtual environment issues:**
- Ensure Python is installed on Jenkins agent
- Check Jenkins agent has write permissions to workspace

## Next Steps

1. Create a SonarQube project (if not auto-created)
2. Set Quality Gate thresholds in SonarQube
3. Add email notifications to post-build actions
4. Configure webhooks for GitHub integration
5. Set up branch analysis for pull requests
