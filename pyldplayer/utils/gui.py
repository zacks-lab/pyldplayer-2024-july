from time import sleep
import pygetwindow as gw
def activate_wnd(window : gw.Window):
    if window.isActive:
        return
    error = False
    try:
        window.activate()
    except Exception:
        error = True

    if error:
        sleep(0.2)
        try:
            window.activate()
        except Exception:
            pass
    sleep(0.2)