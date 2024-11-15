from PyQt5.QtWidgets import QOpenGLWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QPoint
from OpenGL.GL import *
from OpenGL.GLU import *
from shapes import Cube, Grid

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.cube = Cube()  # Инициализация куба
        self.grid = Grid()  # Инициализация сетки
        self.last_pos = QPoint()
        self.rotation = [0, 0, 0]
        self.scale = 1.0
        self.translation = [0.0, 0.0]

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, w / h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.translation[0], self.translation[1], -5.0)
        glScalef(self.scale, self.scale, self.scale)
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)
        glRotatef(self.rotation[2], 0.0, 0.0, 1.0)
        self.grid.draw()  # Рендеринг сетки
        self.cube.draw()  # Рендеринг куба

    def mousePressEvent(self, event):
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        if event.buttons() & Qt.LeftButton:
            self.rotation[0] += dy
            self.rotation[1] += dx
        elif event.buttons() & Qt.RightButton:
            self.translation[0] += dx / 100.0
            self.translation[1] -= dy / 100.0

        self.last_pos = event.pos()
        self.update()

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120  # Количество щелчков колесика мыши
        self.scale += delta * 0.1
        self.scale = max(0.1, self.scale)  # Минимальный масштаб
        self.update()

    def create_controls(self):
        layout = QVBoxLayout(self)

        rotate_button = QPushButton('Вращать')
        rotate_button.clicked.connect(lambda: self.set_interaction_mode('rotate'))
        layout.addWidget(rotate_button)

        translate_button = QPushButton('Перемещать')
        translate_button.clicked.connect(lambda: self.set_interaction_mode('translate'))
        layout.addWidget(translate_button)

        scale_button = QPushButton('Увеличивать')
        scale_button.clicked.connect(lambda: self.set_interaction_mode('scale'))
        layout.addWidget(scale_button)

        widget = QWidget()
        widget.setLayout(layout)
        self.parent().layout().addWidget(widget)

    def set_interaction_mode(self, mode):
        self.interaction_mode = mode

        if mode == 'rotate':
            self.mode_handler = self.rotate_object
        elif mode == 'translate':
            self.mode_handler = self.translate_object
        elif mode == 'scale':
            self.mode_handler = self.scale_object

    def rotate_object(self):
        self.rotation_angle += 1.0
        self.update()

    def translate_object(self):
        self.translation[0] += 0.1
        self.update()

    def scale_object(self):
        self.scale += 0.1
        self.update()
