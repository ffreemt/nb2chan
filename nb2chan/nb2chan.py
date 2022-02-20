"""Test personal push service."""
# pylint: disable=invalid-name
# from quart import request

import platform
import pendulum
from fastapi import Security, Depends, HTTPException, status

# from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader, APIKeyQuery

# from contextvars import ContextVar
import logzero
from logzero import logger

import nonebot

# from aiocqhttp.exceptions import Error as CQHttpError

from .config import Settings

settings_nb2chan = Settings()

# logzero.loglevel(20) to suppress noisy debug messags
logzero.loglevel(10)

try:
    app = nonebot.get_asgi()
except ValueError as e:
    logger.error(e)
    if "Nonebot" in str(e):
        logger.warning("Do import 'nonebot; nonebot.init()' before import nb2chan")
        raise SystemExit(e) from e
    raise
# app.fastapi_openapi_url = "/openapi.json"

node = platform.node()

# may use other methods (e.g., sqlite, redis etc.)
API_TOKENS = settings_nb2chan.token_list

logger.debug("API_TOKENS: %s", API_TOKENS)
logger.info(
    """
    To see nb2chan in action:
    curl "127.0.0.1:8680/nb2chan/?Token=DEMO_TOKEN&qq=1234&msg=hello" """
)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/", StaticFiles(directory="static"), name="root")

api_key_header_ = APIKeyHeader(name="Token", auto_error=False)
api_key_query_ = APIKeyQuery(name="Token", auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query_),
    api_key_header: str = Security(api_key_header_),
    # api_key_cookie: str = Security(api_key_cookie),
):
    """Retrieve api key."""
    logger.debug("api_key_query: %s", api_key_query)
    logger.debug("api_key_header: %s", api_key_header)
    if api_key_query in API_TOKENS:
        logger.debug("valid Token provided in query")
        return api_key_query

    if api_key_header in API_TOKENS:
        logger.debug("valid Token provided in headers")
        return api_key_header

    # elif api_key_cookie == API_KEY:
    # return api_key_cookie
    # else:

    logger.debug("no valid Token provided, raising exception")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unable to validate Token",
    )


@app.get("/")
async def landing():
    """Define landing page."""
    return "Hello nb2chan!"


@app.get("/nb2chan/")
async def nb2chan(
    token: str = Depends(get_api_key),  # pylint: disable=unused-argument  # where to use token?
    qq: str = None,
    msg: str = None,
):
    """Define fastapi query.

    openapi docs at: /docs

    ```bash
    http -v "http://.../nb2chan/?Token=DEMO_TOKEN&qq=123&msg=hello world"

    # send Token via HEADERS
    http -v "http://.../nb2chan/?qq=123&msg=hello world" "token: DEMO_TOKEN"
    curl "http://.../nb2chan/?qq=123&msg=hello world" -H "token: DEMO_TOKEN"
    ```
    """
    try:
        bot = nonebot.get_bot()
    except Exception as exc:
        logger.debug(exc)

        # if not bot:
        _ = "Unable to acquire bot, exiting...(go-cghttp正常运行？ ws://127.0.0.1:端口/onebot/v11/ws 端口对不对？)"
        logger.warning(_)
        return {"error": f"{node}: {_}"}

    if not qq:
        return {"error": "qq# required（e.g. ...&qq=123456...）, 否则发给谁呢？"}

    if msg:
        query = str(msg)
    else:
        query = ""

    msg = f"{node} seen msg: {query}"
    try:
        # await bot.send_private_msg(user_id=41947782, message=msg)
        await bot.send_private_msg(user_id=f"{qq}", message=msg)
        _ = pendulum.now().in_timezone("Asia/Shanghai").format("YYYY-MM-DD HH:mm:ss z")
        res = {"success": f"'{msg}' sent to {qq} {_}"}
    except Exception as exc:
        logger.error(exc)
        # logger.exception(exc)
        msg = f"{node} exc: {exc}, (大佬这个qq号[{qq}]加机器人好友了吗？ 没加的话用不了nb2酱。)"
        res = {"error": msg}

    return res
