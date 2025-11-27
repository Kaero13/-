from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from profile import add_and_create_profile_to_json
import os.path
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
import tkinter as tk
from tkinter import filedialog, messagebox

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


