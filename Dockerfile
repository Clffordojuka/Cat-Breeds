FROM python:3.11-slim

WORKDIR /app

# Copy project metadata first (for caching)
COPY pyproject.toml .
COPY requirements.txt .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy all source code (no src folder)
COPY . .

# Install package in editable mode (if needed)
# RUN pip install -e .

# Make sure Python can find all modules
ENV PYTHONPATH=/app

# Expose port
ENV PORT=8000

# Run Uvicorn pointing to app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]