import asyncio
from concurrent.futures import CancelledError
import pytest
import async_patterns.coro_queue

async def a(a1=1):
    try:
        await asyncio.sleep(a1)
        print('a finished')
    except CancelledError:
        print('a cancelled')

async def b(*args):
    try:
        await asyncio.sleep(1)
        print('b finished')
    except CancelledError:
        print('b cancelled')

async def c(*args, **kwargs):
    try:
        await asyncio.sleep(1)
        print('c finished')
    except CancelledError:
        print('c cancelled')

async def d():
    await asyncio.sleep(1)
    raise Exception()

@pytest.mark.asyncio
async def test1(event_loop):
    q = async_patterns.coro_queue.CoroQueue(event_loop)

    q.schedule_run_forever()

    q.put_nowait(a)
    q.put_nowait(b, 0)
    q.put_nowait(c, 0, a=1)
    q.put_nowait(d)
    
    await q.join()

    await q.close()

@pytest.mark.asyncio
async def test2(event_loop):

    q = async_patterns.coro_queue.CoroQueue(event_loop)

    q.schedule_run_forever()

    q.put_nowait(a, 10)
    q.put_nowait(a, 10)
    q.put_nowait(a, 10)
    
    await asyncio.sleep(1)

    print('close')
    await q.close()


