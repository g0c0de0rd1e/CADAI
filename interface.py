from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from logic import MainWindowLogic
from glwidget import GLWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # Инициализация логики перед вызовом create_buttons
        self.logic = MainWindowLogic(self)

        self.theme = "light"
        self.create_theme_toggle()
        self.create_buttons()

    def create_controls(self, window):
        control_layout = QVBoxLayout()

        rotate_button = QPushButton('Вращать')
        rotate_button.clicked.connect(lambda: window.gl_widget.set_interaction_mode('rotate'))
        control_layout.addWidget(rotate_button)

        translate_button = QPushButton('Перемещать')
        translate_button.clicked.connect(lambda: window.gl_widget.set_interaction_mode('translate'))
        control_layout.addWidget(translate_button)

        scale_button = QPushButton('Увеличивать')
        scale_button.clicked.connect(lambda: window.gl_widget.set_interaction_mode('scale'))
        control_layout.addWidget(scale_button)

        window.main_layout.addLayout(control_layout)

    def create_theme_toggle(self):
        toggle_layout = QHBoxLayout()
        self.main_layout.addLayout(toggle_layout)

        self.theme_toggle = QToolButton()
        self.theme_toggle.setText("Светлая тема")
        self.theme_toggle.clicked.connect(self.switch_theme)
        self.theme_toggle.setFixedSize(150, 30)
        toggle_layout.addWidget(self.theme_toggle)
        toggle_layout.addStretch()

    def create_buttons(self):
        buttons = [
            {"text": "Импортировать данные", "color": "#3498db", "size": 250, "handler": self.logic.import_data},
            {"text": "Экспортировать данные", "color": "#e74c3c", "size": 250, "handler": self.logic.export_data},
            {"text": "Просмотр", "color": "#2ecc71", "size": 250, "handler": self.open_view_window}
        ]

        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)

        for button_data in buttons:
            button = QPushButton(button_data["text"])
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba({self.logic.hex_to_rgb(self.logic.lighter_color(button_data['color']))}),
                        stop:1 rgba({self.logic.hex_to_rgb(button_data['color'])}));
                    color: {'white' if self.theme == 'light' else '#333'};
                    border-radius: 10px;
                    min-width: {button_data['size']}px;
                    max-width: {button_data['size']}px;
                    min-height: {button_data['size']}px;
                    max-height: {button_data['size']}px;
                    font-size: 16pt;
                }}
                QPushButton:hover {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba({self.logic.hex_to_rgb(self.logic.lighter_color(button_data['color']))}),
                        stop:1 rgba({self.logic.hex_to_rgb(self.logic.darker_color(button_data['color']))}));
                    opacity: 0.9;
                }}
            """)
            button.clicked.connect(button_data["handler"])
            button.setFont(QFont("Arial", 12))
            button_layout.addWidget(button)
            button_layout.addStretch()

    def switch_theme(self):
        self.logic.switch_theme()

    def update_buttons(self):
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if isinstance(item.layout(), QHBoxLayout):
                for j in range(item.layout().count()):
                    widget_item = item.layout().itemAt(j)
                    if widget_item.widget():
                        button = widget_item.widget()
                        button.setStyleSheet(button.styleSheet())

    def open_view_window(self):
        self.central_widget.deleteLater()
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        self.gl_widget = GLWidget()
        self.main_layout.addWidget(self.gl_widget)

        self.create_controls(self)
