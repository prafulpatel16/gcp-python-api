# Stage 1: Build, lint, test
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest pylint httpx

COPY . .

# Lint and run tests
RUN PYTHONPATH=. pylint app tests && PYTHONPATH=. pytest tests

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
