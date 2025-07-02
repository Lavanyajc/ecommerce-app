

# 🛍️ E-commerce Backend API

![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![MongoDB](https://img.shields.io/badge/database-mongodb-brightgreen)
![Render](https://img.shields.io/badge/deployed%20on-Render-purple)

 ![License](https://img.shields.io/github/license/Lavanyajc/ecommerce-app.svg)
 ![GitHub last commit](https://img.shields.io/github/last-commit/Lavanyajc/ecommerce-app)
 ![Issues](https://img.shields.io/github/issues/Lavanyajc/ecommerce-app)

> A simple Dockerized Flask + MongoDB e-commerce backend API.

---

## 🚀 Live API

**Base URL**: [https://ecommerce-backend.com](http://localhost:5000/)  
Try it:
- `GET /` → Welcome message
- `GET /products` → List of sample products

---

## 🧱 Tech Stack

- Python 3.9
- Flask
- MongoDB
- Docker & Docker Compose
---

## 📁 Folder Structure

```

ecommerce-app/
│
├── docker-compose.yml
└── backend/
      ├── app.py
      ├── Dockerfile
      └── requirements.txt

```

## 🏁 Next Goals

* [ ] Add user authentication (JWT)
* [ ] Add MongoDB Atlas support
* [ ] Deploy frontend + reverse proxy with NGINX

```
+------------+            +--------------+            +------------+
|  Frontend  |──fetch──▶︎ |   Backend    |──query──▶︎ |  MongoDB   |
| (NGINX)    |            | (Flask API)  |            | (Database) |
+------------+            +--------------+            +------------+
   port 8080                port 5000                   port 27017

---


 
 


