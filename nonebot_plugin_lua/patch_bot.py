# -*- coding: utf-8 -*-
from functools import partial
from nonebot.adapters.onebot.v11 import Bot as OneBot
try:
    from lupa import unpacks_lua_table_method, unpacks_lua_table
except ImportError:
    from lupa.lua import unpacks_lua_table_method, unpacks_lua_table


class Bot:
    def __init__(self, bot: OneBot):
        self._bot = bot

    def __getattr__(self, item: str):
        if not item.startswith("_"):
            return partial(self.call_api, item)
        else:
            raise AttributeError

    # @unpacks_lua_table_method
    async def call_api(self, *args):
        if len(args) > 1:
            data = dict(
                map(lambda x: (
                x[0].decode() if isinstance(x[0], bytes) else x[0], x[1].decode() if isinstance(x[1], bytes) else x[1]),
                    args[1].items())) # 有kw
        else:
            data = {}
        return await self._bot.call_api(args[0], **data)

    # @unpacks_lua_table_method
    async def send(self, *args, **kwargs):
        return await self._bot.send(args[0],args[1], **kwargs)
