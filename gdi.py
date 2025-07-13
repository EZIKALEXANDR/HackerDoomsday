import ctypes
import random
import time
import math
import win32gui
import win32api
import win32con
import win32ui
from PIL import Image, ImageWin
import threading

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

    def run(self):
        pass  # To be implemented by subclasses

class RandomImage(ScreenEffect):
    def __init__(self, image_paths, display_size=(400, 400), stop_event=None, delay=0.25):
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
        super()._release_dc()

    def run(self):
        try:
            while not self.stop_event.is_set():
                image_path = random.choice(self.image_paths)
                try:
                    with Image.open(image_path) as img:
                        img = img.resize(self.display_size, Image.Resampling.LANCZOS)
                        width, height = img.size
                        x = 0 if self.screen_width < width else random.randint(0, self.screen_width - width)
                        y = 0 if self.screen_height < height else random.randint(0, self.screen_height - height)
                        dib = ImageWin.Dib(img)
                        dib.draw(self.desktop_dc.GetHandleOutput(), (x, y, x + width, y + height))
                except Exception as e:
                    print(f"Error processing image {image_path}: {e}")
                time.sleep(self.delay)
        finally:
            self._release_dc()

class VoidEffect(ScreenEffect):
    def run(self):
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                win32gui.BitBlt(
                    hdc, random.randint(1, 10) % 2, random.randint(1, 10) % 2,
                    self.screen_width, self.screen_height, hdc,
                    random.randint(1, 1000) % 2, random.randint(1, 1000) % 2,
                    win32con.SRCAND
                )
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class TunnelEffect(ScreenEffect):
    def __init__(self, stop_event=None, delay=2.5, size=100):
        super().__init__(stop_event, delay)
        self.size = size

    def run(self):
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                win32gui.StretchBlt(
                    hdc, int(self.size / 2), int(self.size / 2),
                    self.screen_width - self.size, self.screen_height - self.size,
                    hdc, 0, 0, self.screen_width, self.screen_height, win32con.SRCCOPY
                )
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class SwipeScreen(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.01):
        super().__init__(stop_event, delay)
        self.desktop = win32gui.GetDesktopWindow()

    def run(self):
        angle = 0
        try:
            while not self.stop_event.is_set():
                hdc = win32gui.GetWindowDC(self.desktop)
                n = 0
                for i in range(int(self.screen_width + self.screen_height)):
                    a = int(math.sin(n) * 20)
                    win32gui.BitBlt(hdc, 0, 0, self.screen_width, self.screen_height, hdc, a, 0, win32con.SRCCOPY)
                    n += 0.1
                win32gui.ReleaseDC(self.desktop, hdc)
                time.sleep(self.delay)
        finally:
            self._release_dc()

class ErrorIcons(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.1):
        super().__init__(stop_event, delay)
        self.icons = [
            win32gui.LoadIcon(None, win32con.IDI_ERROR),
            win32gui.LoadIcon(None, win32con.IDI_EXCLAMATION),
            win32gui.LoadIcon(None, win32con.IDI_INFORMATION)
        ]
        self.x_range = range(0, self.screen_width)
        self.y_range = range(0, self.screen_height)

    def run(self):
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                win32gui.DrawIcon(
                    hdc,
                    random.choice(self.x_range),
                    random.choice(self.y_range),
                    random.choice(self.icons)
                )
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class RasterHorizontal(ScreenEffect):
    def run(self):
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                win32gui.StretchBlt(
                    hdc, -5, 0, self.screen_width + 10, self.screen_height,
                    hdc, 0, 0, self.screen_width, self.screen_height, win32con.SRCCOPY
                )
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class RotateTunnel(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.5):
        super().__init__(stop_event, delay)
        self.screen_rect = win32gui.GetWindowRect(win32gui.GetDesktopWindow())
        self.left, self.top, self.right, self.bottom = self.screen_rect
        self.lpppoint = (
            (self.left + 50, self.top - 50),
            (self.right + 50, self.top + 50),
            (self.left - 50, self.bottom - 50)
        )

    def run(self):
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                mhdc = ctypes.windll.gdi32.CreateCompatibleDC(hdc)
                hbit = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc, self.screen_height, self.screen_width)
                holdbit = ctypes.windll.gdi32.SelectObject(mhdc, hbit)
                ctypes.windll.gdi32.PlgBlt(
                    hdc, self.lpppoint, hdc,
                    self.left - 20, self.top - 20,
                    (self.right - self.left) + 40, (self.bottom - self.top) + 40,
                    None, 0, 0
                )
                ctypes.windll.gdi32.DeleteObject(hbit)
                ctypes.windll.gdi32.DeleteDC(mhdc)
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class PanScreen(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.1, speed=1):
        super().__init__(stop_event, delay)
        self.speed = speed

    def run(self):
        dx = dy = 1
        angle = 0
        size = 1
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                win32gui.BitBlt(hdc, 0, 0, self.screen_width, self.screen_height, hdc, dx, dy, win32con.SRCCOPY)
                dx = math.ceil(math.sin(angle) * size * 10)
                dy = math.ceil(math.cos(angle) * size * 10)
                angle += self.speed / 10
                if angle > math.pi:
                    angle = math.pi * -1
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class SinesEffect(ScreenEffect):
    def __init__(self, stop_event=None, delay=0.01, scaling_factor=10):
        super().__init__(stop_event, delay)
        self.desktop = win32gui.GetDesktopWindow()
        self.scaling_factor = scaling_factor

    def run(self):
        angle = 0
        try:
            while not self.stop_event.is_set():
                hdc = win32gui.GetWindowDC(self.desktop)
                for i in range(0, int(self.screen_width + self.screen_height), self.scaling_factor):
                    a = int(math.sin(angle) * 20 * self.scaling_factor)
                    win32gui.BitBlt(hdc, 0, i, self.screen_width, self.scaling_factor, hdc, a, i, win32con.SRCCOPY)
                    angle += math.pi / 40
                win32gui.ReleaseDC(self.desktop, hdc)
                time.sleep(self.delay)
        finally:
            self._release_dc()

class SuperMelt(ScreenEffect):
    def run(self):
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                rx = random.randint(0, self.screen_width)
                win32gui.BitBlt(hdc, rx, 20, 200, self.screen_height, hdc, rx, 0, win32con.SRCCOPY)
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class Smelt(ScreenEffect):
    def run(self):
        gdi32 = ctypes.WinDLL('gdi32')
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                x = random.randint(0, self.screen_width - 1)
                gdi32.BitBlt(hdc, x, 1, 30, self.screen_height, hdc, x, 0, win32con.SRCCOPY)
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class InvertEffect(ScreenEffect):
    def __init__(self, stop_event=None, delay=1.0):
        super().__init__(stop_event, delay)

    def run(self):
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                win32gui.InvertRect(hdc, (0, 0, self.screen_width, self.screen_height))
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()

class HellEffect(ScreenEffect):
    def run(self):
        try:
            while not self.stop_event.is_set():
                hdc = self._init_dc()
                win32gui.BitBlt(
                    hdc, 0, 0, self.screen_width, self.screen_height, hdc,
                    random.randrange(-3, 4), random.randrange(-3, 4), win32con.NOTSRCCOPY
                )
                time.sleep(self.delay)
                self._release_dc()
        finally:
            self._release_dc()