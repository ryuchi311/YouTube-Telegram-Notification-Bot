# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY YT-BOT.py .
COPY telegram_config.py .

# Create data directory and copy initial data
COPY Pydata/ ./Pydata/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash ytbot && \
    chown -R ytbot:ytbot /app

# Switch to non-root user
USER ytbot

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('https://api.telegram.org', timeout=5)" || exit 1

# Run the bot
CMD ["python", "YT-BOT.py"]