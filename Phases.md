# 🛒 JC E-Commerce Platform – Full Project Documentation

## 🚀 Overview

This project is a complete full-stack Dockerized e-commerce platform with CI/CD pipelines and AWS deployment.

### 🧱 Tech Stack

* **Frontend**: HTML (served via Nginx , GitHub Pages initially)
* **Backend**: Python Flask API
* **Database**: MongoDB (Dockerized)
* **Containerization**: Docker & Docker Compose
* **CI/CD**: GitHub Actions
* **Registry**: AWS ECR
* **Hosting**: AWS EC2
* **IAM**: OIDC-based GitHub role for CI, EC2 IAM role for pull access

---

## 📁 Project Structure

```
ecommerce-app/
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── assets/
│   │   ├── Luffy.gif
│   │   └── run.gif
│   └── Dockerfile
├── docker-compose.yml
```

---

## 📊 Architecture Workflow Diagram

```
User → EC2 Public IP
     → Nginx (Frontend) - port 8080
         → Flask API (Backend) - port 5000
             → MongoDB - Docker container
```

---

## 🔁 Development & Deployment Phases

### ✅ Phase 1: Local Development

1. **Setup Project Locally**

   ```bash
   git clone https://github.com/your/repo.git
   cd ecommerce-app
   ```

2. **Backend (`backend/app.py`)**

   * Flask API with `/products` route
   * Seeds MongoDB on container start

3. **Backend Dockerfile**

   ```Dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   CMD ["python", "app.py"]
   ```

4. **Frontend Dockerfile**

   ```Dockerfile
   FROM nginx:alpine
   COPY index.html /usr/share/nginx/html/
   COPY assets/ /usr/share/nginx/html/assets/
   ```

5. **Docker Compose (`docker-compose.yml`)**

   ```yaml
   version: '3.8'
   services:
     mongo:
       image: mongo:6.0
       ports:
         - "27017:27017"
       volumes:
         - mongo-data:/data/db

     backend:
       build: ./backend
       ports:
         - "5000:5000"
       environment:
         - MONGO_URI=mongodb://mongo:27017/ecommerce
       depends_on:
         - mongo

     frontend:
       build: ./frontend
       ports:
         - "8080:80"
       depends_on:
         - backend
       volumes:
         - ./frontend:/usr/share/nginx/html:ro

   volumes:
     mongo-data:
   ```

6. **Run Locally**

   ```bash
   docker-compose up --build
   ```

   Access:

   * Frontend: `localhost:8080`
   * Backend: `localhost:5000/products`

---

### ✅ Phase 2: CI/CD with GitHub Actions + ECR

1. **Set Secrets in GitHub Repo**:

   * `AWS_REGION`
   * `AWS_ROLE_ARN`
   * `ECR_REPOSITORY`
   * `ECR_REPOSITORY_BACKEND`

2. **GitHub Workflows**

* `frontend.yml`

  ```yaml
  IMAGE_URI=${{ steps.login-ecr.outputs.registry }}/${{ secrets.ECR_REPOSITORY }}:latest
  ```

* `backend.yml`

  ```yaml
  IMAGE_URI=${{ steps.login-ecr.outputs.registry }}/${{ secrets.ECR_REPOSITORY_BACKEND }}:latest
  ```

3. **CI Workflow Actions**

   * `checkout@v3`
   * `configure-aws-credentials@v2`
   * `amazon-ecr-login@v1`
   * `docker build`, `docker push`

4. **Result**:

   * Both frontend and backend images pushed to AWS ECR

---

### ✅ Phase 3: Deploy on AWS EC2

1. **Launch EC2 Instance**

   * Open ports: `22`, `5000`, `8080`
   * Attach IAM role with `AmazonEC2ContainerRegistryReadOnly`

2. **Install Docker & Docker Compose**

   ```bash
   sudo yum install docker -y
   sudo systemctl enable docker
   sudo systemctl start docker

   mkdir -p ~/.docker/cli-plugins/
   curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 \
     -o ~/.docker/cli-plugins/docker-compose
   chmod +x ~/.docker/cli-plugins/docker-compose
   ```

3. **Clone Repo & Pull Images**

   ```bash
   git clone https://github.com/your/repo.git
   cd ecommerce-app

   aws ecr get-login-password --region ap-south-1 | \
     docker login --username AWS --password-stdin <aws_account>.dkr.ecr.ap-south-1.amazonaws.com

   docker pull <repo>/frontend-ecommerce:latest
   docker pull <repo>/backend-ecommerce:latest
   ```

4. **Run With Docker Compose**

   ```bash
   docker-compose up -d --build
   ```

5. **Test**

   * Frontend: `http://<EC2_PUBLIC_IP>:8080`
   * API: `http://<EC2_PUBLIC_IP>:5000/products`

---

## 🐞 Common Errors & Fixes

| ❌ Issue                  | ✅ Fix                                           |
| ------------------------ | ----------------------------------------------- |
| Port 5000 not accessible | Check security group, use `0.0.0.0` binding     |
| MongoDB not seeding      | Use `depends_on` and restart backend            |
| Docker Compose not found | Install manually under `~/.docker/cli-plugins/` |
| Wrong `COPY assets/`     | Typo in folder name (fixed to `assets`)         |

---

## 🧠 DevOps Concepts Applied

* ✅ CI/CD with GitHub Actions
* ✅ Push Docker image to AWS ECR
* ✅ IAM Role-based secure deployments (OIDC + EC2 role)
* ✅ Docker Compose multi-service architecture
* ✅ MongoDB container volume persistence

---

## 🎉 Final Output

* 🚀 E-commerce website running on EC2
* ✅ Dockerized, scalable microservice architecture
* 🧪 Full tested with `curl`, browser, and Docker logs

---

