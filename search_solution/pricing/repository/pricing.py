from pb.price_pb2 import ProductPrice

def _populate_database() -> list:
    return [
        ProductPrice(
            sku="79756",
            originalPrice=21.90,
            finalPrice=17.50
        ),
        ProductPrice(
            sku="72501",
            originalPrice=21.90,
            finalPrice=17.50            
        ),
        ProductPrice(
            sku="76599",
            originalPrice=22.90,
            finalPrice=17.90            
        ),
        ProductPrice(
            sku="72038",
            originalPrice=23.90,
            finalPrice=18.90            
        ),
        ProductPrice(
            sku="83599",
            originalPrice=39.90,
            finalPrice=19.90           
        ),
        ProductPrice(
            sku="83600",
            originalPrice=39.90,
            finalPrice=19.90             
        ),
        ProductPrice(
            sku="83597",
            originalPrice=39.90,
            finalPrice=19.90            
        ),
        ProductPrice(
            sku="80423",
            originalPrice=27.90,
            finalPrice=21.90            
        ),
        ProductPrice(
            sku="81480",
            originalPrice=29.90,
            finalPrice=23.90            
        ),
        ProductPrice(
            sku="83595",
            originalPrice=42.90,
            finalPrice=25.70            
        ),
        ProductPrice(
            sku="81359",
            originalPrice=32.90,
            finalPrice=29.60            
        )
    ]

class PriceRepository:
    _database = _populate_database()

    def GetPriceDataBySku(self, sku: str) -> ProductPrice:
        price_info = [i for i in self._database if i.sku == sku]
        return price_info[0] if price_info else None

    def GetPriceDataBySkus(self, skus: list) -> list:
        prices_info = [i for i in self._database if i.sku in skus]
        return prices_info


