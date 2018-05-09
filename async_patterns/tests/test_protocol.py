import asyncio
import functools
import logging
#logging.basicConfig(level=logging.DEBUG)

import pytest
import async_patterns.protocol

class To:
    def __init__(self):
        self.response_to = None

    async def __call__(self, proto):
        print(self.__class__)
        f = From()
        f.response_to = self.message_id
        proto.write(f)

class ToError:
    async def __call__(self, proto):
        print(self.__class__)
        raise Exception(self.__class__)

class ToSlow:
    async def __call__(self, proto):
        print(self.__class__)
        await asyncio.sleep(100)

class From:
    async def __call__(self, _):
        print(self.__class__)

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

@pytest.mark.asyncio
async def test(event_loop):
    print()

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("").setLevel(logging.DEBUG)
    logging.getLogger("async_patterns").setLevel(logging.DEBUG)

    loop = event_loop
    server = await loop.create_server(functools.partial(ServerProtocol, loop), port=0)
    addr = server.sockets[0].getsockname()
    host = addr[0]
    port = addr[1]
    
    print('serving on', addr)
    print('wait for server start')
    await asyncio.sleep(1)

    print(f'try connecting to {host} port {port}')
    _, client = await loop.create_connection(functools.partial(ClientProtocol, loop), host, port)
    print(f'conencted')

    print('client write')
    resp = await client.write(To())

    print('resp =', resp)

    client.write(ToError())
    client.write(ToSlow())
    
    await asyncio.sleep(1)
    
    print(sp.queue_packet_acall)

    await sp.close()

    server.close()
    await server.wait_closed()


