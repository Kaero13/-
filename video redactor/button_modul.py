from pathlib import Path
import pygame
import cv2
import numpy as np
from moviepy import VideoFileClip
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import atexit
pygame.init()



def select_video_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title="Выберите видео файл",
        filetypes=[
            ("Видео файлы", "*.mp4 *.avi *.mov *.mkv *.wmv"),
            ("Все файлы", "*.*")
        ])
    root.destroy()
    return file_path


def position_el(cur_x, cur_y,screen_fon, video_width, video_height, button, rounded_rect):
    global video_y, button_rect
    fon = pygame.transform.scale(screen_fon, (video_width, video_height))

    video_x = (cur_x - video_width)//2
    button_rect = button.get_rect(center=(cur_x // 2, cur_y // 2 + 300))
    rect_rect = rounded_rect.get_rect(center=(cur_x // 2, cur_y // 2 + 300))
    return cur_x, cur_y

def project_Folders():
    folders = [
        'videos',           # для видеофайлов
        'audio',            # для аудиофайлов
        'exports',          # для экспортированных файлов
        'temp',             # для временных файлов
    ]
    for folder in folders:
        folder_path = Path(folder)
        if folder_path.exists():
            pass
        else:
            folder_path.mkdir(exist_ok=True)

    folder_path = 'temp'
    if os.path.exists(folder_path):
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Удален при запуске: {file_path}")
            except Exception as e:
                print(f"Ошибка удаления при запуске {file_path}: {e}")

def create_rounded_rectangle():
    rect_surface = pygame.Surface((890, 520), pygame.SRCALPHA)
    fill_color = (80, 130, 200, 255)
    border_color = (40, 80, 150, 255)
    pygame.draw.rect(rect_surface, fill_color, (0, 0, 890, 520), border_radius=25)
    pygame.draw.rect(rect_surface, border_color, (0, 0, 890, 520), width=3, border_radius=25)
    return rect_surface

