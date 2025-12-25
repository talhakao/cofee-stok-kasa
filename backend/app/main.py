from fastapi import FastAPI, Depends,HTTPException
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

@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductCreate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"deleted": True}