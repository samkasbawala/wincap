from __future__ import annotations
from typing import List, Optional, Tuple
import numpy as np
import win32gui
import win32ui
import win32con


# https://stackoverflow.com/a/3586280
class Window:
    def __init__(self, window_name: str, scalar: float = 1.0) -> None:

        # Name of window we are trying to capture
        self.window_name = self._get_window_name(window_name)

        # Needed if windows is scaled up in the settings
        self.scalar = scalar

        if self.window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            # Get the window, from the name
            self.hwnd = win32gui.FindWindow(None, self.window_name)
            if not self.hwnd:
                raise Exception(
                    f"Cannot find window with specified name: {window_name}"
                )

        # Get the coords for the window
        self._get_dimensions()

    def _get_dimensions(self) -> None:
        """Sets the height and the width of the window that is trying to be captured"""

        # Get window bounds
        left: int
        top: int
        right: int
        bottom: int
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)

        # Multiply calculated dimensions by scalar
        self.height = int(abs(bottom - top) * self.scalar)
        self.width = int(abs(right - left) * self.scalar)

    def _get_window_name(self, window_name: str) -> Optional[str]:

        if window_name == "":
            return None

        window_titles = Window.get_window_titles()

        for _, window_title in window_titles:
            if window_name.strip().upper() in window_title.strip().upper():
                print(window_title)
                return window_title

        return None

    @classmethod
    def get_window_titles(cls) -> List[Tuple[int, str]]:
        """Class method to get all window titles that are on the machine"""

        # List to hold our window titles
        window_titles: List[Tuple[int, str]] = []

        # https://www.codegrepper.com/code-examples/python/python+get+list+of+all+open+windows
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                window_titles.append((hex(hwnd), win32gui.GetWindowText(hwnd)))

        win32gui.EnumWindows(winEnumHandler, None)
        return window_titles

    def screen_shot(self, path: str = None) -> np.ndarray:

        # Get device context of the window
        wdc = win32gui.GetWindowDC(self.hwnd)

        # Create PyCDC object
        dc = win32ui.CreateDCFromHandle(wdc)

        # Create a memory device context that is compatable with the specified DC
        cdc = dc.CreateCompatibleDC()

        # Create bit map
        bit_map = win32ui.CreateBitmap()
        bit_map.CreateCompatibleBitmap(dc, self.width, self.height)
        cdc.SelectObject(bit_map)
        cdc.BitBlt((0, 0), (self.width, self.height), dc, (0, 0), win32con.SRCCOPY)

        if path:
            bit_map.SaveBitmapFile(cdc, path)

        # Convert the raw data such that OpenCV can read it
        # https://learncodebygaming.com/blog/fast-window-capture
        signed_int_array = bit_map.GetBitmapBits(True)
        img = np.fromstring(signed_int_array, dtype="uint8")
        img.shape = (self.height, self.width, 4)

        # Free Resources
        dc.DeleteDC()
        cdc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wdc)
        win32gui.DeleteObject(bit_map.GetHandle())

        # Drop alpha values (screws up template matching otherwise)
        # https://stackoverflow.com/a/35902359
        img = img[:, :, :3]

        img = np.ascontiguousarray(img)

        return img
