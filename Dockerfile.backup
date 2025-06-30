# Stage 1: Build, Lint, Test
FROM python:3.12-slim-bookworm AS builder

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update + Install only what is needed
RUN apt-get update && apt-get install -y --no-install-recommends gcc curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip and install secure packages
COPY requirements.txt . 
RUN pip install --upgrade pip setuptools==78.1.1 \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest pylint httpx

COPY . .

# Run lint and tests, fail if pylint score < 9.0
RUN PYTHONPATH=. pylint app tests --fail-under=9.0 \
 && PYTHONPATH=. pytest tests

# Stage 2: Runtime image
FROM python:3.12-slim-bookworm

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

COPY --from=builder /app /app

# Only install runtime dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools==78.1.1 \
    && pip install --no-cache-dir -r requirements.txt

USER appuser

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
