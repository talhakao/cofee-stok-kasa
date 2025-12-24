from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .schemas import ProductCreate, ProductOut
from . import crud   

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Stok & Kasa API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/products", response_model=ProductOut)
def add_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, payload)

@app.get("/products", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return crud.list_products(db)