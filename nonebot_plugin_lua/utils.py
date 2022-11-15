# -*- coding: utf-8 -*-
import asyncio
from functools  import wraps
from typing import Set

_all_tasks: Set[asyncio.Task] = set()


def async_to_sync(func):
    @wraps(func)
    def new_func(*args, **kwargs):
        # task = asyncio.create_task(func(*args, **kwargs))
        # _all_tasks.add(task)
        # task.add_done_callback(_all_tasks.discard)
        return asyncio.get_event_loop().run_until_complete(func(*args, **kwargs))
    return new_func


async def wait_lua_tasks_done():
    await asyncio.gather(*_all_tasks)
    for task in _all_tasks:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
