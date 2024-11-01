import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QToolButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Главное окно")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        self.theme = "light"
        self.create_theme_toggle()
        self.create_buttons()

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
            {"text": "Импортировать данные", "color": "#3498db", "size": 250},
            {"text": "Экспортировать данные", "color": "#e74c3c", "size": 250},
            {"text": "Просмотр", "color": "#2ecc71", "size": 250}
        ]
        
        button_layout = QHBoxLayout()
        self.main_layout.addLayout(button_layout)
        
        for button_data in buttons:
            button = QPushButton(button_data["text"])
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                      stop:0 rgba({self.hex_to_rgb(self.lighter_color(button_data['color']))}),
                                                      stop:1 rgba({self.hex_to_rgb(button_data['color'])}));
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
                                                      stop:0 rgba({self.hex_to_rgb(self.lighter_color(button_data['color']))}),
                                                      stop:1 rgba({self.hex_to_rgb(self.darker_color(button_data['color']))}));
                    opacity: 0.9;
                }}
            """)
            
            button.setFont(QFont("Arial", 12))
            button_layout.addWidget(button)
            button_layout.addStretch()

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
        if self.theme == "light":
            self.theme = "dark"
            self.theme_toggle.setText("Тёмная тема")
            self.theme_toggle.setStyleSheet("background-color: #333; color: white;")
        else:
            self.theme = "light"
            self.theme_toggle.setText("Светлая тема")
            self.theme_toggle.setStyleSheet("background-color: #f0f0f0; color: black;")
        
        self.update_buttons()

    def update_buttons(self):
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            if isinstance(item.layout(), QHBoxLayout):
                for j in range(item.layout().count()):
                    widget_item = item.layout().itemAt(j)
                    if widget_item.widget():
                        button = widget_item.widget()
                        button.setStyleSheet(button.styleSheet())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
