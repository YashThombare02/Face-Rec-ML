# Puppet manifest for Face Recognition project

file { 'C:/FaceRecProject':
  ensure => directory,
}

file { 'C:/FaceRecProject/README.txt':
  ensure  => file,
  content => 'This project is managed by Puppet.',
}
