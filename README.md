# 🚀 Overview
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![MongoDB](https://img.shields.io/badge/database-mongodb-brightgreen)


This is a full-stack E-Commerce platform built and deployed using modern DevOps tools and best practices. It features a frontend built with HTML, a Flask-based backend, MongoDB for product data, and Docker containers orchestrated via Docker Compose. The application is deployed to AWS EC2 with CI/CD pipelines pushing Docker images to AWS ECR.



🛒 E-commerce Web App

This is a simple e-commerce application built using:

- 🐍 Flask (Backend)
- 🌐 HTML/CSS (Frontend)
- 🍃 MongoDB (Database)
- 🐳 Docker & Docker Compose (Containerization)
- ☁️ AWS EC2 & ECR (Cloud Hosting)

---

## 🚀 Features

- View a product list from a MongoDB database
- Backend API served over Flask
- Frontend served using Nginx
- Dockerized and deployed to AWS EC2
- MongoDB runs as a Docker service
- Images stored and pulled from Amazon ECR

---

#
---


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
│   ├── Dockerfile
│   └── assets/
│       ├── Luffy.gif
│       └── run.gif
├── docker-compose.yml
```

---

## ⚙️ Features

* 📦 Product catalog pulled from MongoDB
* 📡 REST API served from Flask
* 🌐 Frontend consuming API with `fetch`
* 🔒 Secure OIDC GitHub Actions CI/CD for both frontend & backend
* ☁️ Deployment-ready with Docker Compose on EC2

---

```
+------------+            +--------------+            +------------+
|  Frontend  |──fetch──▶︎ |   Backend    |──query──▶︎ |  MongoDB   |
| (NGINX)    |            | (Flask API)  |            | (Database) |
+------------+            +--------------+            +------------+
   port 8080                port 5000                   port 27017


```

## 🛠️ Local Development

1. **Clone Repo & Navigate**

```bash
git clone https://github.com/Lavanyajc/ecommerce-app.git
cd ecommerce-app
```

2. **Run Docker Compose Locally**

```bash
docker compose up --build
```

3. **Access**

* Frontend: `http://localhost:8080`
* Backend API: `http://localhost:5000/products`

---

## 🚚 CI/CD Process (ECR + EC2)

### Frontend & Backend Workflows

* Created separate `.github/workflows/frontend.yml` and `backend.yml`
* Used secrets:

  * `AWS_ROLE_ARN`, `AWS_REGION`, `ECR_REPOSITORY`, `ECR_REPOSITORY_BACKEND`
* OIDC-based GitHub role + EC2 instance IAM role
* Docker image is built, tagged, and pushed to respective ECR repo

### EC2 Deployment

1. **Launched EC2 instance**, attached ECR read-role
2. **Opened ports 5000, 8080, 22**
3. **SSH into EC2 & Installed Docker + Compose**
4. **Pulled Repo & Ran Compose**

```bash
ssh -i my-key.pem ec2-user@<EC2_PUBLIC_IP>
sudo yum install docker -y
sudo systemctl start docker
# Compose install:
sudo curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64" \
  -o /usr/local/lib/docker/cli-plugins/docker-compose
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

git clone https://github.com/Lavanyajc/ecommerce-app.git
cd ecommerce-app
docker compose up --build -d
```

5. **Visit**:

* Frontend: `http://<EC2_PUBLIC_IP>:8080`
* Backend: `http://<EC2_PUBLIC_IP>:5000/products`

---

## 🧠 Mistakes Fixed

| ❌ Issue                              | ✅ Fix                              |
| ------------------------------------ | ---------------------------------- |
| Wrong asset folder name              | Changed `assests` → `assets`       |
| Backend not reachable                | Used `0.0.0.0` in `app.run()`      |
| Docker Compose not installed         | Installed properly with CLI plugin |
| Confused ports / No browser response | Used `curl`, opened correct ports  |

---

---

## 📦 Future Improvements

* Add terrafoem
* Add checkout/cart functionality
* Deploy backend to ECS or Fargate
* Add monitoring (Prometheus + Grafana)

---

## 🏁 Final Outcome

The E-Commerce application is:

* Dockerized (Frontend, Backend, MongoDB)
* CI/CD integrated via GitHub Actions
* Deployed & running on AWS EC2
* Fully functional with product listing page and backend API

---


## 🐳 Docker Compose Setup (Local)

```bash
# 1. Clone the repo
git clone https://github.com/Lavanyajc/ecommerce-app.git
cd ecommerce-app

# 2. Start services
docker compose up --build -d

# 3. Access app
Backend API: http://localhost:5000/products  
Frontend UI: http://localhost:8080
````

---

## ☁️ AWS Deployment (EC2 + ECR)

### ✅ Backend

1. **Build & Push Backend to ECR**

```bash
cd backend
docker build -t ecommerce-backend .
docker tag ecommerce-backend:latest <your-ecr-url>/ecommerce-backend:latest
docker push <your-ecr-url>/ecommerce-backend:latest
```

2. **SSH into EC2 & Install Docker**

```bash
ssh -i your-key.pem ec2-user@<ec2-public-ip>

sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
```

3. **Pull Image from ECR**

```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <your-ecr-url>
docker pull <your-ecr-url>/ecommerce-backend:latest
```

4. **Run Backend**

```bash
docker run -d -p 5000:5000 <your-ecr-url>/ecommerce-backend:latest
```

### ✅ Frontend ( you can use simple gh-pages or you can do with ecr+ec2+docker)

You can use Docker Compose or ECR again:

```bash
cd ecommerce-app
docker compose up --build -d
```

---

## 🔐 Security Group Settings (EC2)

Ensure these ports are open:

* TCP 22 (SSH)
* TCP 5000 (Backend API)
* TCP 8080 (Frontend)

---

## 📦 API Endpoint

```
GET /products
→ Returns list of products from MongoDB
```

Sample response:

```json
[
  {"name": "T-shirt"},
  {"name": "Saree"},
  {"name": "Laptop"},
  {"name": "Sofa"},
  {"name": "Cricket Bat"},
  {"name": "Novel"}
]
```

---

## 🧪 Test Locally or Remotely

```bash
# Local
curl http://localhost:5000/products

# EC2
curl http://<ec2-public-ip>:5000/products
```

---

## 🙌 Author

Lavanya Jc — [GitHub](https://github.com/Lavanyajc)

---


---

 
 


