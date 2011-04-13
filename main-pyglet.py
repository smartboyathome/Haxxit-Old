#!/usr/bin/python2
from pyglet import *
import math

try:
    config = gl.Config(sample_buffers=1, samples=4, depth_size=16, double_buffer=True,)
    myWindow = window.Window(resizable=False, config=config)
except window.NoSuchConfigException:
    gl.glEnable(gl.GL_LINE_SMOOTH);
    gl.glEnable(gl.GL_POLYGON_SMOOTH);
    gl.glEnable(gl.GL_BLEND);
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA);
    gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_DONT_CARE);
    gl.glHint(gl.GL_POLYGON_SMOOTH_HINT, gl.GL_DONT_CARE);
    myWindow = window.Window(resizable=False)

def drawCircle(x, y, radius, border=0):
    gl.glPushMatrix()
    gl.glTranslatef(x, y, 0)
    quadric = gl.gluNewQuadric()
    res = min(int(round(2*math.pi*radius)), 15)
    gl.gluDisk(quadric, radius-border, radius, res, 1)
    gl.glPopMatrix()

@myWindow.event
def on_draw():
    myWindow.clear()
    drawCircle(50, 125, 10, 2)
    drawCircle(50, 125, 5)

app.run()