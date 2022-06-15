import grpc
import time
import random
from pb.stock_pb2_grpc import ProductStockServiceServicer
from pb.stock_pb2 import ProductStock, ProductsStock, SingleProductStockRequest , ProductsStockRequest
from repository.stock import StockRepository


class ProductStockService(ProductStockServiceServicer):

    def GetProductStockBySku(self, request: SingleProductStockRequest, context: grpc.aio.ServicerContext) -> ProductStock:
        print(f"Getting stock data for sku {request.sku}")
        repository = StockRepository()
        time.sleep(random.choice(range(3)))
        return repository.GetStockDataBySku(sku=request.sku)        

    def GetProductsStockBySkus(self, request: ProductsStockRequest, context: grpc.aio.ServicerContext) -> ProductsStock:
        print(f"Getting stock data for skus {request.skus}")
        repository = StockRepository()
        products_stock = ProductsStock()

        products_stock.productStock.extend(repository.GetStockDataBySkus(skus=request.skus))
        
        time.sleep(random.choice(range(3)))
        return products_stock
