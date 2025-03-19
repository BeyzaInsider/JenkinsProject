pipeline {
    agent any
    environment {
        PYTHONUNBUFFERED = '1'  // Canlı test çıktısı için
    }
    stages {
        stage('Clone Repository') {
            steps {
                git credentialsId: 'github-token', url: 'https://github.com/BeyzaInsider/JenkinsProject.git', branch: 'main'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Run API Tests') {
            steps {
                sh 'pytest --alluredir=allure-results'
            }
        }
        stage('Generate Allure Report') {
            steps {
                sh 'allure generate allure-results -o allure-report --clean'
            }
        }
    }
    post {
        always {
            allure includeProperties: false, jdk: '', reportBuildPolicy: 'ALWAYS', results: [[path: 'allure-results']]
        }
    }
}