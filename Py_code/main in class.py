from button_modul import *

class VideoRedactor(QMainWindow):
    class Explorer:
        def __init__(self, folder_path, parent_folder):
            self.parent_folder = parent_folder
            self.folder_path = folder_path
            # print(self.folder_path)
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
                    return str(self.folder_path + "\\" + self.select_file)
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
            self.select_file = str(VideoRedactor.Explorer(folder_name, self.folder_path))

        def on_select_file(self, file_name):
            self.select_file = file_name
            self.root.destroy()

        def back_door(self):
            k = 0
            for i in self.folder_path[::-1]:
                if i == "\\":
                    k += 1
                    break
                else:
                    k += 1

            if len(self.parent_folder) <= len(self.folder_path[:-k]):
                self.root.destroy()
                VideoRedactor.Explorer(self.folder_path[:-k], self.parent_folder)

        def file_btns(self):

            btns_field = []
            self.btns_frame.pack(padx=10, pady=10)

            btns_field.clear()

            for col_id in range(self.width):
                btns_column = []
                btns_field.append(btns_column)

                for row_id in range(self.height):
                    btn_index = row_id * self.width + col_id

                    if btn_index < self.colwo:
                        file_name = self.data[btn_index]

                        if os.path.isdir(os.path.join(self.folder_path, file_name)):
                            btn_new = tk.Button(self.column_frame,
                                                text=self.text_min(file_name) + "📁",
                                                width=20,
                                                height=3,
                                                bg="green",
                                                command=lambda
                                                    v=self.folder_path + "\\" + file_name: self.on_select_folder(v)
                                                )
                            btn_new.grid(row=row_id, column=col_id, padx=2, pady=2)
                            btns_column.append(btn_new)
                        else:
                            btn_new = tk.Button(self.column_frame,
                                                text=self.text_min(file_name),
                                                width=20,
                                                height=3,
                                                command=lambda v=file_name: self.on_select_file(v)
                                                )
                            btn_new.grid(row=row_id, column=col_id, padx=2, pady=2)
                            btns_column.append(btn_new)

                        self.column_frame.pack(side="left")
                        btns_column.append(self.column_frame)

    def __init__(self):
        super().__init__()
        self.original_video_geometry = None
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Редактор видео")
        self.desctop_screen_geometry = self.screen().availableGeometry()
        self.wigth_desctop_screen , self.height_desctop_screen = self.desctop_screen_geometry.width() , self.desctop_screen_geometry.height()
        self.size_x_app_screen , self.size_y_app_screen = self.desctop_screen_geometry.width() // 1.5 , self.desctop_screen_geometry.height() // 1.5
        self.posit_x_app_screen, self.posit_y_app_screen = self.wigth_desctop_screen//5.5, self.height_desctop_screen//5.5
        self.app_screen = self.setGeometry(int(self.posit_x_app_screen),
                                           int(self.posit_y_app_screen),
                                           int(self.size_x_app_screen),
                                           int(self.size_y_app_screen))
        self.app_screen_geometry = self.frameGeometry()
        self.BackGroundSetting()
        self.gui()
        self.video_widjet(f"{Path(__file__).parent.parent}\\Texture\\WelcomVideo\\vidio.mp4")

    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        if modifiers == Qt.KeyboardModifier.AltModifier and key == Qt.Key.Key_Return:
           self.fullscreen(self.original_video_geometry)

        if Qt.Key.Key_Space == key:
            self.start()

        super().keyPressEvent(event)

    def resize_vide_in_window(self):
        video_frame_width = int(self.width() // 1.75)
        video_frame_height = int(self.height() // 1.75)
        video_frame_x = int((self.width() - video_frame_width) // 2)
        video_frame_y = int((self.height() - video_frame_height) // 2)

        self.videoWidjet.setGeometry(video_frame_x, video_frame_y, video_frame_width, video_frame_height)

    def fullscreen(self, geometry):
        if geometry is None:
            self.original_video_geometry = self.videoWidjet.geometry()
            self.videoWidjet.setGeometry(0, 0, self.width(), self.height())
        else:
            self.resize_vide_in_window()
            self.original_video_geometry = None

    def resizeEvent(self, event):
        self.bacground_lable.setGeometry(0, 0, self.width(), self.height())
        frame_width = int(self.width() // 1.5)
        frame_height = int(self.height() // 1.5)
        frame_x = (self.width() - frame_width) // 2
        frame_y = (self.height() - frame_height) // 2

        self.vide_frame.setGeometry(frame_x, frame_y, frame_width, frame_height)
        self.rectangle_lable.setGeometry(0, 0, frame_width, frame_height)

        start_width = int(self.width() // 1.6)
        start_height = int(self.height() // 1.6)
        start_x = int((self.width() - start_width) * 1.25)
        start_y = int((self.height() - start_height) * 2.25)
        self.start_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.start_button.setGeometry(start_x, start_y, int(start_height // 4.3), int(start_height // 4.3))

        self.open_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.open_button.setGeometry(   start_x + int(start_x // 4.5), start_y, int(frame_height // 4.3), int(frame_height // 4.3))

        self.profile_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.profile_button.setGeometry(start_x + int(start_x // 2.3), start_y, int(frame_height // 4.3), int(frame_height // 4.3))

        if self.original_video_geometry is None:
            self.resize_vide_in_window()
        else:
            self.videoWidjet.setGeometry(0, 0, self.width(), self.height())

        super().resizeEvent(event)

    def BackGroundSetting(self):
        #Подложка под видео
        frame_width = int(self.size_x_app_screen // 1.5)
        frame_height = int(self.size_y_app_screen // 1.5)
        frame_x = int((self.width() - frame_width) // 2)
        frame_y = int((self.height() - frame_height) // 2)

        self.vide_frame = QFrame(self)
        self.vide_frame.setGeometry(frame_x, frame_y, frame_width, frame_height)

        rectangle_image = create_rounded_rectangle()

        self.rectangle_lable = QLabel(self.vide_frame)
        width, height = rectangle_image.get_size()
        image_data = pygame.image.tostring(rectangle_image, "RGBA")

        pqt_image = QImage(image_data, width, height, QImage.Format.Format_RGBA8888)
        self.rectangle_pqt = QPixmap.fromImage(pqt_image)

        self.rectangle_lable.setPixmap(self.rectangle_pqt)
        self.rectangle_lable.setScaledContents(True)  # Чтобы изображение растягивалось
        self.rectangle_lable.setGeometry(0, 0, frame_width, frame_height)

        #Фон
        self.bacground_lable = QLabel(self)
        self.bacground_image = f"{Path(__file__).parent.parent}\\Texture\\fon.jpg"
        self.bacground_lable.setPixmap(QPixmap(self.bacground_image))
        self.bacground_lable.setGeometry(0,0, int(self.size_x_app_screen), int(self.size_y_app_screen))
        self.bacground_lable.setScaledContents(True)
        self.bacground_lable.lower()

    def gui(self):
        frame_width = int(self.width() // 1.5)
        frame_height = int(self.height() // 1.5)
        frame_x = int((self.width() - frame_width) * 1.25)
        frame_y = int((self.height() - frame_height) * 2.25)

        self.start_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\start_button.png"), "", self)
        self.start_button.clicked.connect(self.start)

        self.open_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\select_button.png"), "", self)
        self.open_button.clicked.connect(self.open_funct)

        self.profile_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\select_and_registr_profile.png"), "", self)
        # self.profile_button.clicked.connect()

        self.start_button.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 50);
                }
                QPushButton:pressed {
                    background-color: rgba(255, 255, 255, 100);
                }
            """)

        self.open_button.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 255, 255, 50);
                        }
                        QPushButton:pressed {
                            background-color: rgba(255, 255, 255, 100);
                        }
                    """)

        self.profile_button.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            border: none;
                        }
                        QPushButton:hover {
                            background-color: rgba(255, 255, 255, 50);
                        }
                        QPushButton:pressed {
                            background-color: rgba(255, 255, 255, 100);
                        }
                    """)

    def video_widjet(self, video_path):
        frame_width = int(self.size_x_app_screen // 1.75)
        frame_height = int(self.size_y_app_screen // 1.75)
        frame_x = int((self.width() - frame_width) // 2)
        frame_y = int((self.height() - frame_height) // 2)

        self.videoWidjet = QVideoWidget(self)
        self.videoWidjet.setGeometry(frame_x, frame_y, frame_width, frame_height)

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.videoWidjet)
        self.audioPlayer = QAudioOutput()

        self.mediaPlayer.setAudioOutput(self.audioPlayer)
        self.mediaPlayer.mediaStatusChanged.connect(self.cicle_video)
        self.mediaPlayer.setSource(QUrl.fromLocalFile(video_path))
        self.mediaPlayer.play()

    def cicle_video(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.mediaPlayer.setPosition(0)  # В начало
            self.mediaPlayer.play()  # Запускаем снова

    def start(self):
        if self.mediaPlayer.isPlaying() == True:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def open_funct(self):
        file = str(self.Explorer("C:\\Users\\Acer\\Kaero_video", "C:\\Users\\Acer\\Kaero_video"))

        if file != "":
            self.mediaPlayer.stop()
            self.mediaPlayer.setSource(QUrl.fromLocalFile(file))
            self.videoWidjet.update()
            self.videoWidjet.repaint()
        else:
            print("File not found")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoRedactor()
    window.show()
    sys.exit(app.exec())