from concurrent import futures
import asyncio
import grpc
from pb.stock_pb2_grpc import add_ProductStockServiceServicer_to_server
from service.stock import ProductStockService


async def serve() -> None:
    server = grpc.aio.server()
    add_ProductStockServiceServicer_to_server(ProductStockService(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    print("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())