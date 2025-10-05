from pathlib import Path
import pygame
import cv2
import numpy as np
from moviepy import VideoFileClip
from button_modul import *
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import atexit


project_Folders()       #создание папок приложения
pygame.init()           #инцилизация pygame
pygame.mixer.init()     #инцилизация микшера


#Экран
x = 1200
y = 800

#Видео
video_width = 0
video_height = 0
video_x = 0
video_y = 0
flip_mode = 1
#Подложка под видео
rounded_rect = create_rounded_rectangle()
rect_rect = rounded_rect.get_rect(center=(x // 2, y // 2.7))
video_area_width = rect_rect.width - 40
video_area_height = rect_rect.height - 40

#Кнопка Выбора видео из внутренней памяти
select_button = pygame.image.load("Texture/select_button.png")
select_button_rect = select_button.get_rect()
select_button_rect.right = x
select_button_rect.centery = y // 2 + 250

#Кнопка старт/стоп/пауза
button = pygame.image.load('Texture/start_button.jpg')
button_rect = button.get_rect(center=(x // 2, y // 2 + 300))

#Кнопка загрузки видео во внутрению память
load_button = pygame.image.load('Texture/load_button.png')
load_button_rect = load_button.get_rect()
load_button_rect.right = x - 900
load_button_rect.centery = y // 2 + 300

#Создание окна pygame
screen = pygame.display.set_mode((x, y))
screen_fon = pygame.image.load('Texture/fon.jpg')
screen_fon = pygame.transform.scale(screen_fon, (x, y))


def video_position_and_scale(frame_width, frame_height, area_width, area_height):
    video_ratio = frame_width / frame_height
    area_ratio = area_width / area_height

    if video_ratio > area_ratio:
        scale_factor = area_width / frame_width
        new_width = area_width
        new_height = int(frame_height * scale_factor)
    else:
        scale_factor = area_height / frame_height
        new_width = int(frame_width * scale_factor)
        new_height = area_height

    position_x = rect_rect.left + (area_width - new_width) // 2 + 20
    position_y = rect_rect.top + (area_height - new_height) // 2 + 20

    return position_x, position_y, new_width, new_height

#Функция выбора видео из внутренней памяти
def video_sel(capt, video_area_width, video_area_height):
    global video_y, video_x, video_fps, clock, cap, audio_start, video_width, video_height, flip_mode

    cap = cv2.VideoCapture(capt)

    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_x, video_y, video_width, video_height = video_position_and_scale(
        original_width, original_height, video_area_width, video_area_height)

    video_fps = cap.get(cv2.CAP_PROP_FPS)
    clock = pygame.time.Clock()
    name_ras = os.path.basename(capt)
    name = os.path.splitext(name_ras)[0]
    if not os.path.exists("temp/" + name + ".mp3"):
        video = VideoFileClip(capt)
        audio = video.audio
        audio.write_audiofile(name + '.mp3')
        shutil.move(name + '.mp3', 'temp/' + name + '.mp3')

    pygame.mixer.music.load('temp/' + name + '.mp3')
    audio_start = False
    flip_mode = 0
    paused_frame = None

#Предзагрузка Статичного видео при входе в приложение
cap = cv2.VideoCapture('Texture/WelcomVideo/vidio.mp4')
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_x, video_y, video_width, video_height = video_position_and_scale(
    original_width, original_height, video_area_width, video_area_height)

video_fps = cap.get(cv2.CAP_PROP_FPS)
clock = pygame.time.Clock()
pygame.mixer.music.load('Texture/WelcomVideo/vidio.wav')

#Позиционирование Кнопок
button_rect = button.get_rect(center=(x // 2, y // 2 + 300))
x, y = position_el(x, y, screen_fon, video_area_width, video_area_height, button, rounded_rect)

#Булевые пременные для работы видео, полноэкранного режима, проверки нажатия паузы, работы програииы и аудио
fullscreen = False
mousedown = False
audio_start = False
rab = True

# Инициализация переменных для воспроизведения видео
ret = False
frame = None
paused_frame = None

#Тело программы
while rab:
    clock.tick(video_fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rab = False

        #Кнопки и клавиши
        if event.type == pygame.MOUSEBUTTONDOWN:
            #Пауза/Страт
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                mousedown = not mousedown

                if mousedown:
                    pygame.mixer.music.pause()
                    if frame is not None:
                        paused_frame = frame.copy()
                else:
                    pygame.mixer.music.unpause()
                    paused_frame = None

            #Загрузка во внутреннюю память
            elif load_button_rect.collidepoint(pygame.mouse.get_pos()):
                selected_file = select_video_file()
                if selected_file:
                    shutil.move(selected_file, "videos")

            #Выбор из внутренней памяти
            elif select_button_rect.collidepoint(pygame.mouse.get_pos()):
                selected_file = select_video_file()
                if selected_file:
                    video_sel(selected_file, video_area_width, video_area_height)

        #Полноэкранный режим
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            #Нажатие для входа и выхода
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    new_x, new_y = screen.get_size()

                else:
                    screen = pygame.display.set_mode((1200, 800))
                    new_x, new_y = 1200, 800

                #Проверка Позиции элементов и обновление координат при полноэкранном режиме
                x, y = position_el(new_x, new_y, screen_fon, video_area_width, video_area_height, button, rounded_rect)
                rect_rect = rounded_rect.get_rect(center=(x // 2, y // 2.7))

                #Центрирование и подгонка размера в полноэкранном режиме
                if 'cap' in globals():
                    curent_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    video_x, video_y, video_width, video_height = video_position_and_scale(
                        original_width, original_height, video_area_width, video_area_height)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, curent_pos)

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            if flip_mode == 0:
                flip_mode = 1
            else:
                flip_mode = 0

        #Привычный способ выхода из полноэкранного режима через escape
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            fullscreen = not fullscreen
            screen = pygame.display.set_mode((1200, 800))
            new_x, new_y = 1200, 800
            x, y = position_el(new_x, new_y, screen_fon, video_width, video_height, button, rounded_rect)
            rect_rect = rounded_rect.get_rect(center=(x // 2, y // 2.7))

            # Центрирование и подгонка размера в полноэкранном режиме
            if 'cap' in globals():
                curent_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                video_x, video_y, video_width, video_height = video_position_and_scale(
                    original_width, original_height, video_area_width, video_area_height)
                cap.set(cv2.CAP_PROP_POS_FRAMES, curent_pos)

        #Возврат к прежним координатам кнопок
        button_rect = button.get_rect(center=(x // 2, y // 2 + 300))
        screen_fon = pygame.transform.scale(screen_fon, (x, y))


    #Чтение кадра
    if not mousedown:
        ret, frame = cap.read()
    else:
        pass

    #Запуск аудио если не на паузе
    if not audio_start and ret:
        pygame.mixer.music.play()
        audio_start = True

    #Зацикливание видео
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        pygame.mixer.music.stop()
        audio_start = False
        ret, frame = cap.read()
        if ret:
            pygame.mixer.music.play()
            audio_start = True

    #Отрисовка всего фона и подложки
    screen.blit(screen_fon, (0, 0))
    screen.blit(rounded_rect, rect_rect)

    # Отрисовка текущего кадра
    display_frame = None
    if mousedown and paused_frame is not None:
        display_frame = paused_frame

    elif frame is not None and ret:
        display_frame = frame.copy()

    if display_frame is not None:
        if flip_mode == 1:
            display_frame = cv2.flip(display_frame, 1)
        frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (video_width, video_height))
        video_rotated = np.rot90(frame_resized)
        frame_surface = pygame.surfarray.make_surface(video_rotated)
        screen.blit(frame_surface, (video_x, video_y))

    #Отрисовка Кнопак
    screen.blit(button, button_rect) #Кнопка старт/стоп/пауза
    screen.blit(load_button, load_button_rect)# Кнопка загрузки во внутреннию память
    screen.blit(select_button, select_button_rect)
    pygame.display.flip()