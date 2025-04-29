# Test del repositorio usando una base de datos SQLite en memoria
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Product
from repositories.product_repository import ProductRepository

# Crear una base de datos en memoria para los tests (rápida y aislada)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Crear sesión
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fijar la base para cada test
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)  # Crear tablas
    session = SessionTesting()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)  # Eliminar tablas después de cada test

def test_create_product(db_session):
    repo = ProductRepository(db_session)
    product = repo.create(name="Test Product", price=9.99)

    assert product.id is not None
    assert product.name == "Test Product"
    assert product.price == 9.99

def test_get_product(db_session):
    repo = ProductRepository(db_session)
    new_product = repo.create(name="Another Product", price=19.99)
    
    fetched = repo.get_by_id(new_product.id)
    
    assert fetched.name == "Another Product"
    assert fetched.price == 19.99

def test_update_product(db_session):
    repo = ProductRepository(db_session)
    product = repo.create(name="Old Name", price=5.00)
    
    updated = repo.update(product_id=product.id, name="New Name", price=10.00)
    
    assert updated.name == "New Name"
    assert updated.price == 10.00

def test_delete_product(db_session):
    repo = ProductRepository(db_session)
    product = repo.create(name="To be deleted", price=15.00)
    
    repo.delete(product.id)
    result = repo.get_by_id(product.id)
    
    assert result is None
