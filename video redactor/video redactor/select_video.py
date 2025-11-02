import tkinter as tk
import os
import pygame

class Select_video:
    def __init__(self, path):
        self.path = path
        data = os.listdir(path)
        colwo = len(data)
        self.width = min(4, (colwo + 1)//2)
        self.height = (colwo + self.width - 1)//self.width

class UI:
    def __init__(self, path):
        self.select_video = Select_video(path)
def sssd(path):
    ui = UI(path)
    root = tk.Tk()
    root.title("Проводник по папке профиля")

    root.selected = None

    btns_field = []
    btns_frame = tk.Frame(root)
    btns_frame.pack(padx=5, pady=5)

    def on_select(video_name):
        full_path = os.path.join(path, video_name)
        root.selected = full_path
        root.quit()


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
                    btn_new = tk.Button(column_frame,
                                        text=video_name,
                                        width=2,
                                        height=1,
                                        command=lambda v=video_name: on_select(v)
                                        )
                    btn_new.pack(ipadx=30, padx=5, pady=5)
                    btns_column.append(btn_new)

            column_frame.pack(side="left")
            btns_column.append(column_frame)


    reset()
    root.update()
    while root.selected is None:
        root.update()  # Обновляем Tkinter
        pygame.event.pump()  # Обновляем Pygame
        root.after(10)  # Небольшая задержка

    root.destroy()
    return root.selected

