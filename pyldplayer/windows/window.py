
import typing
from pyldplayer._models.process.instanceMeta import InstanceDict
from pyldplayer.process.container import ProcessContainer
from pyldplayer.process.process import BaseProcess
import pygetwindow as gw
import screeninfo

class WindowInstance:
    def __init__(self, idict : InstanceDict):
        if idict["android_started_int"] != 1:
            raise ValueError("Window is not opened")
    
        self.__idict = idict
        self.__window = None
        for w in gw.getAllWindows():
            w : gw.Window
            if w._hWnd == self.__idict["top_window_handle"]:
                self.__window = w

        if not self.__window:
            raise ValueError("Window is not resolved")
        
    def __hash__(self) -> int:
        return hash(self.__idict["id"])

    @property
    def gwindow(self):
        return self.__window

class WindowMgr(ProcessContainer):
    def __init__(self, *arg, path: str = None, process: BaseProcess | type[BaseProcess] = ...) -> None:
        super().__init__(*arg, path=path, process=process)
        self._window_instance_type = WindowInstance
        self.__staging_list : typing.Set[WindowInstance] = set()

    def stage(self, *ids : typing.Union[str, int]):
        for item in self.process.list2():
            if item["id"] in ids:
                self.__staging_list.add(self._window_instance_type(item))

    def stage_opened(self):
        for item in self.process.list2():
            if item["android_started_int"] == 1:
                self.__staging_list.add(self._window_instance_type(item))

    def _get_screen_dimensions(self, monitor_index=0):
        monitors = screeninfo.get_monitors()
        if monitor_index < 0 or monitor_index >= len(monitors):
            raise ValueError("Invalid monitor index")
        monitor = monitors[monitor_index]
        # Return both dimensions and the position of the monitor
        return (monitor.width, monitor.height, monitor.x, monitor.y)

    def _get_monitor_details(self):
        """Fetch details of all monitors"""
        return screeninfo.get_monitors()

    def _find_current_monitor_for_window(self, window_position):
        """Determine which monitor a window is currently on based on its position"""
        for monitor in self._get_monitor_details():
            if (monitor.x <= window_position[0] < monitor.x + monitor.width and
                    monitor.y <= window_position[1] < monitor.y + monitor.height):
                return monitor
        return None  # Fallback if no monitor matches, should be handled appropriately

    def _grid_orientation(self, num_rows, num_columns, monitor_index=0):
        screen_width, screen_height, monitor_x, monitor_y = self._get_screen_dimensions(monitor_index)
        num_windows = len(self.__staging_list)
        if num_windows == 0 or num_rows == 0 or num_columns == 0:
            return  # Early return if invalid input

        window_width = screen_width // num_columns
        window_height = screen_height // num_rows

        for index, window_instance in enumerate(self.__staging_list):
            new_x = (index % num_columns) * window_width + monitor_x  # Adjusted for monitor's horizontal position
            new_y = (index // num_columns) * window_height + monitor_y  # Adjusted for monitor's vertical position
            
            window_instance.gwindow.resizeTo(window_width, window_height)
            window_instance.gwindow.moveTo(new_x, new_y)

            if index == num_rows * num_columns - 1:
                break

    def orientation(self, preset : typing.Union[str, typing.Literal["in_one_line"]], monitor : int = 0):
        
        if len(preset) == 3 and preset[1] == "X" and preset[0].isdigit() and preset[2].isdigit():
            self._grid_orientation(int(preset[0]), int(preset[2]), monitor)
        elif preset == "in_one_line":
            self._grid_orientation(1, len(self.__staging_list), monitor)
        else:
            raise ValueError("Invalid preset")
        
    def resize(self, width : int, height : int):
        for window_instance in self.__staging_list:
            window_instance.gwindow.resizeTo(width, height)

    def move_to_monitor(self, monitor : int = 0):
        new_monitor = self._get_monitor_details()[monitor]  # Target monitor
        if not new_monitor:
            raise ValueError("Invalid monitor index")

        for window_instance in self.__staging_list:
            # Assuming a method to get the current window position exists
            current_window_x, current_window_y = window_instance.gwindow.getPosition()
            
            # Find the monitor where the window currently is
            current_monitor = self._find_current_monitor_for_window((current_window_x, current_window_y))
            if not current_monitor:
                continue  # Skip if the current monitor couldn't be determined
            
            # Calculate the window's relative position to its current monitor
            relative_x = current_window_x - current_monitor.x
            relative_y = current_window_y - current_monitor.y
            
            # Calculate the new position on the new monitor, maintaining the relative position
            new_x = new_monitor.x + relative_x
            new_y = new_monitor.y + relative_y
            
            # Move the window to its new position on the new monitor
            window_instance.gwindow.moveTo(new_x, new_y)