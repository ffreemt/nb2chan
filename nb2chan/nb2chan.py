"""Test personal push service.

curl 127.0.0.1:5580/admin?q=123
curl 127.0.0.1:8680/admin?q=123

# works only on http not https
# works http://127.0.0.1:8680/admin/
# does not work: https://127.0.0.1:8680/admin/

    koyeb-nb2
or
curl externalip:5580/admin?q=123
    if firewall is set open

display 欢迎来到管理页面 q:123
message sent to 41947782: 欢迎来到管理页面 q:123

---
app = nonebot.get_asgi()
@app.get('/')
async def _():
    pass

@bot.server_app.route('/admin')
改成
   @nonebot.get_asgi().get('/admin')
"""
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
from aiocqhttp.exceptions import Error as CQHttpError

from .config import Settings

config = Settings()

# logzero.loglevel(20)
logzero.loglevel(10)

# bots = nonebot.get_bots()
app = nonebot.get_asgi()
node = platform.node()

# API_TOKEN = "SECRET_API_TOKEN"
API_TOKENS = ["DEMO_TOKEN", "SECRET_API_TOKEN"]

# may use other methods (e.g., sqlite, redis etc.)
API_TOKENS = config.token_list

logger.debug("API_TOKENS: %s", API_TOKENS)

# app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/", StaticFiles(directory="static"), name="root")

api_key_header = APIKeyHeader(name="Token", auto_error=False)
api_key_query = APIKeyQuery(name="Token", auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    # api_key_cookie: str = Security(api_key_cookie),
):
    """Retrieve api key."""
    logger.debug("api_key_query: %s", api_key_query)
    logger.debug("api_key_header: %s", api_key_header)
    if api_key_query in API_TOKENS:
        logger.debug("valid Token provided in query")
        return api_key_query
    elif api_key_header in API_TOKENS:
        logger.debug("valid Token provided in headers")
        return api_key_header
    # elif api_key_cookie == API_KEY:
    # return api_key_cookie
    else:
        logger.debug("no valid Token provided, raising exception")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to validate Token",
        )


@app.get("/nb2chan/")
async def nb2chan(
    token: str = Depends(get_api_key),
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
    except Exception as e:
        logger.debug(e)

        # if not bot:
        _ = "Unable to acquire bot, exiting..."
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
    except CQHttpError as exc:
        logger.error(exc)
        # logger.exception(exc)
        msg = f"{node} exc: {exc}, (大佬加机器人好友了吗？ 没加的话用不了nb2酱。)"
        res = {"error": msg}
    except Exception as exc:
        logger.error(exc)
        # logger.exception(exc)
        msg = f"{node} exc: {exc}"
        res = {"error": msg}

    # return f"{msg}"
    return res
