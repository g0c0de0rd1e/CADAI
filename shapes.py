# shapes.py
from OpenGL.GL import *

class Cube:
    def __init__(self):
        self.position = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]
        self.scale_factors = [1.0, 1.0, 1.0]

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glScalef(*self.scale_factors)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

        glBegin(GL_QUADS)
        # Front face
        glColor3f(1.0, 0.0, 0.0)  # Red
        glVertex3f(-1.0, -1.0,  1.0)
        glVertex3f( 1.0, -1.0,  1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        
        # Back face
        glColor3f(0.0, 1.0, 0.0)  # Green
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        
        # Top face
        glColor3f(0.0, 0.0, 1.0)  # Blue
        glVertex3f(-1.0,  1.0, -1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        
        # Bottom face
        glColor3f(1.0, 1.0, 0.0)  # Yellow
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f( 1.0, -1.0,  1.0)
        glVertex3f(-1.0, -1.0,  1.0)
        
        # Right face
        glColor3f(1.0, 0.0, 1.0)  # Magenta
        glVertex3f( 1.0, -1.0, -1.0)
        glVertex3f( 1.0,  1.0, -1.0)
        glVertex3f( 1.0,  1.0,  1.0)
        glVertex3f( 1.0, -1.0,  1.0)
        
        # Left face
        glColor3f(0.0, 1.0, 1.0)  # Cyan
        glVertex3f(-1.0, -1.0, -1.0)
        glVertex3f(-1.0, -1.0,  1.0)
        glVertex3f(-1.0,  1.0,  1.0)
        glVertex3f(-1.0,  1.0, -1.0)
        
        glEnd()
        glPopMatrix()

    def translate(self, dx, dy, dz):
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz

    def rotate(self, angle, axis):
        self.rotation[axis] += angle

    def scale_object(self, sx, sy, sz):
        self.scale_factors[0] *= sx
        self.scale_factors[1] *= sy
        self.scale_factors[2] *= sz

class Grid:
    def draw(self):
        glColor3f(0.5, 0.5, 0.5)  # Серый цвет для сетки
        glBegin(GL_LINES)
        for i in range(-10, 11):
            glVertex3f(i, 0, -10)
            glVertex3f(i, 0, 10)
            glVertex3f(-10, 0, i)
            glVertex3f(10, 0, i)
        glEnd()
