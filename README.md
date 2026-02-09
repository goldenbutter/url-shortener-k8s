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

## 7-A. Running with Docker (In-memory)
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

##  Screenshots

- **backend testing** - curl

<img width="720" height="280" alt="reddis-port-8000" src="assets\docker-run-redis.png" />

- **backend testing** - redirect

<img width="700" height="450" alt="reddis-port-8000" src="assets\test-docker-redis-8000.png" />

- **backend testing** - health check

<img width="350" height="200" alt="backend-port-8000" src="assets\test-localhost-8000-health.png" />


---

## 7‑B. Running with Docker Compose (Backend + Redis)

Docker Compose allows you to run the entire stack (FastAPI backend + Redis) with a single command.  
This is the recommended way to run the project locally in Redis mode.

---

### 1. docker-compose.yml

The project includes a `docker-compose.yml` file that defines:

- A **Redis** service  
- A **Backend** service built from your Dockerfile  
- A shared Docker network  
- Environment variables for Redis connectivity  
- A persistent Redis volume  

---

### 2. Enable Redis mode in the backend
Inside `backend/app/storage.py`, set:

```
USE_REDIS = True
```

### 3. Start the container

From the project root:

```bash
docker compose up --build
```

This starts Redis on:

- Build the backend image
- Start Redis
- Start the backend
- Connect both services inside the same Docker network

Backend will be available at:





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
  "short_code": "mJj1SK",
  "short_url": "http://localhost:8000/mJj1SK"
}
```
<img width="899" height="127" alt="reddis-port-8000" src="assets\test-redirect-curl-redis.png" />

Redirect:
Open in browser:
```
http://localhost:8000/mJj1SK
```
##  Screenshots

- **Redis-Docker testing** - redirect

<img width="730" height="650" alt="backend-port-8000" src="assets\test-localhost-8000.png" />

### 5. Verify Redis storage

Open a Redis shell:
```bash 
docker exec -it urlshort-redis redis-cli 
```
List stored short codes:
```bash 
keys short:* 
```
Retrieve a URL:
```bash 
get short:<short_code> 
```
<img width="900" height="175" alt="backend-port-8000" src="assets\verify-redis-storage.png" />

### 6. Stop the stack

```bash 
docker compose down
 ```
To remove Redis data as well:

```bash 
docker compose down -v
 ```


## 8. Contributing & Future Improvements

This project is designed to be simple, modular, and easy to extend.  
If you want to contribute or improve the system in the future, here are some recommended areas:

---

### 🔧 1. Add New Features
- URL expiration (TTL) using Redis `EXPIRE`
- Click analytics (count redirects per short code)
- Custom short codes (user‑defined aliases)
- QR code generation for each short URL
- Admin dashboard for viewing stored URLs

---

### 🗄️ 2. Improve Storage Layer
- Add Redis authentication (`REDIS_PASSWORD`)
- Add Redis cluster support
- Add PostgreSQL or MongoDB as optional backends
- Add caching layer for frequently accessed URLs

---

### 🐳 3. Enhance Docker & Deployment
- Add Docker healthchecks for backend and Redis
- Add Docker Compose profiles (dev / prod)
- Add Kubernetes manifests (Deployments, Services, Ingress)
- Add Horizontal Pod Autoscaler (HPA)
- Add CI/CD pipeline (GitHub Actions)

---

### 🧪 4. Testing & Quality
- Add unit tests for storage layer
- Add integration tests for API endpoints
- Add load testing (k6 / Locust)
- Add linting (flake8, black, isort)

---

### 📚 5. Documentation
- Expand API documentation
- Add architecture diagram
- Add sequence diagram for request flow
- Add troubleshooting section

---

### 🤝 6. How to Contribute
1. Fork the repository  
2. Create a new branch  
3. Make your changes  
4. Submit a pull request  
5. Describe what you improved and why  

All contributions are welcome — from small fixes to major features.

## 9. Contribution Workflow

If you want to improve this project, please follow the workflow below.  
This helps keep development organized and ensures everyone works on clearly defined tasks.

---

### 📝 1. Create an Issue
Before starting any work:

1. Go to the **Issues** tab in the repository  
2. Create a new issue describing:
   - What you want to improve or fix  
   - Why it’s useful  
   - Any technical notes or ideas  

This helps avoid duplicate work and lets others discuss the idea.

---

### 👤 2. Assign the Issue to Yourself
Inside the issue page:

- Click **“Assign yourself”**  
- This signals to others that you are actively working on it  

If you cannot assign yourself (permissions), mention in the issue that you are taking it.

---

### 🍴 3. Fork the Repository
Click **“Fork”** at the top right of the repo.

This creates your own copy where you can safely:

- Add features  
- Fix bugs  
- Experiment  
- Make changes without affecting the main project  

---

### 🛠️ 4. Implement Your Changes in Your Fork
Inside your fork:

- Create a new branch  
- Make your changes  
- Test everything locally  
- Follow the project’s coding style and structure  

If your change affects deployment (Docker, Compose, Kubernetes), update the README as well with proper screenshots.

---

### 🔄 5. Submit a Pull Request (PR)
When your work is ready:

1. Go to your fork  
2. Click **“New Pull Request”**  
3. Select your branch → main repository’s `main` branch  
4. Add a clear description:
   - What you changed  
   - Why you changed it  
   - How to test it  

The maintainers will review your PR and merge it if everything looks good.

---

### 🤝 6. Collaboration Guidelines
- Keep PRs focused on one issue at a time  
- Write clean, maintainable code  
- Add comments where needed  
- Be respectful and constructive in discussions  
- Feel free to ask questions — collaboration is welcome  

---

Contributions of all sizes are appreciated — from small fixes to major features.