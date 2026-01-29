# ===============================
# Variables (Windows)
# ===============================
$project_root = 'C:/face_recognition'
$python_path  = 'C:/Users/ythom/AppData/Local/Programs/Python/Python310/python.exe'
$pip_path     = 'C:/Users/ythom/AppData/Local/Programs/Python/Python310/Scripts/pip.exe'
$source_repo  = 'C:/Users/ythom/OneDrive/Desktop/face_recognition-main'
$powershell   = 'C:/Windows/System32/WindowsPowerShell/v1.0/powershell.exe'

# ===============================
# Create Project Directory
# ===============================
file { $project_root:
  ensure => directory,
}

# ===============================
# Backup Existing Deployment
# ===============================
file { 'C:/face_recognition_backup':
  ensure => directory,
}

exec { 'backup-old-deployment':
  command => "\"${powershell}\" -Command \"if (Test-Path 'C:/face_recognition/app') { Copy-Item 'C:/face_recognition/app' 'C:/face_recognition_backup' -Recurse -Force }\"",
  require => File['C:/face_recognition_backup'],
}

# ===============================
# Copy Project Files
# ===============================
file { "${project_root}/app":
  ensure  => directory,
  source  => $source_repo,
  recurse => true,
  ignore  => [
    '.git',
    'venv',
    '__pycache__',
    '*.pyc',
    'data',
    'model'
  ],
  require => Exec['backup-old-deployment'],
}

# ===============================
# Version Tagging
# ===============================
file { 'C:/face_recognition/version.txt':
  ensure  => file,
  source  => "${project_root}/app/version.txt",
}

# ===============================
# Deployment Logs
# ===============================
file { 'C:/face_recognition/deploy.log':
  ensure => file,
}

exec { 'log-deployment':
  command => "\"${powershell}\" -Command \"Add-Content 'C:/face_recognition/deploy.log' ('Deployed at ' + (Get-Date))\"",
  require => File['C:/face_recognition/deploy.log'],
}

# ===============================
# Install Python Dependencies
# ===============================
exec { 'install-requirements':
  command => "\"${pip_path}\" install -r ${project_root}/app/requirements.txt",
  require => File["${project_root}/app"],
}

# ===============================
# Run Unit Tests
# ===============================
exec { 'run-tests':
  command => "\"${python_path}\" -m pytest ${project_root}/app/tests",
  require => Exec['install-requirements'],
}

# ===============================
# Run Great Expectations
# ===============================
exec { 'run-ge':
  command => "\"${python_path}\" ${project_root}/app/run_ge_checkpoint.py",
  require => Exec['run-tests'],
}

# ===============================
# Health Check
# ===============================
exec { 'health-check':
  command => "\"${python_path}\" ${project_root}/app/health_check.py",
  require => Exec['run-ge'],
}

# ===============================
# Start Deployment Dashboard
# ===============================
exec { 'start-dashboard':
  command => "\"${powershell}\" -Command \"Start-Process '${python_path}' '${project_root}/app/dashboard.py'\"",
  require => Exec['health-check'],
}
