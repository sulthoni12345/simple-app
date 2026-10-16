pipeline {
    agent any

    environment {
        IMAGE_NAME = 'sulthoniaja/simple-app'
        CONTAINER  = 'simple-app-deploy'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%BUILD_NUMBER% -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Push Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    bat '''
                    echo %DOCKERHUB_TOKEN%| docker login -u %DOCKERHUB_USER% --password-stdin
                    if errorlevel 1 exit /b 1
                    docker push %IMAGE_NAME%:%BUILD_NUMBER%
                    if errorlevel 1 exit /b 1
                    docker push %IMAGE_NAME%:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                bat 'docker rm -f %CONTAINER% || exit /b 0'
                withCredentials([string(credentialsId: 'db-password', variable: 'DB_PASS')]) {
                    bat 'docker run -d --name %CONTAINER% -p 5001:5000 -e DB_HOST=host.docker.internal -e DB_USER=app_user -e DB_NAME=praktikum_db -e "DB_PASSWORD=%DB_PASS%" %IMAGE_NAME%:latest'
                }
            }
        }

        stage('Verifikasi') {
            steps {
                sleep 5
                bat 'curl -s http://127.0.0.1:5001/db | findstr terhubung'
            }
        }
    }

    post {
        always {
            bat 'docker logout || exit /b 0'
            echo 'Selesai build'
        }
    }
}
