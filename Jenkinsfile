pipeline {  
  stages {
    stage('stop service'){
        sh "docker-compose -f /var/lib/jenkins/docker/rulesEngineApp.yml stop"
    }
    stage('Docker build'){
      sh 'docker image build -t shaffiro-rules-engine .'
    }
    stage('Start service'){
      sh 'docker-compose -f /var/lib/jenkins/docker/rulesEngineApp.yml up -d'
    }
  }
}