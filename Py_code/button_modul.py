from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
import os.path
from pathlib import Path
import pymediainfo as mt
from moviepy import VideoFileClip, concatenate_videoclips
import threading
import json
import cv2
import numpy as np
import sys
import os
import shutil
import os.path
from functools import partial
import threading
import time

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
        folder_path = Path(os.path.join(project_root, folder))
        folder_path.mkdir(parents=True,exist_ok=True)

def project_Folders():
    script_dir = Path(__file__).parent

    # Поднимаемся на уровень выше (родительская директория)
    project_root = script_dir.parent

    # Создаем папку в родительской директории

    folder_path_profile = project_root / "Profile_data"
    folder_path_temp = project_root / "temp"
    folder_path_temp.mkdir(exist_ok=True)
    folder_path_profile.mkdir(exist_ok=True)

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

def creat_standart_settins():
    os.makedirs(f"{Path(__file__).parent}/settings", exist_ok=True)
    with open(f"{Path(__file__).parent}/settings/settings.json", "w") as f:
        standart_settings = {
            "screen": ["800", "600"],
            "mode": "screen"
        }
        json.dump(standart_settings, f)
