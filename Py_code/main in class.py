import os.path

from button_modul import *
import unicodedata

class VideoRedactor(QMainWindow):
    class Explorer(QDialog):
        def __init__(self, current_folder, dop_folder):
            super().__init__()
            self.current_folder = current_folder
            self.dop_folder = dop_folder
            self.file_and_folders_list = os.listdir(self.current_folder)
            self.selected_video_file = None
            self.setWindowTitle("Explorer")
            self.resize(750, 500)
            self.gui()

        def resoult(self):

            if self.selected_video_file is not None:
                return str(self.selected_video_file)
            else:
                return None

        def gui(self):

            main_layout = QVBoxLayout(self)

            self.command_panel(main_layout)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

            self.container_widget = QWidget()
            self.vbox = QVBoxLayout(self.container_widget)

            self.create_hbox()

            scroll_area.setWidget(self.container_widget)

            main_layout.addWidget(scroll_area)

        def command_panel(self, layout):
            command_box = QHBoxLayout()
            back_button = QPushButton("Назад")
            back_button.clicked.connect(
                lambda checked=False, prev_folder=self.dop_folder: self.back_command(prev_folder))
            command_box.addWidget(back_button)

            layout.addLayout(command_box)

        def back_command(self, prev_folder):
            if self.current_folder != prev_folder:
                self.close()
                new_window = VideoRedactor.Explorer(prev_folder, self.dop_folder)
                start = new_window.exec()
                if start == QDialog.DialogCode.Accepted:
                    self.selected_video_file = new_window.selected_video_file
                    self.accept()
            else:
                QMessageBox.information(self, "Важно", "Выйти из папки пользователя нельзя")

        def file_btn_clicked(self, name_file):
            self.selected_video_file = os.path.join(self.current_folder, name_file)
            self.accept()

        def folder_btn_clicked(self, name_file):
            new_dop_folder = os.path.join(self.dop_folder, name_file)
            self.close()
            new_window = VideoRedactor.Explorer(new_dop_folder, self.current_folder)
            start = new_window.exec()
            if start == QDialog.DialogCode.Accepted:
                self.selected_video_file = new_window.selected_video_file
                self.accept()

        def min_text(self, text):
            if len(text) > 14:
                new_text = text[:4] + "..." + text[-6:]
            else:
                new_text = text
            return new_text

        def create_hbox(self):
            hbox = QHBoxLayout()

            k = 0
            for i, item in enumerate(self.file_and_folders_list):
                prov_file_or_folder = os.path.join(self.current_folder, item)

                if os.path.isfile(prov_file_or_folder):
                    k += 1
                    file_btn = QPushButton(self.min_text(item))
                    file_btn.clicked.connect(lambda checked=False, name=item: self.file_btn_clicked(name))
                    file_btn.setToolTip(f"{item}")
                    file_btn.setStyleSheet("""
                        QPushButton {
                            /* Фон и граница */
                            background-color: #4CAF50;  /* Зеленый фон */
                            color: white;               /* Белый текст */
                            border: 2px solid #388E3C;  /* Темно-зеленая граница */
                            border-radius: 5px;         /* Закругленные углы */

                            /* Размеры */
                            min-width: 120px;
                            max-width: 120px;
                            min-height: 40px;
                            max-height: 40px;
                            padding: 5px;
                            font-size: 12px;
                        }

                        /* При наведении курсора */
                        QPushButton:hover {
                            background-color: #45a049;
                            border: 2px solid #2E7D32;
                        }

                        /* При нажатии */
                        QPushButton:pressed {
                            background-color: #388E3C;
                            padding-top: 6px;  /* Эффект нажатия */
                            padding-left: 6px;
                        }

                        /* Отключенная кнопка */
                        QPushButton:disabled {
                            background-color: #cccccc;
                            color: #666666;
                            border: 2px solid #aaaaaa;
                        }
                    """)

                    hbox.addWidget(file_btn)

                elif os.path.isdir(prov_file_or_folder):
                    k += 1
                    folder_btn = QPushButton(self.min_text(item))
                    folder_btn.clicked.connect(lambda checked=False, name=item: self.folder_btn_clicked(name))
                    folder_btn.setToolTip(f"{item}")
                    folder_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #f3e5f5;  /* Светло-фиолетовый */
                            color: #7b1fa2;             /* Фиолетовый текст */
                            border: 1px solid #ce93d8;
                            border-radius: 4px;
                            min-width: 120px;
                            max-width: 120px;
                            min-height: 40px;
                            max-height: 40px;
                            font-size: 12px;
                            font-weight: bold;
                        }
                        QPushButton:hover {
                            background-color: #e1bee7;
                            border: 1px solid #ba68c8;
                        }
                        QPushButton:pressed {
                            background-color: #ce93d8;
                        }
                    """)

                    hbox.addWidget(folder_btn)

                if k == 5:
                    self.vbox.addLayout(hbox)
                    hbox = QHBoxLayout()
                    k = 0

            if k > 0:
                self.vbox.addLayout(hbox)

            self.vbox.addStretch()

    class Load_selector(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.parent_window = parent
            self.setMinimumSize(500, 400)
            self.setWindowTitle("Окно выбора Загрузчика")
            self.setMaximumSize(500, 400)
            self.bacground_lable = QLabel(self)
            self.bacground_image = f"{Path(__file__).parent.parent}/Texture/fon_texture/fon.jpg"
            self.bacground_lable.setPixmap(QPixmap(self.bacground_image))
            self.bacground_lable.setGeometry(0, 0, 500, 400)
            self.bacground_lable.setScaledContents(True)
            self.bacground_lable.lower()
            self.gui()

        #Нстроки окна выбора загрузчика
        def gui(self):
            self.label_video = QLabel(self)
            self.label_video.setText("Загрузчик видео в \n папку пользователя")
            self.load_video_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/load_video_button.png"),"", self)
            self.load_video_button.clicked.connect(self.on_video_load)

            self.label_fon = QLabel(self)
            self.label_fon.setText("Загрузчик изображений \n для фона главного ока")
            self.load_fon_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/load_fon_button.png"),"", self)
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

    class Registr_window(QDialog):
        class Registr_function:
            def __init__(self, login, password, folder):
                self.login = login
                self.password = password
                self.path = folder
                self.json_path = Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json")

            @staticmethod
            def get_keys():
                with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), 'r', encoding='utf-8') as f:
                    profile = json.load(f)

                keys_list = []

                for key in profile.keys():
                    keys_list.append(key)

                return keys_list

            @staticmethod
            def get_profiles_dict():
                with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), 'r', encoding='utf-8') as f:
                    profile = json.load(f)

                return profile

            @staticmethod
            def get_cur_profile(nik):
                try:
                    with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), 'r', encoding='utf-8') as f:
                        profiles = json.load(f)

                    cur_profile = profiles[nik]
                    data = {"0": nik, "1": cur_profile["Video_path"], "2": cur_profile["Fon_path"], "3": cur_profile["remember_me"]}
                    return data
                except Exception as e:
                    print(f"0>>{e}")

            @staticmethod
            def remember(nik):
                try:
                    with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), 'r', encoding='utf-8') as f:
                        profiles = json.load(f)

                    revork_profile = profiles[nik]
                    revork_profile['remember_me'] = True

                    with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), 'w', encoding='utf-8') as f:
                        json.dump(profiles, f, ensure_ascii=False, indent=2)

                except Exception as e:
                    print(f"1>>{e}")

            @staticmethod
            def not_remember(nik):
                try:
                    with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), 'r', encoding='utf-8') as f:
                        profiles = json.load(f)

                    revork_profile = profiles[nik]
                    revork_profile['remember_me'] = False

                    with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), 'w', encoding='utf-8') as f:
                        json.dump(profiles, f, ensure_ascii=False, indent=2)

                except Exception as e:
                    print(f"2>>{e}")

            def dump_data(self):
                try:
                    if not self.json_path.exists():
                        with open(self.json_path, "w", encoding="utf-8") as data:
                            try:
                                new_data = {
                                    self.login : {
                                        "Password": self.password,
                                        "Video_path": self.path,
                                        "Fon_path": "",
                                        "remember_me": False
                                        }
                                    }

                                json.dump(new_data, data, ensure_ascii=False, indent=2)
                            except Exception as e:
                                print(f"3>>{e}")

                    else:
                        with open(self.json_path, "r", encoding="utf-8") as data:
                            old_data = json.load(data)

                        new_data = old_data | {
                                    self.login: {
                                        "Password": self.password,
                                        "Video_path": self.path,
                                        "Fon_path": "",
                                        "remember_me": False
                                        }
                                    }

                        with open(self.json_path, "w", encoding="utf-8") as data:
                            json.dump(new_data, data, ensure_ascii=False, indent=2)

                except Exception as e:
                    print(f"4>>{e}")

        def __init__(self, parent):
            super().__init__()
            self.parent_window = parent
            self.setWindowTitle("Registry")
            self.vertical_layout = QVBoxLayout(self)
            self.Login = ""
            self.gui()

        def gui(self):
            try:
                self.clear_window()

                self.resize(500, 200)
                self.setMaximumSize(500, 200)

                btn_layout = QHBoxLayout()
                folder_layout = QHBoxLayout()

                nik_input = QLineEdit(self)
                nik_input.setPlaceholderText("Введите имя пользователя")
                password_input = QLineEdit(self)
                password_input.setPlaceholderText("Введите пароль")
                password_input.setEchoMode(QLineEdit.EchoMode.Password)
                self.folder_for_input = QLineEdit(self)
                self.folder_for_input.setPlaceholderText("Введите путь к папке проекта или выберите в проводнике")

                explorer_btn = QPushButton("📁", self)
                explorer_btn.clicked.connect(self.open_system_explorer)

                regist_btn = QPushButton(self)
                regist_btn.setText("Зарегистрироваться")
                regist_btn.clicked.connect(partial(self.registred, nik_input, password_input, self.folder_for_input))

                sing_window_btn = QPushButton(self)
                sing_window_btn.setText("Окно входа")
                sing_window_btn.clicked.connect(self.gui_sing)

                folder_layout.addWidget(self.folder_for_input)
                folder_layout.addWidget(explorer_btn)

                btn_layout.addWidget(regist_btn)
                btn_layout.addWidget(sing_window_btn)

                self.vertical_layout.addWidget(nik_input)
                self.vertical_layout.addWidget(password_input)
                self.vertical_layout.addLayout(folder_layout)
                self.vertical_layout.addLayout(btn_layout)

            except Exception as e:
                print(f"5>>{e}")

        def gui_sing(self):
            try:
                self.clear_window()

                self.resize(500, 200)
                self.setMaximumSize(500, 200)

                btn_layout = QHBoxLayout()

                nik_input = QLineEdit(self)
                nik_input.setMinimumWidth(100)
                nik_input.setPlaceholderText("Введите свой ник")
                password_input = QLineEdit(self)
                password_input.setMinimumWidth(100)
                password_input.setEchoMode(QLineEdit.EchoMode.Password)
                nik_input.setPlaceholderText("Введите свой пароль")

                remember_me = QCheckBox(self)
                remember_me.setText("Запомнить меня?")
                remember_me.setChecked(False)

                sing_btn = QPushButton(self)
                sing_btn.setText("Войти")
                sing_btn.clicked.connect(partial(self.sing, nik_input, password_input, remember_me))

                regist_window_btn = QPushButton(self)
                regist_window_btn.setText("Окно регистрации")
                regist_window_btn.clicked.connect(self.gui)

                btn_layout.addWidget(remember_me)
                btn_layout.addWidget(sing_btn)
                btn_layout.addWidget(regist_window_btn)

                self.vertical_layout.addWidget(nik_input)
                self.vertical_layout.addWidget(password_input)
                self.vertical_layout.addLayout(btn_layout)

            except Exception as e:
                print(f"6>>{e}")

        def clear_window(self):
            try:
                while self.vertical_layout.count():
                    item = self.vertical_layout.takeAt(0)
                    widget = item.widget()
                    layout = item.layout()

                    if widget:
                        widget.deleteLater()

                    elif layout:
                        while layout.count():
                            item2 = layout.takeAt(0)
                            widget = item2.widget()

                            if widget:
                                widget.deleteLater()

                        layout.deleteLater()
            except Exception as e:
                print(f"7>>{e}")

        def registred(self, nik_widget, password_widget, folder_widget):
            try:
                nik = nik_widget.text()
                password = password_widget.text()
                folder = folder_widget.text()

                eng_alf = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

                rus_alf = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М',
                           'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ',
                           'Ъ','Ы', 'Ь', 'Э', 'Ю', 'Я']

                Good_password = False

                if len(password) >= 8:
                    for i in password:
                        if i in eng_alf or i in rus_alf:
                            Good_password = True
                            break

                if Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json").exists() and nik != "":

                    if nik not in self.Registr_function.get_keys() and Good_password == True:

                            if os.path.isdir(folder):
                                if not any('CYRILLIC' in unicodedata.name(c, '') for c in folder):
                                    self.Registr_function(nik, password, folder).dump_data()
                                    in_user_folder(folder)
                                    self.accept()
                                else:
                                    QMessageBox.warning(self, "Внимание", "Плохая папка. Название должно быть на английском.")
                            else:
                                QMessageBox.warning(self, "Внимание", "Плохая папка. Введите верный путь.")

                    elif nik not in self.Registr_function.get_keys() and Good_password == False:
                        QMessageBox.warning(self, "Внимание", "Плохой пароль. Введите новый.")

                    elif nik in self.Registr_function.get_keys() and Good_password == True:
                        QMessageBox.warning(self, "Внимание", "Плохой логин. Введите новый.")

                    else:
                        QMessageBox.warning(self, "Внимание", "Плохой пароль, логин или папка. Введите их заново.")

                elif not Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json").exists() and nik != "":

                    if os.path.isdir(folder):
                        if not any('CYRILLIC' in unicodedata.name(c, '') for c in folder):
                            self.Registr_function(nik, password, folder).dump_data()
                            in_user_folder(folder)
                            self.accept()
                        else:
                            QMessageBox.warning(self, "Внимание", "Плохая папка. Название должно быть на английском.")

                    else:
                        QMessageBox.warning(self, "Внимание", "Плохая папка. Введите верный путь.")

                elif nik == "":
                    QMessageBox.warning(self, "Внимание", "Пожалуйста введите логин.")

            except Exception as e:
                print(f"55>>{e}")

        def sing(self, nik_widget, password_widget, remember_me_widget):
            try:
                nik = nik_widget.text()
                password = password_widget.text()
                remember_me = remember_me_widget.isChecked()

                if nik in self.Registr_function.get_keys() and password == self.Registr_function.get_profiles_dict()[nik]["Password"]:

                    data = self.read_json_profile()

                    if remember_me == True:
                        self.Registr_function.remember(nik)

                        if "auto_profile" in data:

                            if data["auto_profile"]["0"] != nik:
                                self.Registr_function.not_remember(data["auto_profile"]["0"])
                                data = self.read_json_profile()
                                self.dump_json_profile(data, nik)

                        else:
                            data = self.read_json_profile()
                            self.dump_json_profile(data, nik)

                    self.Login = nik
                    self.temp_file(data, nik)
                    self.accept()

                else:
                    QMessageBox.warning(self, "Внимание", "Неправильный пароль или ник")

            except Exception as e:
                print(f"8>>{e}")

        def who_singing(self):
            return self.Login

        def dump_json_profile(self, data, nik):
            try:
                profile_data = self.Registr_function.get_cur_profile(nik)
                new_data = data | {"auto_profile": profile_data}

                with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), "w", encoding="utf-8") as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=2)
                    f.flush()

                self.temp_file(data, nik)

            except Exception as e:
                print(f"Error in dump_json_profile: {e}")
                import traceback
                traceback.print_exc()

        def open_system_explorer(self):
            try:
                folder = QFileDialog.getExistingDirectory(self, "")
                if folder and len(self.folder_for_input.text()) == 0:
                    self.folder_for_input.setText(folder)
                elif len(self.folder_for_input.text()) != 0:
                    self.folder_for_input.clear()
                    self.folder_for_input.setText(folder)

            except Exception as e:
                print(f"9>>{e}")

        def temp_file(self, data, nik):
            try:
                if data[nik]["Fon_path"] == "":
                    self.parent_window.bacground_lable.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/fon_texture/fon.jpg"))

                with open(f"{Path(__file__).parent.parent}/temp/profile_path_and_dubl.json", "w", encoding='utf-8') as file:
                    dump_info = {
                        "First": data[nik]["Video_path"],
                        "Third": data[nik]["Fon_path"]
                    }
                    json.dump(dump_info, file)
            except Exception as e:
                print(f"10>>{e}")

        @staticmethod
        def auto_sing():
            try:
                if Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json").exists():
                    with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), "r", encoding="utf-8") as f:
                        data = json.load(f)

                    if "auto_profile" in data.keys():
                        a_p = data["auto_profile"]
                        if a_p["3"]:
                            nik = a_p["0"]
                            return nik
                        else:
                            return False
                    else:
                        pass
                else:
                    pass

            except Exception as e:
                print(f"11>>{e}")

        @staticmethod
        def read_json_profile():
            with open(Path(f"{Path(__file__).parent.parent}/Profile_data/profile.json"), "r", encoding="utf-8") as f:
                data = json.load(f)

            return data

        @classmethod
        def cur_session(cls, nik):
            try:
                return cls.Registr_function.get_cur_profile(nik)
            except Exception as e:
                print(f"12>>{e}")

    class Redactor_video(QDialog):
        def __init__(self, parent):
            super().__init__(parent)
            self.parent = parent
            self.resize(720, 300)
            self.video_format = ["mp4", "mov", "mkv", "avi", "wmv"]
            self.scale_factor = 0
            self.temp_path = get_path()[4]

            self.gui_redactor()
            self.list_value = []

        def scale(self, num):
            s = str(num).rstrip('0')
            if '.' in s:
                return len(s.split('.')[1])
            return 0

        def gui_redactor(self):
            try:
                vertical_layout = QVBoxLayout()
                select_layout = QHBoxLayout()
                glue_layout = QHBoxLayout()
                buttons_layout = QHBoxLayout()
                slider_layout = QHBoxLayout()

                self.slider_start = QSlider(Qt.Orientation.Horizontal)
                self.slider_start.setRange(0, 100)
                self.slider_start.setValue(0)
                self.slider_start.valueChanged.connect(self.get_value)
                self.slider_start.setEnabled(False)

                self.slider_end = QSlider(Qt.Orientation.Horizontal)
                self.slider_end.setRange(0, 100)
                self.slider_end.setValue(100)
                self.slider_end.valueChanged.connect(self.get_value)
                self.slider_end.setEnabled(False)

                self.video_for_redact_input = QLabel()
                self.video_for_redact_input.setStyleSheet("""
                   QLabel {
                           background-color: #ff0000;
                           padding: 10px;
                           border-radius: 8px;
                           border: 2px solid #3498db;
                           } 
                """)
                self.video_for_redact_input.setText("Выберите видео для редактирования")

                self.first_video_for_glue_input = QLineEdit()
                self.first_video_for_glue_input.setPlaceholderText("Введите первое видео для склейки")

                self.second_video_for_glue_input = QLineEdit()
                self.second_video_for_glue_input.setPlaceholderText("Введите второе видео для склейки")

                self.name_video_for_glue_input = QLineEdit()
                self.name_video_for_glue_input.setPlaceholderText("Введите название для склеенного видео")

                self.first_video_for_glue_button = QPushButton("Выберите", self)
                self.first_video_for_glue_button.clicked.connect(partial(self.exporer, self.first_video_for_glue_input))

                self.second_video_for_glue_button = QPushButton("Выберите", self)
                self.second_video_for_glue_button.clicked.connect(partial(self.exporer, self.second_video_for_glue_input))

                self.video_for_redact_button = QPushButton("Выберите", self)
                self.video_for_redact_button.clicked.connect(partial(self.exporer, self.video_for_redact_input))

                self.glue_button = QPushButton("Склеить", self)
                self.glue_button.clicked.connect(self.glue_video)

                self.cut_button = QPushButton("Создать клип", self)
                self.cut_button.clicked.connect(self.create_new_clip)
                self.cut_button.setEnabled(False)

                self.audio_from_video_button = QPushButton("Получить звук", self)
                self.audio_from_video_button.clicked.connect(self.get_audio_from_video)
                self.audio_from_video_button.setEnabled(False)

                select_layout.addWidget(self.video_for_redact_input)
                select_layout.addWidget(self.video_for_redact_button)
                vertical_layout.addLayout(select_layout)
                glue_layout.addWidget(self.first_video_for_glue_input)
                glue_layout.addWidget(self.first_video_for_glue_button)
                glue_layout.addWidget(self.second_video_for_glue_button)
                glue_layout.addWidget(self.second_video_for_glue_input)
                vertical_layout.addLayout(glue_layout)
                slider_layout.addWidget(self.slider_start)
                slider_layout.addWidget(self.slider_end)
                vertical_layout.addLayout(slider_layout)
                buttons_layout.addWidget(self.glue_button)
                buttons_layout.addWidget(self.cut_button)
                buttons_layout.addWidget(self.audio_from_video_button)
                buttons_layout.addWidget(self.name_video_for_glue_input)
                vertical_layout.addLayout(buttons_layout)

                self.setLayout(vertical_layout)
            except Exception as e:
                print(f"13>>{e}")

        def get_value(self):
            # Получаем текущие значения
            start_val = self.slider_start.value()
            end_val = self.slider_end.value()

            if start_val > end_val:
                # Если начало больше конца, корректируем
                sender = self.sender()

                if sender == self.slider_start:
                    # Если двигали начало, делаем конец равным началу
                    self.slider_end.setValue(start_val)
                    end_val = start_val
                elif sender == self.slider_end:
                    # Если двигали конец, делаем начало равным концу
                    self.slider_start.setValue(end_val)
                    start_val = end_val


            self.list_value = []
            if self.scale_factor != 0:
                self.list_value.append(start_val/(self.scale_factor*10))
                self.list_value.append(end_val/(self.scale_factor*10))
            else:
                self.list_value.append(start_val)
                self.list_value.append(end_val)

        def glue_video(self):
            try:
                self.glue_button.setEnabled(False)
                self.first = self.first_video_for_glue_input.text()
                self.second = self.second_video_for_glue_input.text()
                self.name_video = self.name_video_for_glue_input.text()

                if (self.first != "" or self.second != "") and self.name_video != "":
                    name = [i for i in self.name_video]
                    k = 0
                    for i in name:
                        if i in [r"\\", r"/", r":", r"*", r"?", "\"", "<", ">", "|"] or name[0] == " " or name[-1] == " ":
                            QMessageBox.information(self, "Важно", "Введите имя правильного формата.")
                            k = 1
                            self.glue_button.setEnabled(True)
                            break

                    if k != 1:
                        if os.path.splitext(self.first)[1] == os.path.splitext(self.second)[1]:
                            threading.Thread(target=self.glue_in_new_thread, daemon=True).start()

                        else:
                            QMessageBox.information(self, "Важно", "Видео должны быть одно и того же типа.")
                            self.glue_button.setEnabled(True)

                else:
                    QMessageBox.information(self, "Важно", "Выберите оба видео для склейки и введите название нового видео правильного формата.")

                    self.first_video_for_glue_input.setPlaceholderText("Введите первое видео для склейки")
                    self.second_video_for_glue_input.setPlaceholderText("Введите второе видео для склейки")
                    self.name_video_for_glue_input.setPlaceholderText("Введите название для склеенного видео")

                    self.glue_button.setEnabled(True)

            except Exception as e:
                print(f"14>>{e}")

        def glue_in_new_thread(self):
            self.racshirenie = os.path.splitext(self.first)[1]
            self.clip_one = VideoFileClip(self.first)
            self.clip_two = VideoFileClip(self.second)

            final_video = concatenate_videoclips([self.clip_one, self.clip_two], method="compose")
            folder_videos = os.path.join(self.parent.main_path, "videos")
            final_path = os.path.join(folder_videos, (self.name_video + self.racshirenie))

            final_video.write_videofile(final_path, codec="libx264", audio_codec="aac", temp_audiofile_path=self.temp_path)
            self.glue_button.setEnabled(True)

            self.clip_one.close()
            self.clip_two.close()
            final_video.close()

        def create_new_clip(self):
            try:
                self.cut_button.setEnabled(False)
                start_val , end_val = self.list_value[0], self.list_value[1]
                video_for_clip = self.video_for_redact_input.text()
                name = self.name_video_for_glue_input.text()

                if video_for_clip != "" and name != "":
                    name_list = [i for i in name]
                    k = 0
                    for i in name_list:
                        if i in [r"\\", r"/", r":", r"*", r"?", "\"", "<", ">", "|"] or name_list[0] == " " or name_list[-1] == " ":
                            QMessageBox.information(self, "Важно", "Введите имя правильного формата.")
                            k = 1
                            self.cut_button.setEnabled(True)
                            break

                    if k != 1:
                        threading.Thread(target=self.create_clip_in_new_thread, daemon=True, args=(start_val, end_val, video_for_clip, name)).start()

                else:
                    QMessageBox.information(self, "Важно", "Выберите видео и название для нового клипа")
                    self.cut_button.setEnabled(True)

            except Exception as e:
                print(f"15>>{e}")

        def create_clip_in_new_thread(self, start_val, end_val, video_for_clip, name):
            try:
                prev_clip = VideoFileClip(Path(video_for_clip))

                end_video_path = os.path.join(os.path.join(os.path.join(self.parent.main_path, "videos")), (name + os.path.splitext(video_for_clip)[1]))

                new_clip = prev_clip.subclipped(start_val, end_val)
                new_clip.write_videofile(end_video_path, codec='libx264', audio_codec='aac', temp_audiofile_path=self.temp_path)

                prev_clip.close()
                self.cut_button.setEnabled(True)

            except Exception as e:
                print(f"16>>{e}")

        def get_audio_from_video(self):
            try:
                video_for_clip = self.video_for_redact_input.text()

                if video_for_clip != "":
                    self.audio_from_video_button.setEnabled(False)
                    video = VideoFileClip(video_for_clip)
                    audio = video.audio
                    audio.write_audiofile(os.path.join(os.path.join(self.parent.main_path, "audio"), os.path.basename(video_for_clip)[:-4] + ".mp3"))

                    video.close()
                else:
                    QMessageBox.information(self, "Важно", "Выберите видео для котрого хотите получить аудиодорожку")

                self.audio_from_video_button.setEnabled(True)
            except Exception as e:
                print(f"17>>{e}")

        def exporer(self, who_called):
            try:
                start = VideoRedactor.Explorer(self.parent.main_path, self.parent.main_path)
                if start.exec() == QDialog.DialogCode.Accepted:
                    if who_called != self.video_for_redact_input:
                        if os.path.splitext(start.resoult())[1][1:] in self.video_format:
                            who_called.setText(start.resoult())

                        else:
                            QMessageBox.information(self, "Важно","Выбранное видео не является стандартным форматом либо вовсе не является видеом выберите видео из перечня этих форматов: mp4, mov, mkv, avi, wmv")

                    else:
                        if os.path.splitext(start.resoult())[1][1:] in self.video_format:
                            video = VideoFileClip(start.resoult())
                            who_called.setText(start.resoult())
                            who_called.setStyleSheet("""
                                QLabel {
                                        background-color: #00FF00;
                                        padding: 10px;
                                        border-radius: 8px;
                                        border: 2px solid #3498db;
                                        } 
                            """)

                            duration_float = video.duration
                            self.scale_factor = self.scale(duration_float)
                            if self.scale_factor != 0:
                                duration_int = int(duration_float * (self.scale_factor * 10))
                            else:
                                duration_int = duration_float

                            self.cut_button.setEnabled(True)
                            self.audio_from_video_button.setEnabled(True)
                            self.slider_start.setEnabled(True)
                            self.slider_end.setEnabled(True)
                            self.slider_start.setRange(0, duration_int)
                            self.slider_end.setRange(0, duration_int)
                            self.slider_end.setValue(duration_int)
                            video.close()

                        else:
                            QMessageBox.information(self, "Важно","Выбранное видео не является стандартным форматом либо вовсе не является видеом выберите видео из перечня этих форматов: mp4, mov, mkv, avi, wmv")
            except Exception as e:
                print(f"18>>{e}")

    def __init__(self):
        super().__init__()
        self.settings_mode = False
        project_Folders()
        self.vide_select_file = None
        self.original_video_geometry = None
        self.dubl_prof = True
        self.main_path = None
        self.setMinimumSize(800, 600)
        self.setWindowTitle("Редактор видео")
        self.setWindowIcon(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/redactor_button.png"))
        self.desctop_screen_geometry = self.screen().availableGeometry()
        self.wigth_desctop_screen , self.height_desctop_screen = self.desctop_screen_geometry.width() , self.desctop_screen_geometry.height()
        try:
            with open(f"{Path(__file__).parent}/settings/settings.json", "r", encoding='utf-8') as f:
                self.file_settings = json.load(f)

        except Exception as e:
            creat_standart_settins()
            with open(f"{Path(__file__).parent}/settings/settings.json", "r", encoding='utf-8') as f:
                self.file_settings = json.load(f)
        finally:
            self.size_x_app_screen , self.size_y_app_screen = int(self.file_settings["screen"][0]) , int(self.file_settings["screen"][1])
            self.posit_x_app_screen, self.posit_y_app_screen = 0, 0

            timer = QTimer()
            timer.timeout.connect(self.update)
            timer.start(1000)
            if self.isVisible() and self.file_settings["mode"] == "fullscreen":
                self.showFullScreen()
                self.get_size_btn.setEnabled(False)


        self.app_screen = self.setGeometry(int(self.posit_x_app_screen),
                                           int(self.posit_y_app_screen),
                                           int(self.size_x_app_screen),
                                           int(self.size_y_app_screen))
        self.app_fon_profile = None
        self.app_screen_geometry = self.frameGeometry()
        self.BackGroundSetting()
        self.gui()
        self.video_widjet(f"{Path(__file__).parent.parent}/Texture/WelcomVideo/vidio.mp4")
        self.create_settings_menu_gui()
        self.auto_sing()

    def auto_sing(self):
        try:
            nik = self.Registr_window.auto_sing()
            if nik:
                with open(f"{Path(__file__).parent.parent}/Profile_data/profile.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.main_path = data["auto_profile"]["1"]

                    if data["auto_profile"]["2"] != "":
                        self.app_fon_profile = data["auto_profile"]["2"]
                        self.auto_fon_select_function()

            else:
                print("sing or registretion")

        except Exception as e:
            print(f"19>>{e}")

    def showEvent(self, event):
        if self.file_settings["mode"] == "fullscreen":
            self.showFullScreen()
            if hasattr(self, "get_size_btn"):
                self.get_size_btn.setEnabled(False)

    def closeEvent(self, event):
        if self.isEnabled():
            event.accept()
        else:
            QMessageBox.question(self, 'Закрытие окна', 'Пока работает доп окно нельзя закрыть основное окно?',
                                     QMessageBox.StandardButton.Yes)
            event.ignore()

        if self.open_button.isEnabled():
            event.accept()

        elif not self.open_button.isEnabled():
            QMessageBox.question(self, 'Закрытие окна', 'Пока работает доп окно нельзя закрыть основное окно?',
                                 QMessageBox.StandardButton.Yes)
            event.ignore()

        elif self.fon_selector_button.isEnabled():
            event.accept()

        elif not self.fon_selector_button.isEnabled():
            QMessageBox.question(self, 'Закрытие окна', 'Пока работает доп окно нельзя закрыть основное окно?',
                                 QMessageBox.StandardButton.Yes)
            event.ignore()

    #Назначеине комбинаций кнопок для быстрого управления программой
    def keyPressEvent(self, event):
        key_Engl = event.key()
        key_Rus = event.text().lower()
        modifiers = event.modifiers()
        if modifiers == Qt.KeyboardModifier.AltModifier:

            #Переход в полноэкранный режим просмотра видео
            if key_Engl == Qt.Key.Key_Return:
               self.fullscreen(self.original_video_geometry)

            #Вызов окна регистрации/входа
            elif key_Engl == Qt.Key.Key_Q or key_Rus== "й":
                self.profile_function()

            #Вызов окна выбора загрузчикка
            elif key_Engl == Qt.Key.Key_A or key_Rus== "ф":
                self.start_load_selector_class()

            #Вызов проводника по видео
            elif key_Engl == Qt.Key.Key_S or key_Rus== "ы":
                self.open_funct()

            #Вызов окна редактора
            elif key_Engl == Qt.Key.Key_D or key_Rus== "в":
                self.redactor_function()

            #Вызов проводника по фонам
            elif key_Engl == Qt.Key.Key_W or key_Rus== "ц":
                self.fon_selector_function()

        #Старт/пауза
        if Qt.Key.Key_Space == key_Engl:
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

        self.settings_menu_gui.setGeometry(0, 0, self.width(), self.height())
        self.background_settings.setGeometry(0, 0, self.width(), self.height())

        # Выпадающие списки
            # Список размеров экрана
        self.combox.setGeometry(frame_x + 220, frame_y + 15, 300, 20)
        self.get_size_btn.move(frame_x + 220, frame_y + 35)

            # Список режимов экрана
        self.combox_scren_mode.setGeometry(frame_x + 220, frame_y + 114, 300, 20)
        self.get_mode_btn.move(frame_x + 220, frame_y + 134)

        # Лэйбл для размера окна
        self.size_lable.move(frame_x - 100, frame_y)
        self.size_lable.setFixedSize(int(self.width()//1.2), 70)

        # Лэйбл для режима экрана
        self.fullscreen_lable.move(frame_x - 100, frame_y + 100)
        self.fullscreen_lable.setFixedSize(int(self.width()//1.2), 70)

        # Кнопка закрытия настройк
        self.close_settings_menu_btn.move(0, 0)
        self.close_settings_menu_btn.setMinimumWidth(int(frame_width // 2))
        self.close_settings_menu_btn.setMaximumWidth(int(frame_width // 2))

        #Настрока размера и позиции фона
        self.bacground_lable.setGeometry(0, 0, self.width(), self.height())

        #Настрока размера и позиции подложки видео
        self.vide_frame.setGeometry(frame_x, frame_y, frame_width, frame_height)
        self.rectangle_lable.setGeometry(0, 0, frame_width, frame_height)

        self.rectangle_round.setGeometry(frame_x, frame_y, frame_width, frame_height)  # Чтобы изображение растягивалось

        #Общий размер кнопок и их позиции
        start_width = int(self.width() // 1.6)
        start_height = int(self.height() // 1.6)
        start_x = int((self.width() - start_width) * 1.25)
        start_y = int((self.height() - start_height) * 2.25)

        #Более точное позиционирование и настройка размера кнопок

        self.close_app_button.setIconSize(QSize(int(start_height // 4.5), int(start_height // 4.5)))
        self.close_app_button.setGeometry(int(frame_x*5.1), 0, int(frame_width // 4.3), int(frame_height // 4.3))

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

        # self.video_position_slider.move(int(self.videoWidjet.width() - 287), self.videoWidjet.height() + 130)
        # self.video_position_slider.resize(QSize(int(self.width()//1.725), 20))
        #Первоначальное назначение размера окна видео и его изменение размера при растягивание окна программы
        if self.original_video_geometry is None:
            slider_y = frame_y + frame_height - int((frame_y/10)*2.3)  # Под фреймом видео
            slider_x = frame_x + (int((frame_y/10)*2.5)//5)*3
            slider_width = frame_width - (int((frame_y/10)*2.5)//5)*6
            self.video_position_slider.setGeometry(slider_x, slider_y, slider_width, 20)
            self.video_position_slider.show()
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
        self.rectangle_round.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/gui_texture/rounded_rectangle.png"))
        self.rectangle_round.setScaledContents(True)

        self.rectangle_lable.setGeometry(0, 0, frame_width, frame_height)

        #Фон
        self.bacground_lable = QLabel(self)
        self.bacground_image = f"{Path(__file__).parent.parent}/Texture/fon_texture/fon.jpg"
        self.bacground_lable.setPixmap(QPixmap(self.bacground_image))
        self.bacground_lable.setGeometry(0,0, int(self.size_x_app_screen), int(self.size_y_app_screen))
        self.bacground_lable.setScaledContents(True)
        self.bacground_lable.lower()

    #Настройки
    def create_settings_menu_gui(self):
        self.settings_menu_gui = QWidget(self)
        self.settings_menu_gui.hide()  # Скрываем изначально

        self.background_settings = QLabel(self.settings_menu_gui)
        self.background_settings.setStyleSheet("background: rgba(0,0,0,200);")
        self.background_settings.setGeometry(0, 0, self.width(), self.height())

        with open(f"{Path(__file__).parent}/settings/settings.json", "r", encoding='utf-8') as f:
            mode_in_settings_json = json.load(f)
            mode_in_settings_json = mode_in_settings_json["mode"]

        if "fullscreen" == mode_in_settings_json:
            mode = "Полноэкранный"
        elif "creen on  full window" == mode_in_settings_json:
            mode = "Окно на весь экран"
        else:
            mode = "Окно"

        self.size_lable = QLabel( f"Размер окна редактора\n текущий = {self.file_settings["screen"][0]}x{self.file_settings["screen"][1]}",self.settings_menu_gui)
        self.size_lable.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 100);
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #3498db;
                text-align: center;
            }
        """)

        self.fullscreen_lable = QLabel(f"Режим окна\n текущий режим {mode}",self.settings_menu_gui)
        self.fullscreen_lable.setStyleSheet("""
                 QLabel {
                     color: white;
                     font-size: 16px;
                     font-weight: bold;
                     background-color: rgba(0, 0, 0, 100);
                     padding: 10px;
                     border-radius: 8px;
                     border: 2px solid #3498db;
                     text-align: center;
                 }
             """)

        self.close_settings_menu_btn = QPushButton("Закрыть настройки", self.settings_menu_gui)
        self.close_settings_menu_btn.clicked.connect(self.settings_menu)
        self.close_settings_menu_btn.setStyleSheet("""
                 QPushButton {
                     color: white;
                     font-size: 16px;
                     font-weight: bold;
                     background-color: rgba(0, 0, 0, 100);
                     padding: 10px;
                     border-radius: 8px;
                     border: 2px solid #3498db;
                     text-align: center;
                 }
                 
                 QPushButton:hover {
                    background-color: rgba(200, 200, 200, 100);
                 }
             """)

        self.combox_scren_mode = QComboBox(self.settings_menu_gui)
        self.combox_scren_mode.addItem("Полноэкранный")
        self.combox_scren_mode.addItem("Окно на весь экран")
        self.combox_scren_mode.addItem("Окно")

        self.combox = QComboBox(self.settings_menu_gui)
        self.combox.addItem("800x600")
        self.combox.addItem("1024x768")
        self.combox.addItem("1152x864")
        self.combox.addItem("1280x1024")
        self.combox.addItem("1400x1050")
        self.combox.addItem("1920x1080")
        self.combox.addItem(f"Рекомендуемый размер {self.desctop_screen_geometry.width()}x{self.desctop_screen_geometry.height()}")

        self.get_mode_btn = QPushButton("Выбрать новый режим экрана", self.settings_menu_gui)
        self.get_mode_btn.clicked.connect(self.get_settings_menu_screen_mode)
        self.get_size_btn = QPushButton("Выбрать новый размер", self.settings_menu_gui)
        self.get_size_btn.clicked.connect(self.get_settings_menu_size_app)

        self.settings_menu_gui.setGeometry(0, 0, self.width(), self.height())

    def get_settings_menu_size_app(self):
        value_combobox = self.combox.currentText()
        if "Рекомендуемый размер" in value_combobox:
            value_lst = value_combobox.split(" ")
            size = value_lst[2].split("x")
        else:
            size = value_combobox.split("x")

        try:
            with open(f"{Path(__file__).parent}/settings/settings.json", "r", encoding='utf-8') as f:
                data = json.load(f)

            with open(f"{Path(__file__).parent}/settings/settings.json", "w", encoding='utf-8') as f:
                data['screen'] = (size[0], size[1])
                json.dump(data, f)

            self.resize(int(size[0]), int(size[1]))
        except Exception as e:
            print(f"20>>{e}")


        finally:
            self.size_lable.setText(f"Размер окна редактора\n текущий = {size[0]}x{size[1]}")

    def get_settings_menu_screen_mode(self):
        value_combobox = self.combox_scren_mode.currentText()
        if "Полноэкранный" == value_combobox:
            resoult = "fullscreen"
        elif "Окно на весь экран" == value_combobox:
            resoult = "screen on  full window"
        else:
            resoult = "screen"
        try:
            with open(f"{Path(__file__).parent}/settings/settings.json", "r", encoding='utf-8') as f:
                data = json.load(f)

            with open(f"{Path(__file__).parent}/settings/settings.json", "w", encoding='utf-8') as f:
                data["mode"] = resoult
                data["screen"] = [self.desctop_screen_geometry.width(), self.desctop_screen_geometry.height()]
                json.dump(data, f)

        except Exception as e:
            print(f"21>>{e}")


        finally:
            self.fullscreen_lable.setText(f"Режим окна\n текущий режим {value_combobox}")
            if value_combobox == "Полноэкранный":
                self.showFullScreen()
                self.get_size_btn.setEnabled(False)
            elif value_combobox == "Окно на весь экран":
                self.resize(self.desctop_screen_geometry.width(), self.desctop_screen_geometry.height())
            else:
                self.showNormal()
                self.get_size_btn.setEnabled(True)

    def settings_menu(self):
        self.settings_mode = not self.settings_mode

        if self.settings_mode:
            self.settings_menu_gui.show()
            self.settings_menu_gui.raise_()

            self.videoWidjet.hide()
            self.settings_menu_button.hide()
            self.start_button.setEnabled(False)
            self.redactor_button.setEnabled(False)
            self.profile_button.setEnabled(False)
            self.load_button.setEnabled(False)
            self.open_button.setEnabled(False)
            self.fon_selector_button.setEnabled(False)
        else:
            self.settings_menu_gui.hide()
            self.videoWidjet.show()
            self.settings_menu_button.show()
            self.start_button.setEnabled(True)
            self.redactor_button.setEnabled(True)
            self.profile_button.setEnabled(True)
            self.load_button.setEnabled(True)
            self.open_button.setEnabled(True)
            self.fon_selector_button.setEnabled(True)

    #Функия настройки всех кнопок, изображений и слайдера
    def gui(self):

        # Кнопка закрытия программы
        self.close_app_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/close_app_button.png"), "", self)
        self.close_app_button.clicked.connect(self.close_app_function)

        # Кнопка настройки
        self.settings_menu_button = QPushButton("Настройки", self)
        self.settings_menu_button.clicked.connect(self.settings_menu)
        self.settings_menu_button.setMinimumWidth(120)
        self.settings_menu_button.setMinimumHeight(40)

        # Кнопка старт/пауза
        self.start_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/start_button.png"), "", self)
        self.start_button.clicked.connect(self.start)

        # Кнопка выбора видео
        self.open_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/select_button.png"), "", self)
        self.open_button.clicked.connect(self.open_funct)

        # Кнопка регистрации/входа
        self.profile_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/select_and_registr_profile.png"), "", self)
        self.profile_button.clicked.connect(self.profile_function)

        # Кнопка выбора загрузчика
        self.load_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/load_button.png"), "", self)
        self.load_button.clicked.connect(self.start_load_selector_class)

        # Кнопка редактора
        self.redactor_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/redactor_button.png"), "", self)
        self.redactor_button.clicked.connect(self.redactor_function)

        # Кнопка выбора фона
        self.fon_selector_button = QPushButton(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/fon_selector.png"), "", self)
        self.fon_selector_button.clicked.connect(self.fon_selector_function)

        self.video_position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.video_position_slider.sliderPressed.connect(self.slider_pressed)
        self.video_position_slider.sliderReleased.connect(self.slider_released)
        self.video_position_slider.setRange(0,0)

        self.video_position_slider.setEnabled(False)

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
        self.vl_10.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl1.png"))

        self.vl_20 = QLabel()
        self.vl_20.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl2.png"))

        self.vl_30 = QLabel()
        self.vl_30.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl3.png"))

        self.vl_40 = QLabel()
        self.vl_40.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl4.png"))

        self.vl_50 = QLabel()
        self.vl_50.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl5.png"))

        self.vl_60 = QLabel()
        self.vl_60.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl6.png"))

        self.vl_70 = QLabel()
        self.vl_70.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl7.png"))

        self.vl_80 = QLabel()
        self.vl_80.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl8.png"))

        self.vl_90 = QLabel()
        self.vl_90.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl9.png"))

        self.vl_100 = QLabel()
        self.vl_100.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/volume_texture/vl10.png"))

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

        # Кнопка закрытия программы
        self.close_app_button.setStyleSheet("""
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

        self.settings_menu_button.setStyleSheet("""
                    QPushButton {
                        color: white;
                        font-size: 16px;
                        font-weight: bold;
                        background-color: rgba(0, 0, 0, 100);
                        padding: 10px;
                        border-radius: 8px;
                        border: 2px solid #3498db;
                        text-align: center;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0);
                    }
                """)

    def slider_pressed(self):
        if self.mediaPlayer.isPlaying():
            self.mediaPlayer.pause()
            self.start_button.setIcon(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/start_button.png"))

    def slider_released(self):
        position = self.video_position_slider.value()
        self.mediaPlayer.setPosition(position)

        if (self.mediaPlayer.mediaStatus() == QMediaPlayer.MediaStatus.LoadedMedia and
                position < self.mediaPlayer.duration()):
            self.mediaPlayer.play()
            self.start_button.setIcon(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/pause_button.png"))

    def video_position(self, position):
        if not self.video_position_slider.isSliderDown():
            self.video_position_slider.setValue(position)

    def video_duration_position(self, duration):
        self.video_position_slider.setRange(0, duration)

    def close_app_function(self):
        self.close()

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
        self.mediaPlayer.positionChanged.connect(self.video_position)
        self.mediaPlayer.durationChanged.connect(self.video_duration_position)
        self.audioPlayer = QAudioOutput()

        self.mediaPlayer.setAudioOutput(self.audioPlayer)
        self.mediaPlayer.setSource(QUrl.fromLocalFile(video_path))
        self.mediaPlayer.play()
        self.mediaPlayer.pause()
        self.start_button.setIcon(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/start_button.png"))
        self.start_button.setEnabled(False)

    # Функция старт/пауза
    def start(self):
        if self.mediaPlayer.isPlaying() == True:
            self.mediaPlayer.pause()
            self.start_button.setIcon(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/start_button.png"))
        else:
            self.start_button.setIcon(QIcon(f"{Path(__file__).parent.parent}/Texture/gui_texture/pause_button.png"))
            self.mediaPlayer.play()

    # Вызов проводника по видео
    def open_funct(self):
        # Проверка на вход в профиль
        if self.main_path is not None:
            try:
                explorer = VideoRedactor.Explorer(self.main_path, self.main_path)
                video = None
                if explorer.exec() == QDialog.DialogCode.Accepted:
                    video = explorer.resoult()

                if video != None:
                    self.vide_select_file = video
                    self.start_button.setEnabled(True)
                    self.video_position_slider.setEnabled(True)
                    self.finish_explorer_video()

            # Сообщение об ошибке
            except Exception as e:
                print(f"22>>{e}")

                QMessageBox.critical(self, 'Ошибка', f"{e}",
                                     QMessageBox.StandardButton.Yes)

        #Сообщение о необходимости войти в профиль
        else:
            QMessageBox.critical(self, "Ошибка", "Войдите в профилень, чтобы выбирать видео",
                                 QMessageBox.StandardButton.Yes)

    # обновление основного окна после выбора видео
    def finish_explorer_video(self):
        try:
            # Обновление видео в плеере
            if self.vide_select_file != "False" and str(Path(self.vide_select_file[len(self.vide_select_file[:-4]):])) != str(None):
                self.mediaPlayer.stop()
                self.mediaPlayer.setSource(QUrl.fromLocalFile(self.vide_select_file))
                self.videoWidjet.update()
                self.videoWidjet.repaint()

        except Exception as e:
            self.explorer_video_error(e)

    # Функция для вывода ошибки в основном окне для видео
    def explorer_video_error(self, error):
        self.fon_selector_button.setEnabled(True)
        self.profile_button.setEnabled(True)
        self.open_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.redactor_button.setEnabled(True)
        QMessageBox.critical(self, "Ошибка", f"{error}",
                             QMessageBox.StandardButton.Yes)

    # Функция настроки громкости
    def volume_function_slider(self, value):
        for i in range(10, 101, 10):
            eval(f"self.vl_{i}.hide()")

        for i in range(10, value + 1, 10):
            eval(f"self.vl_{i}.show()")

        valume = value / 100
        self.audioPlayer.setVolume(valume)

# Функция вызова окна входа/регистрации
    def profile_function(self):
        try:
            prof = VideoRedactor.Registr_window(self)
            result = prof.exec()
            if result == QDialog.DialogCode.Accepted and os.path.exists(f"{Path(__file__).parent.parent}/temp/profile_path_and_dubl.json"):
                self.read_profile_json()
        except Exception as e:
            print(f"23>>{e}")

    def read_profile_json(self):
        # Чтение временного файла созданного окном входа/регистрации
        try:
            with open(f"{Path(__file__).parent.parent}/temp/profile_path_and_dubl.json", "r", encoding='utf-8') as f:
                local_path = json.load(f)

            if local_path != {}:
                self.main_path = local_path["First"]
                self.app_fon_profile = local_path["Third"]
                if self.app_fon_profile != "":
                    self.auto_fon_select_function()

        # Сообщение об ошибке
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f"{e}",
                                 QMessageBox.StandardButton.Yes)
#Конец

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

                        QMessageBox.critical(self, "Действие выполнено", "Файл был успешно загружен",
                                             QMessageBox.StandardButton.Yes)


                    else:
                        shutil.copy(file, self.main_path)

                        QMessageBox.critical(self, "Действие выполнено", "Файл был успешно загружен",
                                             QMessageBox.StandardButton.Yes)

            else:
                QMessageBox.critical(self, "Ошибка загрузки", "Войдите в профиль для загрузки\n видео в папку профиля.",
                                     QMessageBox.StandardButton.Yes)


        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f"{e}",
                                 QMessageBox.StandardButton.Yes)

    # Функция загрузки изображения фона в папку текстур фона
    def fon_load_function(self):
        # Проверка на вход в профиль
        if self.main_path != None:

            # Попытка открытия json с данными пользователей
            try:
                with open(f"{Path(__file__).parent.parent}/Profile_data/profile.json", "r", encoding='utf-8') as f:
                    data = json.load(f)

                for key in data.keys():

                    # Попытка открытия json для записи нового фона для конкретного пользователя
                    try:
                        if key != "auto_profile":
                            if data[key]["Video_path"] == self.main_path:
                                filter_string = "Images (*.png *.jpg *.bmp);; Any files (*)"
                                fon_file, _ = QFileDialog.getOpenFileName(self,"Выберите изображение", "", filter_string)

                                if fon_file != "" and not any('CYRILLIC' in unicodedata.name(c, '') for c in fon_file) if fon_file else False:
                                    fon_name = fon_file.split("/")[-1]
                                    if r"fon_texture" not in fon_file:

                                        # Проверка на выбор режима загрузчика
                                        if self.loader.on_of_function_global() == 0:
                                            shutil.move(fon_file, f"{Path(__file__).parent.parent}/Texture/fon_texture")
                                            data[key]["Fon_path"] = f"{Path(__file__).parent.parent}/Texture/fon_texture/{fon_name}"

                                            self.bacground_lable.setPixmap(QPixmap(f"{Path(__file__).parent.parent}/Texture/fon_texture/{fon_name}"))

                                        else:
                                            shutil.copy(fon_file, f"{Path(__file__).parent.parent}/Texture/fon_texture")
                                            data[key]["Fon_path"] = f"{Path(__file__).parent.parent}/Texture/fon_texture/{fon_name}"

                                            self.bacground_lable.setPixmap(QPixmap(
                                                f"{Path(__file__).parent.parent}/Texture/fon_texture/{fon_name}"))

                                    else:
                                        print("> error exit")
                                else:
                                    QMessageBox.information(self, "Важно", "Название фона должно быть на англиском.")
                    except Exception as e:
                        raise e

            except Exception as e:
                print(e)
                QMessageBox.critical(self, 'Ошибка', f"213{e}",
                                     QMessageBox.StandardButton.Yes)

        # Сообщение о необходимости войти в профиль
        else:
            QMessageBox.critical(self, "Ошибка", "Войдите в профилень, чтобы загружать фон",
                                 QMessageBox.StandardButton.Yes)

    # Функция выбора фона
    def fon_selector_function(self):
        # Проверка на вход в профиль
        if self.main_path is not None:
            try:
                explorer = VideoRedactor.Explorer(
                    f"{Path(__file__).parent.parent}/Texture/fon_texture",
                    f"{Path(__file__).parent.parent}/Texture/fon_texture"
                )

                if explorer.exec() == QDialog.DialogCode.Accepted:
                    self.app_fon_profile = explorer.resoult()

                    if self.app_fon_profile:
                        self.bacground_lable.setPixmap(QPixmap(self.app_fon_profile))

                        try:
                            profile_path = f"{Path(__file__).parent.parent}/Profile_data/profile.json"

                            if os.path.exists(profile_path):
                                with open(profile_path, "r", encoding='utf-8') as f:
                                    data = json.load(f)

                                for key in data.keys():
                                    if data[key].get("Video_path") == self.main_path:
                                        data[key]["Fon_path"] = self.app_fon_profile

                                        if data[key]["remember_me"]:
                                            data["auto_profile"]["2"] = self.app_fon_profile
                                            break

                                        break

                                with open(profile_path, "w", encoding='utf-8') as f:
                                    json.dump(data, f, ensure_ascii=False, indent=4)
                        except Exception as e:
                            print(f"Ошибка при обновлении профиля: {e}")

            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f"{e}",
                                     QMessageBox.StandardButton.Yes)
        else:
            QMessageBox.critical(self, 'Ошибка',
                                 "Войдите в профиль, чтобы выбирать фон редактора",
                                 QMessageBox.StandardButton.Yes)

    # Функция автоподгрузки не стандартного фона
    def auto_fon_select_function(self):
        self.bacground_lable.setPixmap(QPixmap(self.app_fon_profile))

    # Функция открытия окна выбора загрузчика
    def start_load_selector_class(self):
        try:
            self.loader = VideoRedactor.Load_selector(self)
            self.loader.exec()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f"{e}",
                                 QMessageBox.StandardButton.Yes)

# Функция открытия редактора
    def redactor_function(self):
        if self.main_path is not None:
            prov = self.Redactor_video(self)
            prov.exec()
        else:
            QMessageBox.information(self, "Важно", "Войдите в профиль для редактирования")

def redirect_output_to_null():
    """Перенаправляет stdout и stderr в null"""
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')



# Запуск программы
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoRedactor()
    window.show()
    sys.exit(app.exec())