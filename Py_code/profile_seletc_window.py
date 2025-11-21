from profile import add_and_create_profile_to_json
import os.path
from pathlib import Path
import button_modul
import tkinter as tk
import json

class Profile:
    def __init__(self, dubl, prov):
        self.prov = prov
        self.dubl = dubl

        if self.prov is None:
            print(">" + f"{self.prov}")
            return

        if self.dubl != True:
            self.prov = True
            self.dubl_click()

        if self.prov is False:
            self.Profile_path = self.path()
            self.json_path = self.path()
            self.root = tk.Tk()
            self.root.selected_path = None
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.root.eval('tk::PlaceWindow . center')
            self.select_window()
            self.root.mainloop()

    def load(self):

        a = {"First": self.root.selected_path, "Second" : False}

        with open(f"{Path(__file__).parent.parent}\\temp\\profile_path_and_dubl.json", "w", encoding="utf-8") as f:
            json.dump(a, f)

    def on_closing(self):
        with open(f"{Path(__file__).parent.parent}\\temp\\profile_path_and_dubl.json", "w", encoding="utf-8") as f:
            json.dump({}, f)
        self.prov = True
        self.root.selected_path = None
        self.root.destroy()

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

    def gui(self):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.grid(padx=10, pady=10)
        self.Nick = tk.StringVar()
        self.Password = tk.StringVar()
        self.Folder = tk.StringVar()
        self.sing_Nick = tk.StringVar()
        self.sing_Password = tk.StringVar()

        self.Nick_lable = tk.Label(self.input_frame, text="Имя пользователя:")
        self.Nick_lable.grid(row=0, column=1, sticky=tk.W)
        self.Nick_pol = tk.Entry(self.input_frame, width=30, textvariable=self.Nick)
        self.Nick_pol.grid(row=0, column=2, padx=5, pady=5)

        self.pasword_lable = tk.Label(self.input_frame, text="Пароль:")
        self.pasword_lable.grid(row=1, column=1, sticky=tk.W)
        self.pasword_pol = tk.Entry(self.input_frame, width=30, textvariable=self.Password)
        self.pasword_pol.grid(row=1, column=2, padx=5, pady=5)

        self.sing_Nick_lable = tk.Label(self.input_frame, text="Имя пользователя:")
        self.sing_Nick_pol = tk.Entry(self.input_frame, width=30, textvariable=self.sing_Nick)

        self.sing_pasword_lable = tk.Label(self.input_frame, text="Пароль:")
        self.sing_pasword_pol = tk.Entry(self.input_frame, width=30, textvariable=self.sing_Password)

        self.folder_path_lable = tk.Label(self.input_frame, text="Путь к папке пользователя:")
        self.folder_path_lable.grid(row=2, column=1, sticky=tk.W)
        self.folder_pol = tk.Entry(self.input_frame, width=30, textvariable=self.Folder)
        self.folder_pol.grid(row=2, column=2, padx=5, pady=5)

        self.messages_lable_pole = tk.Label(self.input_frame, text="")
        self.messages_lable_pole.grid(row=3, column=1, padx=5, pady=5)

    def message(self,Bool):
        if Bool == True:
            return "Профиль успешно добавлен"
        else:
            return "Заполните поля ник, пароль, путь к папке профиля."

    def sing_message(self, Bool):
        if Bool == True:
            return "Файл профиля не существует.\n Для начала работы\n создайте новый профиль."
        else:
            return "Файл профиля не существует\n или не правильный пароль/ник.\n Для начала работы\n создайте новый профиль."

    def select_window(self):
        self.gui()

        def registr():
            a = add_and_create_profile_to_json(self.Nick.get(), self.Password.get(), self.folder_pol.get(), self.json_path)

            folder_path = Path(self.fix_path(self.folder_pol.get()))
            folder_path.mkdir(exist_ok=True)
            button_modul.in_user_folder(folder_path)

            if 'messages_lable_pole' in globals():
                self.messages_lable_pole.destroy()

            self.messages_lable_pole = tk.Label(self.input_frame, text=self.message(a))
            self.messages_lable_pole.grid(row=3, column = 1, padx = 5, pady = 5)

        def window_sing():
            self.registr_button.grid_forget()
            self.folder_pol.grid_forget()
            self.folder_path_lable.grid_forget()
            self.sing_window_button.grid_forget()
            self.sing_Nick_pol.grid(row=0, column=2, padx=5, pady=5)
            self.sing_pasword_lable.grid(row=1, column=1, sticky=tk.W)
            self.sing_pasword_pol.grid(row=1, column=2, padx=5, pady=5)

            self.sing_Nick_lable.grid(row=0, column=1, sticky=tk.W)

            self.sing_button = tk.Button(self.root, text="Войти", command=sing)
            self.sing_button.grid(row=1, column=1, padx=5, pady=5)

            self.messages_lable_pole_sing = tk.Label(self.input_frame, text="")
            self.messages_lable_pole_sing.grid(row=2, column=1, padx=5, pady=5)

        def sing():
            self.prov = None
            path = None
            a = self.sing_Nick.get()
            b = self.sing_Password.get()
            c = True
            try:
                with open(os.path.join(self.Profile_path, "Profile_Data.json"), "r", encoding="utf-8") as f:
                    data = json.load(f)

                if a in data.keys():
                    if b == data[a]["Password"]:
                        path = data[a]["Video_path"]
                        self.root.selected_path = path
                        self.load()
                        self.root.destroy()
                        return

                    c = False
                    if c == False:
                        self.messages_lable_pole_sing = tk.Label(self.input_frame, text=self.sing_message(c))
                        self.messages_lable_pole_sing.grid(row=3, column=1, padx=5, pady=5)

                elif a == "" or b == "":
                    c = False
                    if 'messages_lable_pole_sing' in globals():
                        self.messages_lable_pole_sing.destroy()

                    self.messages_lable_pole_sing = tk.Label(self.input_frame, text=self.sing_message(c))
                    self.messages_lable_pole_sing.grid(row=3, column=1, padx=5, pady=5)

            except:
                if 'messages_lable_pole_sing' in globals():
                    self.messages_lable_pole_sing.destroy()
                c = False
                self.messages_lable_pole_sing = tk.Label(self.input_frame, text=self.sing_message(c))
                self.messages_lable_pole_sing.grid(row=3, column=1, padx=5, pady=5)



        self.registr_button = tk.Button(self.root, text="Зарегистрировать", command=registr)
        self.registr_button.grid(row=3, column=2)
        self.sing_window_button = tk.Button(self.root, text="Окно входа",  command=window_sing)
        self.sing_window_button.grid(row=3, column=3)

        self.root.mainloop()


    def dubl_click(self):
        root = tk.Tk()
        def OK_funct():
            a = {"First": "", "Second": True}

            with open(f"{Path(__file__).parent.parent}\\temp\\profile_path_and_dubl.json", "w", encoding="utf-8") as f:
                json.dump(a, f)

            with open(f"{Path(__file__).parent.parent}\\temp\\profile_path_and_dubl.json", "r", encoding='utf-8') as f:
                local_path = json.load(f)

            dubl_prof = str(local_path["Second"])
            exit_command()
            self.__init__(bool(dubl_prof), False)

        def exit_command():
            self.prov = True
            root.destroy()
        root.protocol("WM_DELETE_WINDOW", exit_command)
        lable = tk.Label(text="Вы повторно нажали на выбор профиля\n если хотите сменить профиль, то нажмите ОК")
        lable.grid(row = 0, column = 1)
        OK_button = tk.Button(text="Ок", width=5, height=2, command=OK_funct)
        OK_button.grid(row = 1, column = 1)
        Exit_button = tk.Button(text="Выйти", width=5, height=2, command=exit_command)
        Exit_button.grid(row = 1, column = 2,)

        root.mainloop()

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        dubl = sys.argv[1]
        prov = sys.argv[2]
        if dubl == str(True):
            dubl = True
        if prov == str(False):
            prov = False
        Profile(dubl, prov)