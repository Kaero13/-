import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
from mutagen.mp4 import MP4

class Redactor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.duration_time = self.get_video_duration(video_path) or 100.0
        self.root = tk.Tk()
        self.root.title("Video Redactor")
        self.ui()
        self.root.mainloop()

    def get_video_duration(self, video_path):
        try:
            video = MP4(video_path)
            duration = video.info.length
            return duration
        except:
            return None

    def ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=5, pady=5)

        time_frame = ttk.Frame(self.root)
        time_frame.pack(padx=5, pady=5)

        button = ttk.Button(time_frame, text="button")
        button.grid(row=1, column=4)

        start_label = ttk.Label(time_frame, text="Начало: 0.0")
        start_label.grid(row=0, column=0)

        end_label = ttk.Label(time_frame, text=f"Конец: {self.duration_time:.1f}")
        end_label.grid(row=0, column=1)

        button = ttk.Button(time_frame, text="button")
        button.grid(row=1, column=4)

        slider_start = ttk.Scale(time_frame, from_=0, to=self.duration_time, orient="horizontal")
        slider_start.grid(row=1, column=0)

        slider_end = ttk.Scale(time_frame, from_=self.duration_time, to=0, orient="horizontal")
        slider_end.grid(row=1, column=1)

        def on_slider_change(event):
            start_val = slider_start.get()
            end_val = self.duration_time - slider_end.get()

            # Проверка на недопустимые значения
            if start_val > end_val:
                start_label.config(foreground="red")
                end_label.config(foreground="red")
                # Автоматическая коррекция
                if event.widget == slider_start:
                    slider_start.set(end_val)
                    start_val = end_val
                else:
                    slider_end.set(self.duration_time - start_val)
                    end_val = start_val
            else:
                start_label.config(foreground="black")
                end_label.config(foreground="black")

            start_label.config(text=f"Начало: {start_val:.1f}")
            end_label.config(text=f"Конец: {end_val:.1f}")

        slider_start.bind("<Motion>", on_slider_change)
        slider_end.bind("<Motion>", on_slider_change)

        def preview_video(video_path):
            cap = cv2.VideoCapture(video_path)
            ret, frame = cap.read()
            cap.release()

            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(frame_rgb)
                pil_image = ImageTk.PhotoImage(pil_image)
                return pil_image
            return None

        img = preview_video(self.video_path)
        if img:
            img_lable = ttk.Label(main_frame, image=img)
            img_lable.image = img
            img_lable.pack(padx=5, pady=5)


Redactor(r"C:\Users\Acer\Kaero_video\WhatsApp Video 2025-11-03 at 12.46.18.mp4")