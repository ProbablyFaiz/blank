import sys
import traceback

import ipdb
import rich_click
from rich.console import Console
from rich.traceback import Traceback

import blanket.io.env as env

USE_DEBUG_MODE = env.getenv("BLANKET_USE_DEBUG_MODE", "0") == "1"
USE_RICH_TRACEBACK = env.getenv("BLANKET_USE_RICH_TRACEBACK", "0") == "1"


def excepthook(type, value, tb):
    if issubclass(type, KeyboardInterrupt):
        sys.__excepthook__(type, value, tb)
        return
    if USE_RICH_TRACEBACK:
        traceback_console = Console(stderr=True)
        traceback_console.print(
            Traceback.from_exception(type, value, tb),
        )
    else:
        traceback.print_exception(type, value, tb)
    if USE_DEBUG_MODE:
        ipdb.post_mortem(tb)


def command(*args, **kwargs):
    context_settings = kwargs.get("context_settings", {})
    if "show_default" not in context_settings:
        context_settings["show_default"] = True
    kwargs["context_settings"] = context_settings

    def decorator(f):
        sys.excepthook = excepthook
        return rich_click.command(*args, **kwargs)(f)

    return decorator


def group(*args, **kwargs):
    context_settings = kwargs.get("context_settings", {})
    if "show_default" not in context_settings:
        context_settings["show_default"] = True
    kwargs["context_settings"] = context_settings

    def decorator(f):
        sys.excepthook = excepthook
        return rich_click.group(*args, **kwargs)(f)

    return decorator


def __getattr__(name):
    return getattr(rich_click, name)
