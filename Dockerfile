# Use a small Python base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project metadata first for caching
COPY pyproject.toml .
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN python -m pip install --upgrade pip

# Install dependencies in editable mode (so src/rpcats is importable)
COPY src/ ./src
RUN pip install -e ./src

# Copy rest of the project (tests, README, etc.)
COPY . .

# Set PYTHONPATH so Python finds src/rpcats
ENV PYTHONPATH=/app/src

# Expose port (for Render, Railway, etc.)
ENV PORT=8000

# Default command to run Uvicorn
CMD ["uvicorn", "rpcats.app:app", "--host", "0.0.0.0", "--port", "8000"]