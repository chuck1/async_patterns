import asyncio
import functools

import async_patterns.protocol

class Packet:
    pass

sp = None

class ServerProtocol(async_patterns.protocol.Protocol):
    def __init__(self, loop):
        global sp
        print(self.__class__)
        super(ServerProtocol, self).__init__(loop)
        sp = self

class ClientProtocol(async_patterns.protocol.Protocol):
    def __init__(self, loop):
        print(self.__class__)
        super(ClientProtocol, self).__init__(loop)

async def atest(loop):
    server = await loop.create_server(functools.partial(ServerProtocol, loop), port=0)
    port = server.sockets[0].getsockname()[1]
    
    print('wait for server start')
    await asyncio.sleep(4)
    
    _, client = await loop.create_connection(functools.partial(ClientProtocol, loop), 'localhost', port)
    
    client.write(Packet)
    
    await sp.close()

    server.close()
    await server.wait_closed()

def test(loop):
    loop.run_until_complete(atest(loop))

