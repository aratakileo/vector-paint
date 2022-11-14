from pygame.constants import RESIZABLE, K_z, K_l, K_s, K_y
from pygame.event import get as get_event
from projectmanager import ProjectManager
from core.canvas import Canvas
from core.recorder import *
from pygame import display
from core.pen import Pen
from pygex import *


display.set_caption("vPaint")  # vectorPaint
display.set_mode((800, 800), RESIZABLE)

surface = display.get_surface()

canvas = Canvas()
# canvas.antialiasing = True

pen = Pen(canvas)
pen.color = 0x4caf50

recorder = Recorder(canvas)

project_manager = ProjectManager(canvas)

while True:
    for e in get_event():
        process_event(e)

    if get_mouse().left_is_up:
        recorder.protect_record = False

    recorder.can_record = get_mouse().left_is_hold

    if get_input().is_hold(get_input().GK_CTRL):
        if get_input().is_applying(K_z):
            recorder.undo()
        elif get_input().is_applying(K_y):
            recorder.redo()
        elif get_input().is_up(K_s):
            project_manager.save()
        elif get_input().is_up(K_l):
            project_manager.load()

    recorder.try_record(get_mouse().get_pos())

    canvas.render(surface)

    flip(0xffffff, 60)
