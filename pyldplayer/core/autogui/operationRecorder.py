import os
import typing
import pygetwindow as gw
import pyautogui as pg
from pyldplayer.utils.gui import activate_wnd

class LDOperationRecorder:
    def __startRecordingFind(self, center : bool = False):
        activate_wnd(self.__window)
        startRecordingFind = pg.locateOnScreen(
            os.path.join(os.path.dirname(__file__), "startRecording.png"), 
        )
        
        if center:
            return pg.center(startRecordingFind)
        return startRecordingFind
    
    def __init__(self, wnd : gw.Window):
        self.__window = wnd
        if self.__startRecordingFind() is None:
            raise RuntimeError("Correct Window Not Found")
        
    def __currentRect(self):
        activate_wnd(self.__window)
        startRecordingCoord = pg.locateCenterOnScreen(
            os.path.join(os.path.dirname(__file__), "startRecording.png"
        ))

        """
        left - 100
        top + 50
        width = 500
        height = 550
        """
        return (
            startRecordingCoord.x - 100,
            startRecordingCoord.y - 30,
            500,
            500
        )
        
        
    def locateIndex(self, index : int = 0):
        """
        this is a faster method but it is unable to identify the index beyond 8
        """
        
        runScriptIconPath = os.path.join(os.path.dirname(__file__), "runScript.png")
        
        pg.screenshot(region=self.__currentRect()).show()
        
        res = []
        for v in pg.locateAllOnScreen(runScriptIconPath, region=self.__currentRect()):
            res.append(v)
        
        if index <= 8 and len(res) > index:
            return res[index-1]

        return None
    
    def runScript(self, key : typing.Union[str, int]):
        if isinstance(key, int):
            box = self.locateIndex(key)
            return pg.click(*pg.center(box))
            
        raise NotImplementedError
    