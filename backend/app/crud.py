from sqlalchemy.orm import Session
from .models import Product
from .schemas import ProductCreate

def create_product(db: Session, data: ProductCreate) -> Product:
    p = Product(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def list_products(db: Session) -> list[Product]:
    return db.query(Product).order_by(Product.id.desc()).all()

from . import models
from .schemas import ProductCreate

def update_product(db, product_id: int, payload: ProductCreate):
    p = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not p:
        return None

    p.name = payload.name
    p.category = payload.category
    p.stock = payload.stock
    p.price = payload.price

    db.commit()
    db.refresh(p)
    return p

def delete_product(db, product_id: int) -> bool:
    p = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True