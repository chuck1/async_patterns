import asyncio
import pytest

from async_patterns import Callbacks

def test():
    cb = Callbacks()
    
    l = []

    def func1():
        l.append(1)
    
    def func2():
        l.append(2)
    
    cb.add_callback(func1)
    cb.add_callback(func2)
    
    cb()

    assert l == [1, 2]

@pytest.mark.asyncio
async def test_async(event_loop):
    cb = Callbacks()
    
    l = []

    async def func1():
        l.append(1)
    
    async def func2():
        l.append(2)
    
    cb.add_callback(func1)
    cb.add_callback(func2)
    
    await cb.acall()

    assert l == [1, 2]

