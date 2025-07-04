
# 📘 Project Documentation: Frontend CI/CD for `ecommerce-app`

## ✅ Overview

This frontend is a **static HTML website** that supports **two different CI/CD approaches**:

1. **Static Hosting via GitHub Pages (CI/CD using GitHub Actions only)**
2. **Containerized Hosting via AWS ECR + EC2 (CI via GitHub Actions, CD via Docker on EC2)**

---

## 📁 Folder Structure

```
ecommerce-app/
├── .github/
│   └── workflows/
│       ├── frontend.yml           # GitHub Pages CI/CD workflow
│       └── frontend-ecr.yml       # Docker + AWS ECR + EC2 CI/CD workflow
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.yml             # Optional for orchestration
```

---

## ⚙️ Frontend Files Explanation

### `index.html`

* The main UI for the website (static HTML).

### `Dockerfile` (inside `/frontend`)

Used to containerize the frontend with a lightweight web server (Nginx):

```dockerfile
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY . /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### `nginx.conf`

Custom Nginx config to serve the static site:

```nginx
server {
  listen 80;

  location / {
    root /usr/share/nginx/html;
    index index.html;
    try_files $uri $uri/ =404;
  }
}
```

---

## 🚀 CI/CD Method 1: GitHub Pages (Static Hosting)

### ✅ Use Case:

* Simple deployment for static HTML, no Docker needed.

### 📄 `.github/workflows/frontend.yml`

```yaml
name: 🚀 Deploy Frontend to GitHub Pages

on:
  push:
    branches:
      - main

permissions:
  contents: write  # Needed to push to gh-pages

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout Code
        uses: actions/checkout@v3

      - name: 🚀 Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./frontend
```

### 📝 How It Works:

1. Triggered on every `push` to `main` branch.
2. Checks out code.
3. Deploys `/frontend` directory to `gh-pages` branch.
4. GitHub Pages hosts it publicly.

### 🌐 Result:

* Accessible at: `https://<your-username>.github.io/<repo-name>/`
* Or your custom domain (e.g., `luffyjc.xyz`)

---

## 🐳 CI/CD Method 2: Docker + AWS ECR + EC2

### ✅ Use Case:

* Deploy to a cloud server with full Docker control (custom servers, volumes, scalability, etc.)

### 📄 `.github/workflows/frontend-ecr.yml`

```yaml
name: 🚀 CI/CD: Build & Push Frontend to AWS ECR

on:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
      - name: 📥 Checkout code
        uses: actions/checkout@v3

      - name: 🪪 Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: 🐳 Log in to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: 🛠️ Build, Tag & Push Docker Image
        run: |
          IMAGE_URI=${{ steps.login-ecr.outputs.registry }}/${{ secrets.ECR_REPOSITORY }}:latest
          docker build -t $IMAGE_URI ./frontend
          docker push $IMAGE_URI
```

### 🔐 GitHub Secrets Required:

| Secret Name      | Description                                        |
| ---------------- | -------------------------------------------------- |
| `AWS_ROLE_ARN`   | IAM role ARN with OIDC and ECR permissions         |
| `AWS_REGION`     | AWS region (e.g., `ap-south-1`)                    |
| `ECR_REPOSITORY` | Name of your ECR repo (e.g., `frontend-ecommerce`) |

---

## ☁️ EC2 Deployment (Manual – Public Hosting)

### Prerequisite:

* EC2 instance with Docker installed.
* IAM role attached to EC2 with `AmazonEC2ContainerRegistryReadOnly` access.

### 🔨 Steps:

1. **SSH into EC2**

```bash
ssh -i your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

2. **Install Docker (if not present)**

```bash
sudo yum update -y
sudo yum install docker -y
sudo service docker start
sudo usermod -aG docker ec2-user
newgrp docker
```

3. **Log in to ECR**

```bash
aws ecr get-login-password --region ap-south-1 \
| docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com
```

4. **Pull the image**

```bash
docker pull <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/frontend-ecommerce:latest
```

5. **Run the container**

```bash
docker run -d -p 80:80 <ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/frontend-ecommerce:latest
```

6. **Access the frontend**

```bash
curl http://checkip.amazonaws.com
# Open the IP in browser
```

---

## ✅ Summary: Two CI/CD Options Compared

| Feature        | GitHub Pages   | Docker + ECR + EC2             |
| -------------- | -------------- | ------------------------------ |
| Hosting Type   | Static hosting | Containerized web server       |
| CI Tool        | GitHub Actions | GitHub Actions                 |
| CD Tool        | GitHub Pages   | EC2 manual + Docker            |
| Infra Cost     | Free           | Paid (EC2 instance)            |
| Flexibility    | Low            | High (scaling, custom configs) |
| Domain Support | Yes            | Yes                            |
| Public Access  | Yes            | Yes                            |

---

## 🧠 Additional Notes

* Dockerfile and `nginx.conf` are **used only in Docker-based deployment**.
* GitHub Pages setup does **not require Docker at all**.
* To avoid conflicts:

  * Delete or rename `frontend.yml` if using only EC2.
  * Use different branch triggers or file paths if both are used together.
* **OIDC** was used for secure, secretless access from GitHub to AWS.

---




## 🔐 Required IAM Roles for AWS-Based CI/CD (OIDC + EC2)

To securely and successfully implement CI/CD using **GitHub Actions + AWS ECR + EC2**, you **must configure two IAM roles**:

---

### 1. ✅ **OIDC Role (GitHub Actions → AWS)**

> **Purpose:** Allows GitHub Actions (CI) to **authenticate into AWS** and **push Docker images to ECR** without storing long-lived credentials.

#### Key Features:

* Configured using **OIDC (OpenID Connect)**.
* Uses `token.actions.githubusercontent.com` as the **identity provider**.
* Grants permissions like:

  * `ecr:GetAuthorizationToken`
  * `ecr:PutImage`
  * `ecr:UploadLayerPart`, etc.

#### Trust Policy (Example):

```json
{
  "Effect": "Allow",
  "Principal": {
    "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
  },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
    },
    "StringLike": {
      "token.actions.githubusercontent.com:sub": "repo:Lavanyajc/ecommerce-app:*"
    }
  }
}
```

---

### 2. ✅ **EC2 Instance Role (EC2 → ECR)**

> **Purpose:** Allows your EC2 instance (deployment server) to **pull Docker images from ECR** during the deployment phase.

#### Required Permission:

* Attach `AmazonEC2ContainerRegistryReadOnly` **managed policy**.
* Or create a custom policy that allows:

  * `ecr:GetDownloadUrlForLayer`
  * `ecr:BatchGetImage`
  * `ecr:GetAuthorizationToken`

---

### 🔁 Why Both Are Required?

| Role         | Used For                       | Who Uses It    | Purpose                          |
| ------------ | ------------------------------ | -------------- | -------------------------------- |
| OIDC Role    | CI/CD build & push to ECR      | GitHub Actions | Authenticate & push Docker image |
| EC2 IAM Role | Deployment by pulling from ECR | EC2 Instance   | Pull image and run it in Docker  |

---

> 🔑 Without both roles, the pipeline will break at some stage:

* Without **OIDC**, GitHub can’t push image to ECR.
* Without **EC2 IAM role**, your EC2 can't pull image from ECR.

---

