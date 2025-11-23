import pygame.image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from button_modul import *


class VideoRedactor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Редактор видео")
        self.desctop_screen_geometry = QDesktopWidget().screenGeometry()
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

    def resizeEvent(self, event):
        self.bacground_lable.setGeometry(0, 0, self.width(), self.height())
        frame_width = int(self.width() // 1.5)
        frame_height = int(self.height() // 1.5)
        frame_x = (self.width() - frame_width) // 2
        frame_y = (self.height() - frame_height) // 2

        self.vide_frame.setGeometry(frame_x, frame_y, frame_width, frame_height)
        self.rectangle_lable.setGeometry(0, 0, frame_width, frame_height)

        super().resizeEvent(event)

    def BackGroundSetting(self):
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

        self.bacground_lable = QLabel(self)
        self.bacground_image = f"{Path(__file__).parent.parent}\\Texture\\fon.jpg"
        self.bacground_lable.setPixmap(QPixmap(self.bacground_image))
        self.bacground_lable.setGeometry(0,0, int(self.size_x_app_screen), int(self.size_y_app_screen))
        self.bacground_lable.setScaledContents(True)
        self.bacground_lable.lower()



    def gui(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoRedactor()
    window.show()
    sys.exit(app.exec_())