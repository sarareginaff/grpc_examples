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

class SearchProductService(SearchProductServiceServicer):

    # Tudo síncrono e unário --> busca 
    # Chega o termo, junta todas as informações, devolve a lista completa
    def GetProductsDataByTerm(self, request: TermRequest, context: grpc.aio.ServicerContext) -> CompleteProduct:
        print(f"[unary-unary] Retrieving products data based on term {request.term}")

        try:
            #Get Product data
            products = self._get_products(term = request.term)

            #Get Stock data
            products_stock = self._get_products_stock_by_skus(skus = [p.sku for p in products.product])
            
            #Get Price data
            products_prices = self._get_products_prices_by_skus(skus = [p.sku for p in products.product])

            return self._build_complete_products(products, products_stock, products_prices)
        except Exception as exc:
            message = f"[unary-unary] Error while retrieving data: {exc}"
            print(message)

            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(message)
            return CompleteProducts()
    
    # Chegada unária e devolução em streaming --> busca
    # Chega o termo, junta informações de produto e estoque e a medida que preço for retornando, devolve o que for retornando
    def GetProductsDataStreamByTerm(self, request: TermRequest, context: grpc.aio.ServicerContext) -> CompleteProduct:
        print(f"[unary-stream] Retrieving products data based on term {request.term}")

        try:
            #Get Product data
            products = self._get_products(term = request.term)

            #Get Stock data
            products_stock = self._get_products_stock_by_skus(skus = [p.sku for p in products.product])
            
            #Eh possível enviar mensagens no meio da comunicação e depois continuar algum cálculo e enviar novamente
            for p in products.product:
                yield self._build_product_without_price(p, products_stock)

            #Get Price data
            for product_price in self._get_products_prices_stream_by_skus(skus = [p.sku for p in products.product]):
                yield self._build_complete_product_by_price_sku(products, products_stock, product_price)
        except Exception as exc:
            message = f"[unary-stream] Error while retrieving data: {exc}"
            print(message)

            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(message)
            yield CompleteProducts()

    # Chegada em streaming e devolução unária --> carrinho
    # Chega sku por sku e, quando acaba de receber, junta todas as informações, devolve a lista completa
    async def GetProductsDataBySkusStream(self, request_iterator: SkuRequest, context: grpc.aio.ServicerContext) -> CompleteProduct:
        print(f"[stream-unary] Retrieving products data based on skus streaming")
        try: 
            skus = []
            async for req in request_iterator:
                skus.append(req.sku)

            print(f"[stream-unary] Received skus {skus}")
            #Get Product data
            products = self._get_products_by_skus_request(skus = skus)
            
            #Get Stock data
            products_stock = self._get_products_stock_by_skus(skus = [p.sku for p in products.product])
            
            #Get Price data
            products_prices = self._get_products_prices_by_skus(skus = [p.sku for p in products.product])
                       
            return self._build_complete_products(products, products_stock, products_prices)
        except Exception as exc:
            message = f"[stream-unary] Error while retrieving data: {exc}"
            print(message)

            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(message)
            return CompleteProducts()

    # Chegada em streaming e devolução em streaming --> carrinho
    # Chega sku por sku, junta informações de produto e estoque e a medida que preço for retornando, devolve o que for retornando
    async def GetProductsDataStreamBySkusStream(self, request_iterator: SkuRequest, context: grpc.aio.ServicerContext) -> CompleteProduct:
        print(f"[stream-stream] Retrieving products data based on skus streaming")
        
        try:
            async for req in request_iterator:
                print(f"[stream-stream] Received sku {req.sku}")
                #Get Product data
                products = self._get_products_by_skus_request(skus = [req.sku])

                if (products.product):
                    #Get Stock data
                    products_stock = self._get_products_stock_by_skus(skus = [p.sku for p in products.product])

                    #Get Price data
                    products_prices = self._get_products_prices_by_skus(skus = [p.sku for p in products.product])     
                    for products_prices in products_prices.productsPrices:
                        yield self._build_complete_product_by_price_sku(products, products_stock, products_prices)
        except Exception as exc:
            message = f"[stream-stream] Error while retrieving data: {exc}"
            print(message)

            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(message)
            yield CompleteProducts()

    def _get_products(self, term: str) -> Products:
        with grpc.insecure_channel(PRODUCT_HOST) as channel:
            product_stub = ProductServiceStub(channel)
            return product_stub.GetProducts(GetProductsRequest(term = term))

    def _get_products_by_skus_request(self, skus: list) -> Products:
        with grpc.insecure_channel(PRODUCT_HOST) as channel:
            product_stub = ProductServiceStub(channel)
            request = GetProductsBySkusRequest()
            request.skus.extend(skus)
            return product_stub.GetProductsBySkus(request)

    def _get_products_stock_by_skus(self, skus: list) -> ProductsStock:
        with grpc.insecure_channel(STOCK_HOST) as channel:
            stock_stub = ProductStockServiceStub(channel)
            return stock_stub.GetProductsStockBySkus(
                    ProductsStockRequest(skus = skus))

    def _get_products_prices_by_skus(self, skus: list) -> ProductsPrices:
        with grpc.insecure_channel(PRICE_HOST) as channel:
            price_stub = ProductPriceServiceStub(channel)
            return price_stub.GetProductsPricesBySkus(
                    ProductsPricesRequest(skus = skus))

    def _get_products_prices_stream_by_skus(self, skus: list) -> ProductPrice:
        with grpc.insecure_channel(PRICE_HOST) as channel:
            price_stub = ProductPriceServiceStub(channel)

            for product_price in price_stub.GetProductsPricesStreamBySkus(
                    ProductsPricesRequest(skus = skus)):
                yield product_price

    def _build_complete_products(self, products: Products, products_stock: ProductsStock, products_prices: ProductsPrices) -> CompleteProducts:
        complete_products_list = []
        for p in products.product:
            stock = [s for s in products_stock.productStock if s.sku == p.sku]
            price = [pp for pp in products_prices.productsPrices if pp.sku == p.sku]
            complete_products_list.append(CompleteProduct(
                                                    product=p, 
                                                    stock=stock[0] if stock else None,
                                                    price=price[0] if price else None))

        complete_products = CompleteProducts()
        complete_products.product.extend(complete_products_list)

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

    