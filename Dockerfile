# Use a small Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependency files first
COPY pyproject.toml ./
COPY requirements.txt ./

# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app source
COPY src/ ./src

# Ensure PYTHONPATH is set
ENV PYTHONPATH=/app/src

# Don’t override Render’s PORT
EXPOSE 8000

# Default command (note $PORT and correct module path)
CMD uvicorn src.catinfo.app:app --host 0.0.0.0 --port $PORT