from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, index=True)
    produto = Column(String)
    quantidade = Column(Integer)
    valor_total = Column(Float)
    data_pedido = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pendente") 