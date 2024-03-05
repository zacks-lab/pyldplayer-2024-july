from pydantic import BaseModel
from typing import Optional

from pyldplayer._models.files.basic import WidthHeight, Hotkey

class PropertySettings(BaseModel):
    phoneIMEI: Optional[str] = None
    phoneIMSI: Optional[str] = None
    phoneSimSerial: Optional[str] = None
    phoneAndroidId: Optional[str] = None
    phoneModel: Optional[str] = None
    phoneManufacturer: Optional[str] = None
    macAddress: Optional[str] = None
    phoneNumber: Optional[str] = None

class StatusSettings(BaseModel):
    sharedApplications: Optional[str] = None
    sharedPictures: Optional[str] = None
    sharedMisc: Optional[str] = None
    playerName: Optional[str] = None
    closeOption: Optional[int] = None

class BasicSettings(BaseModel):
    left: Optional[int] = None
    top: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    realHeigh: Optional[int] = None
    realWidth: Optional[int] = None
    networkEnable: Optional[bool] = None
    isForstStart: Optional[bool] = None
    mulFsAddSize: Optional[int] = None
    mulFsAutoSize: Optional[int] = None
    verticalSync: Optional[bool] = None
    fsAutoSize: Optional[int] = None
    noiceHypeVOpen: Optional[bool] = None
    autoRun: Optional[bool] = None
    rootMode: Optional[bool] = None
    heightFrameRate: Optional[bool] = None
    adbDebug: Optional[int] = None
    autoRotate: Optional[bool] = None
    isForceLandscape: Optional[bool] = None
    standaloneSysVmdk: Optional[bool] = None
    lockWindow: Optional[bool] = None
    disableMouseFastOpt: Optional[bool] = None
    cjztdisableMouseFastOpt_new: Optional[int] = None
    HDRQuality: Optional[int] = None
    qjcjdisableMouseFast: Optional[int] = None
    fps: Optional[int] = None
    astc: Optional[bool] = None
    videoQuality: Optional[int] = None

class NetworkSettings(BaseModel):
    networkEnable: Optional[bool] = None
    networkSwitching: Optional[bool] = None
    networkStatic: Optional[bool] = None
    networkAddress: Optional[str] = None
    networkGateway: Optional[str] = None
    networkSubnetMask: Optional[str] = None
    networkDNS1: Optional[str] = None
    networkDNS2: Optional[str] = None
    networkInterface: Optional[str] = None

class AdvancedSettings(BaseModel):
    resolution: Optional[WidthHeight] = None
    resolutionDpi: Optional[int] = None
    cpuCount: Optional[int] = None
    memorySize: Optional[int] = None
    micphoneName: Optional[str] = None
    speakerName: Optional[str] = None

class HotkeySettings(BaseModel):
    backKey: Optional[Hotkey] = None
    homeKey: Optional[Hotkey] = None
    appSwitchKey: Optional[Hotkey] = None
    menuKey: Optional[Hotkey] = None
    zoomInKey: Optional[Hotkey] = None
    zoomOutKey: Optional[Hotkey] = None
    bossKey: Optional[Hotkey] = None
    shakeKey: Optional[Hotkey] = None
    operationRecordKey: Optional[Hotkey] = None
    fullScreenKey: Optional[Hotkey] = None
    showMappingKey: Optional[Hotkey] = None
    videoRecordKey: Optional[Hotkey] = None
    mappingRecordKey: Optional[Hotkey] = None
    keyboardModelKey: Optional[Hotkey] = None

class LeidianCfg(BaseModel):
    propertySettings: Optional['PropertySettings'] = None
    statusSettings: Optional['StatusSettings'] = None
    basicSettings: Optional['BasicSettings'] = None
    networkSettings: Optional['NetworkSettings'] = None
    advancedSettings: Optional['AdvancedSettings'] = None
    hotkeySettings: Optional['HotkeySettings'] = None
