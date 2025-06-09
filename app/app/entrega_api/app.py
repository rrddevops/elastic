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
    'SERVICE_NAME': 'entrega_api',
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

class Entrega(BaseModel):
    pedido_id: int
    endereco: str
    cep: str
    cidade: str
    estado: str

    class Config:
        orm_mode = True

@app.post("/entrega")
def cadastrar_entrega(entrega: Entrega, db: Session = Depends(get_db)):
    logger.info(f"Recebendo requisição para cadastrar entrega: {entrega.dict()}")
    
    try:
        # Remove o hífen antes de validar
        cep = entrega.cep.replace('-', '')
        
        if not cep.isdigit() or len(cep) != 8:
            raise HTTPException(status_code=400, detail="CEP inválido")

        with capture_span('criar_entrega', 'db.insert'):
            endereco_completo = f"{entrega.endereco}, {entrega.cidade} - {entrega.estado}, CEP: {entrega.cep}"
            
            db_entrega = models.Entrega(
                pedido_id=entrega.pedido_id,
                endereco=endereco_completo,
                status="em_preparacao"
            )
            
            db.add(db_entrega)
            db.commit()
            db.refresh(db_entrega)
        
        logger.info(f"Entrega cadastrada com sucesso: ID {db_entrega.id}")
        return {"status": "Entrega recebida com sucesso", "entrega": db_entrega}
    
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Erro de integridade ao cadastrar entrega: {str(e)}")
        elasticapm.capture_exception()
        raise HTTPException(
            status_code=400,
            detail="Erro de integridade ao cadastrar entrega. Verifique se o pedido existe."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Erro ao cadastrar entrega: {str(e)}")
        elasticapm.capture_exception()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao cadastrar entrega: {str(e)}"
        )