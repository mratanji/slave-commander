pipeline {
  agent any
  stages {
    stage('Pre-check') {
      steps {
        parallel(
          "Pre-check-AUTH": {
            sh 'echo hi'
            sh 'echo hi'
            
          },
          "Pre-check-WORKCENTER": {
            sh 'echo hi'
            sh 'echo hi'
            
          }
        )
      }
    }
    stage('Provision') {
      steps {
        parallel(
          "Provision-AUTH": {
            sh 'echo hi'
            sh 'echo hi'
            
          },
          "Provision-WORKCENTER": {
            sh 'echo hi'
            sh 'echo hi'
            
          }
        )
      }
    }
    stage('Label') {
      steps {
        sh 'echo hi'
      }
    }
  }
}
