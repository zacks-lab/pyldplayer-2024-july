
from typing import Optional

from pydantic import BaseModel, Field


class WindowsOrigin(BaseModel):
    x: int
    y: int


class WindowsOffset(BaseModel):
    x: int
    y: int

class LeidiansCfg(BaseModel):
    languageId: Optional[str] = None
    productLanguageId: Optional[str] = None
    channelOpenId: Optional[str] = None
    channelLastOpenId: Optional[str] = None
    reduceAudio: Optional[bool] = None
    isSSD: Optional[bool] = None
    fromInstall: Optional[bool] = None
    strp: Optional[str] = None
    lastZoneArea: Optional[str] = None
    lastZoneName: Optional[str] = None
    vipMode: Optional[bool] = None
    hyperOptime: Optional[str] = None
    isBaseboard: Optional[bool] = None
    basicSettings_lastIP: Optional[str] = Field(None, alias='basicSettings.lastIP')
    nextCheckupdateTime: Optional[int] = None
    noiceUserRed: Optional[bool] = None
    isFirstInstallApk: Optional[bool] = None
    hasPluginLast: Optional[bool] = None
    cloneFromSmallDisk: Optional[bool] = None
    framesPerSecond: Optional[int] = None
    displayMode: Optional[bool] = None
    vmdkFastMode: Optional[bool] = None
    windowsAlignType: Optional[int] = None
    windowsRowCount: Optional[int] = None
    windowsAutoSize: Optional[bool] = None
    sortwndnotoutscreen: Optional[bool] = None
    moreScreenSortInSame: Optional[bool] = None
    windowsOrigin: Optional[WindowsOrigin] = None
    windowsOffset: Optional[WindowsOffset] = None
    batchStartInterval: Optional[int] = None
    batchNewCount: Optional[int] = None
    batchCloneCount: Optional[int] = None
    windowsRecordPos: Optional[bool] = None
    mulTab: Optional[bool] = None
    exitFullscreenEsc: Optional[bool] = None
    disableMouseRightOpt: Optional[bool] = None
    remoteEntranceVersion: Optional[int] = None
    multiPlayerSort: Optional[int] = None
    operaterSort: Optional[int] = None
