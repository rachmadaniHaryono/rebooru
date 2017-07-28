import os


def test_run_plugins():
    from rebooru import plugin
    res = plugin.run_plugins()
    assert len(res) > 1
