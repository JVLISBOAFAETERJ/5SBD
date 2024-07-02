import pandas as pd
import io
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from domain.models import Pedido
from infra.database import get_db
from application.services import PedidoService

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")

    content = await file.read()
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))

    service = PedidoService(db)
    for _, row in df.iterrows():
        pedido_data = row.to_dict()
        service.process_pedido(pedido_data)

    return {"filename": file.filename}

@router.post("/process")
def process_orders(db: Session = Depends(get_db)):
    service = PedidoService(db)
    pedidos = db.query(Pedido).all()
    for pedido in pedidos:
        service.update_stock(pedido.order_id)

    return {"status": "processed"}

