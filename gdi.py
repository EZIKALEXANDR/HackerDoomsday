import ctypes
import random
import time
import math
import win32gui
import os
import sys
import win32api
import win32con
import win32ui
from PIL import Image, ImageWin
import threading

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, "resources")
    else:
        base_path = os.path.join(os.path.abspath("."), "resources")
    return os.path.join(base_path, relative_path)

class ScreenEffect:
    def __init__(self, stop_event=None, delay=0.1):
        self.stop_event = stop_event or threading.Event()
        self.delay = delay
        self.user32 = ctypes.windll.user32
        self.user32.SetProcessDPIAware()
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.hdc = None

    def _init_dc(self):
        self.hdc = win32gui.GetDC(0)
        return self.hdc

    def _release_dc(self):
        if self.hdc:
            win32gui.ReleaseDC(0, self.hdc)
            self.hdc = None

    def run(self):
        pass  


class RandomImage(ScreenEffect):
    def __init__(self, image_paths=None, display_size=(400, 400), stop_event=None, delay=0.25):
        if image_paths is None:
            image_paths = [resource_path(f"{i}.jpg") for i in range(1, 6)]
        super().__init__(stop_event, delay)
        self.image_paths = image_paths
        self.display_size = display_size
        self.desktop_dc = None

    def _init_dc(self):
        hdesktop = super()._init_dc()
        self.desktop_dc = win32ui.CreateDCFromHandle(hdesktop)
        return hdesktop

    def _release_dc(self):
        if self.desktop_dc:
            self.desktop_dc.DeleteDC()
            self.desktop_dc = None
        super()._release_dc()

    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                image_path = random.choice(self.image_paths)
                try:
                    with Image.open(image_path) as img:
                        img = img.resize(self.display_size, Image.Resampling.LANCZOS)
                        width, height = img.size
                        x = random.randint(0, self.screen_width - width)
                        y = random.randint(0, self.screen_height - height)
                        dib = ImageWin.Dib(img)
                        dib.draw(self.desktop_dc.GetHandleOutput(), (x, y, x + width, y + height))
                except Exception as e:
                    print(f"Error processing image {image_path}: {e}")
                time.sleep(self.delay)
        finally:
            self._release_dc()


class VoidEffect(ScreenEffect):
    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                win32gui.BitBlt(
                    self.hdc,
                    random.randint(0, 1), random.randint(0, 1),
                    self.screen_width, self.screen_height,
                    self.hdc,
                    random.randint(0, 1), random.randint(0, 1),
                    win32con.SRCAND
                )
                time.sleep(self.delay)
        finally:
            self._release_dc()


class TunnelEffect(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.5, size=100):
        super().__init__(stop_event, delay)
        self.size = size

    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                win32gui.StretchBlt(
                    self.hdc,
                    int(self.size / 2), int(self.size / 2),
                    self.screen_width - self.size, self.screen_height - self.size,
                    self.hdc, 0, 0, self.screen_width, self.screen_height,
                    win32con.SRCCOPY
                )
                time.sleep(self.delay)
        finally:
            self._release_dc()


class SwipeScreen(ScreenEffect):
    def run(self):
        desktop = win32gui.GetDesktopWindow()
        angle = 0
        try:
            while not self.stop_event.is_set():
                hdc = win32gui.GetWindowDC(desktop)
                n = 0
                for _ in range(int(self.screen_width + self.screen_height)):
                    a = int(math.sin(n) * 20)
                    win32gui.BitBlt(hdc, 0, 0, self.screen_width, self.screen_height, hdc, a, 0, win32con.SRCCOPY)
                    n += 0.1
                win32gui.ReleaseDC(desktop, hdc)
                time.sleep(self.delay)
        finally:
            pass


class ErrorIcons(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.1):
        super().__init__(stop_event, delay)
        self.icons = [
            win32gui.LoadIcon(None, win32con.IDI_ERROR),
            win32gui.LoadIcon(None, win32con.IDI_EXCLAMATION),
            win32gui.LoadIcon(None, win32con.IDI_INFORMATION)
        ]

    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                win32gui.DrawIcon(
                    self.hdc,
                    random.randint(0, self.screen_width),
                    random.randint(0, self.screen_height),
                    random.choice(self.icons)
                )
                time.sleep(self.delay)
        finally:
            self._release_dc()


class RasterHorizontal(ScreenEffect):
    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                win32gui.StretchBlt(
                    self.hdc, -5, 0, self.screen_width + 10, self.screen_height,
                    self.hdc, 0, 0, self.screen_width, self.screen_height,
                    win32con.SRCCOPY
                )
                time.sleep(self.delay)
        finally:
            self._release_dc()

