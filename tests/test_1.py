from pyldplayer._internal.cliProcess import ldprocess
from pyldplayer.core.console_instance import LDConsoleInstance

def test_1():
    x = LDConsoleInstance(
        proc=ldprocess(),
        id=1,
        name="test",
        top_window_handle=1,
        bind_window_handle=1,
        pid=1,
        vbox_pid=1
    )

    y = LDConsoleInstance(
        proc=ldprocess(),
        id=1,
        name="test",
        top_window_handle=3,
        bind_window_handle=3,
        pid=3,
        vbox_pid=3
    )

    assert x is y
    assert x.top_window_handle == y.top_window_handle == 3
    assert x.bind_window_handle == y.bind_window_handle == 3
    assert x.pid == y.pid == 3
    assert x.vbox_pid == y.vbox_pid == 3
