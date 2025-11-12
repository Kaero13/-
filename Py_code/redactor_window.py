from select_video import *
import os
import tkinter as tk
from tkinter import ttk
from mutagen.mp4 import MP4
from moviepy import VideoFileClip, concatenate_videoclips
import threading
import json

class Redactor:
    def __init__(self, video_path, video_output_path):
        self.video_path = video_path
        self.path = None
        self.video_output_path = video_output_path
        self.duration_time = self.get_video_duration(video_path) or 100.0
        self.root = tk.Tk()
        self.dubl()
        self.root.title("Video Redactor")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.ui()
        self.root.mainloop()

    def dubl(self):
        with open('dubl.json', 'w', encoding='utf-8') as f:
            dubl = [False]
            json.dump(dubl, f)

    def on_closing(self):
        with open('dubl.json', 'w', encoding='utf-8') as f:
            dubl = [True]
            json.dump(dubl, f)
        self.root.destroy()


    def select_first_video(self):
        thread = threading.Thread(target=self.select_video_file_first)
        thread.daemon = True
        thread.start()

    def select_video_file_first(self):
        try:
            file_path = select_video_window(self.video_output_path)
            if file_path:
                self.path = file_path
            self.root.after(0, lambda: self.name_first_video.set(file_path))
        finally:
            print(self.path)

    def select_second_video(self):
        thread = threading.Thread(target=self.select_video_file_second)
        thread.daemon = True
        thread.start()

    def select_video_file_second(self):
        try:
            file_path = select_video_window(self.video_output_path)
            if file_path:
                self.path = file_path
            self.root.after(0, lambda: self.name_second_video.set(file_path))
        finally:
            print(self.path)

    def glue_video_thread(self):
        self.button_glue.config(state="disabled")
        self.button_glue.config(text="Склеивание...")

        # Запуск в отдельном потоке
        thread = threading.Thread(target=self.glue_video)
        thread.daemon = True
        thread.start()

    def glue_video(self):
        try:
            clip_one = VideoFileClip(self.first_pol_video.get())
            clip_two = VideoFileClip(self.second_pol_video.get())

            final_video = concatenate_videoclips([clip_one, clip_two], method="compose")

            write = os.path.join(self.video_output_path, "videos")
            output_path = os.path.join(write, (self.video_name_val.get() + ".mp4"))
            final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

            clip_one.close()
            clip_two.close()
            final_video.close()

        finally:
            self.root.after(0, self.enable_glue_button)

    def enable_glue_button(self):
        self.button_glue.config(state="normal")
        self.button_glue.config(text="Склеить видео")

    def get_audio_file(self):
        video = VideoFileClip(self.video_path)
        audio = video.audio
        audio_path = os.path.join(self.video_output_path, "audio")
        audio.write_audiofile(os.path.join(audio_path, os.path.basename(self.video_path)[:-4] + ".mp3"))
        video.close()

    def get_start_and_end_times(self):
        start = self.slider_start.get()
        end = self.duration_time - self.slider_end.get()
        return (start, end)

    def creat_clip(self):
        start, end = self.get_start_and_end_times()
        video = VideoFileClip(self.video_path)
        video_path = os.path.join(self.video_output_path, "videos")
        video_output = os.path.join(video_path, (self.video_name_val.get()+".mp4"))

        new_video = video.subclipped(start, end)
        new_video.write_videofile(video_output, codec='libx264', audio_codec='aac')

        video.close()

    def get_video_duration(self, video_path):
        try:
            video = MP4(video_path)
            duration = video.info.length
            return duration
        except:
            return None

    def ui(self):
        glue_frame = ttk.Frame(self.root)
        glue_frame.pack(padx=5,pady=10)

        self.name_first_video = tk.StringVar()
        self.name_second_video = tk.StringVar()

        self.first_select = tk.Button(glue_frame, text="...", command=lambda:self.select_first_video())
        self.first_select.grid(row=0, column=1)

        self.first_pol_video = tk.Entry(glue_frame, textvariable=self.name_first_video)
        self.first_pol_video.grid(row=0, column=0)

        self.second_pol_video = tk.Entry(glue_frame, textvariable=self.name_second_video)
        self.second_pol_video.grid(row=0, column=4)

        self.second_select = tk.Button(glue_frame, text="...", command=lambda:self.select_second_video())
        self.second_select.grid(row=0, column=3)

        self.button_glue = tk.Button(glue_frame, text="Склеить", command=self.glue_video_thread, bg="lightblue")
        self.button_glue.grid(row=0, column=2, )

        time_frame = ttk.Frame(self.root)
        time_frame.pack(padx=5, pady=5)

        start_label = ttk.Label(time_frame, text="Начало: 0.0")
        start_label.grid(row=0, column=1)

        end_label = ttk.Label(time_frame, text=f"Конец: {self.duration_time:.1f}")
        end_label.grid(row=0, column=2)

        self.slider_start = ttk.Scale(time_frame, from_=0, to=self.duration_time, orient="horizontal")
        self.slider_start.grid(row=1, column=1)

        self.slider_end = ttk.Scale(time_frame, from_=self.duration_time, to=0, orient="horizontal")
        self.slider_end.grid(row=1, column=2)

        video_name_lable = ttk.Label(time_frame, text="Название")
        video_name_lable.grid(row=0, column=0)

        self.video_name_val = tk.StringVar()
        self.video_name = tk.Entry(time_frame, width=20, textvariable=self.video_name_val)
        self.video_name.grid(row=1, column=0)

        sprawka_lable = ttk.Label(time_frame, text="в поле названия не нужно\n указывать расширение,\n также это поле название\n склеенных видео")
        sprawka_lable.grid(row=0, column=5)

        button = tk.Button(time_frame, text="Создать Клип", command=self.creat_clip)
        button.grid(row=1, column=4)

        audio_button = tk.Button(time_frame, text="Выгрузить аудиодорожку", command=self.get_audio_file)
        audio_button.grid(row=1, column=5)

        def on_slider_change(event):
            start_val = self.slider_start.get()
            end_val = self.duration_time - self.slider_end.get()

            # Проверка на недопустимые значения
            if start_val > end_val:
                start_label.config(foreground="red")
                end_label.config(foreground="red")
                # Автоматическая коррекция
                if event.widget == self.slider_start:
                    self.slider_start.set(end_val)
                    start_val = end_val
                else:
                    self.slider_end.set(self.duration_time - start_val)
                    end_val = start_val
            else:
                start_label.config(foreground="black")
                end_label.config(foreground="black")

            start_label.config(text=f"Начало: {start_val:.1f}")
            end_label.config(text=f"Конец: {end_val:.1f}")

        self.slider_start.bind("<Motion>", on_slider_change)
        self.slider_end.bind("<Motion>", on_slider_change)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        video_path = sys.argv[1]
        output_path = sys.argv[2]
        Redactor(video_path, output_path)

# Redactor(r"C:\Users\Acer\Kaero_video\WhatsApp Video 2025-11-03 at 12.46.18.mp4", r"C:\Users\Acer\Kaero_video")