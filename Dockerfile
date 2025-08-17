# Use a small, up-to-date Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files first for efficient caching
COPY pyproject.toml requirements.txt ./

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY src/ ./src

# Set PYTHONPATH to ensure module resolution
ENV PYTHONPATH=/app/src

# Expose port 8000
EXPOSE 8000

# Default command: use shell form to allow $PORT expansion
CMD uvicorn src.catinfo.app:app --host 0.0.0.0 --port ${PORT:-8000}