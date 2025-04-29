# Importamos las librerías necesarias de SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a la base de datos SQLite local
DATABASE_URL = "sqlite:///./products.db"

# Creamos el motor de la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configuramos la sesión para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base que usarán todos los modelos para mapearse a tablas
Base = declarative_base()
