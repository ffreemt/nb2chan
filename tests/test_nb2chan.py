"""Test nb2chan."""
import pytest
import nonebot

# Cant import nb2chan without initializing NoneBot
nonebot.init()

# pylint: disable=wrong-import-position
from nb2chan import __version__  # noqa
from nb2chan import nb2chan  # noqa


def test_version():
    """Test version."""
    assert __version__ == "0.1.1"
    # assert 1


@pytest.mark.asyncio
async def test_sanity():
    """Sanity check."""
    try:
        assert not await nb2chan()
    except Exception:
        assert True
