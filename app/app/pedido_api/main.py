from fastapi import FastAPI, Request
from elasticapm.contrib.starlette import ElasticAPM, make_apm_client
import elasticapm
import logging
from elasticsearch import Elasticsearch
import json
from datetime import datetime
from database import engine
from sqlalchemy import event
import time
import os

# Ensure log directory exists
log_dir = "/usr/share/filebeat/logs"
os.makedirs(log_dir, exist_ok=True)

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{log_dir}/pedido-api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuração do Elasticsearch
es = Elasticsearch(['http://elasticsearch:9200'])

app = FastAPI()

# Configure APM
apm = make_apm_client({
    'SERVICE_NAME': 'pedido-api',
    'SERVER_URL': 'http://apm:8200',
    'ENVIRONMENT': 'production',
    'CAPTURE_BODY': 'all',
    'TRANSACTION_SAMPLE_RATE': '1',
    'CAPTURE_HEADERS': True,
    'DEBUG': True
})

# Add APM middleware
app.add_middleware(ElasticAPM, client=apm)

# SQL Query monitoring
@event.listens_for(engine, 'before_cursor_execute')
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(engine, 'after_cursor_execute')
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time'].pop()
    # Report SQL timing to APM
    apm.client.capture_custom_event('sql', {
        'query': statement,
        'duration': total,
        'parameters': str(parameters)
    })

@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Start transaction
    transaction = apm.client.begin_transaction('request')
    
    try:
        # Log request
        start_time = datetime.utcnow()
        
        # Add custom context to transaction
        apm.client.update_context({
            'custom': {
                'endpoint': request.url.path,
                'method': request.method,
            }
        })
        
        response = await call_next(request)
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds() * 1000

        log_data = {
            "@timestamp": datetime.utcnow().isoformat(),
            "service": "pedido-api",
            "method": request.method,
            "path": request.url.path,
            "duration_ms": duration,
            "status_code": response.status_code
        }

        # Log to file and Elasticsearch
        logger.info(json.dumps(log_data))
        
        try:
            es.index(index=f"api-logs-{datetime.utcnow():%Y.%m.%d}", document=log_data)
        except Exception as e:
            logger.error(f"Failed to log to Elasticsearch: {e}")
            apm.client.capture_exception()

        # End transaction
        apm.client.end_transaction('request', response.status_code)
        return response
        
    except Exception as e:
        logger.error(f"Request failed: {e}")
        apm.client.capture_exception()
        raise
    finally:
        if transaction:
            apm.client.end_transaction('request', 500)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting pedido-api service")
    # Test Elasticsearch connection
    try:
        if not es.ping():
            logger.error("Could not connect to Elasticsearch")
            apm.client.capture_message("Could not connect to Elasticsearch", "error")
    except Exception as e:
        logger.error(f"Elasticsearch error: {e}")
        apm.client.capture_exception()

# ... existing code ... 