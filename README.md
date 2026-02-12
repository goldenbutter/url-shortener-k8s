# URL Shortener (FastAPI + Docker + Kubernetes)

A lightweight, production‑ready **URL Shortener** service built with **FastAPI**, designed to run locally, in **Docker**, and in **Kubernetes**.  
It provides a simple API to shorten URLs, store them (in‑memory or Redis), and redirect users using short codes.



## 1. Project Overview

This project implements a minimal yet scalable **URL Shortener API**.  
It supports:

- Generating short codes for long URLs  
- Redirecting users to the original URL  
- Health monitoring  
- In‑memory storage for local development  
- **Redis** storage for **Docker/Kubernetes** environments  

The service is fully containerized and includes Kubernetes manifests for deployment.



## 2. Features

- FastAPI backend  
- URL shortening  
- Redirect support  
- Health check endpoint  
- Hybrid storage system  
  - **In‑memory mode** (local development)  
  - **Redis mode** (Docker/K8s)  
- Docker‑ready  
- Kubernetes manifests included  



## 3. Architecture Overview

### A. *Local (In‑Memory Mode)*

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

### B. *Docker / Kubernetes (Redis Mode)*

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



## 4. Tech Stack

- **Python 3.12**
- **FastAPI**
- **Uvicorn**
- **Redis** (optional)
- **Docker**
- **Kubernetes (k8s)**



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



## 6. Development Setup (Local PC)

### A. *Create and activate virtual environment*

```bash
python -m venv venv
source venv/Scripts/activate
```

### B. *Install dependencies*

```bash
pip install -r backend/requirements.txt
```
### C. *Ensure in‑memory mode is enabled*
Inside `backend/app/storage.py`:

```
USE_REDIS = False
```

### D. *Run the backend*
From project root:

```bash
uvicorn backend.app.main:app --reload
```

### E. *Test endpoints*
Health check → `GET /health`

Shorten URL → `POST /shorten`

Redirect → `GET /{short_code}`

## 7.A. Running with Docker (In-memory)

### *a. Build the Docker image*
From inside the `backend` folder:
```bash
docker build -t url-shortener-backend .
```

### *b. Run the container*
```bash
docker run -p 8000:8000 url-shortener-backend
```

### *c. Test the service*
```h
http://localhost:8000/health
```

### *d. Test the API*
**Shorten a URL:**

```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```
**Expected response:**

```json
{
  "short_code": "LVNFz1",
  "short_url": "http://localhost:8000/LVNFz1"
}
```


- **backend testing** - curl

<img width="720" height="280" alt="reddis-port-8000" src="assets\docker-run-redis.png" />

- **backend testing** - redirect

<img width="700" height="450" alt="reddis-port-8000" src="assets\test-docker-redis-8000.png" />

- **backend testing** - health check

<img width="350" height="200" alt="backend-port-8000" src="assets\test-localhost-8000-health.png" />


## 7.B. Running with Docker Compose (Backend + Redis)

**Docker Compose allows you to run the entire stack (FastAPI backend + Redis) with a single command.** <br>
**This is the recommended way to run the project locally in Redis mode.**



### *a. docker-compose.yml*

The project includes a `docker-compose.yml` file that defines:

- A **Redis** service  
- A **Backend** service built from your Dockerfile  
- A shared Docker network  
- Environment variables for Redis connectivity  
- A persistent Redis volume  


### *b. Enable Redis mode in the backend*
Inside `backend/app/storage.py`, set:

```
USE_REDIS = True
```

### *c. Start the container*

 - **From the project root:**

```bash
docker compose up --build
```

 - **This starts Redis on:**

- Build the backend image
- Start Redis
- Start the backend
- Connect both services inside the same Docker network


### *d. Test the API*

**Shorten a URL:**

```bash
curl -X POST http://localhost:8000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```
**Expected response:**

```json
{
  "short_code": "mJj1SK",
  "short_url": "http://localhost:8000/mJj1SK"
}
```

<img width="899" height="127" alt="reddis-port-8000" src="assets\test-redirect-curl-redis.png" />

**Redirect:**
*Open in browser:*
```h
http://localhost:8000/mJj1SK
```

- **Redis-Docker testing** - redirect

<img width="730" height="650" alt="backend-port-8000" src="assets\test-localhost-8000.png" />

### *e. Verify Redis storage*

 - **Open a Redis shell:**

```bash 
docker exec -it urlshort-redis redis-cli 
```

 - **List stored short codes:**

```bash 
keys short:* 
```
**Retrieve a URL:**

```bash 
get short:<short_code> 
```
<img width="900" height="175" alt="backend-port-8000" src="assets\verify-redis-storage.png" />

