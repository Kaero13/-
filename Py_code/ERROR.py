from button_modul import *

class Error_messange:
    def __init__(self, param):
        self.param = param
        if param == "sel_err":
            self.select_error_massage()

        elif param == "dow_err":
            self.download_error_massage()

        elif param == "sel_com":
            self.select_complete_massage()

        elif param == "dow_com":
            self.download_complete_massage()

        elif param == "sel_prof_err":
            self.selected_error_massage()

        elif param == "red_err":
            self.redactor_error_message()

        else:
            self.download_no_profile_error_massage()

    def select_error_massage(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка выбора", "Ошибка выбора. Выберите видео из папки videos.")

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

    def selected_error_massage(self):
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
if __name__ == '__main__':
    import sys

    if len(sys.argv) == 2:
        param = sys.argv[1]
        Error_messange(param)