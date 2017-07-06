
import asyncio

import async_patterns.coro_queue

async def a():
    await asyncio.sleep(1)

async def b(*args):
    await asyncio.sleep(1)

def test(loop):

    q = async_patterns.coro_queue.CoroQueue(loop)

    q.schedule_run_forever()

    q.put_nowait(a)
    q.put_nowait(b, 0)

    loop.run_until_complete(q.join())    

