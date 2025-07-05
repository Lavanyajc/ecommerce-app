
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![MongoDB](https://img.shields.io/badge/database-mongodb-brightgreen)
![Render](https://img.shields.io/badge/deployed%20on-Render-purple)


```
+------------+            +--------------+            +------------+
|  Frontend  |──fetch──▶︎ |   Backend    |──query──▶︎ |  MongoDB   |
| (NGINX)    |            | (Flask API)  |            | (Database) |
+------------+            +--------------+            +------------+
   port 8080                port 5000                   port 27017


```
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

## 🗂️ Project Structure

```

ecommerce-app/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── index.html
│   ├── assets/
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md

````

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

### ✅ Frontend (Optional ECR or Direct Compose)

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

## 📜 License

This project is licensed under the MIT License.

```

---

 
 


