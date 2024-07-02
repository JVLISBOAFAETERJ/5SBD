from fastapi import FastAPI
from api.controllers import router
from infra.database import engine, Base

# Inicialização do banco de dados
Base.metadata.create_all(bind=engine)

# Inicialização do aplicativo FastAPI
app = FastAPI()

# Inclusão do roteador principal com prefixo /api
app.include_router(router, prefix="/api")

# Adição de uma rota básica para a raiz
@app.get("/")
def read_root():
    return {"message": "Bem vindo ao bazar"}

# Execução do servidor Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
