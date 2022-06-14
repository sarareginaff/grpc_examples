import asyncio
import grpc
from pb.product_pb2_grpc import add_ProductServiceServicer_to_server
from service.product import ProductService


async def serve() -> None:
    server = grpc.aio.server()
    add_ProductServiceServicer_to_server(ProductService(), server)
    listen_addr = "[::]:50052"
    server.add_insecure_port(listen_addr)
    print("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())