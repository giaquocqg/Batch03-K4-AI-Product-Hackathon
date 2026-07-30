FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for Docker layer caching
COPY codebase/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire codebase
COPY codebase/ ./codebase/
COPY data/ ./data/

# Expose port 8000
EXPOSE 8000

# Run the web app
CMD ["python", "codebase/web_app.py", "--port", "8000"]
