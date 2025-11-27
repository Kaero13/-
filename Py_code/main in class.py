import shutil

from button_modul import *

class VideoRedactor(QMainWindow):
    class Explorer:
        def __init__(self, folder_path, parent_folder):
            self.parent_folder = parent_folder
            self.folder_path = folder_path
            # print(self.folder_path)
            self.select_file = None
            self.root = tk.Tk()
            print("окно")
            self.setting()
            self.file_btns()
            self.root.title("Explorer")
            self.root.eval('tk::PlaceWindow . center')
            self.root.mainloop()

        #Функция для возврата пути для выбранного видео
        def __str__(self):
            # self.root.destroy()
            if self.select_file is not None:
                if self.folder_path in self.select_file:
                    return str(self.select_file)
                else:
                    return str(self.folder_path + "\\" + self.select_file)
            return str(None)

        #Настройки окна проводника
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

        #Сокращение текста если он слишком длинный
        def text_min(self, text):
            if len(text) > 12:
                resoult_text = text[:4] + "..." + text[-6:]
            else:
                resoult_text = text
            return resoult_text

        #Открытие подпапки
        def on_select_folder(self, folder_name):
            self.root.destroy()
            self.select_file = str(VideoRedactor.Explorer(folder_name, self.folder_path))

        #Сохранение выбранного пути видео
        def on_select_file(self, file_name):
            self.select_file = file_name
            self.root.destroy()

        #Функция для возврата в родительскую папку
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

        #Создание кнопок файлов и папок
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

    class Load_selector(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent_window = parent
            self.setMinimumSize(500, 400)
            self.setWindowTitle("Окно выбора Загрузчика")
            self.setMaximumSize(500, 400)
            self.bacground_lable = QLabel(self)
            self.bacground_image = f"{Path(__file__).parent.parent}\\Texture\\fon_texture\\fon.jpg"
            self.bacground_lable.setPixmap(QPixmap(self.bacground_image))
            self.bacground_lable.setGeometry(0, 0, 500, 400)
            self.bacground_lable.setScaledContents(True)
            self.bacground_lable.lower()
            self.gui()

        #Нстроки окна выбора загрузчика
        def gui(self):
            self.label_video = QLabel(self)
            self.label_video.setText("Загрузчик видео в \n папку пользователя")
            self.load_video_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\load_video_button.png"),"", self)
            self.load_video_button.clicked.connect(self.on_video_load)

            self.label_fon = QLabel(self)
            self.label_fon.setText("Загрузчик изображений \n для фона главного ока")
            self.load_fon_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\load_fon_button.png"),"", self)
            self.load_fon_button.clicked.connect(self.on_fon_load)

            self.label_video.setGeometry(255, 0, 200, 200)
            self.load_video_button.setGeometry(250, 130, 200, 200)
            self.load_video_button.setIconSize(QSize(200, 200))

            self.label_fon.setGeometry(55, 0, 200, 200)
            self.load_fon_button.setGeometry(50, 130, 200, 200)
            self.load_fon_button.setIconSize(QSize(200, 200))

            self.on_of_button = QPushButton("Перемещение", self)
            self.on_of_button.setCheckable(True)
            self.on_of_button.setGeometry(200, 343, 100, 50)
            self.on_of_button.clicked.connect(self.on_of_function)

            self.label_video.setStyleSheet("font-size: 15px; color: black;")

            self.load_video_button.setStyleSheet("""
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

            self.label_fon.setStyleSheet("font-size: 15px; color: black;")

            self.load_fon_button.setStyleSheet("""
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

        #Загрузчик видео
        def on_video_load(self):
            if self.parent_window:
                self.parent_window.video_load_function()
                self.accept()

        #Загрузчик изображения для фона программы
        def on_fon_load(self):
            if self.parent_window:
                self.parent_window.fon_load_function()
                self.accept()

        def on_of_function(self):
            if self.on_of_button.isChecked():
                self.on_of_button.setText("Копирование")
                return 1
            else:
                self.on_of_button.setText("Перемещение")
                return 0

        def on_of_function_global(self):
            if self.on_of_button.isChecked():
                return 1
            else:
                return 0

    def __init__(self):
        super().__init__()
        project_Folders()
        self.vide_select_file = None
        self.original_video_geometry = None
        self.dubl_prof = str(True)
        self.main_path = None
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
        self.app_fon_profile = None
        self.app_screen_geometry = self.frameGeometry()
        self.BackGroundSetting()
        self.gui()
        self.video_widjet(f"{Path(__file__).parent.parent}\\Texture\\WelcomVideo\\vidio.mp4")

    #Назначеине комбинаций кнопок для быстрого управления программой
    def keyPressEvent(self, event):
        key = event.key()
        modifiers = event.modifiers()
        if modifiers == Qt.KeyboardModifier.AltModifier:

            #Переход в полноэкранный режим просмотра видео
            if key == Qt.Key.Key_Return:
               self.fullscreen(self.original_video_geometry)

            #Вызов окна регистрации/входа
            elif key == Qt.Key.Key_Q:
                self.profile_function()

            #Вызов окна выбора загрузчикка
            elif key == Qt.Key.Key_A:
                self.start_load_selector_class()

            #Вызов проводника по видео
            elif key == Qt.Key.Key_S:
                self.open_funct()

            #Вызов окна редактора
            elif key == Qt.Key.Key_D:
                self.redactor_function()

            #Вызов проводника по фонам
            elif key == Qt.Key.Key_W:
                self.fon_selector_function()

        #Старт/пауза
        if Qt.Key.Key_Space == key:
            self.start()

        super().keyPressEvent(event)

    #Функция изменения размера окна видео до полноэкранного режима
    def resize_vide_in_window(self):
        video_frame_width = int(self.width() // 1.75)
        video_frame_height = int(self.height() // 1.75)
        video_frame_x = int((self.width() - video_frame_width) // 2)
        video_frame_y = int((self.height() - video_frame_height) // 2)

        self.videoWidjet.setGeometry(video_frame_x, video_frame_y, video_frame_width, video_frame_height)

    #Функция для активации перехода в полноэкранный режим
    def fullscreen(self, geometry):
        if geometry is None:
            self.original_video_geometry = self.videoWidjet.geometry()
            self.videoWidjet.setGeometry(0, 0, self.width(), self.height())
        else:
            self.resize_vide_in_window()
            self.original_video_geometry = None

    #Функция для выравнивания и изменения размера окна и всех его элементов
    def resizeEvent(self, event):
        frame_width = int(self.width() // 1.5)
        frame_height = int(self.height() // 1.5)
        frame_x = (self.width() - frame_width) // 2
        frame_y = (self.height() - frame_height) // 2

        #Настрока размера и позиции фона
        self.bacground_lable.setGeometry(0, 0, self.width(), self.height())

        #Настрока размера и позиции подложки видео
        self.vide_frame.setGeometry(frame_x, frame_y, frame_width, frame_height)
        self.rectangle_lable.setGeometry(0, 0, frame_width, frame_height)

        self.rectangle_round.setGeometry(frame_x, frame_y, frame_width, frame_height)  # Чтобы изображение растягивалось
        self.rectangle_round.raise_()

        #Общий размер кнопок и их позиции
        start_width = int(self.width() // 1.6)
        start_height = int(self.height() // 1.6)
        start_x = int((self.width() - start_width) * 1.25)
        start_y = int((self.height() - start_height) * 2.25)

        #Более точное позиционирование и настройка размера кнопок
        #Кнопка старт/пауза
        self.start_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.start_button.setGeometry(start_x, start_y, int(start_height // 4.3), int(start_height // 4.3))

        #Кнопка выбора видео
        self.open_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.open_button.setGeometry(start_x + int(start_x // 4.5), start_y, int(frame_height // 4.3),
                                     int(frame_height // 4.3))

        #Кнопка регистрации/входа
        self.profile_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.profile_button.setGeometry(start_x + int(start_x // 2.3), start_y, int(frame_height // 4.3),
                                        int(frame_height // 4.3))

        #Кнопка выбора загрузчика
        self.load_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.load_button.setGeometry(start_x - int(start_x // 4.2), start_y, int(frame_height // 4.3),
                                     int(frame_height // 4.3))

        #Кнопка редактора
        self.redactor_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.redactor_button.setGeometry(start_x - int(start_x // 2.1), start_y, int(frame_height // 4.3),
                                         int(frame_height // 4.3))

        #Кнопка выбора фона
        self.fon_selector_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.fon_selector_button.setGeometry(start_x + int(start_x //1.17), start_y - int(start_y // 2), int(frame_height // 4.3),
                                         int(frame_height // 4.3))

        #Общие настроки позиции и размера слайдера громкости
        slider_x = int(start_x + (start_x // 1.4))
        slider_y = int(start_y + (start_y * 0.019))
        slider_width = int(frame_height // 3.5)
        slider_height = int(frame_height // 3.5)

        #Слайдер громкости
        self.volume_slider.setGeometry(slider_x, int(slider_y + (slider_y * 0.1)), slider_width, int(slider_height//8))

        # Настройки изображения громкости над слайдером
        images_width = frame_width
        images_x = slider_x
        images_y = slider_y - 10

        #Лайаут хранящий все изображения громкости
        self.volume_images_container.setGeometry(images_x, images_y, images_width, int(frame_height//6.3))

        #Изображения громкости 10, 20, 30, ... , 90, 100
        self.vl_10.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_10.setScaledContents(True)

        self.vl_20.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_20.setScaledContents(True)

        self.vl_30.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_30.setScaledContents(True)

        self.vl_40.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_40.setScaledContents(True)

        self.vl_50.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_50.setScaledContents(True)

        self.vl_60.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_60.setScaledContents(True)

        self.vl_70.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_70.setScaledContents(True)

        self.vl_80.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_80.setScaledContents(True)

        self.vl_90.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_90.setScaledContents(True)

        self.vl_100.setFixedSize(int(int(frame_width//13.5)//5.2), int(frame_height//8.5))
        self.vl_100.setScaledContents(True)

        #Первоначальное назначение размера окна видео и его изменение размера при растягивание окна программы
        if self.original_video_geometry is None:
            self.resize_vide_in_window()
        else:
            self.videoWidjet.setGeometry(0, 0, self.width(), self.height())

        super().resizeEvent(event)

    #Функция инцилизации фона и подложки видео
    def BackGroundSetting(self):
        #Подложка под видео
        frame_width = int(self.size_x_app_screen // 1.5)
        frame_height = int(self.size_y_app_screen // 1.5)
        frame_x = int((self.width() - frame_width) // 2)
        frame_y = int((self.height() - frame_height) // 2)

        self.vide_frame = QFrame(self)
        self.vide_frame.setGeometry(frame_x, frame_y, frame_width, frame_height)

        self.rectangle_lable = QLabel(self.vide_frame)

        self.rectangle_round = QLabel(self)
        self.rectangle_round.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\rounded_rectangle.png"))
        self.rectangle_round.setScaledContents(True)

        self.rectangle_lable.setGeometry(0, 0, frame_width, frame_height)

        #Фон
        self.bacground_lable = QLabel(self)
        self.bacground_image = f"{Path(__file__).parent.parent}\\Texture\\fon_texture\\fon.jpg"
        self.bacground_lable.setPixmap(QPixmap(self.bacground_image))
        self.bacground_lable.setGeometry(0,0, int(self.size_x_app_screen), int(self.size_y_app_screen))
        self.bacground_lable.setScaledContents(True)
        self.bacground_lable.lower()

    #Функия настройки всех кнопок, изображений и слайдера
    def gui(self):
        # Кнопка старт/пауза
        self.start_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\start_button.png"), "", self)
        self.start_button.clicked.connect(self.start)

        # Кнопка выбора видео
        self.open_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\select_button.png"), "", self)
        self.open_button.clicked.connect(self.open_funct)

        # Кнопка регистрации/входа
        self.profile_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\select_and_registr_profile.png"), "", self)
        self.profile_button.clicked.connect(self.profile_function)

        # Кнопка выбора загрузчика
        self.load_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\load_button.png"), "", self)
        self.load_button.clicked.connect(self.start_load_selector_class)

        # Кнопка редактора
        self.redactor_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\redactor_button.png"), "", self)
        self.redactor_button.clicked.connect(self.redactor_function)

        # Кнопка выбора фона
        self.fon_selector_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\fon_selector.png"), "", self)
        self.fon_selector_button.clicked.connect(self.fon_selector_function)

        # Слайдер громкости
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setValue(100)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.valueChanged.connect(self.volume_function_slider)

        #Контейнер для изображений
        self.volume_images_container = QWidget(self)

        # Горизонтальный layout для изображений
        volume_layout = QHBoxLayout(self.volume_images_container)
        volume_layout.setSpacing(2)  # Минимальное расстояние между изображениями
        volume_layout.setContentsMargins(0, 0, 0, 0)
        volume_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Создаем и добавляем изображения громкости в layout
        self.vl_10 = QLabel()
        self.vl_10.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl1.png"))

        self.vl_20 = QLabel()
        self.vl_20.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl2.png"))

        self.vl_30 = QLabel()
        self.vl_30.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl3.png"))

        self.vl_40 = QLabel()
        self.vl_40.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl4.png"))

        self.vl_50 = QLabel()
        self.vl_50.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl5.png"))

        self.vl_60 = QLabel()
        self.vl_60.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl6.png"))

        self.vl_70 = QLabel()
        self.vl_70.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl7.png"))

        self.vl_80 = QLabel()
        self.vl_80.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl8.png"))

        self.vl_90 = QLabel()
        self.vl_90.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl9.png"))

        self.vl_100 = QLabel()
        self.vl_100.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\volume_texture\\vl10.png"))

        # Добавляем изображения в layout
        volume_layout.addWidget(self.vl_10)
        volume_layout.addWidget(self.vl_20)
        volume_layout.addWidget(self.vl_30)
        volume_layout.addWidget(self.vl_40)
        volume_layout.addWidget(self.vl_50)
        volume_layout.addWidget(self.vl_60)
        volume_layout.addWidget(self.vl_70)
        volume_layout.addWidget(self.vl_80)
        volume_layout.addWidget(self.vl_90)
        volume_layout.addWidget(self.vl_100)

        # Стили для кнопок (остаются без изменений в сравнение с оригинальой текстуркой)
        # Кнопка старт/пауза
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

        # Кнопка выбора видео
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

        # Кнопка регистрации/входа
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

        # Кнопка выбора загрузчика
        self.load_button.setStyleSheet("""
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

        # Кнопка редактора
        self.redactor_button.setStyleSheet("""
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

        # Кнопка выбора фона
        self.fon_selector_button.setStyleSheet("""
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

        # Слайдер громкости
        self.volume_slider.setStyleSheet("""
            QSlider {
                background-color: rgba(128, 128, 128, 100);
            }
        """)

    # Инцилизация плееера
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
        self.mediaPlayer.play()
        self.mediaPlayer.pause()
        self.start_button.setIcon(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\start_button.png"))
        self.start_button.setEnabled(False)

    # Функция старт/пауза
    def start(self):
        if self.mediaPlayer.isPlaying() == True:
            self.mediaPlayer.pause()
            self.start_button.setIcon(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\start_button.png"))
        else:
            self.start_button.setIcon(QIcon(f"{Path(__file__).parent.parent}\\Texture\\gui_texture\\pause_button.png"))
            self.mediaPlayer.play()

    # Вызов проводника по видео
    def open_funct(self):
        # Проверка на вход в профиль
        if self.main_path is not None:
            try:
                self.vide_select_file = str(self.Explorer(self.main_path,self.main_path))

                # Обновление видео в плеере
                if self.vide_select_file != str(None):
                    self.mediaPlayer.stop()
                    self.mediaPlayer.setSource(QUrl.fromLocalFile(self.vide_select_file))
                    self.videoWidjet.update()
                    self.videoWidjet.repaint()
                    self.start_button.setEnabled(True)

                    # Сообщение о успехе
                    subprocess.run([
                        sys.executable,
                        f"{Path(__file__).parent}\\ERROR.py",
                        "sel_com"
                    ])

            # Сообщение об ошибке
            except Exception as e:
                subprocess.run([
                    sys.executable,
                    f"{Path(__file__).parent}\\ERROR.py",
                    "error",
                    str(e)
                ])
        
        #Сообщение о необходимости войти в профиль 
        else:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\ERROR.py",
                "sel_err"
            ])

    # Функция настроки громкости
    def volume_function_slider(self, value):
        for i in range(10, 101, 10):
            eval(f"self.vl_{i}.hide()")

        for i in range(10, value + 1, 10):
            eval(f"self.vl_{i}.show()")

        valume = value / 100
        self.audioPlayer.setVolume(valume)

    # Функция рвызова окна входа/регистрации
    def profile_function(self):
        # Вызов окна
        try:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\profile_seletc_window.py",
                self.dubl_prof,
                str(False)
            ])

        # Сообщение об ошибке
        except Exception as e:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\ERROR.py",
                "error",
                str(e)
            ])

        # Чтение временного файла созданного окном входа/регистрации
        try:
            with open(f"{Path(__file__).parent.parent}\\temp\\profile_path_and_dubl.json", "r", encoding='utf-8') as f:
                local_path = json.load(f)
            
            if local_path != {}:
                self.dubl_prof = str(local_path["Second"])
                self.main_path = local_path["First"]
                self.app_fon_profile = local_path["Third"]
                if self.app_fon_profile != "":
                    self.auto_fon_select_function()

        # Сообщение об ошибке
        except Exception as e:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\ERROR.py",
                "error",
                str(e)
            ])

    # Функция загрузки в личную папку видео
    def video_load_function(self):
        try:
            if self.main_path != None:
                filter_string = "Videos (*.mov *.mp4 *.avi, *.mkv, *.wmv);; Any files (*)"
                file, _ = QFileDialog.getOpenFileName(self, "Выберите видео", "", filter_string)

                if file and file != "":

                    # Проверка на выбор режима загрузчика
                    if self.loader.on_of_function_global() == 0:
                        shutil.move(file, self.main_path)

                        subprocess.run([
                            sys.executable,
                            f"{Path(__file__).parent}\\ERROR.py",
                            "dow_com"
                        ])

                    else:
                        shutil.copy(file, self.main_path)

                        subprocess.run([
                            sys.executable,
                            f"{Path(__file__).parent}\\ERROR.py",
                            "dow_com"
                        ])
            else:
                subprocess.run([
                    sys.executable,
                    f"{Path(__file__).parent}\\ERROR.py",
                    "dow_err"
                ])

        except Exception as e:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\ERROR.py",
                "error",
                str(e)
            ])

    # Функция загрузки изображения фона в папку текстур фона
    def fon_load_function(self):
        # Проверка на вход в профиль
        if self.main_path != None:
            
            # Попытка открытия json с данными пользователей
            try:
                with open(f"{Path(__file__).parent.parent}\\Profile_Data\\Profile_Data.json", "r", encoding='utf-8') as f:
                    data = json.load(f)

                for key in data.keys():
                    
                    # Попытка открытия json для записи нового фона для конкретного пользователя
                    try:
                        if data[key]["Video_path"] == self.main_path:
                            filter_string = "Images (*.png *.jpg *.bmp);; Any files (*)"
                            fon_file, _ = QFileDialog.getOpenFileName(self,"Выберите изображение", "", filter_string)
                            if fon_file != "":
                                fon_name = fon_file.split("/")[-1]
                                if r"fon_texture" not in fon_file:

                                    # Проверка на выбор режима загрузчика
                                    if self.loader.on_of_function_global() == 0:
                                        shutil.move(fon_file, f"{Path(__file__).parent.parent}\\Texture\\fon_texture")
                                        data[key]["Fon_path"] = f"{Path(__file__).parent.parent}\\Texture\\fon_texture\\{fon_name}"

                                        self.bacground_lable.setPixmap(QPixmap(f"{Path(__file__).parent.parent}\\Texture\\fon_texture\\{fon_name}"))

                                    else:
                                        shutil.copy(fon_file, f"{Path(__file__).parent.parent}\\Texture\\fon_texture")
                                        data[key]["Fon_path"] = f"{Path(__file__).parent.parent}\\Texture\\fon_texture\\{fon_name}"

                                        self.bacground_lable.setPixmap(QPixmap(
                                            f"{Path(__file__).parent.parent}\\Texture\\fon_texture\\{fon_name}"))

                                else:
                                    print("> error exit")
                    except Exception as e:
                        raise e

            except Exception as e:
                subprocess.run([
                    sys.executable,
                    f"{Path(__file__).parent}\\ERROR.py",
                    "error",
                    str(e)
                ])

        # Сообщение о необходимости войти в профиль
        else:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\ERROR.py",
                "fon_dow_err"
            ])

    # Функция выбора фона 
    def fon_selector_function(self):
        # Проверка на вход в профиль
        if self.main_path is not None:
            self.app_fon_profile = str(self.Explorer(f"{Path(__file__).parent.parent}\\Texture\\fon_texture",f"{Path(__file__).parent.parent}\\Texture\\fon_texture"))
            
            if os.path.splitext(self.app_fon_profile)[-1] in ('.png', '.jpg', '.bmp', '.jpeg'):
                self.bacground_lable.setPixmap(QPixmap(self.app_fon_profile))
            else:
                self.app_fon_profile = None

            if self.app_fon_profile != None:
                # Попытка открытия json и  попытка записи нового фона для конкретного пользователя 
                try:
                    with open(f"{Path(__file__).parent.parent}\\Profile_Data\\Profile_Data.json", "r", encoding='utf-8') as f:
                        data = json.load(f)
                    for key in data.keys():
                        print(data[key]["Video_path"])
                        data[key]["Fon_path"] = self.app_fon_profile

                        with open(f"{Path(__file__).parent.parent}\\Profile_Data\\Profile_Data.json", "w", encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=4)

                # Сообщения об ошибке
                except Exception as e:
                    subprocess.run([
                        sys.executable,
                        f"{Path(__file__).parent}\\ERROR.py",
                        "error",
                        str(e)
                    ])
        # Сообщение о необходимости войти в профиль
        else:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\ERROR.py",
                "fon_sel_err"
            ])

    # Функция автоподгрузки не стандартного фона
    def auto_fon_select_function(self):
        self.bacground_lable.setPixmap(QPixmap(self.app_fon_profile))

    # Функция открытия окна выбора загрузчика
    def start_load_selector_class(self):
        try:
            self.loader = VideoRedactor.Load_selector(self)
            self.loader.exec()
        except Exception as e:
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\ERROR.py",
                "error",
                str(e)
            ])

    # Функция открытия редактора
    def redactor_function(self):
        if self.main_path != None:
            try:
                if self.vide_select_file != None:
                    subprocess.run([
                        sys.executable,
                        f"{Path(__file__).parent}\\redactor_window.py",
                        self.vide_select_file,
                        self.main_path
                    ])
                else:
                    subprocess.run([
                        sys.executable,
                        f"{Path(__file__).parent}\\ERROR.py",
                        "red_err"
                    ])

            except Exception as e:
                subprocess.run([
                    sys.executable,
                    f"{Path(__file__).parent}\\ERROR.py",
                    "error",
                    str(e)
                ])
        else:
            print(f"> {Path(__file__).parent}")
            subprocess.run([
                sys.executable,
                f"{Path(__file__).parent}\\ERROR.py",
                "red_err"
            ])


# Запуск программы
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoRedactor()
    window.show()
    sys.exit(app.exec())