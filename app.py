# API principal que expone las rutas usando FastAPI
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from repositories.product_repository import ProductRepository
from pydantic import BaseModel

# Crear las tablas automáticamente al iniciar la aplicación
Base.metadata.create_all(bind=engine)

# Instanciamos la aplicación FastAPI
app = FastAPI()

# Definimos los esquemas de entrada y salida usando Pydantic
class ProductCreate(BaseModel):
    name: str
    price: float

class ProductOut(ProductCreate):
    id: int  # Salida incluye el ID

    class Config:
        orm_mode = True  # Para que Pydantic trabaje correctamente con ORM

# Función para obtener una sesión de base de datos en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ruta para crear un producto
@app.post("/products/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)  # Usamos el repositorio
    return repo.create(name=product.name, price=product.price)

# Ruta para obtener todos los productos
@app.get("/products/", response_model=list[ProductOut])
def read_products(db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    return repo.get_all()

# Ruta para obtener un producto específico por ID
@app.get("/products/{product_id}", response_model=ProductOut)
def read_product(product_id: int, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Ruta para actualizar un producto
@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, updated_product: ProductCreate, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.update(product_id=product_id, name=updated_product.name, price=updated_product.price)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Ruta para eliminar un producto
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    repo = ProductRepository(db)
    product = repo.delete(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
