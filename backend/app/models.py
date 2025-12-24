from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, index=True)
    category = Column(String(80), nullable=True)
    stock = Column(Integer, nullable=False, default=0)
    price = Column(Float, nullable=False, default=0.0)