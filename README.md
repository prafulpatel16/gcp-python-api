# 🚀 FastAPI Hello World API - Google Cloud Run CI/CD

## 📌 Objective

- Build and test a simple Python FastAPI web API
- Lint and validate code quality with `pylint`
- Run unit tests using `pytest`
- Package it in a secure Docker image
- Publish the image to Google Artifact Registry
- Deploy to Google Cloud Run (fully managed)
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

