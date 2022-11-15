# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Union

try:
    from lupa import LuaRuntime
except:
    from lupa.lua import LuaRuntime  # custom build
from nonebot import Config


def _add_lua_config(self: Config, path: Union[str, Path]):
    lua = LuaRuntime()
    with open(path, "r", encoding="utf-8") as f:
        lua.execute(f.read())
    lua_conf = lua.globals()
    for k, v in lua_conf.items():
        if k.isupper() and not k.startswith("_"):
            setattr(self, k.lower(), v)


def monkey_patch():
    Config.add_lua_config = _add_lua_config
