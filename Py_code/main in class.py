from button_modul import *

class VideoRedactor(QMainWindow):
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
        self.video_widjet(r"E:\Baby's.Day.Out.1994.HD.720p.2xAVO(Gorchakov,Pronin).Eng.mkv")

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

        start_width = int(self.width() // 1.5)
        start_height = int(self.height() // 1.5)
        start_x = int((self.width() - start_width) * 1.25)
        start_y = int((self.height() - start_height) * 2.25)
        self.start_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.start_button.setGeometry(start_x, start_y, int(start_height // 2), int(start_height // 2))

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
        self.start_button.setIconSize(QSize(int(frame_height // 4.5), int(frame_height// 4.5)))
        self.start_button.setGeometry( frame_x, frame_y, int(frame_height // 2), int(frame_height// 2))
        self.start_button.clicked.connect(self.start)

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
        self.mediaPlayer.setSource(QUrl.fromLocalFile(video_path))

    def start(self):
        if self.mediaPlayer.isPlaying() == True:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoRedactor()
    window.show()
    sys.exit(app.exec())