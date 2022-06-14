import grpc
import asyncio
from pb.searchProduct_pb2_grpc import add_SearchProductServiceServicer_to_server
from service.search import SearchProductService
from pb.searchProduct_pb2 import TermRequest


async def serve() -> None:
    server = grpc.aio.server()
    add_SearchProductServiceServicer_to_server(SearchProductService(), server)
    listen_addr = "[::]:50053"
    server.add_insecure_port(listen_addr)
    print("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())