### *f. Stop the stack*

```bash 
docker compose down
 ```
 - **To remove Redis data as well:**

```bash 
docker compose down -v
 ```

## 8. Environment Variables

The backend uses a small set of environment variables to control storage behavior and Redis connectivity.

 - ### Required Variables

| Variable       | Description                                      | Example            |
|----------------|--------------------------------------------------|--------------------|
| `USE_REDIS`    | Enables Redis mode (`true` or `false`)           | `true`             |
| `REDIS_HOST`   | Redis hostname or service name                   | `redis`            |
| `REDIS_PORT`   | Redis port number                                | `6379`             |

 - ### Optional Variables

| Variable           | Description                                | Example            |
|--------------------|--------------------------------------------|--------------------|
| `REDIS_PASSWORD`   | Password for secured Redis instances        | `mypassword123`    |

 - ### How They Are Used

   - When `USE_REDIS=false` → the app uses **in‑memory storage** (Python dictionary)
   - When `USE_REDIS=true` → the app uses **Redis** for persistent storage

These variables are set automatically in `docker-compose.yml`, but you can override them manually if needed.



## 9. API Endpoints

The backend exposes three main endpoints.


### *A. Health Check*

 **GET /health**

Returns a simple status message used by Docker/Kubernetes.

 **Response:**

```json
{ "status": "ok" }
```

### *B. Shorten a URL*

 - **POST /shorten**

**Accepts a JSON body:**

```json
{
  "url": "https://example.com"
}
```

**Response:**

```json
{
  "short_code": "abc123",
  "short_url": "http://localhost:8000/abc123"
}
```

### *C. Redirect to Original URL*

**GET /{short_code}**

*Example:*

```
GET /abc123
```

**Behavior:**
- If the short code exists → redirects (HTTP 307) to the original URL
- If not found → returns `404 Not Found`




## 10. Redis vs In‑Memory Mode

The application supports two storage backends:



### 🧠 In‑Memory Mode (Default for Local Development)

- Enabled when `USE_REDIS=false`
- Uses a simple Python dictionary
- Fast and easy for local testing
- Data is lost when the server restarts

---

### 🗄️ Redis Mode (Recommended for Docker/Kubernetes)

- Enabled when `USE_REDIS=true`
- Stores URLs in Redis using keys like:
- Data persists across restarts
- Works seamlessly with Docker Compose and Kubernetes
- Required for scaling horizontally (multiple backend replicas)

---

### When to Use What?

| Environment     | Recommended Mode |
|-----------------|------------------|
| Local testing   | In‑memory        |
| Docker Compose  | Redis            |
| Kubernetes      | Redis            |
| Production      | Redis            |


## 11. Kubernetes Deployment Guide

This project is designed to run cleanly inside Kubernetes.  
Below is a high‑level guide for deploying the backend and Redis.



### A. Create a Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

### B. Redis deployment and service

```bash
kubectl apply -f k8s/redis/deployment.yaml
kubectl apply -f k8s/redis/service.yaml
```

### C. Backend ConfigMap & deployment

```bash
kubectl apply -f k8s/backend/configmap.yaml
kubectl apply -f k8s/backend/deployment.yaml
```

### D. Backend service (NodePort)

```bash
kubectl apply -f k8s/backend/service.yaml
```

### E. Verify deployment & services:

```bash
kubectl get pods -n url-shortener
kubectl get svc -n url-shortener
```

<img width="887" height="147" alt="backend-port-8000" src="assets\kubectl-get-pods.png" />


### F. Test the API inside Kubernetes
Create a short URL:

```bash
curl -X POST http://localhost:30080/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```
Output : 

```json
{
  "short_code": "gUkvW6",
  "short_url": "http://localhost:30080/gUkvW6"
}
```

<img width="883" height="124" alt="backend-port-8000" src="assets\k8s-test-curl.png" />


### G. Test redirect:

Open in a browser:

```h
http://localhost:30080/gUkvW6
```

<img width="941" height="659" alt="backend-port-8000" src="assets\k8s-test-redirect.png" />

###  H. Inspecting Redis data (optional)

```bash
kubectl get pods -n url-shortener
kubectl exec -it <redis-pod-name> -n url-shortener -- sh
```

<img width="893" height="141" alt="backend-port-8000" src="assets\k8s-redis-storage-check.png" />

###  I. Cleanup

```bash
kubectl delete namespace url-shortener
```


## 12. Contributing Guide

We welcome contributions! Please read the full contribution guidelines before opening issues or pull requests.

**Read the full Contributing Guide:**  
[Contribute to this project](assets/contribute.md)
