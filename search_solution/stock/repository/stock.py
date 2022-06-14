from pb.stock_pb2 import ProductStock

def _populate_database() -> list:
    return [
        ProductStock(
            sku="79756",
            quantity=897
        ),
        ProductStock(
            sku="72501",
            quantity=3421
        ),
        ProductStock(
            sku="76599",
            quantity=4279
        ),
        ProductStock(
            sku="72038",
            quantity=63
        ),
        ProductStock(
            sku="83599",
            quantity=6894
        ),
        ProductStock(
            sku="83600",
            quantity=25795
        ),
        ProductStock(
            sku="83597",
            quantity=4632
        ),
        ProductStock(
            sku="80423",
            quantity=458
        ),
        ProductStock(
            sku="81480",
            quantity=32
        ),
        ProductStock(
            sku="83595",
            quantity=579
        ),
        ProductStock(
            sku="81359",
            quantity=42
        )
    ]
        
  

class StockRepository:
    _database = _populate_database()

    def GetStockDataBySku(self, sku: str) -> ProductStock:
        stock_info = [i for i in self._database if i.sku == sku]
        return stock_info[0] if stock_info else None

    def GetStockDataBySkus(self, skus: list) -> list:
        stock_info = [i for i in self._database if i.sku in skus]
        return stock_info


