import tkinter as tk
import os


class Select_video:
    def __init__(self, path):
        self.path = path
        data = os.listdir(path)
        colwo = len(data)
        self.width = min(4, max(1, (colwo + 1)//2))
        self.height = (colwo + self.width - 1)//self.width

class UI:
    def __init__(self, path):
        self.select_video = Select_video(path)
def select_video_window(path):
    ui = UI(path)
    root = tk.Tk()

    root.title("Проводник по папке профиля")

    root.selected = None

    def on_closing():
        root.destroy()
        root.selected = None

    root.protocol("WM_DELETE_WINDOW", on_closing)

    btns_field = []
    btns_frame = tk.Frame(root)
    btns_frame.pack(padx=5, pady=5)

    def on_select(video_name):
        full_path = os.path.join(path, video_name)
        root.selected = full_path
        root.destroy()
    def on_select_folder(folder_name):
        folder_path = os.path.join(path, folder_name)

        new_selection = select_video_window(folder_path)

        if new_selection is not None:
            root.selected = new_selection
            root.destroy()

    def text_min(text):
        if len(text) > 12:
            resoult_text = text[:4] + "..." + text[-6:]
        else:
            resoult_text = text
        return resoult_text

    def reset():
        for col in btns_field:
            for widget in col:
                widget.destroy()

        btns_field.clear()

        files = os.listdir(ui.select_video.path)
        colwo = len(files)

        for col_id in range(ui.select_video.width):
            btns_column = []
            btns_field.append(btns_column)
            column_frame = tk.Frame(btns_frame)
            for row_id in range(ui.select_video.height):
                btn_index = row_id*ui.select_video.width + col_id
                if btn_index < colwo:
                    video_name = files[btn_index]
                    if os.path.isdir(os.path.join(ui.select_video.path, video_name)) and video_name != "audio":
                        btn_new = tk.Button(column_frame,
                                            text=text_min(video_name),
                                            width=4,
                                            height=3,
                                            command=lambda v=video_name: on_select_folder(v)
                                            )
                        btn_new.pack(ipadx=30, padx=7, pady=5)
                        btns_column.append(btn_new)
                    if not os.path.isdir(os.path.join(ui.select_video.path, video_name)):
                        btn_new = tk.Button(column_frame,
                                            text=text_min(video_name),
                                            width=4,
                                            height=3,
                                            command=lambda v=video_name: on_select(v)
                                            )
                        btn_new.pack(ipadx=30, padx=7, pady=5)
                        btns_column.append(btn_new)

            column_frame.pack(side="left")
            btns_column.append(column_frame)


    reset()
    root.mainloop()
    return root.selected

