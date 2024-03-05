
from pyldplayer.windows.window import WindowInstance
import pyautogui as pg

class WindowInstanceExtended(WindowInstance):
    def _activateWnd(self):
        self.gwindow.activate()

    def volumeUp(self):
        """
        Increase the volume.
        """
        self._activateWnd()
        with pg.hold("ctrl"):
            pg.press("+")

    def volumeDown(self):
        """
        Decrease the volume.
        """

        self._activateWnd()
        with pg.hold("ctrl"):
            pg.press("-")

    def fullscreen(self):
        self._activateWnd()
        pg.hotkey("f11")

    def operationRecorder(self):
        self._activateWnd()
        
        # ctrl + 8
        with pg.hold("ctrl"):
            pg.press("8")
        
    def installApkDialog(self):
        # ctrl +3
        self._activateWnd()
        with pg.hold("ctrl"):
            pg.press("3")

    def nativeScreenshot(self):
        # ctrl + 0
        self._activateWnd()
        with pg.hold("ctrl"):
            pg.press("0")

    def shake(self):
        # ctrl + 6
        self._activateWnd()
        with pg.hold("ctrl"):
            pg.press("6")

    def sharedFolder(self):
        # ctrl + 5
        self._activateWnd()
        with pg.hold("ctrl"):
            pg.press("5")

    def virtualGpsDialog(self):
        # ctrl + 7 
        self._activateWnd()
        with pg.hold("ctrl"):
            pg.press("7")
            
    