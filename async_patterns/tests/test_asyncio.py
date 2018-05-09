import pytest

async def a():
    raise Exception()

@pytest.mark.asyncio
async def test(event_loop):
    task = event_loop.create_task(a())

    try:
        await task
    except:
        pass
    else:
        raise Exception()


