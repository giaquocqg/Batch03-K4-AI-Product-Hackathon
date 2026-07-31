FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for Docker layer caching
COPY codebase/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code only. Protected course data must be mounted at runtime
# after the hosting provider's retention policy and access controls are approved.
COPY codebase/ ./codebase/

# Expose port 8000
EXPOSE 8000

# Public binds require APP_ACCESS_TOKEN. The corpus path must be a read-only
# private mount such as /protected-data/transcript.
ENV STUDY_PACK_DATA_ROOT=/protected-data/transcript
CMD ["python", "codebase/web_app.py", "--host", "0.0.0.0", "--port", "8000"]
