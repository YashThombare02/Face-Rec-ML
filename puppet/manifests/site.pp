# ===============================
# Variables (Windows)
# ===============================
$project_root = 'C:/face_recognition'
$python_path  = 'C:/Users/ythom/AppData/Local/Programs/Python/Python310/python.exe'
$pip_path     = 'C:/Users/ythom/AppData/Local/Programs/Python/Python310/Scripts/pip.exe'
$source_repo  = 'C:/Users/ythom/OneDrive/Desktop/face_recognition-main'

# ===============================
# Create Project Directory
# ===============================
file { $project_root:
  ensure => directory,
}

# ===============================
# Copy Project Files (Optimized)
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
