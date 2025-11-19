import tkinter as tk
import os

class Explorer:
    def __init__(self, folder_path, parent_folder):
        self.parent_folder = parent_folder
        self.folder_path = folder_path
        # print(self.folder_path)
        self.select_file = None
        self.root = tk.Tk()
        self.setting()
        self.file_btns()
        self.root.title("Explorer")
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()

    def setting(self):
        self.data = os.listdir(self.folder_path)
        self.colwo = len(self.data)
        self.width = min(4, max(1, (self.colwo + 1) // 2))
        self.height = (self.colwo + self.width - 1) // self.width
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="назад", command=self.back_door)
        self.btns_frame = tk.Frame(self.root)
        self.column_frame = tk.Frame(self.btns_frame)

    def text_min(self, text):
        if len(text) > 12:
            resoult_text = text[:4] + "..." + text[-6:]
        else:
            resoult_text = text
        return resoult_text

    def on_select_folder(self, folder_name):
        self.root.destroy()
        Explorer(folder_name, self.folder_path)

    def on_select_file(self, file_name):
        self.select_file = file_name
        self.root.destroy()

    def back_door(self):
        k = 0
        for i in self.folder_path[::-1]:
            if i == "\\":
                k += 1
                break
            else:
                k += 1

        if len(self.parent_folder) <= len(self.folder_path[:-k]):
            self.root.destroy()
            Explorer(self.folder_path[:-k], self.parent_folder)

    def file_btns(self):

        btns_field = []
        self.btns_frame.pack(padx=10, pady=10)

        btns_field.clear()

        for col_id in range(self.width):
            btns_column = []
            btns_field.append(btns_column)

            for row_id in range(self.height):
                btn_index = row_id*self.width + col_id

                if btn_index < self.colwo:
                    file_name = self.data[btn_index]

                    if os.path.isdir(os.path.join(self.folder_path, file_name)) and file_name != "audio":
                        btn_new = tk.Button(self.column_frame,
                                            text=self.text_min(file_name) + "📁",
                                            width=20,
                                            height=3,
                                            bg="green",
                                            command=lambda v=self.folder_path + "\\" + file_name: self.on_select_folder(v)
                                            )
                        btn_new.grid(row=row_id,column=col_id, padx=2, pady=2)
                        btns_column.append(btn_new)
                    else:
                        btn_new = tk.Button(self.column_frame,
                                            text=self.text_min(file_name),
                                            width=20,
                                            height=3,
                                            command=lambda v=file_name: self.on_select_file(v)
                                            )
                        btn_new.grid(row=row_id,column=col_id, padx=2, pady=2)
                        btns_column.append(btn_new)

                    self.column_frame.pack(side="left")
                    btns_column.append(self.column_frame)


# Explorer(r"C:\Users\Acer\Kaero_video\videos")
Explorer(r"C:\Users\Acer\Kaero_video",r"C:\Users\Acer\Kaero_video" )