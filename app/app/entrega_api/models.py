from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Entrega(Base):
    __tablename__ = "entregas"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, index=True)
    endereco = Column(String)
    status = Column(String, default="em_preparacao")
    data_entrega = Column(DateTime, nullable=True)
    data_criacao = Column(DateTime, default=datetime.utcnow) 