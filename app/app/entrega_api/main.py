from fastapi import FastAPI, Request
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
import elasticapm
import logging
from elasticsearch import Elasticsearch
import json
from datetime import datetime

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do Elasticsearch
es = Elasticsearch(['http://elasticsearch:9200'])

app = FastAPI()

# Configure APM
apm = make_apm_client({
    'SERVICE_NAME': 'entrega-api',
    'SERVER_URL': 'http://apm:8200',
    'ENVIRONMENT': 'production',
    'CAPTURE_BODY': 'all'
})

app.add_middleware(ElasticAPM, client=apm)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log request
    start_time = datetime.utcnow()
    response = await call_next(request)
    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds() * 1000

    log_data = {
        "@timestamp": datetime.utcnow().isoformat(),
        "service": "entrega-api",
        "method": request.method,
        "path": request.url.path,
        "duration_ms": duration,
        "status_code": response.status_code
    }

    # Log to Elasticsearch
    try:
        es.index(index=f"api-logs-{datetime.utcnow():%Y.%m.%d}", document=log_data)
    except Exception as e:
        logger.error(f"Failed to log to Elasticsearch: {e}")

    return response

# ... existing code ... 