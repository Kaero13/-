from button_modul import *


class Explorer:
    def __init__(self, folder_path, parent_folder):
        self.parent_folder = parent_folder
        self.folder_path = folder_path
        self.select_file = None
        self.root = tk.Tk()
        self.setting()
        self.file_btns()
        self.root.title("Explorer")
        self.root.eval('tk::PlaceWindow . center')
        self.root.mainloop()

    def __str__(self):
        # self.root.destroy()
        if self.select_file is not None:
            if self.folder_path in self.select_file:
                return str(self.select_file)
            else:
                return str(self.folder_path + "/" + self.select_file)
        return str(None)

    def setting(self):
        self.data = os.listdir(self.folder_path)
        self.colwo = len(self.data)
        self.width = min(4, max(1, (self.colwo + 1) // 2))
        self.height = (self.colwo + self.width - 1) // self.width
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.menu.add_command(label="назад", command=self.back_door)
        self.btns_frame = tk.Frame(self.root)
        self.column_frame = tk.Frame(self.btns_frame)

    def text_min(self, text):
        if len(text) > 12:
            resoult_text = text[:4] + "..." + text[-6:]
        else:
            resoult_text = text
        return resoult_text

    def on_select_folder(self, folder_name):
        self.root.destroy()
        self.select_file = str(Explorer(folder_name, self.folder_path))

    def on_select_file(self, file_name):
        self.select_file = file_name
        self.root.destroy()

    def back_door(self):
        k = 0
        for i in self.folder_path[::-1]:
            if i == "\\":
                k += 1
                break

            if i == "/":
                k += 1
                break

            else:
                k += 1

        if len(self.parent_folder) <= len(self.folder_path[:-k]):
            self.root.destroy()
            Explorer(self.folder_path[:-k], self.parent_folder)

    def file_btns(self):

        btns_field = []
        self.btns_frame.pack(padx=10, pady=10)

        btns_field.clear()

        for col_id in range(self.width):
            btns_column = []
            btns_field.append(btns_column)

            for row_id in range(self.height):
                btn_index = row_id*self.width + col_id

                if btn_index < self.colwo:
                    file_name = self.data[btn_index]

                    if os.path.isdir(os.path.join(self.folder_path, file_name)) and file_name != "audio":
                        btn_new = tk.Button(self.column_frame,
                                            text=self.text_min(file_name) + "📁",
                                            width=20,
                                            height=3,
                                            bg="green",
                                            command=lambda v=self.folder_path + "/" + file_name: self.on_select_folder(v)
                                            )
                        btn_new.grid(row=row_id,column=col_id, padx=2, pady=2)
                        btns_column.append(btn_new)
                    else:
                        btn_new = tk.Button(self.column_frame,
                                            text=self.text_min(file_name),
                                            width=20,
                                            height=3,
                                            command=lambda v=file_name: self.on_select_file(v)
                                            )
                        btn_new.grid(row=row_id,column=col_id, padx=2, pady=2)
                        btns_column.append(btn_new)

                    self.column_frame.pack(side="left")
                    btns_column.append(self.column_frame)

class Redactor:
    def __init__(self, video_path, video_output_path):
        self.temp_path = os.path.join((Path(__file__).parent.parent), "temp")
        self.video_path = video_path
        self.path = None
        self.path2 = None
        self.video_output_path = video_output_path
        self.duration_time = self.get_video_duration(self.video_path) or 117.0
        self.root = tk.Tk()
        self.dubl()
        self.root.title("Video Redactor")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.ui()
        self.root.mainloop()

    def dubl(self):
        with open(f"{Path(__file__).parent.parent}/temp/dubl.json", 'w', encoding='utf-8') as f:
            dubl = [False]
            json.dump(dubl, f)

    def on_closing(self):
        with open(f"{Path(__file__).parent.parent}/temp/dubl.json", 'w', encoding='utf-8') as f:
            dubl = [True]
            json.dump(dubl, f)
        self.root.destroy()


    def select_first_video(self):
        thread = threading.Thread(target=self.select_video_file_first)
        thread.daemon = True
        thread.start()

    def select_video_file_first(self):
        try:
            file_path = Explorer(self.video_output_path, self.video_output_path)
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
            file_path = Explorer(self.video_output_path, self.video_output_path)
            if file_path:
                self.path_2 = file_path
            self.root.after(0, lambda: self.name_second_video.set(file_path))

        except Exception as e:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}/ERROR.py",
                "error",
                str(e)
            ])

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
            if os.path.splitext(self.first_pol_video.get())[1] == os.path.splitext(self.second_pol_video.get())[1]:
                self.racshirenie = os.path.splitext(self.first_pol_video.get())[1]
                clip_one = VideoFileClip(self.first_pol_video.get())
                clip_two = VideoFileClip(self.second_pol_video.get())

                final_video = concatenate_videoclips([clip_one, clip_two], method="compose")

                write = os.path.join(self.video_output_path, "videos")
                output_path = os.path.join(write, (self.video_name_val.get() + self.racshirenie))
                final_video.write_videofile(output_path, codec='libx264', audio_codec='aac',temp_audiofile_path=self.temp_path)

                clip_one.close()
                clip_two.close()
                final_video.close()

        except Exception as e:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}/ERROR.py",
                "error",
                str(e)
            ])

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
            durate = None
            for i in mt.MediaInfo.parse(video_path).tracks:
                durate = i.duration / 1000
                break
            if durate is not None:
                return durate
        except Exception as e:
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
        time_frame.pack(padx=5, pady=0)

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

        info_frame = ttk.Frame(self.root)
        info_frame.pack(padx=5, pady=5)

        info_glue = ttk.Label(info_frame, text="Склеивать можно только видео одно и того же расширения")
        info_glue.pack(padx=1, pady=2)

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

# Redactor(r"C:\Users\Acer\PycharmProjects\PythonProject\video redactor\video2\file_example_AVI_480_750kB.avi", r"C:\Users\Acer\PycharmProjects\PythonProject\video redactor\video2")