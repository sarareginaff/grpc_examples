import grpc
import time
import random
from pb.price_pb2_grpc import ProductPriceServiceServicer
from pb.price_pb2 import ProductPrice, ProductsPrices, SingleProductPriceRequest , ProductsPricesRequest
from repository.pricing import PriceRepository


class ProductPriceService(ProductPriceServiceServicer):

    def GetProductPriceBySku(self, request: SingleProductPriceRequest, context: grpc.aio.ServicerContext) -> ProductPrice:
        print(f"Getting Price data for sku {request.sku}")
        repository = PriceRepository()
        
        time.sleep(random.choice(range(3)))
        return repository.GetPriceDataBySku(sku=request.sku)        

    def GetProductsPricesBySkus(self, request: ProductsPricesRequest, context: grpc.aio.ServicerContext) -> ProductsPrices:
        print(f"Getting Price data for skus {request.skus}")
        repository = PriceRepository()
        products_Price = ProductsPrices()

        products_Price.productsPrices.extend(repository.GetPriceDataBySkus(skus=request.skus))

        time.sleep(random.choice(range(3)))
        return products_Price
    
    def GetProductsPricesStreamBySkus(self, request: ProductsPricesRequest, context: grpc.aio.ServicerContext) -> ProductPrice:
        repository = PriceRepository()
        prouduct_prices = repository.GetPriceDataBySkus(skus=request.skus)
        for product_price in prouduct_prices:
            time.sleep(random.choice(range(3)))
            yield product_price
