# glwidget.py
from PyQt5.QtWidgets import QOpenGLWidget, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QKeyEvent
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
        self.selected_object = None  # Переменная для хранения выделенного объекта
        self.interaction_mode = 'view'  # Режим по умолчанию
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
        if self.selected_object:
            self.draw_outline()
            self.draw_axis()
    def draw_outline(self):
        glPushMatrix()
        glTranslatef(*self.cube.position)
        glScalef(*self.cube.scale_factors)
        glRotatef(self.cube.rotation[0], 1, 0, 0)
        glRotatef(self.cube.rotation[1], 0, 1, 0)
        glRotatef(self.cube.rotation[2], 0, 0, 1)
        glColor3f(1, 1, 1)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex3f(-1.0, -1.0,  1.0)
        glVertex3f( 1.0, -1.0,  1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glEnd()
        glPopMatrix()
    def draw_axis(self):
        axis_length = 3.0  # Увеличенная длина осей
        axis_thickness = 3.0  # Увеличенная толщина осей
        glPushMatrix()
        glTranslatef(self.cube.position[0], self.cube.position[1], self.cube.position[2])
        glLineWidth(axis_thickness)
        glBegin(GL_LINES)
        # X-axis
        glColor3f(1, 0, 0)
        glVertex3f(1.0, 0.0, 0.0)  # От центра грани
        glVertex3f(1.0 + axis_length, 0.0, 0.0)
        # Y-axis
        glColor3f(0, 1, 0)
        glVertex3f(0.0, 1.0, 0.0)  # От центра грани
        glVertex3f(0.0, 1.0 + axis_length, 0.0)
        # Z-axis
        glColor3f(0, 0, 1)
        glVertex3f(0.0, 0.0, 1.0)  # От центра грани
        glVertex3f(0.0, 0.0, 1.0 + axis_length)
        glEnd()
        glPopMatrix()
        glLineWidth(1.0)  # Сброс толщины линии к стандартной
    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        if event.buttons() & Qt.LeftButton:
            self.select_object(event.x(), event.y())
        else:
            # Снять выделение с объекта
            self.selected_object = None
            self.update()
    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()
        if event.buttons() & Qt.LeftButton:
            # Вращение сцены
            if self.interaction_mode == 'view':
                self.rotation[0] += dy
                self.rotation[1] += dx
            elif self.interaction_mode in ['rotate', 'translate', 'scale'] and self.selected_object:
                self.manipulate_object(dx, dy)
        elif event.buttons() & Qt.RightButton:
            # Перемещение сцены
            self.translation[0] += dx / 100.0
            self.translation[1] -= dy / 100.0
        self.last_pos = event.pos()
        self.update()
    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120  # Количество щелчков колесика мыши
        self.scale += delta * 0.1
        self.scale = max(0.1, self.scale)  # Минимальный масштаб
        self.update()
    def select_object(self, x, y):
        # Процедура выделения объекта при нажатии ЛКМ
        # Здесь может быть простой ray-casting для выбора объекта
        self.selected_object = self.cube  # В данном примере всегда выбирается куб
        self.update()
    def set_interaction_mode(self, mode):
        self.interaction_mode = mode
        self.update()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.set_interaction_mode('rotate')
        elif event.key() == Qt.Key_G:
            self.set_interaction_mode('translate')
        elif event.key() == Qt.Key_S:
            self.set_interaction_mode('scale')
    def manipulate_object(self, dx, dy):
        if self.selected_object:
            if self.interaction_mode == 'rotate':
                self.cube.rotate(dy, 0)  # Вращение по X
                self.cube.rotate(dx, 1)  # Вращение по Y
            elif self.interaction_mode == 'translate':
                self.cube.translate(dx / 100.0, -dy / 100.0, 0)
            elif self.interaction_mode == 'scale':
                self.cube.scale_object(1 + dy / 100.0, 1 + dy / 100.0, 1 + dy / 100.0)
        self.update()
