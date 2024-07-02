from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infra.database import Base

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(11), unique=True, index=True)
    buyer_name = Column(String(100))
    buyer_email = Column(String(100))
    buyer_phone_number = Column(String(20))

class Produto(Base):
    __tablename__ = 'produtos'
    sku = Column(String(20), primary_key=True, index=True)
    product_name = Column(String(100))
    price = Column(Float)
    stock_quantity = Column(Integer)

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(20), unique=True, index=True)
    purchase_date = Column(DateTime)
    payments_date = Column(DateTime)
    buyer_id = Column(Integer, ForeignKey('clientes.id'))
    total_value = Column(Float)
    status = Column(String(20))

class ItemPedido(Base):
    __tablename__ = 'itens_pedido'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('pedidos.id'))
    order_item_id = Column(String(20))
    sku = Column(String(20), ForeignKey('produtos.sku'))
    product_name = Column(String(100))
    quantity_purchased = Column(Integer)
    item_price = Column(Float)
    ship_service_level = Column(String(50))

class MovimentacaoEstoque(Base):
    __tablename__ = 'movimentacao_estoque'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(20), ForeignKey('produtos.sku'))
    movement_type = Column(String(10))  # entrada/saída
    quantity = Column(Integer)
    date = Column(DateTime)
    order_id = Column(Integer, ForeignKey('pedidos.id'))

class Compra(Base):
    __tablename__ = 'compras'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(20), ForeignKey('produtos.sku'))
    quantity_needed = Column(Integer)
    order_id = Column(Integer, ForeignKey('pedidos.id'))
    status = Column(String(20))  # pendente/comprado/entregue
