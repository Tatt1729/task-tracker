pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'tatt1729'
        IMAGE_NAME     = "${DOCKERHUB_USER}/task-tracker"
        IMAGE_TAG      = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$IMAGE_TAG -t $IMAGE_NAME:latest .'
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds',
                                                  usernameVariable: 'DH_USER',
                                                  passwordVariable: 'DH_PASS')]) {
                    sh '''
                        echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin
                        docker push $IMAGE_NAME:$IMAGE_TAG
                        docker push $IMAGE_NAME:latest
                    '''
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                sh '''
                    sed "s|IMAGE_PLACEHOLDER|$IMAGE_NAME:$IMAGE_TAG|" k8s/deployment.yaml | kubectl apply -f -
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/task-tracker --timeout=120s
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    kubectl get pods
                    kubectl get deployment task-tracker
                    kubectl get svc task-tracker-service
                    curl -s $(minikube ip):30007/health
                '''
            }
        }
    }
}