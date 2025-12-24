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