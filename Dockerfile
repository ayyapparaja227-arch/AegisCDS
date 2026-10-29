# Dockerfile for AegisCDS

# ---- Builder stage ----
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Install Poetry to lock dependencies
RUN pip install --no-cache-dir poetry

# Copy only the lock files first for caching
COPY pyproject.toml poetry.lock ./

# Export exact requirements
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Copy the rest of the source code
COPY . .

# Install runtime dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime stage ----
FROM python:3.11-slim
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

# Expose the service port (default defined in src/server.py)
EXPOSE 8080

# Health‑check endpoint
HEALTHCHECK --interval=30s --timeout=5s \
  CMD curl -f http://localhost:8080/health || exit 1

# Run the AegisCDS server
CMD ["python", "-m", "src.server"]

