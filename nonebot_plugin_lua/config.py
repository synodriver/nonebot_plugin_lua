from typing import Callable, Optional, Tuple
from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    encoding: Optional[str] = None  # enable python funcs that return bytes
    source_encoding: Optional[str] = None
    attribute_filter: Optional[Callable] = None
    attribute_handlers: Optional[Tuple[Callable, Callable]] = None
    register_eval: bool = True
    unpack_returned_tuples: bool = False
    register_builtins: bool = True
    overflow_handler: Optional[Callable] = None

    class Config:
        extra = "ignore"

plugin_config = Config(**get_driver().config.dict())