async_patterns
==============

.. image:: https://travis-ci.org/chuck1/async_patterns.svg?branch=master
    :target: https://travis-ci.org/chuck1/async_patterns
.. image:: https://codecov.io/gh/chuck1/async_patterns/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/chuck1/async_patterns
.. image:: https://img.shields.io/pypi/v/async_patterns.svg
    :target: https://pypi.python.org/pypi/async_patterns
.. image:: https://readthedocs.org/projects/async_patterns/badge/?version=latest
   :target: http://async_patterns.readthedocs.io
   :alt: Documentation Status
.. image:: https://img.shields.io/pypi/pyversions/async_patterns.svg
   :target: https://pypi.python.org/pypi/async_patterns

Useful python patterns using async.

The module contains the following submodules:

- callbacks_
- coro_queue_
- protocol_

.. _callbacks: http://async-patterns.readthedocs.io/en/latest/module/callbacks.html
.. _coro_queue: http://async-patterns.readthedocs.io/en/latest/module/coro_queue.html
.. _protocol: http://async-patterns.readthedocs.io/en/latest/module/protocol.html

Install
-------

::

    pip3 install async_patterns

Test Source
-----------

::

    git clone git@github.com:chuck1/async_patterns
    cd async_patterns
    pip3 install -e .
    pytest

Examples
--------

.. testsetup::

    import asyncio
    import functools
    from async_patterns import Callbacks
    from async_patterns.coro_queue import CoroQueue

    loop = asyncio.get_event_loop()

Callbacks
~~~~~~~~~

Code:

.. testcode::
   
    cb = Callbacks()
    
    l = []

    def func(a): print(a)
    
    cb.add_callback(functools.partial(func, 1))
    cb.add_callback(functools.partial(func, 2))
    
    cb()

Output:

.. testoutput::

    1
    2

Code:

.. testcode::

    cb = Callbacks()
    
    l = []

    async def func(a): print(a)
    
    cb.add_callback(functools.partial(func, 1))
    cb.add_callback(functools.partial(func, 2))
    
    loop.run_until_complete(cb.acall())

Output:

.. testoutput::

    1
    2

CoroQueue
~~~~~~~~~

.. testcode::

    async def a(i):
        await asyncio.sleep(1)
        print(i)

    async def b(i):
        print(i)

    q = CoroQueue(loop)

    q.schedule_run_forever()

    q.put_nowait(a, 1)
    q.put_nowait(b, 2)
    
    loop.run_until_complete(q.join())

    loop.run_until_complete(q.close())

.. testoutput::

    1
    2




