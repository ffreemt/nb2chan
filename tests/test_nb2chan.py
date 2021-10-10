"""Test nb2chan."""
from nb2chan import __version__
from nb2chan import nb2chan


def test_version():
    """Test version."""
    assert __version__ == "0.1.0"


def test_sanity():
    """Sanity check."""
    try:
        assert not nb2chan()
    except Exception:
        assert True
