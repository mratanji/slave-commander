pipeline {
  agent any
  stages {
    stage('Pre-check') {
      steps {
        parallel(
          "Pre-check-AUTH": {
            sh 'mipm install -p ansible-apd'
            sh 'ansible-playbook apd.yml -i hosts'
            
          },
          "Pre-check-WORKCENTER": {
            sh 'mipm install -p ansible-playbook'
            sh 'ansible-playbook apd.yml'
            
          }
        )
      }
    }
    stage('Provision') {
      steps {
        parallel(
          "Provision-AUTH": {
            sh 'mipm install -p ansible-playbook'
            sh 'ansible-playbook apd.yml -i hosts'
            
          },
          "Provision-WORKCENTER": {
            sh 'mipm install -p ansible-playbook'
            sh 'ansible-playbook apd.yml -i hosts'
            
          }
        )
      }
    }
    stage('Label') {
      steps {
        sh 'mipm label'
      }
    }
  }
}