# Repositorio que gestiona las operaciones CRUD de productos
from models import Product
from sqlalchemy.orm import Session

class ProductRepository:
    def __init__(self, db: Session):
        # Recibimos la sesión de base de datos
        self.db = db

    def get_all(self):
        # Obtener todos los productos
        return self.db.query(Product).all()

    def get_by_id(self, product_id: int):
        # Obtener un producto por su ID
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, name: str, price: float):
        # Crear un nuevo producto
        new_product = Product(name=name, price=price)
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)  # Actualizamos para obtener el ID generado
        return new_product

    def update(self, product_id: int, name: str, price: float):
        # Actualizar un producto existente
        product = self.get_by_id(product_id)
        if product:
            product.name = name
            product.price = price
            self.db.commit()
            self.db.refresh(product)
        return product

    def delete(self, product_id: int):
        # Eliminar un producto
        product = self.get_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()
        return product
