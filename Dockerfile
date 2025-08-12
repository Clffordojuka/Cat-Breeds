# Use a small Python base
FROM python:3.11-slim

WORKDIR /app

# Copy pyproject/requirements first for caching
COPY pyproject.toml .
COPY requirements.txt .

# Install runtime deps
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port (Render provide via $PORT)
ENV PORT 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]