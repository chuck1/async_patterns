import asyncio

class CoroQueue(object):
    """
    A queue of coroutines to be called sequentially.
    """
    def __init__(self, loop):
        self.loop = loop
        self.__queue = asyncio.Queue()

    def schedule_run_forever(self):
        """
        Schedule asyncio to run the consumer loop.
        """
        self.__task_run_forever = self.loop.create_task(self.run_forever())

    async def run_forever(self):
        """
        The consumer loop.
        Loop forever getting the next coroutine in the queue and awaiting it.
        """

        while True:
            coro, future = await self.__queue.get()

            try:
                res = await coro
            except Exception as e:
                res = e

            future.set_result(res)
 
    def put_nowait(self, f, *args):
        """
        Put a coroutine onto the queue.

        :param f: a coroutine function
        :param args: arguments to be passed to the coroutine
        """

        future = self.loop.create_future()
        coro = f(*args)
        
        if not asyncio.iscoroutine(coro):
            raise RuntimeError('{} is not a coroutine'.format(f))
        
        self.__queue.put_nowait((coro, future))

        
        return future

    async def close(self):
        """
        Cancel all pending coroutines.
        """

        self.__task_run_forever.cancel()

        while not self.__queue.empty():
            item = self.__queue.get_nowait()
            coro, future = item
            
            task = self.loop.create_task(coro)

            ret = task.cancel()

            continue

            res = await task

    async def join(self):
        """
        Wait for all coroutines to finish.
        Await the underlying :py:class:`asyncio.Queue` object's join method.
        """
        await self.__queue.join()



