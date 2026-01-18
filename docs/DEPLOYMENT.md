# FairProp Deployment Guide

## 🚀 Production Deployment

### Prerequisites

- Python 3.9+
- 4GB RAM minimum (8GB recommended for AI features)
- Docker (optional but recommended)

---

## Option 1: Docker Deployment (Recommended)

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY setup.py .
COPY fairprop/ ./fairprop/
COPY rules/ ./rules/
COPY fha_rules.json .

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Expose API port
EXPOSE 8000

# Run API server
CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Build and Run

```bash
# Build image
docker build -t fairprop:latest .

# Run container
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  --name fairprop-api \
  fairprop:latest

# Check logs
docker logs -f fairprop-api
```

### 3. Docker Compose

```yaml
version: '3.8'

services:
  fairprop-api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./logs:/app/logs
      - ./rules:/app/rules
    environment:
      - LOG_LEVEL=INFO
    restart: unless-stopped
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - fairprop-api
    restart: unless-stopped
```

---

## Option 2: Traditional Deployment

### 1. System Setup

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3.11 python3-pip tesseract-ocr

# Install FairProp
git clone https://github.com/your-org/fairprop.git
cd fairprop
pip install -e .
```

### 2. Systemd Service

Create `/etc/systemd/system/fairprop.service`:

```ini
[Unit]
Description=FairProp Compliance API
After=network.target

[Service]
Type=simple
User=fairprop
WorkingDirectory=/opt/fairprop
Environment="PATH=/opt/fairprop/venv/bin"
ExecStart=/opt/fairprop/venv/bin/python api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable fairprop
sudo systemctl start fairprop
sudo systemctl status fairprop
```

---

## Option 3: Cloud Platforms

### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 fairprop-api

# Create environment
eb create fairprop-prod

# Deploy
eb deploy
```

### Google Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/fairprop

# Deploy
gcloud run deploy fairprop \
  --image gcr.io/PROJECT_ID/fairprop \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Heroku

```bash
# Create app
heroku create fairprop-api

# Add buildpack
heroku buildpacks:add heroku/python

# Deploy
git push heroku main
```

---

## Configuration

### Environment Variables

```bash
# .env file
LOG_LEVEL=INFO
API_PORT=8000
CACHE_SIZE=1000
ENABLE_AI=true
RULES_PATH=/app/rules/fha_rules.json
```

### Production Settings

```python
# config.py
import os

class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    API_PORT = int(os.getenv('API_PORT', 8000))
    CACHE_SIZE = int(os.getenv('CACHE_SIZE', 1000))
    ENABLE_AI = os.getenv('ENABLE_AI', 'true').lower() == 'true'
    RULES_PATH = os.getenv('RULES_PATH', 'fha_rules.json')
```

---

## Performance Optimization

### 1. Enable Caching

```python
# In api_server.py
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fairprop-cache")
```

### 2. Add Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/scan")
@limiter.limit("100/minute")
async def scan_text(request: Request, scan_request: ScanRequest):
    # ... scanning logic
```

### 3. Use Gunicorn

```bash
# Install
pip install gunicorn uvicorn[standard]

# Run with workers
gunicorn api_server:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120
```

---

## Monitoring

### Health Checks

```bash
# Add to monitoring system
curl http://localhost:8000/api/health

# Expected response
{"status":"healthy","service":"FairProp API"}
```

### Logging

```python
# Configure structured logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/fairprop.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### Metrics

```python
# Add Prometheus metrics
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

## Security

### 1. HTTPS/SSL

```nginx
# nginx.conf
server {
    listen 443 ssl http2;
    server_name api.fairprop.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 2. API Key Authentication

```python
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key
```

### 3. CORS Configuration

```python
# Production CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## Backup & Recovery

### Database Backup

```bash
# Backup rules
tar -czf rules-backup-$(date +%Y%m%d).tar.gz rules/

# Backup logs
tar -czf logs-backup-$(date +%Y%m%d).tar.gz logs/
```

### Automated Backups

```bash
# Add to crontab
0 2 * * * /opt/fairprop/backup.sh
```

---

## Troubleshooting

### Common Issues

**Issue**: API not responding
```bash
# Check if service is running
sudo systemctl status fairprop

# Check logs
sudo journalctl -u fairprop -f
```

**Issue**: Out of memory
```bash
# Reduce cache size
export CACHE_SIZE=500

# Or disable AI features
export ENABLE_AI=false
```

**Issue**: Slow response times
```bash
# Enable caching
# Add Redis
# Increase workers
```

---

## Scaling

### Horizontal Scaling

```yaml
# kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fairprop-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fairprop
  template:
    metadata:
      labels:
        app: fairprop
    spec:
      containers:
      - name: fairprop
        image: fairprop:latest
        ports:
        - containerPort: 8000
```

### Load Balancing

```nginx
upstream fairprop_backend {
    least_conn;
    server fairprop1:8000;
    server fairprop2:8000;
    server fairprop3:8000;
}

server {
    location / {
        proxy_pass http://fairprop_backend;
    }
}
```

---

## Maintenance

### Update Rules

```bash
# Update rules files
git pull origin main

# Reload without downtime
curl -X POST http://localhost:8000/api/reload-rules
```

### Update Code

```bash
# Zero-downtime deployment
git pull
pip install -e .
sudo systemctl reload fairprop
```

---

## Support

For deployment issues, see:
- [GitHub Issues](https://github.com/your-org/fairprop/issues)
- [Documentation](https://docs.fairprop.com)
- [Community Forum](https://community.fairprop.com)
