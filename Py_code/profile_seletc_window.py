from profile import add_and_create_profile_to_json
import os.path
from pathlib import Path
import button_modul
import tkinter as tk
import json

class Profile:
    def __init__(self):
        self.Profile_path = self.path()
        self.json_path = self.path()


    def path(self):
        path = button_modul.get_path()
        return path[3]

    def fix_path(self, path):
        if path is None:
            return None
        elif path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        if "\\" in path:
            path = path.replace("\\", "/")

        try:
            return os.path.normpath(path)
        except:
            return path

    def select_window(self):
        """Окно с выбором папки и дополнительным полем ввода"""
        root = tk.Tk()
        root.selected_path = None

        def on_closing():
            root.selected_path = None
            root.destroy()
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # Центрируем окно
        root.eval('tk::PlaceWindow . center')
        input_frame = tk.Frame(root)
        input_frame.grid(padx = 10, pady = 10)
        Nick = tk.StringVar()
        Password = tk.StringVar()
        Folder = tk.StringVar()
        sing_Nick = tk.StringVar()
        sing_Password = tk.StringVar()

        Nick_lable = tk.Label(input_frame, text = "Имя пользователя:")
        Nick_lable.grid(row = 0, column = 1,sticky=tk.W)
        Nick_pol = tk.Entry(input_frame, width=30, textvariable=Nick)
        Nick_pol.grid(row=0, column=2, padx=5, pady=5)

        pasword_lable = tk.Label(input_frame, text="Пароль:")
        pasword_lable.grid(row=1, column=1,sticky=tk.W)
        pasword_pol = tk.Entry(input_frame, width=30, textvariable=Password)
        pasword_pol.grid(row=1, column=2, padx=5, pady=5)

        sing_Nick_lable = tk.Label(input_frame, text="Имя пользователя:")
        sing_Nick_pol = tk.Entry(input_frame, width=30, textvariable=sing_Nick)

        sing_pasword_lable = tk.Label(input_frame, text="Пароль:")
        sing_pasword_pol = tk.Entry(input_frame, width=30, textvariable=sing_Password)

        folder_path_lable = tk.Label(input_frame, text="Путь к папке пользователя:")
        folder_path_lable.grid(row=2, column=1,sticky=tk.W)
        folder_pol = tk.Entry(input_frame, width=30, textvariable=Folder)
        folder_pol.grid(row=2, column=2, padx=5, pady=5)

        messages_lable_pole = tk.Label(input_frame, text="")
        messages_lable_pole.grid(row=3, column=1, padx=5, pady=5)

        def message(Bool):
            if Bool == True:
                return "Профиль успешно добавлен"
            else:
                return "Заполните поля ник, пароль, путь к папке профиля."

        def sing_message(Bool):
            if Bool == True:
                return "Файл профиля не существует.\n Для начала работы\n создайте новый профиль."
            else:
                return "Файл профиля не существует\n или не правильный пароль/ник.\n Для начала работы\n создайте новый профиль."

        def registr():
            global messages_lable_pole
            a = add_and_create_profile_to_json(Nick.get(), Password.get(), folder_pol.get(), self.json_path)

            folder_path = Path(self.fix_path(folder_pol.get()))
            folder_path.mkdir(exist_ok=True)
            button_modul.in_user_folder(folder_path)

            if 'messages_lable_pole' in globals():
                messages_lable_pole.destroy()

            messages_lable_pole = tk.Label(input_frame, text=message(a))
            messages_lable_pole.grid(row=3, column = 1, padx = 5, pady = 5)

        def window_sing():
            registr_button.grid_forget()
            folder_pol.grid_forget()
            folder_path_lable.grid_forget()
            sing_window_button.grid_forget()
            sing_Nick_pol.grid(row=0, column=2, padx=5, pady=5)
            sing_pasword_lable.grid(row=1, column=1, sticky=tk.W)
            sing_pasword_pol.grid(row=1, column=2, padx=5, pady=5)

            sing_Nick_lable.grid(row=0, column=1, sticky=tk.W)

            sing_button = tk.Button(root, text="Войти", command=sing)
            sing_button.grid(row=1, column=1, padx=5, pady=5)

            messages_lable_pole_sing = tk.Label(input_frame, text="")
            messages_lable_pole_sing.grid(row=2, column=1, padx=5, pady=5)

        def sing():
            global messages_lable_pole_sing
            path = None
            a = sing_Nick.get()
            b = sing_Password.get()
            c = True
            try:
                with open(os.path.join(self.Profile_path, "Profile_Data.json"), "r", encoding="utf-8") as f:
                    data = json.load(f)

                print(data)
                print(a, b)
                if a in data.keys():
                    if b == data[a]["Password"]:
                        path = data[a]["Video_path"]
                        root.selected_path = path
                        root.destroy()
                elif a == "" or b == "":
                    c = False
                    if 'messages_lable_pole_sing' in globals():
                        messages_lable_pole_sing.destroy()

                    messages_lable_pole_sing = tk.Label(input_frame, text=sing_message(c))
                    messages_lable_pole_sing.grid(row=3, column=1, padx=5, pady=5)

            except:
                if 'messages_lable_pole_sing' in globals():
                    messages_lable_pole_sing.destroy()

                messages_lable_pole_sing = tk.Label(input_frame, text=sing_message(c))
                messages_lable_pole_sing.grid(row=3, column=1, padx=5, pady=5)



        registr_button = tk.Button(root, text="Зарегистрировать", command=registr)
        registr_button.grid(row=3, column=2)
        sing_window_button = tk.Button(root, text="Окно входа",  command=window_sing)
        sing_window_button.grid(row=3, column=3)

        root.mainloop()
        return root.selected_path

    def dubl_click(self):
        root = tk.Tk()
        root.exit = None
        def OK_funct():
            exit_command()
            self.select_window()

        def exit_command():
            root.exit = None
            root.destroy()
        root.protocol("WM_DELETE_WINDOW", exit_command)
        lable = tk.Label(text="Вы повторно нажали на выбор профиля\n если хотите сменить профиль, то нажмите ОК")
        lable.grid(row = 0, column = 1)
        OK_button = tk.Button(text="Ок", width=5, height=2, command=OK_funct)
        OK_button.grid(row = 2, column = 1)
        Exit_button = tk.Button(text="Выйти", width=5, height=2, command=exit_command)
        Exit_button.grid(row = 1, column = 1,)

        root.mainloop()
        return root.exit
