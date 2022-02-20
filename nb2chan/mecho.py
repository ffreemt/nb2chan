"""Send msg back via echo with hostname attached."""
# pylint: disable=invalid-name, unused-argument
from platform import node

from nonebot.plugin import on_command
from nonebot.typing import T_State

# from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.onebot.v11 import Bot, Event

from logzero import logger

# echo = on_command("echo", to_me())
mecho = on_command(
    "mecho",
    aliases={"ping", "ryt", "在不", "p"},
    priority=1,
)
node_ = node()


@mecho.handle()
# async def handle(bot: Bot, event: MessageEvent, state: dict):
async def handle(bot: Bot, event: Event, state: T_State):
    """Echo with hostname attached."""
    msg = f"{node_}: {event.get_message()}"
    logger.debug(msg)
    try:
        # await bot.send(**_)  # OK
        await bot.send(message=msg, event=event)
    except Exception as e:
        logger.error(e)
