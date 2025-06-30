# 🚀 FastAPI Hello World API - Google Cloud Run CI/CD

## 📌 Objective

- Build and test a simple Python FastAPI web API
- Lint and validate code quality with `pylint`
- Run unit tests using `pytest`
- Package it in a secure Docker image and scan with Docker scout for vulnerabilities
- Publish the image to Google Artifact Registry
- Deploy to Google Cloud Run (fully managed)
- Set up uptime check with Monitoring an logging
- Automate CI/CD pipeline using GitHub Actions on `main` branch push

---

## ✅ Step-by-Step Implementation Checklist

### 🧱 Step 1: Local Setup and Hello World API

- [x] Create Python virtual environment and activate it
- [x] Install FastAPI, Uvicorn, Httpx

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn httpx
````

* [x] Create a simple API in `app/main.py`

```
* [x] Run API locally

```bash
uvicorn app.main:app --reload
```

Visit: `http://localhost:8000/`

![alt text](docs/images/local2.png)

---

### 🔍 Step 2: Linting with Pylint

* [x] Install `pylint`

```bash
pip install pylint
```

* [x] Run `pylint` on source and tests

```bash
pylint app tests/ | tee lint-results.txt
```

---

### 🧪 Step 3: Unit Testing with Pytest

* [x] Install `pytest`

```bash
pip install pytest
```

* [x] Create `tests/test_main.py`

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

* [x] Create `pytest.ini`:

```ini
[pytest]
addopts = -v --junitxml=results.xml
testpaths = tests
```

* [x] Run tests:

```bash
PYTHONPATH=. pytest --color=yes | tee test-results.txt
```

---

## ============= Docker =============================

# Docker image tag
```shell
docker tag gcp-fastapi:v2 praful2018/gcp-fastapi:v2

```
![alt text](docs/images/tag1.png)


# Push to Docker Hub

```shell
docker push praful2018/gcp-fastapi:v2

```
![alt text](docs/images/tag2.png)

![alt text](docs/images/tag3.png)


### =================== Docker Image Optimization =================================

# 🐋 FastAPI Docker Image Optimization using Alpine (Multi-Stage Build)

This guide provides a step-by-step Dockerfile setup using **Alpine Linux** and **multi-stage builds** to significantly reduce your FastAPI application's image size, maintain code quality enforcement (via `pylint`), and ensure testing with `pytest`.

---

## 🎯 Objective

- Build a lightweight Docker image for a FastAPI + Uvicorn app
- Reduce image size to below 50MB
- Separate build and runtime stages
- Run tests and linting during the build phase

---

## 🏗️ Multi-Stage Dockerfile using `python:3.12-alpine`

```Dockerfile
# Stage 1: Builder (Lint, Test)
FROM python:3.12-alpine AS builder

# Environment config
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install required build tools
RUN apk add --no-cache gcc musl-dev libffi-dev make

# Set work directory
WORKDIR /app

# Install Python dependencies for linting and testing
COPY requirements.txt .
RUN pip install --upgrade pip setuptools==78.1.1 \
 && pip install -r requirements.txt \
 && pip install pytest pylint httpx

# Copy application source code
COPY . .

# Lint and test the application
RUN PYTHONPATH=. pylint app tests --fail-under=9.0 \
 && PYTHONPATH=. pytest tests
````

```Dockerfile
# Stage 2: Runtime
FROM python:3.12-alpine

# Create a non-root user
RUN adduser -D appuser

# Set working directory
WORKDIR /app

# Copy built app from builder
COPY --from=builder /app /app
COPY requirements.txt .

# Install only runtime dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use non-root user
USER appuser

# Expose the service port
EXPOSE 8080

# Start the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
```

---


![alt text](image.png)

## 📦 Estimated Image Size

| Base Image           | Approx Final Size | Notes                        |
| -------------------- | ----------------- | ---------------------------- |
| `python:3.12-slim`   | \~70–84 MB        | More compatible              |
| `python:3.12-alpine` | ✅ **\~35–45 MB**  | Lightweight, musl-based libc |

---

## 🚫 Caveats with Alpine

* Some Python libraries (e.g., `psycopg2`, `numpy`) may **not compile cleanly** without extra dependencies.
* Stick with Alpine **only** if your app doesn’t require heavy native dependencies.

---

## 🧼 Optional: .dockerignore

```dockerignore
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
.env
tests/
*.db
```

---

## ✅ Summary

This Alpine-based multi-stage Dockerfile:

* Separates build and runtime
* Enforces code quality
* Minimizes final image size
* Ensures production security by using a non-root user


```
