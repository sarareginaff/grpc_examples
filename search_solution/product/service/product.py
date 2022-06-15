import grpc
import time
import random
from pb.product_pb2_grpc import ProductServiceServicer
from pb.product_pb2 import GetProductsBySkusRequest, GetProductsRequest, Product, Products
from repository.product import ProductRepository


class ProductService(ProductServiceServicer):

    def GetProducts(self, request: GetProductsRequest, context: grpc.aio.ServicerContext) -> Product:
        print(f"Getting product data for term {request.term}")
        repository = ProductRepository()
        products = Products()
        
        products.product.extend(repository.GetProductDataByTerm(term=request.term))
        
        time.sleep(random.choice(range(3)))
        return products

    def GetProductsBySkus(self, request: GetProductsBySkusRequest, context: grpc.aio.ServicerContext) -> Product:
        print(f"Getting product data for skus {request.skus}")
        repository = ProductRepository()
        products = Products()
        products.product.extend(repository.GetProductDataBySkus(skus=request.skus))
        
        time.sleep(random.choice(range(3)))
        return products