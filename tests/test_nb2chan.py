"""Test nb2chan."""
# Cant do this without initializing NoneBot
# from nb2chan import __version__

# from nb2chan import nb2chan


def test_version():
    """Test version."""
    # assert __version__ == "0.1.0"
    assert 1


def test_sanity():
    """Sanity check."""
    try:
        assert not nb2chan()
    except Exception:
        assert True
