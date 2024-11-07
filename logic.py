# logic.py

from PyQt5.QtWidgets import QFileDialog
from glwidget import GLWidget

class MainWindowLogic:
    def __init__(self, window):
        self.window = window

    def hex_to_rgb(self, hex_color):
        r = int(hex_color.lstrip('#')[0:2], 16)
        g = int(hex_color.lstrip('#')[2:4], 16)
        b = int(hex_color.lstrip('#')[4:6], 16)
        return f"{r}, {g}, {b}"

    def lighter_color(self, hex_color):
        r, g, b = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = min(255, r+50), min(255, g+50), min(255, b+50)
        return f"#{r:02x}{g:02x}{b:02x}"

    def darker_color(self, hex_color):
        r, g, b = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = max(0, r-50), max(0, g-50), max(0, b-50)
        return f"#{r:02x}{g:02x}{b:02x}"

    def switch_theme(self):
        if self.window.theme == "light":
            self.window.theme = "dark"
            self.window.theme_toggle.setText("Тёмная тема")
            self.window.theme_toggle.setStyleSheet("background-color: #333; color: white;")
        else:
            self.window.theme = "light"
            self.window.theme_toggle.setText("Светлая тема")
            self.window.theme_toggle.setStyleSheet("background-color: #f0f0f0; color: black;")
        
        self.window.update_buttons()

    def import_data(self):
        # Открытие проводника для выбора файла
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self.window, "Импортировать STEP файл", "", "STEP Files (*.step);;All Files (*)", options=options)
        if file_path:
            print(f"Файл для импорта: {file_path}")
            # Здесь можно добавить логику для импорта файла

    def export_data(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self.window, "Экспортировать STEP файл", "", "STEP Files (*.step);;All Files (*)", options=options)
        if file_path:
            print(f"Файл для экспорта: {file_path}")
            # Здесь можно добавить логику для экспорта файла

    def view_data(self):
        self.window.glWidget = GLWidget()
        self.window.setCentralWidget(self.window.glWidget)
