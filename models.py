# Definimos nuestro modelo de datos "Product"
from sqlalchemy import Column, Integer, String, Float
from database import Base

class Product(Base):
    __tablename__ = "products"  # Nombre de la tabla en la base de datos

    # Definimos las columnas
    id = Column(Integer, primary_key=True, index=True)  # Identificador único
    name = Column(String, index=True)                   # Nombre del producto
    price = Column(Float)                                # Precio del producto
