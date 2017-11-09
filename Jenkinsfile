#!/usr/bin/env groovy

pipeline {
    agent { docker 'python:2.7.10' }

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
			  SAUCE_ACCESS = credentials('sauce-lab-dev')
    }

    stages {
        stage('build') {
            steps {
                sh 'make build'
            }
				}
        stage('build-docker') {
            steps {
                sh 'make build-docker'
            }
				}
        stage('test') {
            steps {
                sh 'make test'
                junit 'build/reports/**/*.xml'
            }
        }
    }

   post {
        always {
            echo 'This will always run'
            archive 'build/libs/**/*.jar'
            deleteDir() /* clean up our workspace */
        }
        failure {
            echo 'This will run only if failed'
            mail to: 'jheron@gmail.com',
            subject: "Failed feflask Pipeline: ${currentBuild.fullDisplayName}",
            body: "Something is wrong with ${env.BUILD_URL}"
        }
    }

}
