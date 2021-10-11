# nb2chan
[![tests](https://github.com/ffreemt/nb2chan/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/nb2chan/actions)[![nonebot2](https://img.shields.io/static/v1?label=nonebot&message=v2.0.0a16&color=green)](https://v2.nonebot.dev/)[![cqhttp](https://img.shields.io/static/v1?label=driver&message=cqhttp&color=green)](https://v2.nonebot.dev/guide/cqhttp-guide.html)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/nb2chan.svg)](https://badge.fury.io/py/nb2chan)

nonebot2酱（推送服务插件）nonebot2chan (push service plugin)

## Install it

```shell
# x pip install nb2chan
# x or poetry add nb2chan

pip install git+https://github.com/ffreemt/nb2chan
# or poetry add git+https://github.com/ffreemt/nb2chan

# git clone https://github.com/ffreemt/nb2chan && cd nb2chan && poetry  install --nodev

# To upgrade
# x pip install nb2chan -U
# x or poetry add nb2chan@latest
```

## Use it
```python
# bot.py
import nonebot
...
nonebot.init()

driver = nonebot.get_driver()

driver.register_adapter("cqhttp", CQHTTPBot)

nonebot.load_from_toml("pyproject.toml")
nonebot.load_plugin("nb2chan")
...
```

* 目标qq号（例如QQ号 1234）加`nonebot2`机器人qq号好友
* `nonebot2`部署至外网`ip`，例如 `uvicorn --host 0.0.0.0 bot:app` (火墙需放行`nonebot2`的端口)
* 给qq号发消息(浏览器地址栏或`curl/httpie`或`python reqests/httpx` 或`云函数`/`claudflare worker` etc.)：
```bash
http://...:port/nb2chan/?Token=DEMO_TOKEN&qq=1234&msg=hello
```
令牌也可在`headers`里设定，例如
```
curl http://...:port/nb2chan/?qq=1234&msg=hello -H "token: DEMO_TOKEN"
http -v "http://...:port/nb2chan/?qq=1234&msg=hello world" "token: DEMO_TOKEN"
```

## 其他
`nb2chan`采用简单令牌鉴权。 有效令牌可在 `.env.nb2chan` 里设定。 默认有效令牌为`['DEMO_TOKEN', 'SECRET_TOKEN']` (参看`config.py`）
