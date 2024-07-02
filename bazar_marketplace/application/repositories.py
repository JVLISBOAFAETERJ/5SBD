from sqlalchemy.orm import Session
from domain.models import Cliente, Produto, Pedido, ItemPedido, MovimentacaoEstoque, Compra

class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_cpf(self, cpf: str):
        return self.db.query(Cliente).filter(Cliente.cpf == cpf).first()

    def create(self, cliente: Cliente):
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

class ProdutoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_sku(self, sku: str):
        return self.db.query(Produto).filter(Produto.sku == sku).first()

    def create(self, produto: Produto):
        self.db.add(produto)
        self.db.commit()
        self.db.refresh(produto)
        return produto

    def update_stock(self, sku: str, quantity: int):
        produto = self.get_by_sku(sku)
        if produto:
            produto.stock_quantity += quantity
            self.db.commit()
            self.db.refresh(produto)
        return produto

class PedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_order_id(self, order_id: str):
        return self.db.query(Pedido).filter(Pedido.order_id == order_id).first()

    def create(self, pedido: Pedido):
        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)
        return pedido

class ItemPedidoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item_pedido: ItemPedido):
        self.db.add(item_pedido)
        self.db.commit()
        self.db.refresh(item_pedido)
        return item_pedido

class MovimentacaoEstoqueRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, movimentacao: MovimentacaoEstoque):
        self.db.add(movimentacao)
        self.db.commit()
        self.db.refresh(movimentacao)
        return movimentacao

class CompraRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, compra: Compra):
        self.db.add(compra)
        self.db.commit()
        self.db.refresh(compra)
        return compra
