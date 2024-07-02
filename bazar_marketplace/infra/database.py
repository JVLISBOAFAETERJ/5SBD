from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Carregar configurações do banco de dados do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

# Criar o engine do SQLAlchemy
engine = create_engine(DATABASE_URL)

# Criar uma classe base declarativa
Base = declarative_base()

# Criar uma fábrica de sessões configurada para o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

