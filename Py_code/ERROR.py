from button_modul import *

class Error_messange:
    def __init__(self, param, error):
        self.param = param
        self.error = error

        if param == "sel_err":
            self.select_error_massage()

        elif param == "dow_err":
            self.download_error_massage()

        elif param == "sel_com":
            self.select_complete_massage()

        elif param == "dow_com":
            self.download_complete_massage()

        elif param == "red_err":
            self.redactor_error_message()

        elif param == "error":
            self.showerror_for_user()

        elif param == "fon_dow_err":
            self.fon_error_download()

        elif param == "fon_sel_err":
            self.fon_error_select()

        else:
            self.download_no_profile_error_massage()

    def download_error_massage(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка загрузки", "Ошибка выбора. Загружаемый файл не является видеом.")

    def select_complete_massage(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Действие выполнено", "Файл был успешно выбран")

    def download_complete_massage(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Действие выполнено", "Файл был успешно загружен")

    def select_error_massage(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Войдите в профилень, чтобы выбирать видео")

    def download_no_profile_error_massage(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Войдите в профилень, чтобы загружать видео")

    def redactor_error_message(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Выберите видео для редактирования"
                             )

    def showerror_for_user(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", f"{self.error}")

    def fon_error_download(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Войдите в профилень, чтобы загружать фон")

    def fon_error_select(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", "Войдите в профилень, чтобы выбирать фон")

if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        param = sys.argv[1]
        Error_messange(param, None)

    elif len(sys.argv) == 3:
        param = sys.argv[1]
        param2 = sys.argv[2]
        Error_messange(param, param2)