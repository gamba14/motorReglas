pipeline {
  agent { docker { image 'python:3.7.2' } }
  stages {
    stage('stop service'){
        sh "docker-compose -f /var/lib/jenkins/docker/rulesEngineApp.yml stop"
    }

    stage('install requirements') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }
    // stage('test') {
    //   steps {
    //     sh 'python3 -m unittest'
    //   }   
    // }
    stage('Docker build'){
      sh 'docker image build -t shaffiro-rules-engine .'
    }

    stage('Start service'){
      sh 'docker-compose -f /var/lib/jenkins/docker/rulesEngineApp.yml up -d'
    }
  }
}