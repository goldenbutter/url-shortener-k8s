# URL Shortener (FastAPI + Docker + Kubernetes)

A lightweight, production‑ready **URL Shortener** service built with **FastAPI**, designed to run locally, in **Docker**, and in **Kubernetes**.  
It provides a simple API to shorten URLs, store them (in‑memory or Redis), and redirect users using short codes.

---

## 1. Project Overview

This project implements a minimal yet scalable **URL Shortener API**.  
It supports:

- Generating short codes for long URLs  
- Redirecting users to the original URL  
- Health monitoring  
- In‑memory storage for local development  
- **Redis** storage for **Docker/Kubernetes** environments  

The service is fully containerized and includes Kubernetes manifests for deployment.

---

## 2. Features

- 🚀 FastAPI backend  
- 🔗 URL shortening  
- ↪️ Redirect support  
- ❤️ Health check endpoint  
- 🧠 Hybrid storage system  
  - **In‑memory mode** (local development)  
  - **Redis mode** (Docker/K8s)  
- 🐳 Docker‑ready  
- ☸️ Kubernetes manifests included  

---

## 3. Architecture Overview

### **Local (In‑Memory Mode)**

```
Client → FastAPI Backend → In‑Memory Storage
```

```
                 ┌──────────────────────────┐
                 │        Client App        │
                 │  (Browser / API Client)  │
                 └─────────────┬────────────┘
                               │ HTTP
                               ▼
                 ┌──────────────────────────┐
                 │      FastAPI Backend     │
                 │  (Uvicorn, Python 3.12)  │
                 └─────────────┬────────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │     In‑Memory Storage    │
                 │   (Python dictionary)    │
                 └──────────────────────────┘
```

### **Docker / Kubernetes (Redis Mode)**

```
Client → FastAPI Backend → Redis
```
```
                 ┌──────────────────────────┐
                 │        Client App        │
                 │  (Browser / API Client)  │
                 └─────────────┬────────────┘
                               │ HTTP
                               ▼
                 ┌──────────────────────────┐
                 │   FastAPI Backend Pod    │
                 │   (Docker + Uvicorn)     │
                 └─────────────┬────────────┘
                               │
                               │ Redis Protocol (TCP 6379)
                               ▼
                 ┌──────────────────────────┐
                 │        Redis Pod         │
                 │   (Key‑Value Storage)    │
                 └─────────────┬────────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │   Persistent Volume      │
                 │ (Optional for durability)│
                 └──────────────────────────┘
```

---

## 4. Tech Stack

- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **Redis** (optional)
- **Docker**
- **Kubernetes (k8s)**

---

## 5. Folder Structure

```
url-shortener-k8s/
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── storage.py
│       ├── models.py
│       └── init.py
│
└── k8s/
├── namespace.yaml
├── backend/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   └── service.yaml
└── redis/
├── deployment.yaml
└── service.yaml
```

---

## 6. Local Development Setup

### **1. Create and activate virtual environment**

```bash
python -m venv venv
source venv/Scripts/activate   # Git Bash
```

### **2. Install dependencies**

```bash
pip install -r backend/requirements.txt
```
### **3. Ensure in‑memory mode is enabled**
Inside `backend/app/storage.py`:

```
USE_REDIS = False
```

### **4. Run the backend**
From project root:

```
uvicorn backend.app.main:app --reload
```

### **5. Test endpoints**
Health check → `GET /health`

Shorten URL → `POST /shorten`

Redirect → `GET /{short_code}`

## 7-A. Running with Docker
### **1. Build the Docker image**
From inside the `backend` folder:
```bash
docker build -t url-shortener-backend .
```
### **2. Run the container**
```bash
docker run -p 8000:8000 url-shortener-backend
```
### **3. Test the service**
```
http://localhost:8000/health
```

---


##  Screenshots

- **backend testing** - redirect

<img width="700" height="450" alt="backend-port-8000" src="assets\test-localhost-8000.png" />

- **backend testing** - health check

<img width="350" height="200" alt="backend-port-8000" src="assets\test-localhost-8000-health.png" />

---

## 7‑B. Running with Docker (Redis Mode)

This mode enables Redis‑backed storage for short URLs.  
Use this when running the backend in Docker or Kubernetes.

---

### 1. Start Redis in Docker

Run Redis locally using Docker:

```bash
docker run -p 6379:6379 redis:alpine
```

This starts Redis on:

- Host: localhost

- Port: 6379

### 2. Enable Redis mode in the backend
Inside `backend/app/storage.py`, set:

```
USE_REDIS = True
```
### 3. Run the backend container with Redis environment variables
Because Redis is running on your host machine, and the backend runs inside Docker,
use host.docker.internal so the container can reach your host:
```
docker run -p 8000:8000 \
  -e REDIS_HOST=host.docker.internal \
  -e REDIS_PORT=6379 \
  url-shortener-backend
```
<img width="720" height="280" alt="reddis-port-8000" src="assets\docker-run-redis.png" />

### 4. Test the API
Shorten a URL:
```
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```
Expected response:
```
{
  "short_code": "LVNFz1",
  "short_url": "http://localhost:8000/LVNFz1"
}
```
<img width="937" height="180" alt="reddis-port-8000" src="assets\test-redirect-curl.png" />

Redirect:
Open in browser:
```
http://localhost:8000/LVNFz1
```
##  Screenshots

- **Redis-Docker testing** - redirect

<img width="700" height="450" alt="reddis-port-8000" src="assets\test-docker-redis-8000.png" />

