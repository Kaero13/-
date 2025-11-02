import tkinter as tk
import json



from profile import add_and_create_profile_to_json
json_path = r"C:\Users\Acer\PycharmProjects\PythonProject\video redactor\Profile_data"
def select_window():
    """Окно с выбором папки и дополнительным полем ввода"""
    root = tk.Tk()

    root.selected_path = None
    # Центрируем окно
    root.eval('tk::PlaceWindow . center')
    input_frame = tk.Frame(root)
    input_frame.grid(padx = 10, pady = 10)
    Nick = tk.StringVar()
    Password = tk.StringVar()
    Folder = tk.StringVar()

    Nick_lable = tk.Label(input_frame, text = "Имя пользователя:")
    Nick_lable.grid(row = 0, column = 1,sticky=tk.W)
    Nick_pol = tk.Entry(input_frame, width=30, textvariable=Nick)
    Nick_pol.grid(row=0, column=2, padx=5, pady=5)
    pasword_lable = tk.Label(input_frame, text="Пароль:")
    pasword_lable.grid(row=1, column=1,sticky=tk.W)
    pasword_pol = tk.Entry(input_frame, width=30, textvariable=Password)
    pasword_pol.grid(row=1, column=2, padx=5, pady=5)
    folder_path_lable = tk.Label(input_frame, text="Путь к папке пользователя:")
    folder_path_lable.grid(row=2, column=1)
    folder_pol = tk.Entry(input_frame, width=30, textvariable=Folder)
    folder_pol.grid(row=2, column=2, padx=5, pady=5)


    def registr():
        add_and_create_profile_to_json(Nick.get(), Password.get(), folder_pol.get(), json_path)

    def window_sing():
        registr_button.grid_forget()
        folder_pol.grid_forget()
        sing_window_button.grid_forget()
        folder_path_lable.grid_forget()
        sing_button = tk.Button(root, text="Войти", command=sing)
        sing_button.grid(row=1, column=1, padx=5, pady=5)

    def sing():
        path = None
        a = Nick.get()
        b = Password.get()
        with open(r"C:\Users\Acer\PycharmProjects\PythonProject\video redactor\Profile_data\Profile_Data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        if a in data.keys():
            if b == data[a]["Password"]:
                path = data[a]["Video_path"]
                root.selected_path = path
                root.destroy()

    registr_button = tk.Button(root, text="Зарегистрировать", command=registr)
    registr_button.grid(row=3, column=1)
    sing_window_button = tk.Button(root, text="Окно входа",  command=window_sing)
    sing_window_button.grid(row=3, column=2)
    root.mainloop()
    return root.selected_path
