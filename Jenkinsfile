pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('install requirements') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    stage('test') {
      steps {
        sh 'python3 -m unittest'
      }   
    }
    stage(''){
      
    }
  }
}