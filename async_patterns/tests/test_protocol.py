import asyncio
import functools

import async_patterns.protocol

class Packet:
    pass

class ServerProtocol(async_patterns.protocol.Protocol):
    pass

class ClientProtocol(async_patterns.protocol.Protocol):
    pass

async def atest(loop):
    server = await loop.create_server(functools.partial(ServerProtocol, loop), port=0)
    port = server.sockets[0].getsockname()[1]
    
    await asyncio.sleep(2)

    _, client = await loop.create_connection(functools.partial(ClientProtocol, loop), 'localhost', port)
    
    client.write(Packet)

    server.close()
    await server.wait_closed()

def test(loop):
    loop.run_until_complete(atest(loop))