class RotateTunnel(ScreenEffect):
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

    def __init__(self, stop_event=None, delay=0.5):
        super().__init__(stop_event, delay)
        self.screen_rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        self.left, self.top, self.right, self.bottom = self.screen_rect

        # Встроенное создание массива точек
        self.lpppoint = (self.POINT * 3)(
            self.POINT(self.left + 50, self.top - 50),
            self.POINT(self.right + 50, self.top + 50),
            self.POINT(self.left - 50, self.bottom - 50)
        )

    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                mhdc = ctypes.windll.gdi32.CreateCompatibleDC(self.hdc)
                hbit = ctypes.windll.gdi32.CreateCompatibleBitmap(self.hdc, self.screen_height, self.screen_width)
                ctypes.windll.gdi32.SelectObject(mhdc, hbit)

                ctypes.windll.gdi32.PlgBlt(
                    self.hdc, self.lpppoint, self.hdc,
                    self.left - 20, self.top - 20,
                    (self.right - self.left) + 40, (self.bottom - self.top) + 40,
                    None, 0, 0
                )

                ctypes.windll.gdi32.DeleteObject(hbit)
                ctypes.windll.gdi32.DeleteDC(mhdc)
                time.sleep(self.delay)
        finally:
            self._release_dc()



class PanScreen(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.1, speed=1):
        super().__init__(stop_event, delay)
        self.speed = speed

    def run(self):
        self._init_dc()
        dx = dy = 1
        angle = 0
        try:
            while not self.stop_event.is_set():
                win32gui.BitBlt(self.hdc, 0, 0, self.screen_width, self.screen_height, self.hdc, dx, dy, win32con.SRCCOPY)
                dx = math.ceil(math.sin(angle) * 10)
                dy = math.ceil(math.cos(angle) * 10)
                angle += self.speed / 10
                if angle > math.pi:
                    angle = -math.pi
                time.sleep(self.delay)
        finally:
            self._release_dc()


class SinesEffect(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.01, scaling_factor=10):
        super().__init__(stop_event, delay)
        self.scaling_factor = scaling_factor

    def run(self):
        desktop = win32gui.GetDesktopWindow()
        angle = 0
        try:
            while not self.stop_event.is_set():
                hdc = win32gui.GetWindowDC(desktop)
                for i in range(0, int(self.screen_width + self.screen_height), self.scaling_factor):
                    a = int(math.sin(angle) * 20 * self.scaling_factor)
                    win32gui.BitBlt(hdc, 0, i, self.screen_width, self.scaling_factor, hdc, a, i, win32con.SRCCOPY)
                    angle += math.pi / 40
                win32gui.ReleaseDC(desktop, hdc)
                time.sleep(self.delay)
        finally:
            pass


class SuperMelt(ScreenEffect):
    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                rx = random.randint(0, self.screen_width)
                win32gui.BitBlt(self.hdc, rx, 20, 200, self.screen_height, self.hdc, rx, 0, win32con.SRCCOPY)
                time.sleep(self.delay)
        finally:
            self._release_dc()

class ErrorIconsCursor(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.1):
        super().__init__(stop_event, delay)
        self.icons = [
            win32gui.LoadIcon(None, win32con.IDI_ERROR),
            win32gui.LoadIcon(None, win32con.IDI_EXCLAMATION),
            win32gui.LoadIcon(None, win32con.IDI_INFORMATION)
        ]

    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                # Получаем текущую позицию курсора
                x, y = win32api.GetCursorPos()
                # Рисуем иконку рядом с курсором с небольшим случайным смещением
                win32gui.DrawIcon(
                    self.hdc,
                    x + random.randint(-30, 30),
                    y + random.randint(-30, 30),
                    random.choice(self.icons)
                )
                time.sleep(self.delay)
        finally:
            self._release_dc()

class Smelt(ScreenEffect):
    def run(self):
        gdi32 = ctypes.WinDLL("gdi32")
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                for _ in range(random.randint(3, 6)):
                    width = random.randint(50, 200)
                    x = random.randint(0, self.screen_width - width)
                    offset_x = random.randint(-3, 3)
                    gdi32.BitBlt(
                        self.hdc,
                        x + offset_x, 1,
                        width, self.screen_height,
                        self.hdc,
                        x, 0,
                        win32con.SRCCOPY
                    )
                time.sleep(0.02)
        finally:
            self._release_dc()


class InvertEffect(ScreenEffect):
    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                win32gui.InvertRect(self.hdc, (0, 0, self.screen_width, self.screen_height))
                time.sleep(self.delay)
        finally:
            self._release_dc()


class HellEffect(ScreenEffect):
    def run(self):
        self._init_dc()
        try:
            while not self.stop_event.is_set():
                win32gui.BitBlt(
                    self.hdc, 0, 0, self.screen_width, self.screen_height, self.hdc,
                    random.randint(-3, 3), random.randint(-3, 3),
                    win32con.NOTSRCCOPY
                )
                time.sleep(self.delay)
        finally:
            self._release_dc()
