# ───────────────
# Stage 1: Builder
# ───────────────
FROM python:3.12-alpine AS builder

# Set environment variables to reduce image size and prevent prompts
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install build dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev make

# Set work directory
WORKDIR /app

# Install pip dependencies for build and testing
COPY requirements.txt .
RUN pip install --upgrade pip setuptools==78.1.1 \
 && pip install -r requirements.txt \
 && pip install pytest pylint httpx

# Copy app source and run tests/lint
COPY . .

# Run lint and test; fail if score < 9.0
RUN PYTHONPATH=. pylint app tests --fail-under=9.0 \
 && PYTHONPATH=. pytest tests

# ─────────────────────────────
# Stage 2: Final Runtime Image
# ─────────────────────────────
FROM python:3.12-alpine

# Create a non-root user
RUN adduser -D appuser

# Set working directory
WORKDIR /app

# Copy files from builder stage
COPY --from=builder /app /app
COPY requirements.txt .

# Install only runtime dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER appuser

# Expose Uvicorn port
EXPOSE 8080

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
