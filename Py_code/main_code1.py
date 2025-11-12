import pygame
import cv2
import numpy as np
import subprocess
import sys

from button_modul import *
import os
import shutil
from profile_seletc_window import*
from select_video import select_video_window
from redactor_window import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
project_Folders()       #создание папки для временных файлов
pygame.init()           #инцилизация pygame
pygame.mixer.init()     #инцилизация микшера

path = get_path()
Texture_path = path[0]
Temp_path = path[4]
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
select_button = pygame.image.load(os.path.join(Texture_path,"select_button.png"))
select_button_rect = select_button.get_rect()
select_button_rect.right = x - 375
select_button_rect.centery = y // 2 + 335

#Кнопка старт/стоп/пауза
button = pygame.image.load(os.path.join(Texture_path,'start_button.png'))
button_rect = button.get_rect(center=(x // 2, y // 2 + 330))

#Кнопка загрузки видео во внутрению память
load_button = pygame.image.load(os.path.join(Texture_path,'load_button.png'))
load_button_rect = load_button.get_rect()
load_button_rect.right = x - 700
load_button_rect.centery = y // 2 + 330

#Кнопка входа и регистрации профиля
profile_button = pygame.image.load(os.path.join(Texture_path,'select_and_registr_profile.png'))
profile_button_rect = load_button.get_rect()
profile_button_rect.right = x - 80
profile_button_rect.centery = y - 70
profile_button = pygame.transform.scale(profile_button, (128,128))

#Создание окна pygame
screen = pygame.display.set_mode((x, y))
screen_fon = pygame.image.load(os.path.join(Texture_path,'fon.jpg'))
screen_fon = pygame.transform.scale(screen_fon, (x, y))

#Кнопка открытия окна редактора выбранного видео в основном окне
redactor_button = pygame.image.load(os.path.join(Texture_path, "redactor_button.png"))
redactor_button_rect = redactor_button.get_rect()
redactor_button_rect.right = x - 900
redactor_button_rect.centery = y - 70

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
    if not os.path.exists(os.path.join(Temp_path,(name + ".mp3"))):
        video = VideoFileClip(capt)
        audio = video.audio
        audio.write_audiofile(name + '.mp3')
        shutil.move(name + '.mp3', os.path.join(Temp_path,(name + ".mp3")))

    pygame.mixer.music.load(os.path.join(Temp_path,(name + '.mp3')))
    audio_start = False
    flip_mode = 0
    paused_frame = None

#Предзагрузка Статичного видео при входе в приложение
cap = cv2.VideoCapture(os.path.join(Texture_path,'WelcomVideo/vidio.mp4'))
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_x, video_y, video_width, video_height = video_position_and_scale(
    original_width, original_height, video_area_width, video_area_height)

video_fps = cap.get(cv2.CAP_PROP_FPS)
clock = pygame.time.Clock()
pygame.mixer.music.load(os.path.join(Texture_path,'WelcomVideo/vidio.wav'))



#Булевые пременные для работы видео, полноэкранного режима, проверки нажатия паузы, работы програииы и аудио
fullscreen = False
mousedown = False
audio_start = False
rab = True
dubl_red = None
if dubl_red == None:
    with open('dubl.json', "w", encoding='utf-8') as f:
       json.dump(["True"], f)

    with open('dubl.json', "r", encoding='utf-8') as f:
       dubl_red = json.load(f)

# Инициализация переменных для воспроизведения видео
ret = False
frame = None
paused_frame = None
main_path = None
selected_file = None

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
                if main_path == None:
                    a = download_no_profile_error_massage()
                    if a == None:
                        pygame.display.flip()
                else:
                    dowloand_file = dowload_video_file()
                    if dowloand_file and dowloand_file != "":
                        shutil.move(dowloand_file, main_path)
                        a = download_complete_massage()
                        if a == None:
                            pygame.display.flip()

                    elif dowloand_file == "":
                        pass
                    else:
                        a_er = download_error_massage()
                        if a_er == None:
                            pygame.display.flip()

            elif profile_button_rect.collidepoint(pygame.mouse.get_pos()):
                # global main_path
                dubl = None
                if main_path == None:
                    main_path = select_window()
                    if main_path is None:
                        pygame.display.flip()
                else:
                    dubl = dubl_click()
                    if dubl is None:
                        pygame.display.flip()

            #Выбор из внутренней памяти
            elif select_button_rect.collidepoint(pygame.mouse.get_pos()):
                if main_path == None:
                    a = selected_error_massage()
                    if a == None:
                        pygame.display.flip()
                else:
                    selected_file = select_video_window(main_path)

                    if selected_file is None:
                        pygame.display.flip()

                    if selected_file and selected_file != "":
                        # Получаем абсолютный путь к выбранному файлу и папке videos
                        abs_selected = os.path.abspath(selected_file)
                        abs_videos_dir = os.path.abspath(main_path)

                        # Проверяем нахождение в папке videos
                        if os.path.commonpath([abs_selected, abs_videos_dir]) == abs_videos_dir:
                            video_sel(selected_file, video_area_width, video_area_height)
                            b = select_complete_massage()
                            if b == None:
                                pygame.display.flip()
                        else:
                            select_error_massage()
                    else:
                        pass

            elif redactor_button_rect.collidepoint(pygame.mouse.get_pos()):

                with open('dubl.json', "r", encoding='utf-8') as f:
                    dubl_red = json.load(f)

                print(dubl_red[0])
                if dubl_red[0]:
                    subprocess.Popen([
                        sys.executable,
                        "redactor_window.py",
                        selected_file,
                        main_path,
                    ])
                else:
                    print(13)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            mousedown = not mousedown

            if mousedown:
                pygame.mixer.music.pause()
                if frame is not None:
                    paused_frame = frame.copy()
            else:
                pygame.mixer.music.unpause()
                paused_frame = None

            #Полноэкранный режим
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            #Нажатие для входа и выхода

            fullscreen = not fullscreen
            if fullscreen:
                new_x, new_y = pygame.display.get_desktop_sizes()[0]
                screen = pygame.display.set_mode((new_x, new_y-40))


                #Проверка Позиции элементов и обновление координат при полноэкранном режиме
                x, y = new_x, new_y
                rect_rect = rounded_rect.get_rect(center=(x // 2, y // 2.7))
                button_rect = button.get_rect(center=(x // 2, y  - 110))
                load_button_rect = load_button.get_rect()
                load_button_rect.right = x - 865
                load_button_rect.centery = y - 110
                select_button_rect = select_button.get_rect()
                select_button_rect.right = x - 550
                select_button_rect.centery = y - 100
                profile_button_rect = profile_button.get_rect(center=(x - 200, y - 110))


                #Центрирование и подгонка размера в полноэкранном режиме
                if 'cap' in globals():
                    curent_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    video_x, video_y, video_width, video_height = video_position_and_scale(
                        original_width, original_height, video_area_width, video_area_height)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, curent_pos)
                fullscreen = not fullscreen

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
            x, y = new_x, new_y
            rect_rect = rounded_rect.get_rect(center=(x // 2, y // 2.7))
            button_rect = button.get_rect(center=(x // 2, y // 2 + 330))
            load_button_rect = load_button.get_rect()
            load_button_rect.right = x - 700
            load_button_rect.centery = y // 2 + 330
            select_button_rect = select_button.get_rect()
            select_button_rect.right = x - 375
            select_button_rect.centery = y // 2 + 335
            profile_button_rect = profile_button.get_rect(center=(x - 150, y - 70))

            # Центрирование и подгонка размера в полноэкранном режиме
            if 'cap' in globals():
                curent_pos = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                video_x, video_y, video_width, video_height = video_position_and_scale(
                    original_width, original_height, video_area_width, video_area_height)
                cap.set(cv2.CAP_PROP_POS_FRAMES, curent_pos)

        #Возврат к прежним координатам кнопок
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
    screen.blit(redactor_button, redactor_button_rect)
    screen.blit(button, button_rect) #Кнопка старт/стоп/пауза
    screen.blit(load_button, load_button_rect)# Кнопка загрузки во внутреннию память
    screen.blit(select_button, select_button_rect)
    screen.blit(profile_button, profile_button_rect)
    pygame.display.flip()