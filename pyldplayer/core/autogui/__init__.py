
import time

from time import sleep
from pyldplayer.core.autogui.operationRecorder import LDOperationRecorder
from pyldplayer.core.console import LDConsole, LDConsoleInstance
import typing
import pygetwindow as gw
import pyautogui as pg

from pyldplayer.utils.gui import activate_wnd

class LDAutoGui:
    def __init__(self, ld : LDConsole):
        self.__player : LDConsole = ld
        
    def __getitem__(self, id : typing.Union[str, int]) -> 'LDAutoGuiInstance':
        """
        Retrieves an 'LDAutoGuiInstance' object associated with the given 'id' from the '__player' dictionary.

        Parameters:
            id (Union[str, int]): The identifier of the 'LDAutoGuiInstance' object to retrieve.

        Returns:
            LDAutoGuiInstance: The 'LDAutoGuiInstance' object associated with the given 'id'.

        Raises:
            RuntimeError: If the 'id' is not found in the '__player' dictionary.
        """
        instance : LDConsoleInstance = self.__player[id]
        
        if not instance.isrunning():
            raise RuntimeError("instance is not running")

        for w in gw.getAllWindows():
            w : gw.Window
            if w._hWnd == instance.top_window_handle:
                return LDAutoGuiInstance(w)
    
        raise RuntimeError("instance is not running")
    
    def waitFor(self, id : typing.Union[str, int], maxwait : int = 30) -> 'LDAutoGuiInstance':
        """
        Waits for the specified ID to be running and returns an instance of 'LDAutoGuiInstance' associated with it.
        
        Parameters:
            id (Union[str, int]): The ID of the instance to wait for.
            maxwait (int, optional): The maximum time in seconds to wait for the instance to start running. 
            Defaults to 30.
            
        Returns:
            LDAutoGuiInstance: An instance of 'LDAutoGuiInstance' associated with the specified ID.
            
        Raises:
            RuntimeError: If the instance does not start running within the specified 'maxwait' time.
            RuntimeError: If the instance is not running.
        """
        instance : LDConsoleInstance = self.__player[id]
        starttime = time.time()
        
        while not instance.isrunning():
            if time.time() - starttime > maxwait:
                raise RuntimeError("instance is not running")
            time.sleep(0.1)
            
        for w in gw.getAllWindows():
            w : gw.Window
            if w._hWnd == instance.top_window_handle:
                return LDAutoGuiInstance(w)
            
        raise RuntimeError("instance is not running")
        
    
class LDAutoGuiInstance:
    def __init__(self, wnd : gw.Window):
        self.__window = wnd
        
    @property
    def window(self):
        """
        Returns the 'gw.Window' object associated with the 'LDAutoGuiInstance' object.

        :return: The 'gw.Window' object associated with the 'LDAutoGuiInstance' object.
        :rtype: gw.Window
        """
        return self.__window
        
    @property
    def windowRect(self):
        """
        Return the rectangle representing the position and size of the window.

        :return: A tuple containing the left, top, width, and height values of the window rectangle.
        :rtype: tuple[int, int, int, int]
        """
        return (
            self.__window.left, 
            self.__window.top, 
            self.__window.width, 
            self.__window.height
        )

    def __windowTrimMenu(self, val : int = 40):
        """
        Trim the window rectangle by the given value.
        """
        return (
            self.__window.left, 
            self.__window.top + val, 
            self.__window.width - val, 
            self.__window.height - val
        )
        
    def __activate_wnd(self):
        activate_wnd(self.__window)

    def volumeUp(self):
        """
        Increase the volume.
        """
        self.__activate_wnd()
        with pg.hold("ctrl"):
            pg.press("+")

    def volumeDown(self):
        """
        Decrease the volume.
        """

        self.__activate_wnd()
        with pg.hold("ctrl"):
            pg.press("-")

    def fullscreen(self):
        self.__activate_wnd()
        pg.hotkey("f11")

    def operationRecorder(self, parse : bool = True):
        self.__activate_wnd()
        
        # ctrl + 8
        with pg.hold("ctrl"):
            pg.press("8")

        if not parse:
            return
        
        sleep(0.2)
        
        return LDOperationRecorder(self.__window)
        
    def installApkDialog(self):
        # ctrl +3
        self.__activate_wnd()
        with pg.hold("ctrl"):
            pg.press("3")

    def nativeScreenshot(self):
        # ctrl + 0
        self.__activate_wnd()
        with pg.hold("ctrl"):
            pg.press("0")

    def screenshot(self, trimBoundary : int = 40):
        self.__activate_wnd()
        return pg.screenshot(region=self.__windowTrimMenu(trimBoundary))

    def shake(self):
        # ctrl + 6
        self.__activate_wnd()
        with pg.hold("ctrl"):
            pg.press("6")

    def sharedFolder(self):
        # ctrl + 5
        self.__activate_wnd()
        with pg.hold("ctrl"):
            pg.press("5")

    def virtualGpsDialog(self):
        # ctrl + 7 
        self.__activate_wnd()
        with pg.hold("ctrl"):
            pg.press("7")

    def clickAt(
        self,
        x, y,
        trimBoundary : int = 40,
        method : typing.Callable = pg.click
    ):
        rect = self.__windowTrimMenu(trimBoundary)
        
        x = rect[0] + x
        y = rect[1] + y
        
        method(x, y)
        
    def locateAt(
        self,
        img : str,
        trimBoundary : int = 40,
        method : typing.Callable = pg.click
    ):
        rect = self.__windowTrimMenu(trimBoundary)
        
        x, y = pg.locateCenterOnScreen(img, region=rect)
        
        x = rect[0] + x
        y = rect[1] + y
        
        method(x, y)
        
        
        