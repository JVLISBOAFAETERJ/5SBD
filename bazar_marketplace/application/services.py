from sqlalchemy.orm import Session
from domain.models import Cliente, Produto, Pedido, ItemPedido, MovimentacaoEstoque, Compra
from application.repositories import ClienteRepository, ProdutoRepository, PedidoRepository, ItemPedidoRepository, MovimentacaoEstoqueRepository, CompraRepository

class PedidoService:
    def __init__(self, db: Session):
        self.db = db
        self.cliente_repository = ClienteRepository(db)
        self.produto_repository = ProdutoRepository(db)
        self.pedido_repository = PedidoRepository(db)
        self.item_pedido_repository = ItemPedidoRepository(db)
        self.movimentacao_estoque_repository = MovimentacaoEstoqueRepository(db)
        self.compra_repository = CompraRepository(db)

    def process_pedido(self, pedido_data):
        cpf = pedido_data['cpf']
        cliente = self.cliente_repository.get_by_cpf(cpf)
        if not cliente:
            cliente = Cliente(
                cpf=cpf,
                buyer_name=pedido_data['buyer_name'],
                buyer_email=pedido_data['buyer_email'],
                buyer_phone_number=pedido_data['buyer_phone_number']
            )
            self.cliente_repository.create(cliente)

        sku = pedido_data['sku']
        produto = self.produto_repository.get_by_sku(sku)
        if not produto:
            produto = Produto(
                sku=sku,
                product_name=pedido_data['product_name'],
                price=pedido_data['item_price'],
                stock_quantity=0  # inicializado com 0, pois precisa ser comprado
            )
            self.produto_repository.create(produto)

        pedido = self.pedido_repository.get_by_order_id(pedido_data['order_id'])
        if not pedido:
            pedido = Pedido(
                order_id=pedido_data['order_id'],
                purchase_date=pedido_data['purchase_date'],
                payments_date=pedido_data['payments_date'],
                buyer_id=cliente.id,
                total_value=pedido_data['item_price'] * pedido_data['quantity_purchased'],
                status='pending'
            )
            self.pedido_repository.create(pedido)
        else:
            pedido.total_value += pedido_data['item_price'] * pedido_data['quantity_purchased']
            self.db.commit()
            self.db.refresh(pedido)

        item_pedido = ItemPedido(
            order_id=pedido.id,
            order_item_id=pedido_data['order_item_id'],
            sku=produto.sku,
            product_name=pedido_data['product_name'],
            quantity_purchased=pedido_data['quantity_purchased'],
            item_price=pedido_data['item_price'],
            ship_service_level=pedido_data['ship_service_level']
        )
        self.item_pedido_repository.create(item_pedido)

        return pedido_data

    def update_stock(self, order_id):
        pedido = self.pedido_repository.get_by_order_id(order_id)
        if not pedido:
            return None

        items = self.db.query(ItemPedido).filter(ItemPedido.order_id == pedido.id).all()
        all_items_available = True

        for item in items:
            produto = self.produto_repository.get_by_sku(item.sku)
            if produto.stock_quantity < item.quantity_purchased:
                all_items_available = False
                self.compra_repository.create(
                    Compra(
                        product_id=produto.sku,
                        quantity_needed=item.quantity_purchased - produto.stock_quantity,
                        order_id=pedido.id,
                        status='pending'
                    )
                )

        if all_items_available:
            for item in items:
                self.produto_repository.update_stock(item.sku, -item.quantity_purchased)
                self.movimentacao_estoque_repository.create(
                    MovimentacaoEstoque(
                        product_id=item.sku,
                        movement_type='saida',
                        quantity=item.quantity_purchased,
                        date=pedido.purchase_date,
                        order_id=pedido.id
                    )
                )
            pedido.status = 'completed'
            self.db.commit()
            self.db.refresh(pedido)
        else:
            pedido.status = 'partial'
            self.db.commit()
            self.db.refresh(pedido)

        return pedido
