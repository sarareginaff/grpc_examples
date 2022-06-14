from ast import ExceptHandler
from math import prod
import grpc
import time
from pb.searchProduct_pb2_grpc import SearchProductServiceServicer
from pb.searchProduct_pb2 import TermRequest, SkuRequest, CompleteProduct, CompleteProducts
from pb.stock_pb2_grpc import ProductStockServiceStub
from pb.stock_pb2 import ProductsStockRequest, ProductsStock
from pb.product_pb2_grpc import ProductServiceStub
from pb.product_pb2 import GetProductsRequest, GetProductsBySkusRequest, Products, Product
from pb.price_pb2_grpc import ProductPriceServiceStub
from pb.price_pb2 import ProductsPricesRequest, ProductsPrices, ProductPrice

STOCK_HOST = 'localhost:50051'
PRODUCT_HOST = 'localhost:50052'
PRICE_HOST = 'localhost:50054'
#https://grpc.io/docs/guides/auth/#python

class SearchProductService(SearchProductServiceServicer):

    # Tudo síncrono e unário --> busca 
    # Chega o termo, junta todas as informações, devolve a lista completa
    def GetProductsDataByTerm(self, request: TermRequest, context: grpc.aio.ServicerContext) -> CompleteProduct:
        print(f"[unary-unary] Retrieving products data based on term {request.term}")

        #Get Product data
        with grpc.insecure_channel(PRODUCT_HOST) as channel:
            product_stub = ProductServiceStub(channel)
            products = product_stub.GetProducts(GetProductsRequest(term = request.term))

        #Get Stock data
        with grpc.insecure_channel(STOCK_HOST) as channel:
            stock_stub = ProductStockServiceStub(channel)
            products_stock = stock_stub.GetProductsStockBySkus(
                    ProductsStockRequest(skus = [p.sku for p in products.product]))
        
        #Get Price data
        with grpc.insecure_channel(PRICE_HOST) as channel:
            price_stub = ProductPriceServiceStub(channel)
            products_prices = price_stub.GetProductsPricesBySkus(
                    ProductsPricesRequest(skus = [p.sku for p in products.product]))

        return_message = CompleteProducts()
        complete_products = self._build_complete_products(products, products_stock, products_prices)
        return_message.product.extend(complete_products)

        return return_message
    
    # Chegada unária e devolução em streaming --> busca
    # Chega o termo, junta informações de produto e estoque e a medida que preço for retornando, devolve o que for retornando
    def GetProductsDataStreamByTerm(self, request: TermRequest, context: grpc.aio.ServicerContext) -> CompleteProduct:
        print(f"[unary-stream] Retrieving products data based on term {request.term}")

        #Get Product data
        with grpc.insecure_channel(PRODUCT_HOST) as channel:
            product_stub = ProductServiceStub(channel)
            products = product_stub.GetProducts(GetProductsRequest(term = request.term))

        #Get Stock data
        with grpc.insecure_channel(STOCK_HOST) as channel:
            stock_stub = ProductStockServiceStub(channel)
            products_stock = stock_stub.GetProductsStockBySkus(
                    ProductsStockRequest(skus = [p.sku for p in products.product]))
        
        for p in products.product:
            yield self._build_product_without_price(p, products_stock)

        #Get Price data
        with grpc.insecure_channel(PRICE_HOST) as channel:
            price_stub = ProductPriceServiceStub(channel)

            for product_price in price_stub.GetProductsPricesStreamBySkus(
                    ProductsPricesRequest(skus = [p.sku for p in products.product])):
                yield self._build_complete_product_by_price_sku(products, products_stock, product_price)

    # Chegada em streaming e devolução unária --> carrinho
    # Chega sku por sku e, quando acaba de receber, junta todas as informações, devolve a lista completa
    async def GetProductsDataBySkusStream(self, request_iterator: SkuRequest, context: grpc.aio.ServicerContext) -> CompleteProduct:
        print(f"[stream-unary] Retrieving products data based on skus streaming")
        skus = []
        async for req in request_iterator:
            skus.append(req.sku)

        print(f"[stream-unary] Received skus {skus}")
        #Get Product data
        with grpc.insecure_channel(PRODUCT_HOST) as channel:
            product_stub = ProductServiceStub(channel)
            request = GetProductsBySkusRequest()
            request.skus.extend(skus)
            products = product_stub.GetProductsBySkus(request)

        #Get Stock data
        with grpc.insecure_channel(STOCK_HOST) as channel:
            stock_stub = ProductStockServiceStub(channel)
            products_stock = stock_stub.GetProductsStockBySkus(
                    ProductsStockRequest(skus = [p.sku for p in products.product]))
        
        #Get Price data
        with grpc.insecure_channel(PRICE_HOST) as channel:
            price_stub = ProductPriceServiceStub(channel)
            products_prices = price_stub.GetProductsPricesBySkus(
                    ProductsPricesRequest(skus = [p.sku for p in products.product]))

        return_message = CompleteProducts()
        complete_products = self._build_complete_products(products, products_stock, products_prices)
        return_message.product.extend(complete_products)

        return return_message

    # Chegada em streaming e devolução em streaming --> carrinho
    # Chega sku por sku, junta informações de produto e estoque e a medida que preço for retornando, devolve o que for retornando
    async def GetProductsDataStreamBySkusStream(self, request_iterator: SkuRequest, context: grpc.aio.ServicerContext) -> CompleteProduct:
        pass
        print(f"[stream-stream] Retrieving products data based on skus streaming")
        async for req in request_iterator:
            print(f"[stream-stream] Received sku {req.sku}")
            #Get Product data
            with grpc.insecure_channel(PRODUCT_HOST) as channel:
                product_stub = ProductServiceStub(channel)
                request = GetProductsBySkusRequest()
                request.skus.extend([req.sku])
                products = product_stub.GetProductsBySkus(request)

            #Get Stock data
            if (products.product):
                with grpc.insecure_channel(STOCK_HOST) as channel:
                    stock_stub = ProductStockServiceStub(channel)
                    products_stock = stock_stub.GetProductsStockBySkus(
                                    ProductsStockRequest(skus = [p.sku for p in products.product]))
    
                #Get Price data
                with grpc.insecure_channel(PRICE_HOST) as channel:
                    price_stub = ProductPriceServiceStub(channel)
                    products_prices = price_stub.GetProductsPricesBySkus(
                                                ProductsPricesRequest(skus = [p.sku for p in products.product]))
                    
                    for products_prices in products_prices.productsPrices:
                        yield self._build_complete_product_by_price_sku(products, products_stock, products_prices)


    def _build_complete_products(self, products: Products, products_stock: ProductsStock, products_prices: ProductsPrices) -> list:
        complete_products = []
        for p in products.product:
            stock = [s for s in products_stock.productStock if s.sku == p.sku]
            price = [pp for pp in products_prices.productsPrices if pp.sku == p.sku]
            complete_products.append(CompleteProduct(
                                                    product=p, 
                                                    stock=stock[0] if stock else None,
                                                    price=price[0] if price else None))

        return complete_products

    def _build_product_without_price(self, product: Product, products_stock: ProductsStock) -> list:
        stock = [s for s in products_stock.productStock if s.sku == product.sku]
        return CompleteProduct(product=product, 
                                stock=stock[0] if stock else None)

    def _build_complete_product_by_price_sku(self, products: Products, products_stock: ProductsStock, product_price: ProductPrice) -> CompleteProduct:
        stock = [s for s in products_stock.productStock if s.sku == product_price.sku]
        product = [p for p in products.product if p.sku == product_price.sku]
        return CompleteProduct(product=product[0] if stock else None, 
                                stock=stock[0] if stock else None,
                                price=product_price)
