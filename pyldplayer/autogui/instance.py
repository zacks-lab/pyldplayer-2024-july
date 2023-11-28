
from pyldplayer.console.player import LDConsoleInstance
import pygetwindow as gw
import pyautogui as pg

class LDAutoInstance:

    __window : gw.Window
    __console_instance : LDConsoleInstance

    @property
    def window_rect(self):
        """
        Return the rectangle representing the position and size of the window.

        :return: A tuple containing the left, top, width, and height values of the window rectangle.
        :rtype: tuple[int, int, int, int]
        """
        return (self.__window.left, self.__window.top, self.__window.width, self.__window.height)

    def __init__(self, ldinstance: LDConsoleInstance):
        """
        Initializes the class with an LDConsoleInstance object.

        Parameters:
            ldinstance (LDConsoleInstance): An instance of the LDConsoleInstance class.

        Raises:
            RuntimeError: If the LDConsoleInstance is not running or if the window is not found.
        """
        if not ldinstance.isrunning():
            raise RuntimeError("instance is not running")
        self.__console_instance = ldinstance

        # get window
        win_list = [x for x in gw.getAllWindows() if x._hWnd == ldinstance.top_window_handle]
        if len(win_list) == 0:
            raise RuntimeError("window not found")
        self.__window = win_list[0]

    def volumeUp(self):
        """
        Increase the volume.
        """
        self.__window.activate()
        with pg.hold("ctrl"):
            pg.press("+")

    def volumeDown(self):
        """
        Decrease the volume.
        """

        self.__window.activate()
        with pg.hold("ctrl"):
            pg.press("-")

    def fullscreen(self):
        self.__window.activate()
        pg.hotkey("f11")

    def operationRecorder(self):
        self.__window.activate()
        # ctrl + 8
        with pg.hold("ctrl"):
            pg.press("8")

    def installApkDialog(self):
        # ctrl +3
        self.__window.activate()
        with pg.hold("ctrl"):
            pg.press("3")

    def nativeScreenshot(self):
        # ctrl + 0
        self.__window.activate()
        with pg.hold("ctrl"):
            pg.press("0")

    def screenshot(self):
        self.__window.activate()
        return pg.screenshot(region=self.window_rect)

    def shake(self):
        # ctrl + 6
        self.__window.activate()
        with pg.hold("ctrl"):
            pg.press("6")

    def sharedFolder(self):
        # ctrl + 5
        self.__window.activate()
        with pg.hold("ctrl"):
            pg.press("5")

    def virtualGpsDialog(self):
        # ctrl + 7 
        self.__window.activate()
        with pg.hold("ctrl"):
            pg.press("7")
