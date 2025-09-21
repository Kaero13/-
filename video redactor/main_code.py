import pygame
import cv2
import numpy as np


pygame.init()

x = 1200
y = 800
screen = pygame.display.set_mode((x, y))
button = pygame.image.load('Изображение WhatsApp 2025-09-21 в 07.13.57_995f08d2.jpg')
button_rect = button.get_rect(center = (x//2, y//2 + 300))

cap = cv2.VideoCapture('vidio.mp4')
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_x = (x - video_width) // 2
video_y = 50

mousedown = False

rab = True
while rab:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rab = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                mousedown = not mousedown
                print('T' if mousedown else 'F')
    if mousedown:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret,frame = cap.read()

    screen.fill((121,121,121))
    if 'frame' in locals() and ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_roted = np.rot90(frame_rgb)
        frame_surface = pygame.surfarray.make_surface(video_roted)
        screen.blit(frame_surface, (video_x, video_y))

    screen.blit(button, button_rect)
    pygame.display.flip()
