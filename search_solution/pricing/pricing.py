from concurrent import futures
import asyncio
import grpc
from pb.price_pb2_grpc import add_ProductPriceServiceServicer_to_server
from service.pricing import ProductPriceService


async def serve() -> None:
    server = grpc.aio.server()
    add_ProductPriceServiceServicer_to_server(ProductPriceService(), server)
    listen_addr = "[::]:50054"
    server.add_insecure_port(listen_addr)
    print("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())