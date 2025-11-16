# -*- coding: utf-8 -*-
import asyncio
from typing import Union
from functools import partial

from nonebot import get_driver
from nonebot import on_command, on_notice
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, Event, Message, MessageEvent
from nonebot.params import CommandArg
from nonebot.typing import T_State

try:
    from lupa import LuaError, LuaRuntime
except:
    from lupa.lua import LuaRuntime, LuaError  # custom build

from .patch_bot import Bot as _Bot
from .config import plugin_config
from .utils import handle_lua_thread

lua_on_notice = on_notice()


def ensure_name(name: str) -> Union[str, bytes]:
    if plugin_config.encoding is None:
        return name.encode()
    else:
        return name


on_notice_code: str = ""


@lua_on_notice.handle()
async def handle_on_notice(bot: Bot, event: Event, state: T_State):
    lua = LuaRuntime()
    if on_notice_code:
        try:
            lua.execute(on_notice_code)
            func = lua.globals()["on_notice"]
            if func and callable(func):
                co = func.coroutine(_Bot(bot), event, state)
                await handle_lua_thread(co)
        except LuaError as e:
            await bot.send(event, str(e))


matcher = on_command("修改on_notice")


@matcher.handle()
async def _(bot: Bot, event: Event, cmd: Message = CommandArg()):
    global on_notice_code
    on_notice_code = cmd.extract_plain_text()
    await bot.send(event, "修改成功")


matcher2 = on_command("查看on_notice")


@matcher2.handle()
async def _(bot: Bot, event: Event, cmd: Message = CommandArg()):
    global on_notice_code
    await bot.send(event, on_notice_code)


matcher3 = on_command("runlua", rule=to_me())


async def reply(bot: Bot, event, msg):
    return await bot.send(event, msg.decode() if isinstance(msg, bytes) else msg)


@matcher3.handle()
async def _(bot: Bot, event: MessageEvent, cmd: Message = CommandArg()):
    lua = LuaRuntime(**plugin_config.dict())  # type: ignore
    _G = lua.globals()
    if event.get_user_id() in get_driver().config.superusers:
        _G[ensure_name("bot")] = _Bot(bot)
        _G[ensure_name("reply")] = partial(reply, bot, event)
    try:
        f = lua.eval(cmd.extract_plain_text())
        co = f.coroutine()
        # task = co.send(None)
        # if asyncio.iscoroutine(task):
        #     ret = await task
        # else:
        #     ret = task # coro end, this is return value 根本就不是协程的屑函数
        await handle_lua_thread(co)
    except LuaError as e:
        if not str(e):
            await bot.send("py异常被吞, see https://github.com/scoder/lupa/issues/144")
        await bot.send(event, str(e))
