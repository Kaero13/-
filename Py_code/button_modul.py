from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from tkinter import filedialog, messagebox
from profile import add_and_create_profile_to_json
import os.path
from pathlib import Path
import button_modul
import json
from tkinter import ttk
from pathlib import Path
import pymediainfo as mt
from moviepy import VideoFileClip, concatenate_videoclips
import threading
import json
import cv2
import numpy as np
import subprocess
import sys
import os
import shutil
import pygame
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


import os
from pathlib import Path

def get_path():
    Py_code_dir = Path(__file__).parent
    Py_code_dir = str(Py_code_dir)
    if "Py_code" in Py_code_dir:
        Py_code_dir = Py_code_dir.replace("Py_code", "")
    directorys = [
        os.path.join(Py_code_dir,"Texture"),
        os.path.join(Py_code_dir, "audio"),
        os.path.join(Py_code_dir, "videos"),
        os.path.join(Py_code_dir, "Profile_data"),
        os.path.join(Py_code_dir, "temp")
    ]
    return directorys

def in_user_folder(path_user_folder):
    project_root = path_user_folder

    folders = [
        'videos',  # для итоговых видеофайлов
        'audio',  # для аудиофайлов
    ]

    # Создаем папки в родительской директории
    for folder in folders:
        folder_path = project_root / folder
        folder_path.mkdir(exist_ok=True)


def project_Folders():
    script_dir = Path(__file__).parent

    # Поднимаемся на уровень выше (родительская директория)
    project_root = script_dir.parent

    # Создаем папку в родительской директории

    folder_path = project_root / "temp"
    folder_path.mkdir(exist_ok=True)

    # Очистка папки temp
    temp_path = project_root / 'temp'
    if temp_path.exists():
        for file in temp_path.iterdir():
            file_path = temp_path / file
            try:
                if file_path.is_file():
                    file_path.unlink()
            except Exception as e:
                print(f"Ошибка удаления при запуске {file_path}: {e}")

def create_rounded_rectangle():
    rect_surface = pygame.Surface((890, 520), pygame.SRCALPHA)
    fill_color = (80, 130, 200, 255)
    border_color = (40, 80, 150, 255)
    pygame.draw.rect(rect_surface, fill_color, (0, 0, 890, 520), border_radius=25)
    pygame.draw.rect(rect_surface, border_color, (0, 0, 890, 520), width=3, border_radius=25)
    return rect_surface

