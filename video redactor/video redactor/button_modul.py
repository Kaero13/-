from pathlib import Path
import pygame

import os

import tkinter as tk
from tkinter import filedialog, messagebox

pygame.init()


def select_video_file():
    root = tk.Tk()
    root.withdraw()

    videos_path = os.path.abspath('videos')
    if not os.path.exists('videos'):
        os.makedirs(videos_path)
    file_path = filedialog.askopenfilename(
        title="Выберите видео файл",
        initialdir=videos_path,
        filetypes=[
            ("Видео файлы", "*.mp4 *.avi *.mov *.mkv *.wmv"),
            ("Все файлы", "*.*")
        ])
    root.destroy()
    return file_path

def dowload_video_file():
    root = tk.Tk()
    root.withdraw()


    file_path = filedialog.askopenfilename(
        title="Выберите видео файл",
        filetypes=[
            ("Видео файлы", "*.mp4 *.avi *.mov *.mkv *.wmv"),
            ("Все файлы", "*.*")
        ])
    root.destroy()
    return file_path


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

def select_error_massage():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка выбора","Ошибка выбора. Выберите видео из папки videos.")
    return None

def download_error_massage():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка загрузки","Ошибка выбора. Загружаемый файл не является видеом.")
    return None

def select_complete_massage():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Действие выполнено","Файл был успешно выбран")
    return None

def download_complete_massage():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Действие выполнено","Файл был успешно загружен")
    return None

def profile_error_massage():
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка","Профиль уже существует")

