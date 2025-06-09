from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models
from database import engine, get_db
import logging
import elasticapm
from elasticapm.contrib.starlette import ElasticAPM
from elasticapm.traces import capture_span

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuração do APM
app = FastAPI()
apm = elasticapm.Client({
    'SERVICE_NAME': 'pedido_api',
    'SERVER_URL': 'http://apm-server:8200',
    'ENVIRONMENT': 'production',
    'CAPTURE_BODY': 'all',
    'CAPTURE_HEADERS': True,
    'CAPTURE_SQL_QUERIES': True,
    'TRANSACTION_MAX_SPANS': 500,
    'STACK_TRACE_LIMIT': 50
})

# Adiciona o middleware do APM
app.add_middleware(ElasticAPM, client=apm)

# Cria as tabelas
models.Base.metadata.create_all(bind=engine)

class Pedido(BaseModel):
    cliente_id: int
    produto: str
    quantidade: int
    valor_total: float

    class Config:
        orm_mode = True

@app.post("/pedido")
def cadastrar_pedido(pedido: Pedido, db: Session = Depends(get_db)):
    logger.info(f"Recebendo requisição para cadastrar pedido: {pedido.dict()}")
    
    try:
        with capture_span('criar_pedido', 'db.insert'):
            db_pedido = models.Pedido(
                cliente_id=pedido.cliente_id,
                produto=pedido.produto,
                quantidade=pedido.quantidade,
                valor_total=pedido.valor_total
            )
            
            db.add(db_pedido)
            db.commit()
            db.refresh(db_pedido)
        
        logger.info(f"Pedido cadastrado com sucesso: ID {db_pedido.id}")
        return {"status": "Pedido recebido com sucesso", "pedido": db_pedido}
    
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erro de integridade ao cadastrar pedido: {str(e)}")
        elasticapm.capture_exception()
        raise HTTPException(
            status_code=400,
            detail="Erro de integridade ao cadastrar pedido. Verifique se o cliente existe."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao cadastrar pedido: {str(e)}")
        elasticapm.capture_exception()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao cadastrar pedido: {str(e)}"
        )