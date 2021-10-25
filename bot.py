"""Bootstrap the bot."""
import nonebot

from nonebot.adapters.cqhttp import Bot as CQHTTPBot

config = {
    "host": "0.0.0.0",
    "port": 8680,
    "debug": True,
    "nickname": {"elf", },
    "apscheduler.timezone": "Asia/Shanghai",
}

nonebot.init(**config)

import nb2chan  # pylint: disable=wrong-import-position, unused-import  # noqa
# 或不用 import nb2chan，而用 load_plugin， 例如
# nonebot.load_plugin("nb2chan")

driver = nonebot.get_driver()

driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_builtin_plugins()

# import nb2chan.autohelp  # pylint: disable=wrong-import-position, unused-import  # noqa
# nonebot.load_plugin("nb2chan.autohelp")

nonebot.load_plugin("nb2chan.mecho")

app = nonebot.get_asgi()


if __name__ == "__main__":
    nonebot.run(app="bot:app")

    # or
    # uvicorn --host 0.0.0.0 --port 8680 bot:app

    # to test
    # curl "127.0.0.1:8680/nb2chan/?Token=DEMO_TOKEN&qq=1234&msg=hello"
